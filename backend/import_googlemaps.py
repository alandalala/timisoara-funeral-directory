"""
Import Google Maps scraped data into Supabase database.
Dedicated importer for Maps data - handles service mapping and rating/reviews.
"""
import json
import logging
import sys
import re
import unicodedata
from pathlib import Path
from typing import List, Dict, Optional

sys.path.insert(0, str(Path(__file__).parent))

from tools.supabase_tool import SupabaseTool

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    # Normalize unicode characters
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    # Convert to lowercase
    text = text.lower()
    # Replace spaces and special chars with hyphens
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text).strip('-')
    return text


# Map scraped service keywords to valid service tags
SERVICE_MAPPING = {
    # Transport
    'transport funerar': 'transport',
    'transport decedat': 'transport',
    'transport': 'transport',
    # Repatriation
    'repatriere': 'repatriation',
    'transport internațional': 'repatriation',
    'transport international': 'repatriation',
    # Cremation
    'incinerare': 'cremation',
    'crematoriu': 'cremation',
    'cremație': 'cremation',
    'crematie': 'cremation',
    # Embalming
    'îmbălsămare': 'embalming',
    'imbalsamare': 'embalming',
    'tanatopraxie': 'embalming',
    # Wake house
    'priveghi': 'wake_house',
    'capelă': 'wake_house',
    'capela': 'wake_house',
    'sala de priveghi': 'wake_house',
    # Coffins
    'sicriu': 'coffins',
    'sicrie': 'coffins',
    'sicri': 'coffins',
    'coșciug': 'coffins',
    'cosciug': 'coffins',
    # Flowers
    'coroană': 'flowers',
    'coroane': 'flowers',
    'aranjamente florale': 'flowers',
    'flori': 'flowers',
    # Bureaucracy
    'acte deces': 'bureaucracy',
    'documente': 'bureaucracy',
    'formalități': 'bureaucracy',
    'formalitati': 'bureaucracy',
    'servicii complete': 'bureaucracy',
    'pachet funerar': 'bureaucracy',
    # Religious
    'religios': 'religious',
    'slujbă': 'religious',
    'slujba': 'religious',
    'preot': 'religious',
    # Monuments
    'cruce': 'monuments',
    'cruci': 'monuments',
    'monument': 'monuments',
    'monumente': 'monuments',
    # Burial
    'înmormântare': 'bureaucracy',
    'inmormantare': 'bureaucracy',
    'înhumare': 'bureaucracy',
}


def map_services(raw_services: List[str]) -> List[str]:
    """Map scraped service keywords to valid service tags."""
    mapped = set()
    
    for service in raw_services:
        service_lower = service.lower().strip()
        
        # Direct mapping
        if service_lower in SERVICE_MAPPING:
            mapped.add(SERVICE_MAPPING[service_lower])
            continue
        
        # Partial matching
        for keyword, tag in SERVICE_MAPPING.items():
            if keyword in service_lower or service_lower in keyword:
                mapped.add(tag)
                break
    
    return list(mapped)


def normalize_city(city: str) -> str:
    """
    Normalize city name by removing diacritics for consistent database storage.
    Timișoara, Timişoara -> Timisoara
    """
    if not city:
        return None
    # Remove diacritics
    normalized = unicodedata.normalize('NFKD', city)
    normalized = normalized.encode('ascii', 'ignore').decode('ascii')
    return normalized.strip()


def normalize_phone(phone: str) -> tuple:
    """
    Normalize Romanian phone number.
    Returns (normalized, type) where type is 'mobile' or 'landline'.
    """
    if not phone:
        return None, None
    
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    
    # Handle Romanian formats
    if digits.startswith('40'):
        digits = digits[2:]
    elif digits.startswith('0'):
        digits = digits[1:]
    
    # Determine type
    phone_type = 'mobile' if digits.startswith('7') else 'landline'
    
    # Validate length
    if len(digits) < 9 or len(digits) > 10:
        return phone, 'unknown'  # Return raw if invalid
    
    # Return with leading 0
    normalized = '0' + digits if not digits.startswith('0') else digits
    return normalized, phone_type


