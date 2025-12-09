"""
Firecrawl Extractor Tool - Uses Firecrawl API to convert websites to markdown.
"""
from typing import Optional, Dict
from firecrawl import FirecrawlApp
from config.settings import FIRECRAWL_API_KEY, USER_AGENT
import time


class FirecrawlExtractorTool:
    """
    Tool to extract website content as markdown using Firecrawl.
    """
    
    def __init__(self, api_key: str = FIRECRAWL_API_KEY):
        if not api_key:
            raise ValueError("FIRECRAWL_API_KEY must be set")
        
        self.app = FirecrawlApp(api_key=api_key)
    
    def scrape_url(self, url: str, include_subpages: bool = False) -> Dict:
        """
        Scrape a URL and return markdown content.
        
        Args:
            url: URL to scrape
            include_subpages: Whether to crawl subpages like /about, /contact
        
        Returns:
            Dict with 'markdown', 'metadata', 'success' keys
        """
        try:
            print(f"Scraping {url} with Firecrawl...")
            
            # Basic scrape configuration
            params = {
                'formats': ['markdown', 'html'],
                'onlyMainContent': True,
                'waitFor': 2000,  # Wait 2 seconds for JS to load
            }
            
            result = self.app.scrape_url(url, params=params)
            
            if result and 'markdown' in result:
                markdown_content = result['markdown']
                
                # If include_subpages, try to find and scrape common pages
                subpages_content = ""
                if include_subpages:
                    subpages_content = self._scrape_subpages(url)
                
                return {
                    'success': True,
                    'markdown': markdown_content + "\n\n" + subpages_content if subpages_content else markdown_content,
                    'metadata': result.get('metadata', {}),
                    'url': url
                }
            else:
                return {
                    'success': False,
                    'error': 'No markdown content returned',
                    'url': url
                }
                
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return {
                'success': False,
                'error': str(e),
                'url': url
            }
    
    def _scrape_subpages(self, base_url: str) -> str:
        """
        Attempt to scrape common subpages (about, contact, services).
        """
        from urllib.parse import urljoin
        
        subpages = ['/about', '/despre-noi', '/contact', '/contacte', '/servicii', '/services']
        combined_content = ""
        
        for subpage in subpages:
            try:
                subpage_url = urljoin(base_url, subpage)
                time.sleep(1)  # Brief delay between requests
                
                result = self.app.scrape_url(subpage_url, {
                    'formats': ['markdown'],
                    'onlyMainContent': True
                })
                
                if result and 'markdown' in result:
                    combined_content += f"\n\n--- Content from {subpage} ---\n\n"
                    combined_content += result['markdown']
                    
            except Exception as e:
                # Subpage might not exist, continue
                continue
        
        return combined_content
    
    def crawl_website(self, url: str, max_pages: int = 5) -> Dict:
        """
        Crawl an entire website (up to max_pages) and return combined content.
        
        Args:
            url: Base URL to crawl
            max_pages: Maximum number of pages to crawl
        
        Returns:
            Dict with 'markdown', 'pages_crawled', 'success' keys
        """
        try:
            print(f"Crawling website {url}...")
            
            params = {
                'limit': max_pages,
                'scrapeOptions': {
                    'formats': ['markdown'],
                    'onlyMainContent': True
                }
            }
            
            result = self.app.crawl_url(url, params=params)
            
            if result and result.get('success'):
                # Combine all pages' content
                combined_markdown = ""
                pages = result.get('data', [])
                
                for page in pages:
                    if 'markdown' in page:
                        combined_markdown += f"\n\n--- Page: {page.get('url', 'unknown')} ---\n\n"
                        combined_markdown += page['markdown']
                
                return {
                    'success': True,
                    'markdown': combined_markdown,
                    'pages_crawled': len(pages),
                    'base_url': url
                }
            else:
                return {
                    'success': False,
                    'error': 'Crawl failed',
                    'base_url': url
                }
                
        except Exception as e:
            print(f"Error crawling {url}: {e}")
            return {
                'success': False,
                'error': str(e),
                'base_url': url
            }
