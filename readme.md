# E-commerce Product URL Crawler

A scalable web crawler designed to discover and list product URLs across multiple e-commerce websites.

## Objective

The primary task of this crawler is to discover and list all product URLs across multiple e-commerce websites. The crawler can handle various e-commerce platforms and scales efficiently to process large websites with deep hierarchies.

## Features

- **Intelligent URL Discovery**: Identifies product pages by analyzing URL patterns, page content, and site-specific heuristics
- **Scalability**: Handles large websites with thousands of pages efficiently
- **Asynchronous Processing**: Executes crawling in parallel using asyncio for optimal performance
- **Adaptive Learning**: Improves pattern recognition based on discovered product URLs
- **Robustness**: Handles various URL structures across different e-commerce platforms
- **Visualization**: Includes tools to analyze and visualize the discovered product URLs

## Project Structure

```
├── main.py               # Main script to run the crawler
├── crawler.py            # Core crawler implementation
├── site_patterns.py      # Site-specific pattern detection
├── utils.py              # Utility functions
├── test_crawler.py       # Script for testing on individual domains
├── visualize_results.py  # Script to generate HTML reports of results
├── requirements.txt      # Project dependencies
├── APPROACH.md           # Detailed explanation of the methodology
└── README.md             # Project documentation
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Ambar-06/ecommerce-product-url-crawler.git
cd ecommerce-product-url-crawler
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

## Usage

### Basic Usage

Run the crawler with default settings:

```bash
python main.py
```

This will crawl the default domains:
- https://www.virgio.com/
- https://www.tatacliq.com/
- https://nykaafashion.com/
- https://www.westside.com/

### Custom Domains

Specify custom domains to crawl:

```bash
python main.py --domains example1.com example2.com example3.com
```

### Advanced Options

```bash
python main.py --domains example.com --max-pages 500 --max-depth 3 --concurrency 5 --rate-limit 3 --output results.json
```

Parameters:
- `--domains`: List of domains to crawl
- `--max-pages`: Maximum number of pages to crawl per domain (default: 1000)
- `--max-depth`: Maximum depth to crawl (default: 5)
- `--concurrency`: Maximum number of concurrent requests (default: 10)
- `--rate-limit`: Maximum number of requests per second (default: 5)
- `--output`: Output file path (default: product_urls.json)

### Testing Individual Domains

To test the crawler on a single domain:

```bash
python test_crawler.py example.com
```

### Visualizing Results

Generate an HTML report of the crawl results:

```bash
python visualize_results.py product_urls.json
```

This will create an HTML report (`crawler_report.html`) that you can open in a web browser to analyze the discovered product URLs.

## Output Format

The crawler generates a JSON file with the following structure:

```json
{
  "https://www.example1.com/": [
    "https://www.example1.com/product/12345",
    "https://www.example1.com/product/67890",
    ...
  ],
  "https://www.example2.com/": [
    "https://www.example2.com/p/12345",
    "https://www.example2.com/p/67890",
    ...
  ]
}
```

## Approach

Our approach to identifying product URLs combines several techniques:

1. **URL Pattern Recognition**: Analyzing URL structures to identify common product patterns
2. **Content Analysis**: Examining page content for product indicators
3. **Site-Specific Heuristics**: Using domain-specific patterns for better accuracy
4. **Adaptive Learning**: Improving pattern recognition based on discovered URLs

For a detailed explanation of the methodology, see [APPROACH.md](APPROACH.md).

## Performance Considerations

- **Rate Limiting**: The crawler implements rate limiting to avoid overloading servers
- **Concurrency Control**: The number of concurrent requests can be adjusted based on server capacity
- **Memory Usage**: The crawler uses sets to efficiently track visited URLs and avoid duplicates
- **Timeout Handling**: Requests have timeouts to prevent hanging on slow responses

## Limitations

- The crawler respects robots.txt implicitly through rate limiting but does not explicitly parse it
- JavaScript-rendered content may not be fully accessible (consider using a headless browser for such cases)
- Some websites may implement anti-scraping measures that could affect the crawler's performance