def import_googlemaps_json(json_file: str, dry_run: bool = False):
    """
    Import businesses from Google Maps JSON file into Supabase.
    
    Args:
        json_file: Path to JSON file with Maps data
        dry_run: If True, don't actually save to database
    """
    logger.info(f"Loading data from {json_file}...")
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    logger.info(f"Found {len(data)} businesses in JSON file")
    
    if not dry_run:
        db = SupabaseTool()
    
    success = 0
    failed = 0
    skipped = 0
    
    for item in data:
        name = item.get('name', 'Unknown')
        logger.info(f"\nProcessing: {name}")
        
        # Skip if no useful contact info
        if not item.get('phone') and not item.get('website'):
            logger.warning(f"  [SKIP] No phone or website")
            skipped += 1
            continue
        
        # Build company data for Supabase
        try:
            company_data = build_company_data(item)
            
            if dry_run:
                logger.info(f"  [DRY RUN] Would save: {company_data['name']}")
                logger.info(f"    Services: {company_data.get('services', [])}")
                logger.info(f"    Rating: {company_data.get('rating')} ({company_data.get('review_count')} reviews)")
                success += 1
                continue
            
            # Insert into Supabase
            result = save_to_supabase(db, company_data, item)
            
            if result.get('success'):
                success += 1
                logger.info(f"  [OK] Saved: {result.get('action', 'inserted')}")
            else:
                failed += 1
                logger.error(f"  [FAIL] {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            failed += 1
            logger.error(f"  [ERROR] {e}")
    
    logger.info(f"\n{'='*60}")
    logger.info(f"IMPORT COMPLETE")
    logger.info(f"{'='*60}")
    logger.info(f"Success: {success}")
    logger.info(f"Failed: {failed}")
    logger.info(f"Skipped: {skipped}")
    logger.info(f"{'='*60}")
    
    return {'success': success, 'failed': failed, 'skipped': skipped}


def build_company_data(item: Dict) -> Dict:
    """Build company data dictionary from Maps item."""
    
    # Map services
    raw_services = item.get('services') or []
    services = map_services(raw_services)
    
    # Build metadata with rating/reviews
    metadata = {}
    if item.get('rating'):
        metadata['rating'] = item.get('rating')
    if item.get('review_count'):
        metadata['review_count'] = item.get('review_count')
    if item.get('category'):
        metadata['category'] = item.get('category')
    metadata['source'] = 'google_maps'
    
    # Build company dict
    company = {
        'name': item.get('name'),
        'description': item.get('description'),
        'website': item.get('website'),
        'is_non_stop': item.get('is_non_stop', False),
        'services': services,
        'metadata': metadata,
    }
    
    # Clean up None values
    company = {k: v for k, v in company.items() if v is not None}
    
    return company


def save_to_supabase(db: SupabaseTool, company_data: Dict, item: Dict) -> Dict:
    """Save company and related data to Supabase."""
    
    try:
        # Check if company already exists by website or phone
        existing = None
        
        if item.get('website'):
            result = db.client.table('companies').select('*').eq('website', item['website']).execute()
            if result.data:
                existing = result.data[0]
        
        if not existing and item.get('phone'):
            normalized_phone, _ = normalize_phone(item['phone'])
            if normalized_phone:
                # Check contacts table for matching phone
                result = db.client.table('contacts').select('company_id, value').ilike('value', f'%{normalized_phone[-9:]}%').execute()
                if result.data:
                    company_id = result.data[0]['company_id']
                    comp_result = db.client.table('companies').select('*').eq('id', company_id).execute()
                    if comp_result.data:
                        existing = comp_result.data[0]
        
        if existing:
            # Update existing company
            company_id = existing['id']
            
            # Only update fields that are empty in existing record
            updates = {}
            existing_metadata = existing.get('metadata') or {}
            
            if not existing_metadata.get('rating') and company_data.get('metadata', {}).get('rating'):
                existing_metadata['rating'] = company_data['metadata']['rating']
            if not existing_metadata.get('review_count') and company_data.get('metadata', {}).get('review_count'):
                existing_metadata['review_count'] = company_data['metadata']['review_count']
            if not existing.get('description') and company_data.get('description'):
                updates['description'] = company_data['description']
            
            # Always update metadata if we have new data
            if existing_metadata:
                updates['metadata'] = existing_metadata
            
            if updates:
                db.client.table('companies').update(updates).eq('id', company_id).execute()
            
            return {'success': True, 'action': 'updated', 'id': company_id}
        
        else:
            # Insert new company
            insert_data = {
                'name': company_data['name'],
                'slug': slugify(company_data['name']),
                'description': company_data.get('description'),
                'website': company_data.get('website'),
                'is_non_stop': company_data.get('is_non_stop', False),
                'metadata': company_data.get('metadata', {}),
            }
            
            result = db.client.table('companies').insert(insert_data).execute()
            
            if not result.data:
                return {'success': False, 'error': 'Insert returned no data'}
            
            company_id = result.data[0]['id']
            
            # Insert contacts
            contacts_to_insert = []
            
            if item.get('phone'):
                normalized, phone_type = normalize_phone(item['phone'])
                contact_type = 'phone_mobile' if phone_type == 'mobile' else 'phone_landline'
                contacts_to_insert.append({
                    'company_id': company_id,
                    'type': contact_type,
                    'value': normalized,
                    'is_primary': True
                })
            
            if item.get('email'):
                contacts_to_insert.append({
                    'company_id': company_id,
                    'type': 'email',
                    'value': item['email'],
                    'is_primary': False
                })
            
            if contacts_to_insert:
                db.client.table('contacts').insert(contacts_to_insert).execute()
            
            # Insert location
            if item.get('address'):
                location_data = {
                    'company_id': company_id,
                    'address': item['address'],
                    'city': normalize_city(item.get('city')) or 'Timisoara',
                    'county': normalize_city(item.get('county')) or 'Timis',
                    'type': 'headquarters'
                }
                # Add coordinates if available
                if item.get('latitude') and item.get('longitude'):
                    location_data['latitude'] = item['latitude']
                    location_data['longitude'] = item['longitude']
                    location_data['geo_point'] = f"POINT({item['longitude']} {item['latitude']})"
                db.client.table('locations').insert(location_data).execute()
            
            # Insert services
            services = company_data.get('services', [])
            if services:
                services_to_insert = [
                    {'company_id': company_id, 'service_tag': service}
                    for service in services
                ]
                db.client.table('services').insert(services_to_insert).execute()
            
            return {'success': True, 'action': 'inserted', 'id': company_id}
    
    except Exception as e:
        return {'success': False, 'error': str(e)}


if __name__ == "__main__":
    import argparse
    import glob
    
    parser = argparse.ArgumentParser(description='Import Google Maps data to Supabase')
    parser.add_argument('json_file', nargs='?', help='Path to JSON file with Maps data')
    parser.add_argument('--dry-run', action='store_true', help='Preview without saving')
    parser.add_argument('--county', type=str, help='Import specific county file from data/scraped/')
    parser.add_argument('--all-counties', action='store_true', help='Import all county files from data/scraped/')
    parser.add_argument('--list', action='store_true', help='List available county files')
    
    args = parser.parse_args()
    
    scraped_dir = Path(__file__).parent / "data" / "scraped"
    
    # List available files
    if args.list:
        if scraped_dir.exists():
            files = list(scraped_dir.glob("maps_*.json"))
            if files:
                print(f"\n📁 Available county files in {scraped_dir}:\n")
                total_businesses = 0
                for f in sorted(files):
                    with open(f, 'r', encoding='utf-8') as fp:
                        data = json.load(fp)
                        count = len(data)
                        total_businesses += count
                        print(f"  • {f.name}: {count} businesses")
                print(f"\n  Total: {total_businesses} businesses across {len(files)} files")
            else:
                print(f"No county files found in {scraped_dir}")
        else:
            print(f"Scraped directory not found: {scraped_dir}")
        sys.exit(0)
    
    # Import all counties
    if args.all_counties:
        if not scraped_dir.exists():
            print(f"❌ Scraped directory not found: {scraped_dir}")
            sys.exit(1)
        
        files = sorted(scraped_dir.glob("maps_*.json"))
        if not files:
            print(f"❌ No county files found in {scraped_dir}")
            sys.exit(1)
        
        print(f"\n📥 Importing {len(files)} county files...\n")
        
        for filepath in files:
            print(f"\n{'='*50}")
            print(f"📁 {filepath.name}")
            print(f"{'='*50}")
            import_googlemaps_json(str(filepath), dry_run=args.dry_run)
        
        print(f"\n✅ Completed importing {len(files)} county files")
        sys.exit(0)
    
    # Import specific county
    if args.county:
        slug = args.county.lower().replace(' ', '_').replace('ș', 's').replace('ț', 't').replace('ă', 'a').replace('â', 'a').replace('î', 'i')
        filepath = scraped_dir / f"maps_{slug}.json"
        
        if not filepath.exists():
            print(f"❌ County file not found: {filepath}")
            print(f"   Run 'python scrape_romania.py --county \"{args.county}\"' first")
            sys.exit(1)
        
        import_googlemaps_json(str(filepath), dry_run=args.dry_run)
        sys.exit(0)
    
    # Import single file
    if args.json_file:
        import_googlemaps_json(args.json_file, dry_run=args.dry_run)
    else:
        parser.print_help()
        print("\n⚠️ Specify a JSON file, --county, or --all-counties")

