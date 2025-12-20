"""
Import Google Maps scraped data into Supabase database.
Transforms MapsBusinessData to Company model and saves.
"""
import json
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from tools.maps_scraper import GoogleMapsScraper, MapsBusinessData, scrape_city
from tools.supabase_tool import SupabaseTool
from tools.geocoding import geocode_address
from models import Company, Contact, Location
from utils import normalize_phone_number

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def maps_data_to_company(data: MapsBusinessData) -> Company:
    """Convert MapsBusinessData to Company model."""
    
    # Build contacts list
    contacts = []
    if data.phone:
        try:
            normalized, phone_type = normalize_phone_number(data.phone)
            if normalized:
                contact_type = 'phone_mobile' if phone_type == 'mobile' else 'phone_landline'
                contacts.append(Contact(type=contact_type, value=normalized))
        except (ValueError, Exception) as e:
            # If normalization fails, use raw phone
            contacts.append(Contact(type='phone', value=data.phone))
    
    if data.email:
        contacts.append(Contact(type='email', value=data.email))
    
    # Build locations list
    locations = []
    if data.address:
        location = Location(
            address=data.address,
            city=data.city or 'Timișoara',
            county=data.county or 'Timiș',
            latitude=data.latitude,
            longitude=data.longitude,
            type='headquarters'
        )
        locations.append(location)
    
    # Build company
    company = Company(
        name=data.name,
        description=data.description,
        fiscal_code=data.fiscal_code,
        website=data.website,
        is_non_stop=data.is_non_stop,
        services=data.services or [],
        contacts=contacts,
        locations=locations
    )
    
    return company


def import_from_json(json_file: str):
    """Import businesses from a JSON file into the database."""
    logger.info(f"Loading data from {json_file}...")
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    logger.info(f"Found {len(data)} businesses in JSON file")
    
    db = SupabaseTool()
    
    success = 0
    failed = 0
    skipped = 0
    
    for item in data:
        # Convert dict back to MapsBusinessData
        business = MapsBusinessData(**item)
        
        logger.info(f"\nProcessing: {business.name}")
        
        # Skip if no useful data
        if not business.phone and not business.website:
            logger.warning(f"  Skipping - no phone or website")
            skipped += 1
            continue
        
        # Convert to Company model
        company = maps_data_to_company(business)
        
        # Geocode if we don't have coordinates
        if company.locations and not company.locations[0].latitude:
            try:
                coords = geocode_address(company.locations[0].address, company.locations[0].city)
                if coords:
                    company.locations[0].latitude = coords[0]
                    company.locations[0].longitude = coords[1]
                    logger.info(f"  Geocoded: {coords}")
            except Exception as e:
                logger.warning(f"  Geocoding failed: {e}")
        
        # Save to database
        try:
            result = db.upsert_company(company)
            if result.get('success'):
                success += 1
                logger.info(f"  Saved: {result.get('action')}")
            else:
                failed += 1
                logger.error(f"  Failed: {result.get('error')}")
        except Exception as e:
            failed += 1
            logger.error(f"  Error: {e}")
    
    logger.info(f"\n{'='*60}")
    logger.info(f"IMPORT COMPLETE")
    logger.info(f"{'='*60}")
    logger.info(f"Success: {success}")
    logger.info(f"Failed: {failed}")
    logger.info(f"Skipped: {skipped}")
    logger.info(f"{'='*60}")


def scrape_and_import(city: str = "Timișoara", headless: bool = True, enrich: bool = True):
    """Scrape Google Maps and import directly to database."""
    logger.info(f"Starting Maps scrape for: {city}")
    
    # Scrape
    with GoogleMapsScraper(headless=headless) as scraper:
        businesses = scraper.search_and_enrich(
            query="servicii funerare",
            location=city,
            enrich_websites=enrich
        )
        
        # Save backup to JSON
        backup_file = f"maps_{city.lower().replace(' ', '_')}_backup.json"
        scraper.save_to_json(businesses, backup_file)
    
    logger.info(f"\nImporting {len(businesses)} businesses to database...")
    
    db = SupabaseTool()
    
    success = 0
    failed = 0
    
    for business in businesses:
        logger.info(f"\nProcessing: {business.name}")
        
        company = maps_data_to_company(business)
        
        # Geocode if needed
        if company.locations and not company.locations[0].latitude:
            try:
                coords = geocode_address(company.locations[0].address, company.locations[0].city)
                if coords:
                    company.locations[0].latitude = coords[0]
                    company.locations[0].longitude = coords[1]
            except:
                pass
        
        try:
            result = db.upsert_company(company)
            if result.get('success'):
                success += 1
            else:
                failed += 1
        except Exception as e:
            failed += 1
            logger.error(f"  Error: {e}")
    
    logger.info(f"\n{'='*60}")
    logger.info(f"SCRAPE & IMPORT COMPLETE")
    logger.info(f"{'='*60}")
    logger.info(f"Found: {len(businesses)} businesses")
    logger.info(f"Imported: {success}")
    logger.info(f"Failed: {failed}")
    logger.info(f"{'='*60}")
    
    # Print database stats
    stats = db.get_statistics()
    logger.info(f"\nDatabase now has:")
    logger.info(f"  Total companies: {stats.get('total_companies', 0)}")
    logger.info(f"  Verified: {stats.get('verified_companies', 0)}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Import Maps data to database')
    parser.add_argument('--json', type=str, help='Import from JSON file')
    parser.add_argument('--scrape', type=str, help='Scrape city and import')
    parser.add_argument('--no-headless', action='store_true', help='Show browser')
    parser.add_argument('--no-enrich', action='store_true', help='Skip website enrichment')
    
    args = parser.parse_args()
    
    if args.json:
        import_from_json(args.json)
    elif args.scrape:
        scrape_and_import(
            city=args.scrape,
            headless=not args.no_headless,
            enrich=not args.no_enrich
        )
    else:
        # Default: scrape Timișoara
        scrape_and_import(
            city="Timișoara",
            headless=True,
            enrich=True
        )
