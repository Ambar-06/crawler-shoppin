# Approach to E-commerce Product URL Crawling

This document outlines the methodology used to identify and extract product URLs from e-commerce websites.

## Architecture Overview

The project follows a modular architecture with the following components:

1. **Base Crawler Class**: Provides common functionality for all specialized crawlers
2. **Specialized Crawlers**: Implement site-specific logic for each e-commerce platform
3. **Constants Module**: Centralizes configuration and patterns
4. **Logger Module**: Provides standardized logging across all components

## Challenges in E-commerce Crawling

Identifying product URLs across different e-commerce platforms presents several challenges:

1. **Varying URL patterns**: Different platforms use different URL structures (e.g., `/product/`, `/p-`, `/item/`)
2. **Dynamic content loading**: Many sites use JavaScript to load products
3. **Pagination**: Products may be spread across multiple pages
4. **Anti-scraping measures**: Websites implement measures to prevent automated crawling
5. **Site-specific structures**: Each e-commerce platform has unique page layouts and navigation patterns

## Our Approach

### 1. Modular Design

The crawler is designed with modularity in mind:

- **BaseCrawler**: Contains common functionality like browser setup, cookie handling, and popup management
- **Specialized Crawlers**: Extend the base crawler with site-specific implementations
- **Centralized Constants**: Store all URL patterns and configurations in a single location

This approach allows for:
- Code reusability
- Easier maintenance
- Simpler addition of new e-commerce platforms

### 2. Dynamic Category Discovery

Instead of relying on hardcoded category URLs, the crawlers:

- Automatically discover category URLs from the homepage
- Interact with navigation menus to reveal more categories
- Fall back to predefined URLs only if discovery fails

This makes the crawlers more robust against site changes and less reliant on manual updates.

### 3. URL Pattern Recognition

We identify product URLs through several methods:

- **Path analysis**: Looking for common product URL patterns such as:
  - `/product/`
  - `/p-`
  - `/item/`
  - `/products/`
  - `/shop/`

- **Exclusion patterns**: Filtering out non-product URLs like:
  - `/cart/`
  - `/account/`
  - `/login/`
  - `/category/`

### 4. Browser Automation with Selenium

We use Selenium WebDriver to:

- Handle JavaScript-rendered content
- Interact with dynamic elements
- Scroll pages to load lazy-loaded content
- Handle cookie consent and popups

### 5. Anti-Bot Evasion

To avoid detection by anti-scraping mechanisms, we implement:

- Random delays between requests
- User-agent rotation
- Browser fingerprint modification
- Handling of cookie consent and popups

### 6. Robust Error Handling

The crawlers implement comprehensive error handling:

- Graceful recovery from timeouts and connection errors
- Retry mechanisms for failed requests
- Detailed logging for debugging

## Site-Specific Implementations

### 1. TataCliq Crawler

- **URL Patterns**: Identifies product URLs containing `/p-`, `/-p-`, `/product/`, `/mdp/`, `/pdp/`, `/buy/`, `/shop/`
- **Category Discovery**: Dynamically discovers category URLs containing `/c-`
- **Scrolling**: Implements page scrolling to load lazy-loaded products
- **Search-based Crawling**: Uses search functionality with common terms to discover more products

### 2. Nykaa Fashion Crawler

- **URL Patterns**: Identifies product URLs containing `/buy/`, `/product/`, `/p/`, `/products/`, `/item/`
- **Navigation**: Navigates through category pages and pagination
- **Content Analysis**: Examines page content for product indicators

### 3. Virgio Crawler

- **URL Patterns**: Focuses on URLs containing `/products/`
- **Exclusion Patterns**: Filters out URLs containing `/collections/`, `/pages/`, `/smile-in-style`, `/know-your-size`
- **Category Navigation**: Navigates through category pages to discover products

### 4. Westside Crawler

- **URL Patterns**: Identifies product URLs containing `/products/`, `/shop/`
- **Category and Search Crawling**: Combines category navigation and search functionality
- **Exclusion Patterns**: Filters out URLs containing `/collection/`, `/collections/`

## Performance Optimization

To ensure efficient crawling:

- **Headless Browser**: Uses headless mode for better performance
- **Controlled Scrolling**: Limits scrolling to avoid excessive page loading
- **Random Delays**: Implements random delays between requests to avoid detection
- **Resource Cleanup**: Ensures proper cleanup of browser resources

## Conclusion

By combining a modular architecture, dynamic discovery, and site-specific optimizations, our crawler effectively identifies product URLs across different e-commerce platforms while maintaining robustness and adaptability to site changes.
