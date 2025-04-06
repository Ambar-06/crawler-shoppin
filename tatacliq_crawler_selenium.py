import json
import time
import random

from fake_useragent import UserAgent
from base_crawler import BaseCrawler
from constants import Constant
from logger import get_configured_logger
from typing import Set, List

from selenium import webdriver
from selenium.webdriver.common.by import By

site_name = "tatacliq"
file = "crawler"

logging = get_configured_logger(f"{site_name}_{file}.log")
logger = logging.getLogger(f"{site_name}_{file}")

base_url, core_url = Constant().URL_MAPPING.get(site_name)

class TataCliqCrawler(BaseCrawler):
    """Specialized crawler for TataCliq website."""
    
    def __init__(self):
        """
        Initialize the TataCliq crawler.
        
        Args:
            max_pages: Maximum number of pages to crawl per section
        """
        self.user_agent = UserAgent()
        
        self.fallback_category_urls = [
            "https://www.tatacliq.com/men-clothing/c-msh11",
            "https://www.tatacliq.com/women-clothing/c-wsh11",
            "https://www.tatacliq.com/men-clothing-tshirts/c-msh11101001",
            "https://www.tatacliq.com/men-clothing-shirts/c-msh11101002",
            "https://www.tatacliq.com/women-clothing-tops-tees/c-wsh11101001",
            "https://www.tatacliq.com/women-clothing-dresses/c-wsh11101002",
            "https://www.tatacliq.com/men-footwear/c-msh12",
            "https://www.tatacliq.com/women-footwear/c-wsh12"
        ]
        
        self.category_urls = []
    
    def _is_product_url(self, url: str) -> bool:
        """Check if a URL is likely to be a product URL."""
        if not url or not isinstance(url, str):
            return False
            
        for pattern in Constant().TATACLIQ_EXCLUDE_PATTERNS:
            if pattern in url:
                return False
                
        for pattern in Constant().TATACLIQ_PRODUCT_PATTERNS:
            if pattern in url:
                return True
                
        return False
    
    def _is_category_url(self, url: str) -> bool:
        """Check if a URL is likely to be a category URL."""
        if not url or not isinstance(url, str):
            return False
            
        if "/c-" in url and "tatacliq.com" in url:
            for product_pattern in self.product_patterns:
                if product_pattern in url:
                    return False
            return True
        
        return False
    
    def _discover_category_urls(self, driver: webdriver.Chrome) -> Set[str]:
        """Discover category URLs from the homepage and navigation menus."""
        category_urls = set()
        
        try:
            logger.info("Discovering category URLs from homepage")
            
            elements = driver.find_elements(By.TAG_NAME, "a")
            
            for element in elements:
                try:
                    href = element.get_attribute("href")
                    if href and self._is_category_url(href):
                        category_urls.add(href)
                        logger.info(f"Found category URL: {href}")
                except Exception:
                    logger.error(f"Error getting href from element: {e}")
                    continue
            
            menu_selectors = [
                "//li[contains(@class, 'menu-item')]",
                "//div[contains(@class, 'menu')]//a",
                "//nav//a",
                "//div[contains(@class, 'category-menu')]//a",
                "//div[contains(@class, 'main-menu')]//a"
            ]
            
            for selector in menu_selectors:
                try:
                    menu_items = driver.find_elements(By.XPATH, selector)
                    for item in menu_items[:5]:  # Limit to first 5 menu items to avoid too many clicks
                        try:
                            webdriver.ActionChains(driver).move_to_element(item).perform()
                            time.sleep(1)
                            
                            dropdown_links = driver.find_elements(By.TAG_NAME, "a")
                            for link in dropdown_links:
                                try:
                                    href = link.get_attribute("href")
                                    if href and self._is_category_url(href):
                                        category_urls.add(href)
                                        logger.info(f"Found category URL from dropdown: {href}")
                                except Exception:
                                    logger.error(f"Error getting href from dropdown link: {e}")
                                    continue
                        except Exception:
                            logger.error(f"Error clicking on menu item: {e}")
                            continue
                except Exception:
                    logger.error(f"Error finding menu items with selector {selector}: {e}")
                    continue
            
            logger.info(f"Discovered {len(category_urls)} category URLs")
            
        except Exception as e:
            logger.error(f"Error discovering category URLs: {e}")
        
        return category_urls
    
    def _extract_links_from_page(self, driver: webdriver.Chrome) -> Set[str]:
        """Extract all links from the current page."""
        links = set()
        
        try:
            elements = driver.find_elements(By.TAG_NAME, "a")
            
            for element in elements:
                try:
                    href = element.get_attribute("href")
                    if href and isinstance(href, str) and "tatacliq.com" in href:
                        if self._is_product_url(href):
                            links.add(href)
                            logger.info(f"Found product URL: {href}")
                except Exception:
                    logger.error(f"Error getting href from element: {e}")
                    continue
        except Exception as e:
            logger.error(f"Error extracting links: {e}")
        
        return links
    
    def _extract_links_from_categories(self, driver: webdriver.Chrome) -> Set[str]:
        """Extract product links from category pages."""
        product_urls = set()
        
        try:
            categories_to_visit = list(self.category_urls)
            if not categories_to_visit:
                logger.warning("No category URLs discovered, using fallback URLs")
                # categories_to_visit = self.fallback_category_urls
                logger.warning("No category URLs discovered, using fallback URLs")
                return product_urls
            
            categories_to_visit = categories_to_visit[:min(len(categories_to_visit), 10)]
            
            for i, category_url in enumerate(categories_to_visit):
                try:
                    logger.info(f"Visiting category {i+1}/{len(categories_to_visit)}: {category_url}")
                    driver.get(category_url)
                    time.sleep(5)
                    
                    self._handle_cookie_consent(driver)
                    self._handle_popups(driver)
                    
                    self._scroll_page(driver)
                    
                    # Extract links
                    category_links = self._extract_links_from_page(driver)
                    product_urls.update(category_links)
                    logger.info(f"Found {len(category_links)} product URLs from category {category_url}")
                    
                    time.sleep(random.uniform(2, 4)) # nosec
                    
                except Exception as e:
                    logger.error(f"Error processing category {category_url}: {e}")
                    continue
        
        except Exception as e:
            logger.error(f"Error extracting links from categories: {e}")
        
        return product_urls
    
    def _extract_links_from_search(self, driver: webdriver.Chrome) -> Set[str]:
        """Extract product links from search results."""
        product_urls = set()
        
        try:
            for term in Constant().COMMON_SEARCH_TERMS[:min(len(Constant().COMMON_SEARCH_TERMS), 10)]:
                try:
                    search_url = f"{base_url}search/?searchCategory=all&text={term}"
                    logger.info(f"Searching for: {term}")
                    driver.get(search_url)
                    time.sleep(5)  # Wait for page to load
                    
                    self._handle_cookie_consent(driver)
                    self._handle_popups(driver)
                    
                    self._scroll_page(driver)
                    
                    search_links = self._extract_links_from_page(driver)
                    product_urls.update(search_links)
                    logger.info(f"Found {len(search_links)} product URLs from search term '{term}'")
                    
                    time.sleep(random.uniform(2, 4)) # nosec
                    
                except Exception as e:
                    logger.error(f"Error processing search for {term}: {e}")
                    continue
        
        except Exception as e:
            logger.error(f"Error extracting links from search: {e}")
        
        return product_urls
    
    def crawl(self) -> List[str]:
        """
        Crawl TataCliq website to find product URLs.
        
        Returns:
            A list of product URLs discovered
        """
        logger.info("Starting TataCliq crawler")
        product_urls = set()
        driver = None
        
        try:
            driver = self._setup_driver()
            
            logger.info("Loading homepage")
            driver.get(base_url)
            time.sleep(5)  # Wait for page to load
            
            self._handle_cookie_consent(driver)
            self._handle_popups(driver)
            
            self.category_urls = self._discover_category_urls(driver)
            
            category_product_urls = self._extract_links_from_categories(driver)
            product_urls.update(category_product_urls)
            logger.info(f"Found {len(category_product_urls)} product URLs from categories")
            
            search_product_urls = self._extract_links_from_search(driver)
            product_urls.update(search_product_urls)
            logger.info(f"Found {len(search_product_urls)} product URLs from search")
            
        except Exception as e:
            logger.error(f"Error during crawling: {e}")
        
        finally:
            if driver:
                try:
                    driver.quit()
                    logger.info("Browser closed")
                except Exception as e:
                    logger.error(f"Error closing browser: {e}")
        
        self._save_results(product_urls)
        
        return list(product_urls)
    
    def _save_results(self, product_urls: Set[str]) -> None:
        """Save the product URLs to a JSON file."""
        results = {
            f"{base_url}": list(product_urls)
        }
        
        with open(f"{site_name}_product_urls.json", 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Results saved to tatacliq_product_urls.json with {len(product_urls)} URLs")

if __name__ == "__main__":
    crawler = TataCliqCrawler()
    product_urls = crawler.crawl()
    print(f"Found {len(product_urls)} product URLs from TataCliq")
