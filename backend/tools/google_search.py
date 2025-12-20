"""
Google Search Tool - Finds funeral home websites via search.
Uses Bing for more reliable results with Romanian queries.
"""
import requests
from typing import List, Set
from urllib.parse import urlparse, quote_plus
from bs4 import BeautifulSoup
import time

from config.settings import SEARCH_QUERIES
from utils import human_delay


class GoogleSearchTool:
    """
    Search for funeral home websites using Bing.
    Bing provides better results for Romanian language queries.
    """
    
    def __init__(self):
        self.found_urls: Set[str] = set()
        
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
    
    def search_bing(self, query: str, max_results: int = None) -> List[str]:
        """
        Search Bing for Romanian funeral services.
        
        Args:
            query: Search query string
            max_results: Maximum number of URLs to return (None = no limit, defaults to 30)
        
        Returns:
            List of URLs found
        """
        urls = []
        max_pages = 5 if not max_results else (max_results // 10) + 1
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ro-RO,ro;q=0.9,en;q=0.8',
        }
        
        for page in range(max_pages):
            try:
                first = page * 10 + 1
                search_url = f"https://www.bing.com/search?q={quote_plus(query)}&first={first}&setlang=ro"
                
                response = requests.get(search_url, headers=headers, timeout=30)
                
                if response.status_code != 200:
                    print(f"  Bing returned status {response.status_code}")
                    break
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find all search result links
                found_on_page = 0
                for result in soup.find_all('li', class_='b_algo'):
                    link = result.find('a', href=True)
                    if link:
                        url = link.get('href', '')
                        
                        if url and url.startswith('http'):
                            # Filter out excluded domains
                            parsed_url = urlparse(url)
                            domain = parsed_url.netloc.lower().replace('www.', '')
                            
                            # Check excluded domains
                            if any(excl in domain for excl in self.excluded_domains):
                                continue
                            
                            if url not in self.found_urls:
                                urls.append(url)
                                self.found_urls.add(url)
                                found_on_page += 1
                                
                                if max_results and len(urls) >= max_results:
                                    break
                
                if found_on_page == 0:
                    break  # No more results
                    
                if max_results and len(urls) >= max_results:
                    break
                    
                # Delay between pages
                if page < max_pages - 1:
                    time.sleep(2)
                    
            except Exception as e:
                print(f"  Error searching Bing page {page+1}: {e}")
                break
        
        print(f"  Found {len(urls)} URLs for: {query[:50]}...")
        return urls
    
    def search_duckduckgo(self, query: str, max_results: int = None) -> List[str]:
        """
        Search using Bing (DuckDuckGo's backend).
        This is an alias for backward compatibility.
        """
        return self.search_bing(query, max_results)
    
    def find_funeral_homes(self, 
                           queries: List[str] = None, 
                           max_per_query: int = None,
                           total_limit: int = None) -> List[str]:
        """
        Search for funeral home websites using predefined queries.
        
        Args:
            queries: List of search queries (uses SEARCH_QUERIES if None)
            max_per_query: Maximum results per query (None = no limit)
            total_limit: Total maximum URLs to return (None = no limit)
        
        Returns:
            List of unique funeral home website URLs
        """
        if queries is None:
            queries = SEARCH_QUERIES
        
        all_urls = []
        
        print(f"\n{'='*50}")
        print(f"Searching for funeral home websites...")
        print(f"Queries: {len(queries)}, Max per query: {max_per_query or 'unlimited'}")
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
