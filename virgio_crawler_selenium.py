import time
import json
from base_crawler import BaseCrawler
from logger import get_configured_logger
from typing import List, Set
from constants import Constant
from selenium import webdriver
from selenium.webdriver.common.by import By


from fake_useragent import UserAgent

site_name = "virgio"
file = "crawler"
base_url, core_url = Constant().URL_MAPPING.get(site_name)

logging = get_configured_logger(f"{site_name}_{file}.log")
logger = logging.getLogger(f"{site_name}_{file}")

class VirgioCrawler(BaseCrawler):
    """
    Specialized crawler for Virgio website.
    """
    
    def __init__(self):
        """Initialize the crawler."""
        self.user_agent = UserAgent()
    
    def _is_product_url(self, url: str) -> bool:
        """Check if a URL is likely to be a product URL."""
        for pattern in Constant().VIGIO_PRODUCT_PATTERNS:
            if pattern in url:
                for exclude in Constant().VIGIO_EXCLUDE_PATTERNS:
                    if exclude in url:
                        return False
                return True
        return False
    
    def _extract_links_from_collections(self, driver: webdriver.Chrome) -> Set[str]:
        """Extract product links from collection pages."""
        product_urls = set()
        
        try:
            logger.info("Looking for collection links...")
            collection_links = []
            
            collection_selectors = [
                "//a[contains(@href, '/collections/')]",
                "//a[contains(@class, 'collection')]",
                "//div[contains(@class, 'collection')]//a",
                "//div[contains(@class, 'menu')]//a",
                "//nav//a"
            ]
            
            for selector in collection_selectors:
                try:
                    elements = driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        href = element.get_attribute("href")
                        if href and isinstance(href, str) and core_url in href and "/collections/" in href:
                            collection_links.append(href)
                except Exception:
                    logger.error(f"Error finding collections with selector {selector}: {e}")
                    continue
            
            logger.info(f"Found {len(collection_links)} collection links")
            
            for i, collection_url in enumerate(collection_links[:5]):  # Limit to 5 collections for speed
                try:
                    logger.info(f"Visiting collection {i+1}/{min(5, len(collection_links))}: {collection_url}")
                    driver.get(collection_url)
                    time.sleep(5)  # Wait for page to load
                    
                    for _ in range(3):
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(2)
                    
                    product_selectors = [
                        "//a[contains(@href, '/products/')]",
                        "//div[contains(@class, 'product')]//a",
                        "//div[contains(@class, 'item')]//a",
                        "//div[contains(@class, 'card')]//a"
                    ]
                    
                    for selector in product_selectors:
                        try:
                            elements = driver.find_elements(By.XPATH, selector)
                            for element in elements:
                                href = element.get_attribute("href")
                                if href and isinstance(href, str) and core_url in href:
                                    if self._is_product_url(href):
                                        product_urls.add(href)
                                        logger.info(f"Found product URL: {href}")
                        except Exception as e:
                            logger.error(f"Error finding products with selector {selector}: {e}")
                            continue
                
                except Exception as e:
                    logger.error(f"Error processing collection {collection_url}: {e}")
                    continue
        
        except Exception as e:
            logger.error(f"Error extracting links from collections: {e}")
        
        return product_urls
    
    def _extract_links_from_search(self, driver: webdriver.Chrome) -> Set[str]:
        """Extract product links from search results."""
        product_urls = set()
        
        try:
            
            for term in Constant().COMMON_SEARCH_TERMS:
                try:
                    search_url = f"{base_url}search?q={term}"
                    logger.info(f"Searching for: {term}")
                    driver.get(search_url)
                    time.sleep(5)  # Wait for page to load
                    
                    for _ in range(3):
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(2)
                    
                    product_selectors = [
                        "//a[contains(@href, '/products/')]",
                        "//div[contains(@class, 'product')]//a",
                        "//div[contains(@class, 'item')]//a",
                        "//div[contains(@class, 'card')]//a"
                    ]
                    
                    for selector in product_selectors:
                        try:
                            elements = driver.find_elements(By.XPATH, selector)
                            for element in elements:
                                href = element.get_attribute("href")
                                if href and isinstance(href, str) and core_url in href:
                                    if self._is_product_url(href):
                                        product_urls.add(href)
                                        logger.info(f"Found product URL from search: {href}")
                        except Exception:
                            logger.info(f"Error finding products with selector {selector}: {e}")
                            continue
                
                except Exception as e:
                    logger.error(f"Error processing search for {term}: {e}")
                    continue
        
        except Exception as e:
            logger.error(f"Error extracting links from search: {e}")
        
        return product_urls
    
    def crawl(self) -> List[str]:
        """
        Crawl Virgio to discover product URLs.
        
        Returns:
            A list of product URLs discovered
        """
        logger.info("Starting Virgio crawler")
        product_urls = set()
        driver = None
        
        try:
            driver = self._setup_driver()
            
            logger.info("Loading homepage")
            driver.get(base_url)
            time.sleep(5)
            
            self._handle_cookie_consent(driver)
            
            collection_product_urls = self._extract_links_from_collections(driver)
            product_urls.update(collection_product_urls)
            logger.info(f"Found {len(collection_product_urls)} product URLs from collections")
            
            search_product_urls = self._extract_links_from_search(driver)
            product_urls.update(search_product_urls)
            logger.info(f"Found {len(search_product_urls)} product URLs from search")
            
        except Exception as e:
            logger.error(f"Error during crawling: {e}")
        
        finally:
            if driver:
                try:
                    driver.quit()
                except Exception:
                    logger.error("Error quitting driver")
                    pass
        
        product_url_list = list(product_urls)
        logger.info(f"Completed crawl. Found {len(product_url_list)} product URLs.")
        return product_url_list

if __name__ == "__main__":
    crawler = VirgioCrawler()
    product_urls = crawler.crawl()
    
    results = {
            f"{base_url}": list(product_urls)
        }
        
    with open(f"{site_name}_product_urls.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Found {len(product_urls)} product URLs from Virgio")
    print(f"Results saved to {site_name}_product_urls.json")
