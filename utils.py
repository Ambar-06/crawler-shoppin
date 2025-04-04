"""
Utility functions for the e-commerce product URL crawler.
"""

import json
import logging
from typing import Dict, List, Set
import os
import time
from urllib.parse import urlparse

logger = logging.getLogger("ecommerce_crawler")

def save_results(results: Dict[str, List[str]], output_file: str = "product_urls.json"):
    """
    Save crawl results to a JSON file.
    
    Args:
        results: Dictionary mapping domains to lists of product URLs
        output_file: Path to save the results
    """
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
    
    # Write results to file
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"Results saved to {output_file}")

def load_results(input_file: str) -> Dict[str, List[str]]:
    """
    Load crawl results from a JSON file.
    
    Args:
        input_file: Path to the results file
        
    Returns:
        Dictionary mapping domains to lists of product URLs
    """
    try:
        with open(input_file, 'r') as f:
            results = json.load(f)
        return results
    except Exception as e:
        logger.error(f"Error loading results from {input_file}: {e}")
        return {}

def merge_results(results1: Dict[str, List[str]], results2: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """
    Merge two sets of crawl results.
    
    Args:
        results1: First set of results
        results2: Second set of results
        
    Returns:
        Merged results
    """
    merged = results1.copy()
    
    for domain, urls in results2.items():
        if domain in merged:
            # Convert to set to remove duplicates
            merged_urls = set(merged[domain])
            merged_urls.update(urls)
            merged[domain] = list(merged_urls)
        else:
            merged[domain] = urls
    
    return merged

def print_summary(results: Dict[str, List[str]]):
    """
    Print a summary of crawl results.
    
    Args:
        results: Dictionary mapping domains to lists of product URLs
    """
    total_products = sum(len(urls) for urls in results.values())
    logger.info(f"Crawling completed. Found {total_products} product URLs across {len(results)} domains.")
    
    # Print breakdown by domain
    for domain, urls in results.items():
        logger.info(f"  {domain}: {len(urls)} product URLs")

def get_domain_name(url: str) -> str:
    """
    Extract the domain name from a URL.
    
    Args:
        url: The URL
        
    Returns:
        The domain name
    """
    parsed = urlparse(url)
    domain = parsed.netloc
    # Remove 'www.' prefix if present
    if domain.startswith('www.'):
        domain = domain[4:]
    return domain

def create_output_filename(domain: str) -> str:
    """
    Create an output filename for a domain.
    
    Args:
        domain: The domain name
        
    Returns:
        Output filename
    """
    domain_name = get_domain_name(domain)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    return f"product_urls_{domain_name}_{timestamp}.json"
