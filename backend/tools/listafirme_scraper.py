"""
CUI Lookup Tool - Find company CUI and official name using Firecrawl + listafirme.ro

Uses Firecrawl to scrape listafirme.ro search results and get company details.
"""
import re
import time
from typing import Optional, List, Tuple

# Import Firecrawl tool
try:
    from tools.firecrawl_extractor import FirecrawlExtractorTool
except ImportError:
    from firecrawl_extractor import FirecrawlExtractorTool


class CUILookupTool:
    """Look up company CUI and official name from listafirme.ro using Firecrawl."""
    
    BASE_URL = "https://www.listafirme.ro"
    
    def __init__(self):
        self.firecrawl = FirecrawlExtractorTool()
        self._last_request_time = 0
    
    def _rate_limit(self, min_delay: float = 1.5):
        """Polite delay between requests."""
        elapsed = time.time() - self._last_request_time
        if elapsed < min_delay:
            time.sleep(min_delay - elapsed)
        self._last_request_time = time.time()
    
    def search_company(self, name: str, city: Optional[str] = None) -> List[dict]:
        """
        Search for companies by name using DuckDuckGo site search.
        
        Args:
            name: Company name to search for
            city: Optional city to narrow results
            
        Returns:
            List of matching companies with CUI
        """
        self._rate_limit()
        
        # Build search URL - search listafirme.ro directly
        query = f"{name} {city or ''} pompe funerare".strip()
        search_url = f"https://www.listafirme.ro/search.asp?what={query.replace(' ', '+')}"
        
        print(f"Searching listafirme.ro for: {query}")
        
        result = self.firecrawl.scrape_url(search_url)
        
        if not result or not result.get('success'):
            print(f"Search failed: {result}")
            return []
        
        # Parse results from markdown
        return self._parse_search_results(result.get('markdown', ''))
    
    def _parse_search_results(self, markdown: str) -> List[dict]:
        """Extract company info from search results markdown."""
        results = []
        
        # Look for listafirme.ro company links in markdown
        # Format: [Company Name](https://listafirme.ro/company-slug-CUI/)
        pattern = r'\[([^\]]+)\]\(https?://(?:www\.)?listafirme\.ro/([^/]+-(\d{5,10}))/?\)'
        
        for match in re.finditer(pattern, markdown):
            name = match.group(1).strip()
            slug = match.group(2)
            cui = match.group(3)
            
            if name and cui and len(name) > 2:
                results.append({
                    'name': name,
                    'cui': cui,
                    'url': f"{self.BASE_URL}/{slug}/"
                })
        
        # Also try to find CUI patterns in URLs
        url_pattern = r'listafirme\.ro/([a-z0-9\-\.]+)-(\d{5,10})/?'
        for match in re.finditer(url_pattern, markdown, re.IGNORECASE):
            slug = match.group(1)
            cui = match.group(2)
            
            # Convert slug to name
            name = slug.replace('-', ' ').replace('.', ' ').upper()
            
            # Check if already in results
            if not any(r['cui'] == cui for r in results):
                results.append({
                    'name': name,
                    'cui': cui,
                    'url': f"{self.BASE_URL}/{slug}-{cui}/"
                })
        
        return results[:10]
    
    def get_company_by_cui(self, cui: str) -> Optional[dict]:
        """
        Get company details by CUI.
        
        Args:
            cui: Company fiscal code (CUI/CIF)
            
        Returns:
            Company details dict or None
        """
        self._rate_limit()
        
        # Search by CUI
        search_url = f"https://www.listafirme.ro/search.asp?what={cui}"
        
        print(f"Looking up CUI: {cui}")
        
        result = self.firecrawl.scrape_url(search_url)
        
        if not result or not result.get('success'):
            return None
        
        markdown = result.get('markdown', '')
        
        # Find the company URL
        url_match = re.search(rf'listafirme\.ro/([^/]+-{cui})/?', markdown)
        if url_match:
            company_url = f"{self.BASE_URL}/{url_match.group(1)}/"
            return self.get_company_details(company_url, cui)
        
        return None
    
    def get_company_details(self, url: str, cui: str = None) -> Optional[dict]:
        """
        Get detailed company info from listafirme.ro company page.
        
        Args:
            url: Full listafirme.ro company URL
            cui: Optional CUI if known
            
        Returns:
            Company details dict
        """
        self._rate_limit()
        
        print(f"Fetching company details from: {url}")
        
        result = self.firecrawl.scrape_url(url)
        
        if not result or not result.get('success'):
            return None
        
        markdown = result.get('markdown', '')
        
        # Extract CUI from URL if not provided
        if not cui:
            cui_match = re.search(r'-(\d{5,10})/?$', url)
            if cui_match:
                cui = cui_match.group(1)
        
        company = {
            'cui': cui,
            'name': '',
            'address': '',
            'city': '',
            'county': '',
            'caen': '',
            'caen_description': ''
        }
        
        # Extract official name - look for "# COMPANY NAME" pattern
        name_match = re.search(r'^#\s+([A-ZĂÂÎȘȚ][A-ZĂÂÎȘȚĂ-Z0-9\.\s]+(?:SRL|SA|SNC|SCS|PFA|II|IF))', markdown, re.MULTILINE)
        if name_match:
            company['name'] = name_match.group(1).strip()
        
        # Extract from table: | Denumire | COMPANY NAME |
        denumire_match = re.search(r'\|\s*Denumire\s*\|\s*([^|]+)\|', markdown)
        if denumire_match:
            company['name'] = denumire_match.group(1).strip()
        
        # Extract CUI from table
        cui_table_match = re.search(r'\|\s*CUI\s*\|\s*(\d+)\s*\|', markdown)
        if cui_table_match:
            company['cui'] = cui_table_match.group(1)
        
        # Extract county
        county_match = re.search(r'\|\s*Jude[țt]\s*\|\s*([^|]+)\|', markdown)
        if county_match:
            company['county'] = county_match.group(1).strip()
        
        # Extract city/locality
        city_match = re.search(r'\|\s*Localitate\s*\|\s*(?:Loc\.)?\s*([^|]+)\|', markdown)
        if city_match:
            company['city'] = city_match.group(1).strip()
        
        # Extract address
        addr_match = re.search(r'\|\s*Adres[aă]\s*\|\s*([^|]+)\|', markdown)
        if addr_match:
            company['address'] = addr_match.group(1).strip()
        
        # Extract CAEN
        caen_match = re.search(r'\|\s*Cod CAEN preponderent\s*\|\s*(\d{4})', markdown)
        if caen_match:
            company['caen'] = caen_match.group(1)
        
        # Extract CAEN description
        caen_desc_match = re.search(r'\|\s*Obiect Activitate\s*\|\s*([^|]+)\|', markdown)
        if caen_desc_match:
            company['caen_description'] = caen_desc_match.group(1).strip()
        
        return company
    
    def lookup_company(self, name: str, city: Optional[str] = None) -> Optional[dict]:
        """
        Main method: Look up a company by name and get its official details.
        
        Args:
            name: Company name or trade name
            city: Optional city to narrow results
            
        Returns:
            Dict with cui, official_name, city, county, caen, etc.
        """
        # First search for the company
        results = self.search_company(name, city)
        
        if not results:
            print(f"No results found for: {name}")
            return None
        
        # Find best match
        search_name = self._normalize(name)
        best_match = None
        best_score = 0
        
        for r in results:
            result_name = self._normalize(r['name'])
            score = self._similarity_score(search_name, result_name)
            
            if score > best_score:
                best_score = score
                best_match = r
        
        if not best_match:
            best_match = results[0]
        
        print(f"Best match: {best_match['name']} (CUI: {best_match['cui']}, score: {best_score})")
        
        # Get full details
        details = self.get_company_details(best_match['url'], best_match['cui'])
        
        if details:
            return {
                'cui': details['cui'],
                'official_name': details['name'],
                'city': details['city'],
                'county': details['county'],
                'address': details['address'],
                'caen': details['caen'],
                'caen_description': details['caen_description'],
                'source_url': best_match['url'],
                'match_score': best_score
            }
        
        return {
            'cui': best_match['cui'],
            'official_name': best_match['name'],
            'source_url': best_match['url'],
            'match_score': best_score
        }
    
    def _normalize(self, name: str) -> str:
        """Normalize company name for comparison."""
        name = name.lower()
        # Remove common prefixes/suffixes
        name = re.sub(r'\b(s\.?c\.?|s\.?r\.?l\.?|s\.?a\.?|srl|sa|sc)\b', '', name)
        # Remove punctuation
        name = re.sub(r'[^\w\s]', ' ', name)
        # Normalize whitespace
        name = ' '.join(name.split())
        return name.strip()
    
    def _similarity_score(self, name1: str, name2: str) -> float:
        """Calculate similarity between two names."""
        words1 = set(name1.split())
        words2 = set(name2.split())
        
        if not words1 or not words2:
            return 0.0
        
        # Check containment
        if name1 in name2 or name2 in name1:
            return 0.9
        
        # Word overlap
        overlap = len(words1 & words2)
        total = len(words1 | words2)
        
        return overlap / total if total > 0 else 0.0


# Test
if __name__ == "__main__":
    lookup = CUILookupTool()
    
    print("="*60)
    print("Looking up 'Subin Funerare' in Timisoara...")
    print("="*60)
    
    result = lookup.lookup_company("Subin Funerare", "Timisoara")
    
    if result:
        print(f"\n✅ Found company:")
        print(f"   CUI: {result['cui']}")
        print(f"   Official Name: {result['official_name']}")
        print(f"   City: {result.get('city', 'N/A')}")
        print(f"   County: {result.get('county', 'N/A')}")
        print(f"   CAEN: {result.get('caen', 'N/A')}")
        print(f"   Source: {result.get('source_url', 'N/A')}")
    else:
        print("\n❌ Company not found")
