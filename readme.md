# E-commerce Product URL Crawler

A modular and scalable web crawler designed to discover and list product URLs across multiple e-commerce websites.

## Objective

The primary task of this crawler is to discover and list all product URLs across multiple e-commerce websites. The crawler can handle various e-commerce platforms and scales efficiently to process large websites with deep hierarchies.

## Features

- **Modular Architecture**: Follows a clean, modular design with a base crawler class and specialized implementations
- **Intelligent URL Discovery**: Identifies product pages by analyzing URL patterns, page content, and site-specific heuristics
- **Dynamic Category Discovery**: Automatically discovers category URLs from homepage and navigation menus
- **Anti-Bot Evasion**: Implements techniques to avoid detection by anti-scraping mechanisms
- **Robust Error Handling**: Gracefully handles exceptions and timeouts during crawling
- **Centralized Constants**: Uses a constants file for easy configuration and maintenance
- **Standardized Logging**: Implements consistent logging across all crawler components

## Project Structure

```
├── base_crawler.py                # Base crawler class with common functionality
├── constants.py                   # Centralized constants and configuration
├── logger.py                      # Logging configuration
├── tatacliq_crawler_selenium.py   # TataCliq specialized crawler
├── nykaa_crawler_selenium.py      # Nykaa Fashion specialized crawler
├── virgio_crawler_selenium.py     # Virgio specialized crawler
├── westside_crawler_selenium.py   # Westside specialized crawler
├── APPROACH.md                    # Detailed explanation of the methodology
└── README.md                      # Project documentation
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Ambar-06/crawler-shoppin.git
cd crawler-shoppin
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Dependencies

The project relies on the following main dependencies:
- Selenium for browser automation
- WebDriverManager for managing browser drivers
- Fake UserAgent for generating user agents

## Usage

### Running Individual Crawlers

Each crawler can be run independently:

```bash
python3 tatacliq_crawler_selenium.py  # Run TataCliq crawler
python3 nykaa_crawler_selenium.py     # Run Nykaa Fashion crawler
python3 virgio_crawler_selenium.py    # Run Virgio crawler
python3 westside_crawler_selenium.py  # Run Westside crawler
```

### Output

Each crawler generates a JSON file with the discovered product URLs:
- `tatacliq_product_urls.json`
- `nykaa_product_urls.json`
- `virgio_product_urls.json`
- `westside_product_urls.json`

The output format is a dictionary mapping domain URLs to lists of product URLs:

```json
{
  "https://www.example.com/": [
    "https://www.example.com/product/item1",
    "https://www.example.com/product/item2",
    ...
  ]
}
```

## Extending the Crawler

To add support for a new e-commerce website:

1. Create a new file for the specialized crawler (e.g., `newsite_crawler_selenium.py`)
2. Extend the `BaseCrawler` class
3. Implement site-specific methods for URL detection and crawling
4. Add site-specific constants to `constants.py`

Example:

```python
from base_crawler import BaseCrawler
from constants import Constant
from logger import get_configured_logger

class NewSiteCrawler(BaseCrawler):
    def __init__(self):
        # Initialize crawler
        
    def _is_product_url(self, url):
        # Implement product URL detection
        
    def crawl(self):
        # Implement crawling logic
```

## Performance Considerations

- The crawlers use a headless browser by default for better performance
- Adjust the scrolling and delay parameters in the crawler implementations for optimal results
- Consider running crawlers in parallel for faster processing of multiple sites

## Troubleshooting

- If you encounter "ChromeDriver not found" errors, ensure you have Chrome installed and WebDriverManager is properly set up
- If websites block the crawler, try adjusting the delay between requests or using different user agent patterns
- For memory issues with large websites, consider limiting the maximum number of pages to crawl

