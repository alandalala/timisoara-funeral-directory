#!/usr/bin/env python3
"""
Process a single URL - run from command line:
    python scrape_single.py https://example.com
"""
import sys
import signal
import logging
from datetime import datetime

# Set up logging FIRST
log_filename = f"scrape_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Handle Ctrl+C gracefully
def signal_handler(sig, frame):
    logger.warning("Interrupted by user - exiting gracefully")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def process_url(url: str):
    """Process a single URL with full logging."""
    logger.info(f"=" * 60)
    logger.info(f"Processing: {url}")
    logger.info(f"=" * 60)
    
    try:
        from main import FuneralDirectoryScraper
        
        scraper = FuneralDirectoryScraper()
        logger.info("Scraper initialized")
        
        # Step 1: Firecrawl extraction
        logger.info("Step 1: Scraping with Firecrawl...")
        scraped_data = scraper.firecrawl.scrape_url(url, include_subpages=True)
        
        if not scraped_data.get('success'):
            logger.error(f"Firecrawl failed: {scraped_data.get('error')}")
            return False
            
        content = scraped_data.get('markdown', '')
        logger.info(f"Scraped {len(content)} characters of content")
        
        # Step 2: LLM extraction
        logger.info("Step 2: Extracting data with LLM...")
        extracted = scraper.llm_extractor.extract_company_data(content, url)
        
        if not extracted.get('success'):
            logger.error(f"LLM extraction failed: {extracted.get('error')}")
            return False
            
        company_data = extracted.get('data', {})
        logger.info(f"Extracted company: {company_data.get('company_name', 'Unknown')}")
        logger.info(f"  Phones: {company_data.get('phones', [])}")
        logger.info(f"  Emails: {company_data.get('emails', [])}")
        logger.info(f"  Locations: {len(company_data.get('locations', []))} found")
        
        for i, loc in enumerate(company_data.get('locations', [])):
            logger.info(f"    Location {i+1}: {loc.get('address', 'N/A')}, {loc.get('city', 'N/A')}")
        
        # Step 3: Validation
        logger.info("Step 3: Validating location...")
        
        # Check if it's a directory (too many phones)
        phones = company_data.get('phones', [])
        if len(phones) > 5:
            logger.warning(f"REJECTED: Too many phones ({len(phones)}) - likely a directory")
            return False
        
        # Check location
        if not scraper._validate_location(company_data, url):
            logger.warning("REJECTED: Not in Timișoara/Timiș")
            return False
            
        logger.info("Location validated: Timișoara/Timiș")
        
        # Step 4: Transform and save
        logger.info("Step 4: Saving to database...")
        company = scraper._transform_to_company(company_data, url)
        
        # Geocode
        if company.addresses:
            logger.info("Geocoding addresses...")
            for addr in company.addresses:
                coords = scraper.geocoding.geocode_address(addr.full_address)
                if coords:
                    addr.latitude, addr.longitude = coords
                    logger.info(f"  Geocoded: {addr.full_address} -> {coords}")
                else:
                    logger.warning(f"  Failed to geocode: {addr.full_address}")
        
        # Save
        result = scraper.supabase.save_company(company)
        
        if result.get('success'):
            logger.info(f"SUCCESS: Saved company with ID {result.get('id')}")
            return True
        else:
            logger.error(f"Database error: {result.get('error')}")
            return False
            
    except Exception as e:
        logger.exception(f"Error processing {url}: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python scrape_single.py <url>")
        print("Example: python scrape_single.py https://example-funeral.ro")
        sys.exit(1)
    
    url = sys.argv[1]
    
    # Ensure URL has protocol
    if not url.startswith('http'):
        url = 'https://' + url
    
    logger.info(f"Starting scrape for: {url}")
    logger.info(f"Log file: {log_filename}")
    
    success = process_url(url)
    
    if success:
        logger.info("Scraping completed successfully!")
    else:
        logger.error("Scraping failed or company rejected")
    
    logger.info(f"Full log saved to: {log_filename}")

if __name__ == "__main__":
    main()
