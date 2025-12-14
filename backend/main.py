"""
Main orchestration script for the funeral directory scraper.
"""
import sys
import json
from pathlib import Path
from typing import Optional

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from tools.dsp_verification import DSPVerificationTool
from tools.firecrawl_extractor import FirecrawlExtractorTool
from tools.llm_extractor import LLMExtractorTool
from tools.supabase_tool import SupabaseTool
from tools.google_search import GoogleSearchTool
from tools.geocoding import geocode_address
from models import Company, Contact, Location
from utils import normalize_phone_number, extract_cui_from_text, rate_limit_delay, check_robots_txt, HumanBehaviorSimulator
from config.settings import SEED_URLS_PATH
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# City to county mapping for Romania
CITY_TO_COUNTY = {
    'timișoara': 'Timiș', 'timisoara': 'Timiș', 'lugoj': 'Timiș', 'buziaș': 'Timiș', 'sânnicolau mare': 'Timiș',
    'bucurești': 'București', 'bucuresti': 'București', 'sector 1': 'București', 'sector 2': 'București', 
    'sector 3': 'București', 'sector 4': 'București', 'sector 5': 'București', 'sector 6': 'București',
    'cluj-napoca': 'Cluj', 'cluj': 'Cluj', 'turda': 'Cluj', 'dej': 'Cluj', 'câmpia turzii': 'Cluj',
    'iași': 'Iași', 'iasi': 'Iași', 'pașcani': 'Iași',
    'constanța': 'Constanța', 'constanta': 'Constanța', 'mangalia': 'Constanța', 'medgidia': 'Constanța',
    'craiova': 'Dolj', 'brașov': 'Brașov', 'brasov': 'Brașov',
    'galați': 'Galați', 'galati': 'Galați',
    'ploiești': 'Prahova', 'ploiesti': 'Prahova', 'câmpina': 'Prahova',
    'oradea': 'Bihor', 'arad': 'Arad', 'sibiu': 'Sibiu',
    'târgu mureș': 'Mureș', 'târgu mures': 'Mureș', 'targu mures': 'Mureș',
    'baia mare': 'Maramureș', 'satu mare': 'Satu Mare',
    'suceava': 'Suceava', 'botoșani': 'Botoșani', 'botosani': 'Botoșani',
    'bacău': 'Bacău', 'bacau': 'Bacău', 'piatra neamț': 'Neamț',
    'focșani': 'Vrancea', 'focsani': 'Vrancea', 'buzău': 'Buzău', 'buzau': 'Buzău',
    'pitești': 'Argeș', 'pitesti': 'Argeș', 'târgoviște': 'Dâmbovița',
    'râmnicu vâlcea': 'Vâlcea', 'slatina': 'Olt', 'târgu jiu': 'Gorj',
    'drobeta-turnu severin': 'Mehedinți', 'reșița': 'Caraș-Severin', 'resita': 'Caraș-Severin',
    'alba iulia': 'Alba', 'deva': 'Hunedoara', 'hunedoara': 'Hunedoara',
    'alexandria': 'Teleorman', 'giurgiu': 'Giurgiu', 'călărași': 'Călărași', 'slobozia': 'Ialomița',
    'tulcea': 'Tulcea', 'brăila': 'Brăila', 'braila': 'Brăila',
    'vaslui': 'Vaslui', 'bârlad': 'Vaslui',
    'bistrița': 'Bistrița-Năsăud', 'bistrita': 'Bistrița-Năsăud',
    'zalău': 'Sălaj', 'sfântu gheorghe': 'Covasna', 'miercurea ciuc': 'Harghita',
}


