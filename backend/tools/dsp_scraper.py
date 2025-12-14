"""
DSP Scraper - Scrapes funeral company authorization lists from all Romanian DSP websites.
"""
import os
import json
import re
import time
import requests
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from bs4 import BeautifulSoup
from pypdf import PdfReader
import io

# Try to import tabula for PDF table extraction
try:
    import tabula
    HAS_TABULA = True
except ImportError:
    HAS_TABULA = False
    print("Warning: tabula-py not installed. PDF table extraction may be limited.")


@dataclass
class DSPCompany:
    """Authorized funeral company from DSP"""
    name: str
    cui: Optional[str] = None
    address: Optional[str] = None
    county: Optional[str] = None
    county_code: Optional[str] = None
    authorization_number: Optional[str] = None
    authorization_date: Optional[str] = None
    valid_until: Optional[str] = None
    services: Optional[List[str]] = None
    source_url: Optional[str] = None
    scraped_at: Optional[str] = None


class DSPScraper:
    """
    Scraper for Romanian DSP authorization lists.
    """
    
    # Rotating User Agents
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    ]
    
    # Keywords to find funeral-related PDFs/pages
    FUNERAL_KEYWORDS = [
        'funerar', 'funerare', 'pompe funebre', 'mortuare', 'mortuar',
        'transport decedat', 'camera mortuara', 'servicii funerare'
    ]
    
    def __init__(self, sources_path: str = None):
        self.sources_path = sources_path or os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 'data', 'dsp_sources.json'
        )
        self.sources = self._load_sources()
        self.companies: List[DSPCompany] = []
        self.session = requests.Session()
        self._request_count = 0
        
    def _load_sources(self) -> Dict:
        """Load DSP sources configuration."""
        if os.path.exists(self.sources_path):
            with open(self.sources_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"sources": []}
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with rotating User-Agent."""
        import random
        return {
            'User-Agent': random.choice(self.USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ro-RO,ro;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
    
    def _rate_limit(self):
        """Respect rate limits - 1 request per 2 seconds."""
        self._request_count += 1
        if self._request_count > 1:
            time.sleep(2)
    
    def _fetch_page(self, url: str) -> Optional[str]:
        """Fetch HTML page content."""
        self._rate_limit()
        try:
            response = self.session.get(url, headers=self._get_headers(), timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"  Error fetching {url}: {e}")
            return None
    
    def _fetch_pdf(self, url: str) -> Optional[bytes]:
        """Fetch PDF file content."""
        self._rate_limit()
        try:
            response = self.session.get(url, headers=self._get_headers(), timeout=60)
            response.raise_for_status()
            if 'pdf' in response.headers.get('Content-Type', '').lower() or url.endswith('.pdf'):
                return response.content
            return None
        except Exception as e:
            print(f"  Error fetching PDF {url}: {e}")
            return None
    
    def _find_funeral_pdfs(self, html: str, base_url: str) -> List[str]:
        """Find PDF links related to funeral services in HTML page."""
        soup = BeautifulSoup(html, 'html.parser')
        pdf_links = []
        
        for link in soup.find_all('a', href=True):
            href = link.get('href', '')
            text = link.get_text().lower()
            
            # Check if link or surrounding text contains funeral keywords
            is_funeral = any(kw in text for kw in self.FUNERAL_KEYWORDS)
            is_funeral = is_funeral or any(kw in href.lower() for kw in self.FUNERAL_KEYWORDS)
            
            if is_funeral and ('.pdf' in href.lower() or 'pdf' in text):
                # Make absolute URL
                if href.startswith('http'):
                    pdf_links.append(href)
                elif href.startswith('/'):
                    from urllib.parse import urljoin
                    pdf_links.append(urljoin(base_url, href))
                else:
                    from urllib.parse import urljoin
                    pdf_links.append(urljoin(base_url + '/', href))
        
        return list(set(pdf_links))
    
    def _parse_pdf(self, pdf_content: bytes, county: str, county_code: str, source_url: str) -> List[DSPCompany]:
        """Parse PDF content to extract company records."""
        companies = []
        
        try:
            reader = PdfReader(io.BytesIO(pdf_content))
            full_text = ""
            
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
            
            # Parse the text
            companies = self._extract_companies_from_text(full_text, county, county_code, source_url)
            
        except Exception as e:
            print(f"  Error parsing PDF: {e}")
        
        return companies
    
    def _extract_companies_from_text(self, text: str, county: str, county_code: str, source_url: str) -> List[DSPCompany]:
        """Extract company records from text."""
        companies = []
        
        # Split into lines and process
        lines = text.split('\n')
        
        # Buffer for multi-line company entries
        current_entry = ""
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line starts with a number (new entry)
            if re.match(r'^\d+\.?\s+', line):
                # Process previous entry if exists
                if current_entry:
                    company = self._parse_dsp_entry(current_entry, county, county_code, source_url)
                    if company:
                        companies.append(company)
                current_entry = line
            elif current_entry:
                # Continue previous entry
                current_entry += " " + line
        
        # Process last entry
        if current_entry:
            company = self._parse_dsp_entry(current_entry, county, county_code, source_url)
            if company:
                companies.append(company)
        
        return companies
    
    def _parse_dsp_entry(self, entry: str, county: str, county_code: str, source_url: str) -> Optional[DSPCompany]:
        """Parse a single DSP table entry."""
        # Remove leading number
        entry = re.sub(r'^\d+\.?\s*', '', entry)
        
        # Extract company name - usually SC ... SRL/SA or ... II/PFA
        name_match = re.match(r'((?:SC\s+)?[A-Z][A-Za-z0-9\s\-\.]+(?:S\.?R\.?L\.?|S\.?A\.?|I\.?I\.?|P\.?F\.?A\.?))', entry, re.IGNORECASE)
        if not name_match:
            return None
        
        name = name_match.group(1).strip()
        
        # Clean up name
        name = re.sub(r'\s+', ' ', name)
        
        # Extract authorization number (format: XX.XXX/XXX/X/DD.MM.YYYY)
        auth_match = re.search(r'(\d+\.?\d*/\d+/[A-Z]/\d{2}\.\d{2}\.\d{4})', entry)
        auth_number = auth_match.group(1) if auth_match else None
        
        # Extract address - usually after company name, before auth number
        address = None
        if auth_match:
            addr_text = entry[name_match.end():auth_match.start()]
            # Clean up address
            addr_text = re.sub(r'^[\s,]+', '', addr_text)
            addr_text = re.sub(r'[\s,]+$', '', addr_text)
            if len(addr_text) > 10:
                address = addr_text
        
        if not name or len(name) < 5:
            return None
        
        return DSPCompany(
            name=name,
            address=address,
            county=county,
            county_code=county_code,
            authorization_number=auth_number,
            source_url=source_url,
            scraped_at=datetime.now().isoformat()
        )
    
    def _parse_company_line(self, line: str) -> Optional[Dict]:
        """Parse a single line to extract company information."""
        result = {}
        
        # Remove row numbers (e.g., "1.", "23.")
        line = re.sub(r'^\d+\.?\s*', '', line)
        
        # Extract CUI (fiscal code) - usually 6-10 digits
        cui_patterns = [
            r'CUI[:\s]*(\d{6,10})',
            r'C\.U\.I\.[:\s]*(\d{6,10})',
            r'(?:^|\s)(\d{6,10})(?:\s|$)',  # Standalone number
            r'RO(\d{6,10})',
        ]
        
        cui = None
        for pattern in cui_patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                cui = match.group(1)
                break
        
        # Extract authorization number
        auth_match = re.search(r'(?:autorizatie|autorizatia|nr\.?\s*aut)[:\s]*(\d+/?[\d/]*)', line, re.IGNORECASE)
        auth_number = auth_match.group(1) if auth_match else None
        
        # Extract company name
        # Usually appears before CUI or at the start
        company_name = line
        
        # Remove CUI part
        company_name = re.sub(r'CUI[:\s]*\d+', '', company_name, flags=re.IGNORECASE)
        company_name = re.sub(r'C\.U\.I\.[:\s]*\d+', '', company_name, flags=re.IGNORECASE)
        
        # Remove authorization part
        company_name = re.sub(r'(?:autorizatie|autorizatia|nr\.?\s*aut)[:\s]*\d+/?[\d/]*', '', company_name, flags=re.IGNORECASE)
        
        # Clean up
        company_name = company_name.strip(' ,.-')
        
        # Validate company name (should contain S.R.L., S.A., I.I., P.F.A., etc.)
        company_patterns = [r'S\.?R\.?L\.?', r'S\.?A\.?', r'I\.?I\.?', r'P\.?F\.?A\.?', r'S\.?C\.?', r'S\.?N\.?C\.?']
        is_company = any(re.search(pattern, company_name, re.IGNORECASE) for pattern in company_patterns)
        
        if is_company and len(company_name) > 5:
            result['name'] = company_name
            result['cui'] = cui
            result['auth_number'] = auth_number
            return result
        
        return None
    
    def scrape_county(self, county_code_or_source) -> List[DSPCompany]:
        """Scrape DSP data for a single county.
        
        Args:
            county_code_or_source: Either a county code string (e.g., 'TM') 
                                   or a source dict from dsp_sources.json
        """
        # Handle both string county codes and dict sources
        if isinstance(county_code_or_source, str):
            # Find source by county code
            source = None
            for s in self.sources.get('sources', []):
                if s.get('county_code', '').upper() == county_code_or_source.upper():
                    source = s
                    break
            if not source:
                print(f"County code '{county_code_or_source}' not found in sources")
                return []
        else:
            source = county_code_or_source
        
        county = source.get('county', 'Unknown')
        county_code = source.get('county_code', 'XX')
        auth_url = source.get('authorization_url', '')
        website = source.get('website', '')
        direct_pdf = source.get('direct_pdf_url', '')
        
        print(f"\nScraping DSP {county} ({county_code})...")
        
        companies = []
        
        # Strategy 1: Try direct PDF URL if available
        if direct_pdf:
            print(f"  Direct PDF: {direct_pdf}")
            pdf_content = self._fetch_pdf(direct_pdf)
            if pdf_content:
                pdf_companies = self._parse_pdf(pdf_content, county, county_code, direct_pdf)
                print(f"  Extracted {len(pdf_companies)} companies from direct PDF")
                companies.extend(pdf_companies)
                if companies:
                    return companies
        
        # Strategy 2: Fetch the authorization page and find PDFs
        print(f"  Fetching: {auth_url}")
        html = self._fetch_page(auth_url)
        if not html:
            html = self._fetch_page(website)
        
        if not html:
            print(f"  Could not fetch page for {county}")
            return companies
        
        # Find funeral-related PDF links
        pdf_links = self._find_funeral_pdfs(html, website)
        print(f"  Found {len(pdf_links)} funeral-related PDF links")
        
        # Download and parse each PDF
        for pdf_url in pdf_links:
            print(f"  Downloading: {pdf_url[:80]}...")
            pdf_content = self._fetch_pdf(pdf_url)
            
            if pdf_content:
                pdf_companies = self._parse_pdf(pdf_content, county, county_code, pdf_url)
                print(f"    Extracted {len(pdf_companies)} companies")
                companies.extend(pdf_companies)
        
        # Also try HTML tables
        html_companies = self._parse_html_tables(html, county, county_code, auth_url)
        if html_companies:
            print(f"  Found {len(html_companies)} companies in HTML tables")
            companies.extend(html_companies)
        
        return companies
    
    def _parse_html_tables(self, html: str, county: str, county_code: str, source_url: str) -> List[DSPCompany]:
        """Parse HTML tables for company data."""
        companies = []
        soup = BeautifulSoup(html, 'html.parser')
        
        for table in soup.find_all('table'):
            rows = table.find_all('tr')
            
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    text = ' '.join(cell.get_text() for cell in cells)
                    
                    # Check if row contains funeral-related content
                    if any(kw in text.lower() for kw in self.FUNERAL_KEYWORDS):
                        company_info = self._parse_company_line(text)
                        if company_info and company_info.get('name'):
                            company = DSPCompany(
                                name=company_info['name'],
                                cui=company_info.get('cui'),
                                county=county,
                                county_code=county_code,
                                source_url=source_url,
                                scraped_at=datetime.now().isoformat()
                            )
                            companies.append(company)
        
        return companies
    
    def scrape_all(self, counties: List[str] = None) -> List[DSPCompany]:
        """
        Scrape all DSP sources or specific counties.
        
        Args:
            counties: List of county codes to scrape (e.g., ['TM', 'CJ']). 
                      If None, scrapes all.
        """
        all_companies = []
        
        for source in self.sources.get('sources', []):
            county_code = source.get('county_code', '')
            
            # Skip if specific counties requested and this isn't one
            if counties and county_code not in counties:
                continue
            
            try:
                companies = self.scrape_county(source)
                all_companies.extend(companies)
            except Exception as e:
                print(f"  Error scraping {source.get('county', 'unknown')}: {e}")
        
        self.companies = all_companies
        return all_companies
    
    def save_results(self, output_path: str = None):
        """Save scraped results to JSON file."""
        if not output_path:
            output_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'data',
                'dsp_authorized_companies.json'
            )
        
        # Create directory if needed
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        data = {
            'scraped_at': datetime.now().isoformat(),
            'total_companies': len(self.companies),
            'companies': [asdict(c) for c in self.companies]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\nSaved {len(self.companies)} companies to {output_path}")
        return output_path
    
    def get_companies_by_county(self, county_code: str) -> List[DSPCompany]:
        """Get companies for a specific county."""
        return [c for c in self.companies if c.county_code == county_code]
    
    def search_company(self, name: str = None, cui: str = None) -> List[DSPCompany]:
        """Search for a company by name or CUI."""
        results = []
        
        for company in self.companies:
            if cui and company.cui == cui:
                results.append(company)
            elif name:
                # Fuzzy match on name
                from thefuzz import fuzz
                if fuzz.partial_ratio(name.lower(), company.name.lower()) > 80:
                    results.append(company)
        
        return results


def main():
    """Main function to run DSP scraper."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Scrape DSP funeral authorization lists')
    parser.add_argument('--counties', '-c', nargs='+', help='County codes to scrape (e.g., TM CJ)')
    parser.add_argument('--output', '-o', help='Output JSON file path')
    parser.add_argument('--test', '-t', action='store_true', help='Test mode - scrape only first county')
    
    args = parser.parse_args()
    
    scraper = DSPScraper()
    
    if args.test:
        # Test mode - just scrape Timiș
        companies = scraper.scrape_all(counties=['TM'])
    elif args.counties:
        companies = scraper.scrape_all(counties=args.counties)
    else:
        companies = scraper.scrape_all()
    
    # Save results
    output_path = scraper.save_results(args.output)
    
    # Print summary
    print("\n" + "="*60)
    print("DSP SCRAPING COMPLETE")
    print("="*60)
    print(f"Total companies found: {len(companies)}")
    
    # Group by county
    by_county = {}
    for c in companies:
        county = c.county or 'Unknown'
        by_county[county] = by_county.get(county, 0) + 1
    
    print("\nBy county:")
    for county, count in sorted(by_county.items()):
        print(f"  {county}: {count}")


if __name__ == '__main__':
    main()
