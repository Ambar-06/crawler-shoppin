#!/usr/bin/env python3
"""
Specialized crawler for Nykaa Fashion website
"""

import time
import json
from logger import get_configured_logger
import random
from typing import List, Set
from urllib.parse import urlparse
from constants import Constant
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent

logging = get_configured_logger("nykaa_crawler.log")
logger = logging.getLogger("nykaa_crawler")

class NykaaFashionCrawler:
    """
    Specialized crawler for Nykaa Fashion website.
    """
    
    def __init__(self):
        """Initialize the crawler."""
        self.user_agent = UserAgent()
    
    def _setup_driver(self) -> webdriver.Chrome:
        """Set up and return a Chrome browser instance."""
        chrome_options = Options()
        # chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument(f"--user-agent={self.user_agent.random}")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        
        chrome_prefs = {
            "profile.default_content_setting_values.notifications": 1,
            "profile.default_content_setting_values.cookies": 1,
        }
        chrome_options.add_experimental_option("prefs", chrome_prefs)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(30)
        
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver
    
    def _is_product_url(self, url: str) -> bool:
        """Check if a URL is likely to be a product URL."""
        for pattern in Constant().NYKAA_PRODUCT_PATTERNS:
            if pattern in url:
                for exclude in Constant().NYKAA_EXCLUDE_PATTERNS:
                    if exclude in url:
                        return False
                return True
        return False
    
    def _extract_links_from_categories(self, driver: webdriver.Chrome) -> Set[str]:
        """Extract product links from category pages."""
        product_urls = set()
        
        try:
            logger.info("Looking for category links...")
            category_links = []
            
            category_selectors = [
                "//a[contains(@href, '/category/')]",
                "//a[contains(@href, '/c/')]",
                "//a[contains(@class, 'category')]",
                "//a[contains(@class, 'cat-link')]",
                "//div[contains(@class, 'category')]//a",
                "//div[contains(@class, 'menu')]//a",
                "//nav//a"
            ]
            
            for selector in category_selectors:
                try:
                    elements = driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        href = element.get_attribute("href")
                        if href and isinstance(href, str) and "nykaafashion.com" in href:
                            category_links.append(href)
                except Exception:
                    logger.info(f"Error finding categories with selector {selector}")
                    continue
            
            logger.info(f"Found {len(category_links)} category links")
            
            for i, category_url in enumerate(category_links[:5]):  # Limit to 5 categories for speed
                try:
                    logger.info(f"Visiting category {i+1}/{min(5, len(category_links))}: {category_url}")
                    driver.get(category_url)
                    time.sleep(5)  
                    
                    for _ in range(3):
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(2)
                    
                    product_selectors = [
                        "//a[contains(@href, '/buy/')]",
                        "//a[contains(@href, '/product/')]",
                        "//a[contains(@href, '/p/')]",
                        "//a[contains(@href, '/products/')]",
                        "//a[contains(@href, '/item/')]",
                        "//div[contains(@class, 'product')]//a",
                        "//div[contains(@class, 'item')]//a",
                        "//div[contains(@class, 'card')]//a"
                    ]
                    
                    for selector in product_selectors:
                        try:
                            elements = driver.find_elements(By.XPATH, selector)
                            for element in elements:
                                href = element.get_attribute("href")
                                if href and isinstance(href, str) and "nykaafashion.com" in href:
                                    if self._is_product_url(href):
                                        product_urls.add(href)
                                        logger.info(f"Found product URL: {href}")
                        except Exception as e:
                            logger.error(f"Error finding products with selector {selector}: {e}")
                            continue
                
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
            search_terms = ["dress"]
            
            for term in search_terms:
                try:
                    search_url = f"https://nykaafashion.com/search?q={term}"
                    logger.info(f"Searching for: {term}")
                    driver.get(search_url)
                    time.sleep(5) 
                    
                    for _ in range(3):
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(2)
                    
                    product_selectors = [
                        "//a[contains(@href, '/buy/')]",
                        "//a[contains(@href, '/product/')]",
                        "//a[contains(@href, '/p/')]",
                        "//a[contains(@href, '/products/')]",
                        "//a[contains(@href, '/item/')]",
                        "//div[contains(@class, 'product')]//a",
                        "//div[contains(@class, 'item')]//a",
                        "//div[contains(@class, 'card')]//a"
                    ]
                    
                    for selector in product_selectors:
                        try:
                            elements = driver.find_elements(By.XPATH, selector)
                            for element in elements:
                                href = element.get_attribute("href")
                                if href and isinstance(href, str) and "nykaafashion.com" in href:
                                    if self._is_product_url(href):
                                        product_urls.add(href)
                                        logger.info(f"Found product URL from search: {href}")
                        except Exception:
                            logger.info(f"Error finding products with selector {selector}")
                            continue
                
                except Exception as e:
                    logger.error(f"Error processing search for {term}: {e}")
                    continue
        
        except Exception as e:
            logger.error(f"Error extracting links from search: {e}")
        
        return product_urls
    
    def crawl(self) -> List[str]:
        """
        Crawl Nykaa Fashion to discover product URLs.
        
        Returns:
            A list of product URLs discovered
        """
        logger.info("Starting Nykaa Fashion crawler")
        product_urls = set()
        driver = None
        
        try:
            driver = self._setup_driver()
            
            logger.info("Loading homepage")
            driver.get("https://nykaafashion.com/")
            time.sleep(5) 
            
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
                except Exception:
                    logger.info(f"Error quitting driver: {e}")
                    pass
        
        product_url_list = list(product_urls)
        logger.info(f"Completed crawl. Found {len(product_url_list)} product URLs.")
        return product_url_list

if __name__ == "__main__":
    crawler = NykaaFashionCrawler()
    product_urls = crawler.crawl()
    
    with open("nykaa_product_urls.json", "w") as f:
        json.dump(product_urls, f, indent=2)
    
    print(f"Found {len(product_urls)} product URLs from Nykaa Fashion")
    print(f"Results saved to nykaa_product_urls.json")