class FuneralDirectoryScraper:
    """
    Main scraper orchestrator using the tools.
    """
    
    def __init__(self):
        logger.info("Initializing Funeral Directory Scraper...")
        
        self.dsp_tool = DSPVerificationTool()
        self.firecrawl = FirecrawlExtractorTool()
        self.llm_extractor = LLMExtractorTool()
        self.db = SupabaseTool()
        self.search_tool = GoogleSearchTool()
        self.behavior = HumanBehaviorSimulator()
        
        self.stats = {
            'processed': 0,
            'success': 0,
            'failed': 0,
            'verified': 0
        }
    
    def load_seed_urls(self) -> list:
        """
        Load seed URLs from JSON file.
        """
        try:
            with open(SEED_URLS_PATH, 'r', encoding='utf-8') as f:
                urls = json.load(f)
                logger.info(f"Loaded {len(urls)} seed URLs")
                return urls
        except FileNotFoundError:
            logger.warning(f"Seed URLs file not found at {SEED_URLS_PATH}")
            return []
        except Exception as e:
            logger.error(f"Error loading seed URLs: {e}")
            return []
    
    def process_url(self, url: str) -> bool:
        """
        Process a single URL: scrape, extract, verify, and store.
        
        Returns:
            True if successful, False otherwise
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"Processing: {url}")
        logger.info(f"{'='*60}")
        
        self.stats['processed'] += 1
        
        try:
            # Check robots.txt
            if not check_robots_txt(url):
                logger.warning(f"URL disallowed by robots.txt: {url}")
                return False
            
            # Rate limiting
            rate_limit_delay()
            
            # Step 1: Scrape with Firecrawl
            logger.info("Step 1: Scraping website...")
            scrape_result = self.firecrawl.scrape_url(url, include_subpages=True)
            
            if not scrape_result['success']:
                logger.error(f"Failed to scrape: {scrape_result.get('error')}")
                self.stats['failed'] += 1
                return False
            
            markdown_content = scrape_result['markdown']
            logger.info(f"[OK] Scraped {len(markdown_content)} characters")
            
            # Step 2: Extract with LLM
            logger.info("Step 2: Extracting structured data with LLM...")
            extraction_result = self.llm_extractor.extract_company_data(markdown_content, url)
            
            if not extraction_result['success']:
                logger.error(f"Failed to extract: {extraction_result.get('error')}")
                self.stats['failed'] += 1
                return False
            
            extracted = extraction_result['data']
            
            # Fallback: Use domain as company name if LLM missed it
            if not extracted.get('company_name') or extracted.get('company_name', '').lower() in ('unknown', 'null', 'none', ''):
                from urllib.parse import urlparse
                domain = urlparse(url).netloc.replace('www.', '')
                # Convert domain to title case: funero.ro -> Funero
                company_name_from_domain = domain.split('.')[0].replace('-', ' ').title()
                extracted['company_name'] = company_name_from_domain
                logger.info(f"[OK] Using domain as company name: {company_name_from_domain}")
            else:
                logger.info(f"[OK] Extracted data for: {extracted.get('company_name', 'Unknown')}")
            
            # Check if this looks like a directory (multiple companies listed)
            phones = extracted.get('phones', [])
            if len(phones) > 5:
                logger.warning(f"[SKIP] Detected as directory site (too many phones: {len(phones)})")
                self.stats['failed'] += 1
                return False
            
            # Validate location matches target city (Timișoara / Timiș)
            if not self._validate_location(extracted, url):
                logger.warning(f"[SKIP] Company location doesn't match target area (Timișoara/Timiș)")
                self.stats['failed'] += 1
                return False
            
            # Fallback: Try to find email with regex if LLM missed it
            if not extracted.get('email'):
                import re
                email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
                emails_found = re.findall(email_pattern, markdown_content)
                # Filter out common non-contact emails
                excluded = ['example.com', 'domain.com', 'email.com', 'test.com']
                valid_emails = [e for e in emails_found if not any(ex in e for ex in excluded)]
                if valid_emails:
                    extracted['email'] = valid_emails[0]
                    logger.info(f"[OK] Found email via regex fallback: {extracted['email']}")
            
            # Fallback: Try to find CUI/CIF with regex if LLM missed it
            if not extracted.get('fiscal_code'):
                import re
                # Pattern for Romanian CUI/CIF: 6-10 digits, optionally prefixed with RO
                cui_patterns = [
                    r'(?:CUI|CIF|Cod\s*fiscal)[:\s]*(?:RO)?(\d{6,10})',  # CUI: 12345678
                    r'(?:RO)(\d{6,10})',  # RO12345678 (VAT format)
                    r'(?:cod\s*unic)[:\s]*(\d{6,10})',  # Cod unic: 12345678
                ]
                for pattern in cui_patterns:
                    match = re.search(pattern, markdown_content, re.IGNORECASE)
                    if match:
                        extracted['fiscal_code'] = match.group(1)
                        logger.info(f"[OK] Found CUI via regex fallback: {extracted['fiscal_code']}")
                        break
            
            # Fallback: Try to find address with regex if LLM missed it
            if not extracted.get('locations') and not extracted.get('address'):
                import re
                address = self._extract_address_regex(markdown_content)
                if address:
                    extracted['address'] = address
                    extracted['city'] = 'Timișoara'
                    extracted['county'] = 'Timiș'
                    logger.info(f"[OK] Found address via regex fallback: {address}")
            
            # Step 3: Validate and transform data
            logger.info("Step 3: Validating and transforming data...")
            company = self._transform_to_company(extracted)
            
            if not company:
                logger.error("Failed to create valid company object")
                self.stats['failed'] += 1
                return False
            
            # Step 4: DSP Verification - DISABLED
            # logger.info("Step 4: Verifying against DSP list...")
            # # Get county from company locations if available
            # county = None
            # if company.locations and len(company.locations) > 0:
            #     loc = company.locations[0]
            #     if loc.county:
            #         county = loc.county
            #     elif loc.city:
            #         # Try to map city to county
            #         county = CITY_TO_COUNTY.get(loc.city.lower())
            # 
            # verification = self.dsp_tool.verify_company(
            #     company.name,
            #     county=county
            # )
            # 
            # company.is_verified = verification['is_verified']
            # 
            # if verification['is_verified']:
            #     logger.info(f"[VERIFIED] (score: {verification.get('match_score', 0)}%)")
            #     self.stats['verified'] += 1
            # else:
            #     logger.info(f"[NOT VERIFIED] (best score: {verification.get('match_score', 0)}%)")
            company.is_verified = False  # Default to not verified since DSP check is disabled
            
            # Step 5: Store in database
            logger.info("Step 5: Storing in database...")
            result = self.db.upsert_company(company)
            
            if result['success']:
                self.stats['success'] += 1
                logger.info(f"[SUCCESS] Company {result['action']}")
                
                # Log data completeness check
                missing_fields = []
                if not company.contacts or not any(c.type.startswith('phone') for c in company.contacts):
                    missing_fields.append('phone')
                if not company.contacts or not any(c.type == 'email' for c in company.contacts):
                    missing_fields.append('email')
                if not company.locations:
                    missing_fields.append('address')
                if not company.fiscal_code:
                    missing_fields.append('fiscal_code')
                
                if missing_fields:
                    logger.warning(f"[INCOMPLETE] Missing data: {', '.join(missing_fields)}")
                else:
                    logger.info(f"[COMPLETE] All key fields extracted")
                
                return True
            else:
                logger.error(f"Failed to store: {result.get('error')}")
                self.stats['failed'] += 1
                return False
                
        except Exception as e:
            logger.error(f"Unexpected error processing {url}: {e}", exc_info=True)
            self.stats['failed'] += 1
            return False
    
    def _validate_location(self, extracted: dict, url: str) -> bool:
        """
        Validate that the extracted company location matches our target area (Timișoara/Timiș).
        
        This prevents including companies that have a page for Timișoara but are actually
        located in a different city (like funero.ro showing Baia Mare address on their Timișoara page).
        
        Returns:
            True if location is valid (in target area), False otherwise
        """
        # Target cities and county for our directory
        target_cities = {
            'timișoara', 'timisoara', 'timişoara',
            'lugoj', 'sânnicolau mare', 'sannicolau mare',
            'jimbolia', 'buziaș', 'buzias', 'deta', 'făget', 'faget',
            'recaș', 'recas', 'gătaia', 'gataia'  # Major cities in Timiș county
        }
        target_counties = {'timiș', 'timis', 'timiş'}
        
        # Check locations array (new format)
        locations = extracted.get('locations', [])
        if locations and isinstance(locations, list):
            for loc in locations:
                city = (loc.get('city') or '').lower().strip()
                county = (loc.get('county') or '').lower().strip()
                address = (loc.get('address') or '').lower()
                
                # Check if city matches
                if any(target in city for target in target_cities):
                    return True
                # Check if county matches
                if any(target in county for target in target_counties):
                    return True
                # Check if address contains target city
                if any(target in address for target in target_cities):
                    return True
        
        # Check legacy format (single address/city/county)
        city = (extracted.get('city') or '').lower().strip()
        county = (extracted.get('county') or '').lower().strip()
        address = (extracted.get('address') or '').lower()
        
        if any(target in city for target in target_cities):
            return True
        if any(target in county for target in target_counties):
            return True
        if any(target in address for target in target_cities):
            return True
        
        # If no location info at all, we can't validate - allow it but log warning
        if not locations and not city and not address:
            logger.warning(f"No location info found for {url} - allowing by default")
            return True
        
        # Location found but doesn't match target area
        found_city = city or (locations[0].get('city') if locations else 'unknown')
        found_county = county or (locations[0].get('county') if locations else 'unknown')
        logger.info(f"  Location mismatch: found {found_city}, {found_county}")
        return False
    
    def _extract_address_regex(self, content: str) -> Optional[str]:
        """
        Extract address from content using regex patterns.
        Fallback when LLM misses the address.
        """
        import re
        
        # Romanian street prefixes
        street_prefixes = r'(?:Str(?:ada)?\.?|Calea|B(?:ulevardul|d)?\.?|Al(?:eea)?\.?|Piața|P-ța|Splaiul|Drumul|Intrarea)'
        
        # Pattern 1: Street + Number (e.g., "Str. Gheorghe Doja, Nr. 20" or "Iuliu Grozescu 16")
        patterns = [
            # "Str. Name Nr. 123" or "Strada Name, Nr. 123"
            rf'{street_prefixes}\s+([A-ZĂÂÎȘȚ][a-zăâîșț\s]+?)[\s,]+(?:Nr\.?\s*)?(\d+[A-Za-z]?)',
            # "Name Street 123" (without prefix)
            r'([A-ZĂÂÎȘȚ][a-zăâîșț]+(?:\s+[A-ZĂÂÎȘȚ][a-zăâîșț]+)?)\s+(\d{1,4}[A-Za-z]?)\s*[,\n]',
            # Address after "Adresă:" or "Locație:"
            r'(?:Adres[aă]|Loca[țt]ie|Sediu)[:\s]+([A-ZĂÂÎȘȚ][^,\n]{5,50}?,?\s*(?:Nr\.?\s*)?\d+[A-Za-z]?)',
            # With city name: "Street 123, Timișoara"
            r'([A-ZĂÂÎȘȚ][a-zăâîșț\s]+\d+[A-Za-z]?)\s*[,\s]+Timi[șs]oara',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE | re.MULTILINE)
            if matches:
                if isinstance(matches[0], tuple):
                    # Combine street name and number
                    match = matches[0]
                    if len(match) >= 2:
                        address = f"{match[0].strip()} {match[1]}".strip()
                    else:
                        address = match[0].strip()
                else:
                    address = matches[0].strip()
                
                # Clean up the address
                address = re.sub(r'\s+', ' ', address)
                address = address.strip(' ,.')
                
                # Validate it looks like an address (has some length and structure)
                if len(address) > 5 and any(c.isdigit() for c in address):
                    return address
        
        return None
    
    def _transform_to_company(self, extracted: dict) -> Company:
        """
        Transform extracted dict to Company model with validation.
        """
        try:
            # Process contacts
            contacts = []
            seen_phones = set()  # Track seen phone numbers to avoid duplicates
            
            # Process phones
            for phone in extracted.get('phones', []):
                try:
                    normalized, phone_type = normalize_phone_number(phone)
                    
                    # Skip duplicate phone numbers
                    if normalized in seen_phones:
                        logger.debug(f"Skipping duplicate phone: {normalized}")
                        continue
                    seen_phones.add(normalized)
                    
                    contact_type = 'phone_mobile' if phone_type == 'mobile' else 'phone_landline'
                    
                    contacts.append(Contact(
                        type=contact_type,
                        value=normalized,
                        is_primary=(len([c for c in contacts if 'phone' in c.type]) == 0)  # First phone is primary
                    ))
                except Exception as e:
                    logger.warning(f"Invalid phone number '{phone}': {e}")
            
            # Process email
            if extracted.get('email'):
                contacts.append(Contact(
                    type='email',
                    value=extracted['email'],
                    is_primary=False
                ))
            
            # Process locations - support multiple locations from LLM
            locations = []
            extracted_locations = extracted.get('locations', [])
            
            # Handle both new format (locations array) and legacy format (single address)
            if extracted_locations and isinstance(extracted_locations, list):
                # New format: array of location objects
                for i, loc_data in enumerate(extracted_locations):
                    if not loc_data.get('address'):
                        continue
                    
                    city = loc_data.get('city')
                    county = loc_data.get('county')
                    loc_type = loc_data.get('type', 'headquarters' if i == 0 else 'wake_house')
                    
                    # Normalize location type
                    if loc_type not in ['headquarters', 'wake_house', 'showroom']:
                        loc_type = 'headquarters' if i == 0 else 'wake_house'
                    
                    # Infer county from city if not provided
                    if not county and city:
                        county = CITY_TO_COUNTY.get(city.lower())
                    
                    # Geocode the address
                    lat, lon = None, None
                    company_name = extracted.get('company_name', '')
                    logger.info(f"  Geocoding location {i+1}: {loc_data['address'][:50]}...")
                    coords = geocode_address(loc_data['address'], city, county, company_name)
                    if coords:
                        lat, lon = coords
                    
                    locations.append(Location(
                        address=loc_data['address'],
                        city=city,
                        county=county,
                        latitude=lat,
                        longitude=lon,
                        type=loc_type
                    ))
                
                logger.info(f"  Extracted {len(locations)} location(s)")
            
            elif extracted.get('address'):
                # Legacy format: single address field
                city = extracted.get('city')
                if not city:
                    address_lower = extracted['address'].lower()
                    for c in CITY_TO_COUNTY.keys():
                        if c in address_lower:
                            city = c.title().replace('ș', 'ș').replace('ț', 'ț')
                            if city.lower() in ['timisoara', 'timișoara']:
                                city = 'Timișoara'
                            elif city.lower() in ['bucuresti', 'bucurești']:
                                city = 'București'
                            break
                
                county = extracted.get('county')
                if not county and city:
                    county = CITY_TO_COUNTY.get(city.lower())
                
                lat, lon = None, None
                company_name = extracted.get('company_name', '')
                logger.info("  Geocoding address...")
                coords = geocode_address(extracted['address'], city, county, company_name)
                if coords:
                    lat, lon = coords
                
                locations.append(Location(
                    address=extracted['address'],
                    city=city,
                    county=county,
                    latitude=lat,
                    longitude=lon,
                    type='headquarters'
                ))
            
            # Extract fiscal code and clean it
            fiscal_code = extracted.get('fiscal_code')
            
            # Handle LLM returning literal "null" string
            if fiscal_code and str(fiscal_code).lower() in ('null', 'none', 'n/a', 'undefined', ''):
                fiscal_code = None
            
            if not fiscal_code and extracted.get('description'):
                # Try to extract from description
                fiscal_code = extract_cui_from_text(extracted.get('description', ''))
            
            # Handle motto (truncate if too long)
            motto = extracted.get('motto')
            if motto and len(motto) > 200:
                motto = motto[:197] + '...'
            
            # Handle is_non_stop (default to False if None)
            is_non_stop = extracted.get('is_non_stop')
            if is_non_stop is None:
                is_non_stop = False
            
            # Create Company object
            company = Company(
                name=extracted['company_name'],
                motto=motto,
                description=extracted.get('description'),
                fiscal_code=fiscal_code,
                website=extracted.get('url'),
                facebook_url=extracted.get('facebook_url'),
                instagram_url=extracted.get('instagram_url'),
                is_non_stop=is_non_stop,
                founded_year=extracted.get('founded_year'),
                services=extracted.get('services', []),
                contacts=contacts,
                locations=locations
            )
            
            return company
            
        except Exception as e:
            logger.error(f"Error transforming data: {e}", exc_info=True)
            return None
    
    def run(self, urls: list = None, search_mode: bool = False, max_results: int = 5):
        """
        Main execution method.
        
        Args:
            urls: List of URLs to process (optional)
            search_mode: If True, search for URLs automatically
            max_results: Max URLs to find when in search_mode
        """
        if urls is None:
            if search_mode:
                logger.info("Search mode enabled - finding funeral home websites...")
                urls = self.search_tool.find_funeral_homes(total_limit=max_results)
            else:
                urls = self.load_seed_urls()
        
        if not urls:
            logger.error("No URLs to process! Try running with search_mode=True")
            return
        
        logger.info(f"\n{'='*60}")
        logger.info(f"Starting scraper run with {len(urls)} URLs")
        logger.info(f"{'='*60}\n")
        
        for url in urls:
            self.process_url(url)
        
        # Print summary
        logger.info(f"\n{'='*60}")
        logger.info("SCRAPING COMPLETE")
        logger.info(f"{'='*60}")
        logger.info(f"Processed: {self.stats['processed']}")
        logger.info(f"Success: {self.stats['success']}")
        logger.info(f"Failed: {self.stats['failed']}")
        logger.info(f"Verified: {self.stats['verified']}")
        logger.info(f"{'='*60}\n")
        
        # Print database stats
        db_stats = self.db.get_statistics()
        logger.info("Database Statistics:")
        logger.info(f"Total companies: {db_stats.get('total_companies', 0)}")
        logger.info(f"Verified companies: {db_stats.get('verified_companies', 0)}")
        logger.info(f"Verification rate: {db_stats.get('verification_rate', 0):.1f}%")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Funeral Directory Scraper')
    parser.add_argument('--search', action='store_true', help='Auto-search for funeral homes')
    parser.add_argument('--limit', type=int, default=5, help='Max URLs to process (default: 5)')
    parser.add_argument('--url', type=str, help='Single URL to process')
    parser.add_argument('--test', action='store_true', help='Test mode: search and process 3 URLs')
    
    args = parser.parse_args()
    
    scraper = FuneralDirectoryScraper()
    
    if args.test:
        # Test mode: auto-search and process first 3 results
        logger.info("\n" + "="*60)
        logger.info("TEST MODE - Processing first 3 search results")
        logger.info("="*60 + "\n")
        scraper.run(search_mode=True, max_results=3)
    elif args.url:
        # Process single URL
        scraper.run(urls=[args.url])
    elif args.search:
        # Auto-search mode
        scraper.run(search_mode=True, max_results=args.limit)
    else:
        # Load from seed file
        scraper.run()
