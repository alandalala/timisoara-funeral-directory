"""
Main orchestration script for the funeral directory scraper.
"""
import sys
import json
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from tools.dsp_verification import DSPVerificationTool
from tools.firecrawl_extractor import FirecrawlExtractorTool
from tools.llm_extractor import LLMExtractorTool
from tools.supabase_tool import SupabaseTool
from tools.google_search import GoogleSearchTool
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
            logger.info(f"✓ Scraped {len(markdown_content)} characters")
            
            # Step 2: Extract with LLM
            logger.info("Step 2: Extracting structured data with LLM...")
            extraction_result = self.llm_extractor.extract_company_data(markdown_content, url)
            
            if not extraction_result['success']:
                logger.error(f"Failed to extract: {extraction_result.get('error')}")
                self.stats['failed'] += 1
                return False
            
            extracted = extraction_result['data']
            logger.info(f"✓ Extracted data for: {extracted.get('company_name', 'Unknown')}")
            
            # Step 3: Validate and transform data
            logger.info("Step 3: Validating and transforming data...")
            company = self._transform_to_company(extracted)
            
            if not company:
                logger.error("Failed to create valid company object")
                self.stats['failed'] += 1
                return False
            
            # Step 4: DSP Verification
            logger.info("Step 4: Verifying against DSP list...")
            verification = self.dsp_tool.verify_company(
                company.name,
                company.fiscal_code
            )
            
            company.is_verified = verification['is_verified']
            
            if verification['is_verified']:
                logger.info(f"✓ VERIFIED (score: {verification.get('match_score', 0)})")
                self.stats['verified'] += 1
            else:
                logger.info("✗ Not verified")
            
            # Step 5: Store in database
            logger.info("Step 5: Storing in database...")
            result = self.db.upsert_company(company)
            
            if result['success']:
                self.stats['success'] += 1
                logger.info(f"✓ SUCCESS - Company {result['action']}")
                return True
            else:
                logger.error(f"Failed to store: {result.get('error')}")
                self.stats['failed'] += 1
                return False
                
        except Exception as e:
            logger.error(f"Unexpected error processing {url}: {e}", exc_info=True)
            self.stats['failed'] += 1
            return False
    
    def _transform_to_company(self, extracted: dict) -> Company:
        """
        Transform extracted dict to Company model with validation.
        """
        try:
            # Process contacts
            contacts = []
            
            # Process phones
            for phone in extracted.get('phones', []):
                try:
                    normalized, phone_type = normalize_phone_number(phone)
                    contact_type = 'phone_mobile' if phone_type == 'mobile' else 'phone_landline'
                    
                    contacts.append(Contact(
                        type=contact_type,
                        value=normalized,
                        is_primary=(len(contacts) == 0)  # First one is primary
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
            
            # Process locations
            locations = []
            if extracted.get('address'):
                locations.append(Location(
                    address=extracted['address'],
                    type='headquarters'
                ))
            
            # Extract fiscal code
            fiscal_code = extracted.get('fiscal_code')
            if not fiscal_code and extracted.get('description'):
                # Try to extract from description
                fiscal_code = extract_cui_from_text(extracted.get('description', ''))
            
            # Create Company object
            company = Company(
                name=extracted['company_name'],
                motto=extracted.get('motto'),
                description=extracted.get('description'),
                fiscal_code=fiscal_code,
                website=extracted.get('url'),
                is_non_stop=extracted.get('is_non_stop', False),
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
