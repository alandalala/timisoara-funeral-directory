"""
Google Search Tool - Finds funeral home websites via search.
Uses human-like behavior to avoid detection.
"""
import requests
from typing import List, Set
from urllib.parse import urlparse, quote_plus
from bs4 import BeautifulSoup

from config.settings import SEARCH_QUERIES
from utils import get_human_headers, human_delay, HumanBehaviorSimulator


class GoogleSearchTool:
    """
    Search for funeral home websites using DuckDuckGo.
    DuckDuckGo HTML is more scraping-friendly than Google.
    """
    
    def __init__(self):
        self.found_urls: Set[str] = set()
        self.behavior = HumanBehaviorSimulator()
        
        # Domains to exclude
        self.excluded_domains = {
            # Social media
            'facebook.com', 'instagram.com', 'twitter.com', 'linkedin.com',
            'youtube.com', 'tiktok.com', 'pinterest.com',
            # Search engines
            'google.com', 'google.ro', 'bing.com', 'duckduckgo.com',
            # Reference sites
            'wikipedia.org', 'wikidata.org',
            # Government
            'anaf.ro', 'gov.ro',
            # Business directories
            'listafirme.ro', 'risco.ro', 'termene.ro',
            'paginiaurii.ro', 'firme.info', 'cylex.ro',
            # Funeral directories (list multiple companies)
            'condoleante.ro', 'sefuro.ro', 'alo-deces.ro',
            'funebris.ro', 'funero.ro', 'serviciifunerare.ro',
        }
    
    def search_duckduckgo(self, query: str, max_results: int = 10) -> List[str]:
        """
        Search DuckDuckGo HTML version.
        
        Args:
            query: Search query string
            max_results: Maximum number of URLs to return
        
        Returns:
            List of URLs found
        """
        urls = []
        
        try:
            search_url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
            
            # Simple headers without the complex behavior simulator
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'ro-RO,ro;q=0.9,en;q=0.8',
            }
            
            response = requests.get(search_url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all links that contain uddg parameter (DuckDuckGo redirect URLs)
            for link in soup.find_all('a', href=True):
                href = link.get('href', '')
                
                # Only process DuckDuckGo redirect links
                if '//duckduckgo.com/l/?uddg=' not in href:
                    continue
                
                # Extract actual URL from DuckDuckGo redirect
                try:
                    import urllib.parse
                    parsed = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
                    if 'uddg' in parsed:
                        actual_url = urllib.parse.unquote(parsed['uddg'][0])
                        
                        if actual_url and actual_url.startswith('http'):
                            # Filter out excluded domains
                            parsed_url = urlparse(actual_url)
                            domain = parsed_url.netloc.lower().replace('www.', '')
                            
                            # Check excluded domains (only social media, search engines, etc.)
                            if any(excl in domain for excl in self.excluded_domains):
                                continue
                            
                            if actual_url not in self.found_urls:
                                urls.append(actual_url)
                                self.found_urls.add(actual_url)
                                
                            if len(urls) >= max_results:
                                break
                except Exception:
                    continue
            
            print(f"  Found {len(urls)} URLs for: {query[:50]}...")
            return urls
            
        except Exception as e:
            print(f"  Error searching: {e}")
            return urls
    
    def find_funeral_homes(self, 
                           queries: List[str] = None, 
                           max_per_query: int = 5,
                           total_limit: int = None) -> List[str]:
        """
        Search for funeral home websites using predefined queries.
        
        Args:
            queries: List of search queries (uses SEARCH_QUERIES if None)
            max_per_query: Maximum results per query
            total_limit: Total maximum URLs to return
        
        Returns:
            List of unique funeral home website URLs
        """
        if queries is None:
            queries = SEARCH_QUERIES
        
        all_urls = []
        
        print(f"\n{'='*50}")
        print(f"Searching for funeral home websites...")
        print(f"Queries: {len(queries)}, Max per query: {max_per_query}")
        print(f"{'='*50}")
        
        for i, query in enumerate(queries):
            print(f"\n[{i+1}/{len(queries)}] Searching: {query}")
            
            urls = self.search_duckduckgo(query, max_per_query)
            all_urls.extend(urls)
            
            # Check total limit
            if total_limit and len(all_urls) >= total_limit:
                all_urls = all_urls[:total_limit]
                break
            
            # Human-like pause between searches
            if i < len(queries) - 1:
                human_delay('between_sites')
        
        # Remove duplicates while preserving order
        unique_urls = list(dict.fromkeys(all_urls))
        
        print(f"\n{'='*50}")
        print(f"Total unique URLs found: {len(unique_urls)}")
        print(f"{'='*50}\n")
        
        return unique_urls
    
    def find_funeral_homes_in_county(self, 
                                      county: str, 
                                      city: str = None, 
                                      max_results: int = 10) -> List[str]:
        """
        Search for funeral homes in a specific county/city.
        
        Args:
            county: County name (e.g., "Timiș")
            city: Optional city name (e.g., "Timișoara")
            max_results: Maximum URLs to return
        
        Returns:
            List of funeral home website URLs
        """
        location = city if city else county
        
        queries = [
            f"servicii funerare {location}",
            f"pompe funebre {location}",
            f"casa funerara {location}",
            f"firma funerara {location}",
        ]
        
        return self.find_funeral_homes(
            queries=queries,
            max_per_query=max_results // len(queries) + 1,
            total_limit=max_results
        )
