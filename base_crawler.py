from fake_useragent import UserAgent
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from logger import get_configured_logger

logging = get_configured_logger("base_crawler.log")
logger = logging.getLogger("base_crawler")


class BaseCrawler:

    def __init__(self):
        """Initialize the crawler."""
        self.user_agent = UserAgent()

    def _scroll_page(self, driver: webdriver.Chrome) -> None:
        """Scroll down the page to load lazy-loaded content."""
        try:
            last_height = driver.execute_script("return document.body.scrollHeight")
            
            for _ in range(5):  # Scroll 5 times
                # Scroll down
                driver.execute_script("window.scrollBy(0, window.innerHeight);")
                
                time.sleep(2)
                
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
                
        except Exception as e:
            logger.warning(f"Error scrolling page: {e}")
     
    def _setup_driver(self) -> webdriver.Chrome:
        """Set up and return a Chrome browser instance."""
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
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

    def _handle_cookie_consent(self, driver: webdriver.Chrome) -> None:
        """Handle cookie consent popups that might appear on the page."""
        try:
            cookie_button_selectors = [
                "//button[contains(text(), 'Accept') or contains(text(), 'Accept All') or contains(text(), 'I Accept')]",
                "//button[contains(@class, 'cookie') and (contains(text(), 'Accept') or contains(text(), 'OK'))]",
                "//a[contains(text(), 'Accept') or contains(text(), 'Accept All') or contains(text(), 'I Accept')]",
                "//div[contains(@class, 'cookie') and (contains(text(), 'Accept') or contains(text(), 'OK'))]",
                "//button[contains(@id, 'cookie') and (contains(text(), 'Accept') or contains(text(), 'OK'))]"
            ]
            
            for selector in cookie_button_selectors:
                try:
                    WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    button = driver.find_element(By.XPATH, selector)
                    button.click()
                    logger.info("Clicked cookie consent button")
                    time.sleep(1)
                    return
                except (TimeoutException, NoSuchElementException, WebDriverException):
                    continue
        except Exception as e:
            logger.error(f"Error handling cookie consent: {e}")

    def _handle_popups(self, driver: webdriver.Chrome) -> None:
        """Handle popups like newsletter subscriptions, etc."""
        try:
            popup_close_selectors = [
                "//button[contains(@class, 'close') or contains(@class, 'dismiss') or contains(@class, 'cancel')]",
                "//div[contains(@class, 'close') or contains(@class, 'dismiss') or contains(@class, 'cancel')]",
                "//span[contains(@class, 'close') or contains(@class, 'dismiss') or contains(@class, 'cancel')]",
                "//a[contains(@class, 'close') or contains(@class, 'dismiss') or contains(@class, 'cancel')]",
                "//button[contains(text(), 'Close') or contains(text(), 'Dismiss') or contains(text(), 'Cancel') or contains(text(), 'No thanks')]",
                "//button[contains(@class, 'newsletter-popup-close')]",
                "//div[contains(@class, 'newsletter-popup-close')]",
                "//button[contains(@class, 'popup-close')]",
                "//div[contains(@class, 'popup-close')]"
            ]
            
            for selector in popup_close_selectors:
                try:
                    WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    button = driver.find_element(By.XPATH, selector)
                    button.click()
                    logger.info("Closed a popup")
                    time.sleep(1)
                    return
                except (TimeoutException, NoSuchElementException, WebDriverException):
                    continue
        except Exception as e:
            logger.error(f"Error handling popups: {e}")