#!/usr/bin/env python3
"""
E-commerce Product URL Crawler

This script crawls e-commerce websites to discover product URLs.
"""

import asyncio
import json
import argparse
import logging
import os
import validators
from typing import List, Dict

from crawler import ProductURLCrawler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("crawler.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("ecommerce_crawler")

def validate_domains(domains: List[str]) -> List[str]:
    """
    Validate and normalize domain URLs.
    
    Args:
        domains: List of domain URLs to validate
        
    Returns:
        List of validated and normalized domain URLs
    """
    validated_domains = []
    
    for domain in domains:
        # Strip whitespace
        domain = domain.strip()
        
        if not domain.startswith(('http://', 'https://')):
            domain = f"https://{domain}"
        
        # Validate URL
        if validators.url(domain):
            validated_domains.append(domain)
        else:
            logger.warning(f"Invalid domain URL: {domain}")
    
    return validated_domains

async def main():
    """
    Main function to run the crawler.
    """
    parser = argparse.ArgumentParser(description='E-commerce Product URL Crawler')
    parser.add_argument('--domains', nargs='+', help='List of domains to crawl', 
                        default=[
                            'https://www.virgio.com/',
                            'https://www.tatacliq.com/',
                            'https://nykaafashion.com/',
                            'https://www.westside.com/'
                        ])
    parser.add_argument('--max-pages', type=int, default=1000, 
                        help='Maximum number of pages to crawl per domain')
    parser.add_argument('--max-depth', type=int, default=5, 
                        help='Maximum depth to crawl')
    parser.add_argument('--concurrency', type=int, default=10, 
                        help='Maximum number of concurrent requests')
    parser.add_argument('--rate-limit', type=int, default=5, 
                        help='Maximum number of requests per second')
    parser.add_argument('--output', type=str, default='product_urls.json', 
                        help='Output file path')
    
    args = parser.parse_args()
    
    domains = validate_domains(args.domains)
    
    if not domains:
        logger.error("No valid domains provided. Exiting.")
        return
    
    logger.info(f"Starting crawler with {len(domains)} domains")
    logger.info(f"Domains: {domains}")
    
    crawler = ProductURLCrawler(
        domains=domains,
        max_pages_per_domain=args.max_pages,
        max_depth=args.max_depth,
        concurrency=args.concurrency,
        rate_limit=args.rate_limit
    )
    
    results = await crawler.crawl_all_domains()
    
    os.makedirs(os.path.dirname(args.output) if os.path.dirname(args.output) else '.', exist_ok=True)
    
    with open(args.output, 'w') as f:
        json.dump(results, f, indent=2)
    
    total_products = sum(len(urls) for urls in results.values())
    logger.info(f"Crawling completed. Found {total_products} product URLs across {len(domains)} domains.")
    logger.info(f"Results saved to {args.output}")
    
    for domain, urls in results.items():
        logger.info(f"  {domain}: {len(urls)} product URLs")

if __name__ == "__main__":
    asyncio.run(main())
