import asyncio
import re
import json
import logging
from urllib.parse import urlparse, urljoin
from typing import Set, Dict, List, Optional

from bs4 import BeautifulSoup
from aiolimiter import AsyncLimiter
import aiohttp

from site_patterns import SitePatternDetector

logger = logging.getLogger("shoppin_crawler")


PRODUCT_URL_PATTERNS = [
        r'/product[s]?/',
        r'/p/',
        r'/item[s]?/',
        r'/shop/',
        r'/pd/',
        r'/-p-',
        r'/buy/'
    ]

EXCLUDED_PATTERNS = [
        r'/account',
        r'/login',
        r'/cart',
        r'/checkout',
        r'/wishlist',
        r'/search',
        r'/auth',
        r'/register',
        r'/password',
        r'/know-your-size',
        r'/ambassador-program',
        r'/order',
        r'/payment',
        r'/contact',
        r'/about',
        r'/help',
        r'/faq',
        r'/terms',
        r'/policy',
        r'/blog',
        r'/news',
        r'/press',
        r'/careers',
        r'/jobs',
        r'/support',
        r'/customer-service',
        r'#',
        r'\?',
        r'javascript:',
        r'tel:',
        r'mailto:'
    ]

EXCLUDED_EXTENSIONS = [
        '.jpg', '.jpeg', '.png', '.gif', '.svg', '.css', '.js', 
        '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.zip', '.rar'
    ]

