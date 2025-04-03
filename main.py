import logging
from typing import List, Dict
import validators


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

        domain = domain.strip()
        if not domain.startswith(('http://', 'https://')):
            domain = f"https://{domain}"
        
        if validators.url(domain):
            validated_domains.append(domain)
        else:
            logger.warning(f"Invalid domain URL: {domain}")
    
    return validated_domains

def extract_product_data(product: Dict) -> Dict: ...