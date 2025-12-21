"""
Batch Geocoding Script - Geocode scraped businesses that are missing coordinates.

Run this AFTER scraping to add accurate coordinates to all businesses.
Nominatim rate limit: 1 request/second, so this can take a while for large datasets.

Usage:
    python geocode_scraped.py                    # Geocode all files
    python geocode_scraped.py bucuresti          # Geocode only București
    python geocode_scraped.py --dry-run          # Show what would be geocoded
"""
import json
import sys
import logging
from pathlib import Path
from datetime import datetime

from tools.geocoding import GeocodingTool, has_street_number

# Setup logging
log_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = f"geocode_{log_timestamp}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_filename, encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent / "data" / "scraped"


def geocode_file(filepath: Path, dry_run: bool = False) -> tuple:
    """
    Geocode businesses in a single file that are missing coordinates.
    
    Args:
        filepath: Path to the JSON file
        dry_run: If True, don't save changes, just report
        
    Returns:
        Tuple of (total, already_geocoded, newly_geocoded, failed)
    """
    logger.info(f"\n📁 Processing: {filepath.name}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        businesses = json.load(f)
    
    total = len(businesses)
    already_geocoded = 0
    newly_geocoded = 0
    failed = 0
    
    geocoder = GeocodingTool()
    
    for i, biz in enumerate(businesses):
        name = biz.get('name', 'Unknown')
        
        # Skip if already has valid coordinates
        if biz.get('latitude') and biz.get('longitude'):
            # Check if it's not a placeholder/city-center coordinate
            lat, lng = biz['latitude'], biz['longitude']
            # Skip if coord_quality is already set and is 'exact'
            if biz.get('coord_quality') == 'exact':
                already_geocoded += 1
                continue
            # Also skip approximate if coordinates look reasonable
            if biz.get('coord_quality') == 'approximate':
                already_geocoded += 1
                continue
        
        address = biz.get('address')
        if not address:
            logger.warning(f"  [{i+1}/{total}] ⚠️ No address: {name}")
            failed += 1
            continue
        
        if dry_run:
            logger.info(f"  [{i+1}/{total}] Would geocode: {name}")
            continue
        
        # Geocode the address
        try:
            coords = geocoder.geocode(
                address=address,
                city=biz.get('city'),
                county=biz.get('county'),
                company_name=name
            )
            
            if coords:
                biz['latitude'], biz['longitude'] = coords
                biz['coord_quality'] = 'exact' if has_street_number(address) else 'approximate'
                newly_geocoded += 1
                logger.info(f"  [{i+1}/{total}] ✅ {name} -> ({coords[0]:.6f}, {coords[1]:.6f})")
            else:
                failed += 1
                biz['coord_quality'] = 'none'
                logger.warning(f"  [{i+1}/{total}] ❌ Could not geocode: {name}")
                
        except Exception as e:
            failed += 1
            logger.error(f"  [{i+1}/{total}] ❌ Error geocoding {name}: {e}")
    
    # Save updated data
    if not dry_run and newly_geocoded > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(businesses, f, ensure_ascii=False, indent=2)
        logger.info(f"  💾 Saved {filepath.name}")
    
    return total, already_geocoded, newly_geocoded, failed


def main():
    args = sys.argv[1:]
    dry_run = '--dry-run' in args
    args = [a for a in args if a != '--dry-run']
    
    # Get files to process
    if args:
        # Filter by county name
        county_filter = args[0].lower()
        files = [f for f in DATA_DIR.glob("maps_*.json") if county_filter in f.stem.lower()]
    else:
        files = list(DATA_DIR.glob("maps_*.json"))
    
    if not files:
        logger.error("No scraped files found in data/scraped/")
        return
    
    logger.info(f"{'='*60}")
    logger.info(f"🌍 Batch Geocoding - {len(files)} files to process")
    if dry_run:
        logger.info("🔍 DRY RUN - no changes will be saved")
    logger.info(f"📝 Log file: {log_filename}")
    logger.info(f"{'='*60}")
    
    # Process each file
    grand_total = 0
    grand_already = 0
    grand_new = 0
    grand_failed = 0
    
    for filepath in sorted(files):
        total, already, new, failed = geocode_file(filepath, dry_run)
        grand_total += total
        grand_already += already
        grand_new += new
        grand_failed += failed
    
    # Summary
    logger.info(f"\n{'='*60}")
    logger.info(f"📊 GEOCODING SUMMARY")
    logger.info(f"{'='*60}")
    logger.info(f"Total businesses:     {grand_total}")
    logger.info(f"Already geocoded:     {grand_already}")
    logger.info(f"Newly geocoded:       {grand_new}")
    logger.info(f"Failed/No address:    {grand_failed}")
    logger.info(f"{'='*60}")


if __name__ == "__main__":
    main()
