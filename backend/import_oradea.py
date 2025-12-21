"""Import Oradea businesses that were missed in the original scrape."""
import json
import logging
from pathlib import Path
from tools.maps_scraper import GoogleMapsScraper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Scrape Oradea with improved scraper
logger.info("Scraping Oradea, Bihor with improved scroll logic...")
with GoogleMapsScraper(headless=True) as scraper:
    results = scraper.search_and_enrich('funerare', 'Oradea, Bihor, Romania', enrich_websites=False)
    logger.info(f'Scraped {len(results)} businesses')
    
    # Convert to dict format and save
    data = []
    for biz in results:
        item = {
            'name': biz.name,
            'address': biz.address,
            'city': 'Oradea',
            'county': 'Bihor',
            'phone': biz.phone,
            'website': biz.website,
            'rating': biz.rating,
            'review_count': biz.review_count,
            'business_hours': biz.business_hours,
            'is_non_stop': biz.is_non_stop,
            'services': biz.services,
        }
        data.append(item)
        logger.info(f"  - {biz.name}")
    
    # Save to JSON
    output_file = Path('data/scraped/maps_oradea_update.json')
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Saved to {output_file}")

# Now import using the existing importer
logger.info("Importing to database...")
import import_googlemaps
import_googlemaps.import_googlemaps_json(str(output_file), dry_run=False)