class ProductURLCrawler:
    """
    A crawler designed to discover product URLs on e-commerce websites.
    """
    
    def __init__(self, domains: List[str],  max_pages_per_domain: int = 1000, max_depth: int = 5, concurrency: int = 10, rate_limit: int = 5):
        self.domains = domains
        self.max_pages_per_domain = max_pages_per_domain
        self.max_depth = max_depth
        self.concurrency = concurrency
        self.rate_limiter = AsyncLimiter(rate_limit, 1)  # rate_limit requests per second
        self.site_detector = SitePatternDetector()
        
    async def crawl_all_domains(self) -> Dict[str, List[str]]:
    
        results = {}
        
        for domain in self.domains:
            logger.info(f"Starting crawl for domain: {domain}")
            product_urls = await self.crawl_domain(domain)
            results[domain] = list(product_urls)
            logger.info(f"Completed crawl for {domain}. Found {len(product_urls)} product URLs.")
            
            # Learn from results to improve future crawls
            self.site_detector.learn_from_results(list(product_urls), domain)
            
        return results
    
    async def crawl_domain(self, domain: str) -> Set[str]:
        parsed_domain = urlparse(domain)
        base_url = f"{parsed_domain.scheme}://{parsed_domain.netloc}"
        
        visited_urls = set()
        queued_urls = {domain}
        product_urls = set()
        
        domain_name = parsed_domain.netloc.replace('www.', '')
        
        semaphore = asyncio.Semaphore(self.concurrency)
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            for url in queued_urls:
                task = asyncio.create_task(
                    self._crawl_url(
                        url, 
                        base_url, 
                        visited_urls, 
                        queued_urls, 
                        product_urls, 
                        session, 
                        semaphore, 
                        domain_name, 
                        0
                    )
                )
                tasks.append(task)
            
                while tasks and len(visited_urls) < self.max_pages_per_domain:
                    done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                    
                    for task in done:
                        try:
                            new_urls = await task
                            if new_urls:
                                for url in new_urls:
                                    if url not in visited_urls and url not in queued_urls and len(visited_urls) < self.max_pages_per_domain:
                                        queued_urls.add(url)
                                        new_task = asyncio.create_task(
                                            self._crawl_url(
                                                url, 
                                                base_url, 
                                                visited_urls, 
                                                queued_urls, 
                                                product_urls, 
                                                session, 
                                                semaphore, 
                                                domain_name, 
                                                0
                                            )
                                        )
                                        tasks.append(new_task)
                        except Exception as e:
                            logger.error(f"Error processing task: {e}")
                            continue
            
        return product_urls
    
    async def _crawl_url(
        self, 
        url: str, 
        base_url: str, 
        visited_urls: Set[str], 
        queued_urls: Set[str], 
        product_urls: Set[str], 
        session: aiohttp.ClientSession, 
        semaphore: asyncio.Semaphore, 
        domain_name: str, 
        depth: int
    ) -> Set[str]:
        if depth > self.max_depth:
            return set()
        
        visited_urls.add(url)
        queued_urls.discard(url)
        
        if self._is_likely_product_url(url, domain_name):
            product_urls.add(url)
        
        new_urls = set()
        
        try:
            async with self.rate_limiter:
                async with semaphore:
                    # Get random user agent
                    headers = {'User-Agent': self.user_agent.random}
                    
                    async with session.get(url, headers=headers, timeout=10) as response:
                        if response.status != 200:
                            logger.warning(f"Failed to fetch {url}: HTTP {response.status}")
                            return new_urls
                        
                        html_content = await response.text()
                        soup = BeautifulSoup(html_content, 'lxml')
                        
                        if self._is_product_page_content(soup, domain_name):
                            product_urls.add(url)
                        
                        for link in soup.find_all('a', href=True):
                            href = link['href']
                            
                            # Normalize the URL
                            if href.startswith('/'):
                                full_url = urljoin(base_url, href)
                            elif href.startswith(('http://', 'https://')):
                                if urlparse(href).netloc != urlparse(base_url).netloc:
                                    continue
                                full_url = href
                            else:
                                continue
                            
                            if self._should_exclude_url(full_url):
                                continue
                            
                            if full_url not in visited_urls and full_url not in queued_urls:
                                new_urls.add(full_url)
                                
                                if self._is_likely_product_url(full_url, domain_name):
                                    product_urls.add(full_url)
        
        except Exception as e:
            logger.error(f"Error crawling {url}: {e}")
        
        return new_urls
    
    def _is_likely_product_url(self, url: str, domain_name: str) -> bool:
        if self.site_detector.is_product_url(url, domain_name):
            return True
        
        for pattern in self.PRODUCT_URL_PATTERNS:
            if re.search(pattern, url):
                return True
        
            return True
        
        if re.search(r'/[a-zA-Z0-9-]+-[a-zA-Z0-9-]+$', url) and not self._should_exclude_url(url):
            return True
            
        return False
    
    def _should_exclude_url(self, url: str) -> bool:
        
        for pattern in self.EXCLUDED_PATTERNS:
            if re.search(pattern, url):
                return True
        
        for ext in self.EXCLUDED_EXTENSIONS:
            if url.endswith(ext):
                return True
                
        return False
    
    def _is_product_page_content(self, soup: BeautifulSoup, domain_name: str) -> bool:
        
        if self.site_detector.is_product_page_content(soup, domain_name):
            return True
            
        if soup.find('script', type='application/ld+json'):
            scripts = soup.find_all('script', type='application/ld+json')
            for script in scripts:
                try:
                    json_data = json.loads(script.string)
                    if '@type' in json_data and json_data['@type'] == 'Product':
                        return True
                    if '@graph' in json_data:
                        for item in json_data['@graph']:
                            if '@type' in item and item['@type'] == 'Product':
                                return True
                except:
                    logger.warning("Failed to parse JSON-LD script.")
        
        og_type = soup.find('meta', property='og:type')
        if og_type and og_type.get('content', '') == 'product':
            return True
        
        indicators = [
            soup.find('span', {'class': re.compile(r'price', re.I)}),
            soup.find('div', {'class': re.compile(r'price', re.I)}),
            
            soup.find('button', text=re.compile(r'add to (cart|bag)', re.I)),
            soup.find('a', text=re.compile(r'add to (cart|bag)', re.I)),
            soup.find('button', {'class': re.compile(r'(cart|add)', re.I)}),
            
            soup.find('div', {'class': re.compile(r'product(-info|-details|-description)', re.I)}),
            soup.find('div', {'id': re.compile(r'product(-info|-details|-description)', re.I)})
        ]
        
        return sum(1 for i in indicators if i is not None) >= 2
