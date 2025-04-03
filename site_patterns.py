from typing import Dict, List, Optional
from bs4 import BeautifulSoup
import re

class SitePatternDetector:
    
    DEFAULT_PATTERNS = {
        'virgio.com': {
            'url_patterns': [r'/products/'],
            'product_selectors': [
                {'tag': 'div', 'attrs': {'class': 'product-details'}},
                {'tag': 'button', 'attrs': {'class': 'add-to-cart'}}
            ],
            'excluded_patterns': [r'/collections/', r'/pages/']
        },
        'tatacliq.com': {
            'url_patterns': [r'/p-', r'/-p-'],
            'product_selectors': [
                {'tag': 'div', 'attrs': {'class': 'ProductDetailsMainCard'}},
                {'tag': 'div', 'attrs': {'class': 'PDPDesktopDescriptionText'}}
            ],
            'excluded_patterns': [r'/c-']
        },
        'nykaafashion.com': {
            'url_patterns': [r'/buy/'],
            'product_selectors': [
                {'tag': 'div', 'attrs': {'class': 'css-1dbjc4n'}},
                {'tag': 'div', 'attrs': {'class': 'product-details'}}
            ],
            'excluded_patterns': [r'/category/', r'/brand/']
        },
        'westside.com': {
            'url_patterns': [r'/products/'],
            'product_selectors': [
                {'tag': 'div', 'attrs': {'class': 'product-single__meta'}},
                {'tag': 'form', 'attrs': {'class': 'product-form'}}
            ],
            'excluded_patterns': [r'/collections/', r'/pages/']
        }
    }
    
    def __init__(self):
        self.site_patterns = self.DEFAULT_PATTERNS.copy()
    
    def add_site_pattern(self, domain: str, url_patterns: List[str], 
                         product_selectors: List[Dict], excluded_patterns: List[str] = None):
        self.site_patterns[domain] = {
            'url_patterns': url_patterns,
            'product_selectors': product_selectors,
            'excluded_patterns': excluded_patterns or []
        }
    
    def is_product_url(self, url: str, domain: str) -> bool:
        matching_domain = None
        for site_domain in self.site_patterns:
            if site_domain in domain:
                matching_domain = site_domain
                break
        
        if not matching_domain:
            return False
        
        for pattern in self.site_patterns[matching_domain]['url_patterns']:
            if re.search(pattern, url):
                for excluded in self.site_patterns[matching_domain]['excluded_patterns']:
                    if re.search(excluded, url):
                        return False
                return True
        
        return False
    
    def is_product_page_content(self, soup: BeautifulSoup, domain: str) -> bool:
        matching_domain = None
        for site_domain in self.site_patterns:
            if site_domain in domain:
                matching_domain = site_domain
                break
        
        if not matching_domain:
            return False
        
        for selector in self.site_patterns[matching_domain]['product_selectors']:
            if soup.find(selector['tag'], selector['attrs']):
                return True
        
        return False
    
    def learn_from_results(self, product_urls: List[str], domain: str):
        
        path_segments = []
        for url in product_urls:
            path = url.split('://', 1)[-1].split('/', 1)[-1]
            segments = path.split('/')
            path_segments.extend(segments)
        
        segment_counts = {}
        for segment in path_segments:
            if segment and not segment.isdigit():
                segment_counts[segment] = segment_counts.get(segment, 0) + 1
        
        for segment, count in segment_counts.items():
            if count >= len(product_urls) * 0.3:
                pattern = f'/{segment}/'
                
                matching_domain = None
                for site_domain in self.site_patterns:
                    if site_domain in domain:
                        matching_domain = site_domain
                        break
                
                if matching_domain and pattern not in self.site_patterns[matching_domain]['url_patterns']:
                    self.site_patterns[matching_domain]['url_patterns'].append(pattern)
