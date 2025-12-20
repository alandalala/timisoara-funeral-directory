"""
Romania-wide Google Maps Scraper Orchestration Script.
Scrapes funeral companies across all counties and cities in Romania.

Features:
- Progress tracking with resume capability
- Per-county JSON output files  
- Graceful stop on Ctrl+C
- Configurable: single county, list of counties, or all Romania

Usage:
    python scrape_romania.py --county "Timiș"        # Single county
    python scrape_romania.py --counties "Timiș,Arad" # Multiple counties
    python scrape_romania.py --all                   # All Romania
    python scrape_romania.py --resume                # Resume interrupted scrape
"""
import json
import os
import sys
import time
import signal
import logging
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from tools.maps_scraper import GoogleMapsScraper, MapsBusinessData

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Paths
DATA_DIR = Path(__file__).parent / "data"
CITIES_FILE = DATA_DIR / "romania_cities.json"
PROGRESS_FILE = DATA_DIR / "scrape_progress.json"
OUTPUT_DIR = DATA_DIR / "scraped"


class RomaniaScraper:
    """Orchestrates scraping across all Romanian counties and cities."""
    
    def __init__(self, headless: bool = True, enrich: bool = False):
        """
        Initialize the Romania-wide scraper.
        
        Args:
            headless: Run browser in headless mode
            enrich: Enrich data from company websites (slower but more data)
        """
        self.headless = headless
        self.enrich = enrich
        self.stop_requested = False
        self.counties_data = self._load_cities()
        
        # Create output directory
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        # Setup signal handler for graceful stop
        signal.signal(signal.SIGINT, self._signal_handler)
        
    def _signal_handler(self, signum, frame):
        """Handle Ctrl+C for graceful shutdown."""
        logger.warning("\n⚠️ Stop requested. Finishing current city and saving progress...")
        self.stop_requested = True
        
    def _load_cities(self) -> Dict:
        """Load Romania cities data."""
        with open(CITIES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _load_progress(self) -> Dict:
        """Load scraping progress."""
        if PROGRESS_FILE.exists():
            with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "started_at": None,
            "last_updated": None,
            "completed_counties": [],
            "completed_cities": {},  # {county: [city1, city2]}
            "current_county": None,
            "current_city": None,
            "failed": [],
            "total_businesses": 0,
            "stats": {}
        }
    
    def _save_progress(self, progress: Dict):
        """Save scraping progress."""
        progress["last_updated"] = datetime.now().isoformat()
        with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
            json.dump(progress, f, ensure_ascii=False, indent=2)
    
    def _get_county_output_file(self, county_name: str) -> Path:
        """Get output file path for a county."""
        slug = county_name.lower().replace(' ', '_').replace('ș', 's').replace('ț', 't').replace('ă', 'a').replace('â', 'a').replace('î', 'i')
        return OUTPUT_DIR / f"maps_{slug}.json"
    
    def _load_county_data(self, county_name: str) -> List[Dict]:
        """Load existing scraped data for a county."""
        filepath = self._get_county_output_file(county_name)
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _save_county_data(self, county_name: str, businesses: List[Dict]):
        """Save scraped data for a county."""
        filepath = self._get_county_output_file(county_name)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(businesses, f, ensure_ascii=False, indent=2)
        logger.info(f"💾 Saved {len(businesses)} businesses to {filepath}")
    
    def _append_businesses(self, county_name: str, new_businesses: List[MapsBusinessData]):
        """Append new businesses to county data (avoiding duplicates)."""
        existing = self._load_county_data(county_name)
        existing_names = {b['name'].lower() for b in existing}
        
        for biz in new_businesses:
            biz_dict = {k: v for k, v in biz.__dict__.items() if not k.startswith('_')}
            if biz.name.lower() not in existing_names:
                existing.append(biz_dict)
                existing_names.add(biz.name.lower())
        
        self._save_county_data(county_name, existing)
        return len(existing)
    
    def get_counties_to_scrape(self, county_filter: List[str] = None) -> List[Dict]:
        """Get list of counties to scrape."""
        counties = self.counties_data['counties']
        
        if county_filter:
            counties = [c for c in counties if c['name'] in county_filter]
        
        return counties
    
    def _normalize_city_name(self, city: str) -> str:
        """Normalize city name for comparison (remove diacritics, lowercase)."""
        import unicodedata
        # Remove diacritics
        normalized = unicodedata.normalize('NFD', city)
        normalized = ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')
        return normalized.lower().strip()
    
    def _business_matches_city(self, business: MapsBusinessData, city: str, county: str) -> bool:
        """
        Check if a business actually belongs to the searched city.
        
        Args:
            business: Business data to check
            city: Expected city name
            county: Expected county name
            
        Returns:
            True if business appears to be in the target city
        """
        city_normalized = self._normalize_city_name(city)
        county_normalized = self._normalize_city_name(county)
        
        # Check address field
        if business.address:
            address_normalized = self._normalize_city_name(business.address)
            
            # Check if city name appears in address
            if city_normalized in address_normalized:
                return True
            
            # For county capitals (city name = county name), just verify county
            if city_normalized == county_normalized and county_normalized in address_normalized:
                return True
        
        # Check the city field if set
        if business.city:
            business_city_normalized = self._normalize_city_name(business.city)
            if city_normalized in business_city_normalized or business_city_normalized in city_normalized:
                return True
        
        return False
    
    def scrape_city(self, city: str, county: str, scraper: GoogleMapsScraper) -> List[MapsBusinessData]:
        """
        Scrape a single city.
        
        Args:
            city: City name
            county: County name
            scraper: Active GoogleMapsScraper instance
            
        Returns:
            List of business data
        """
        query = "servicii funerare"
        location = f"{city}, {county}, Romania"
        
        logger.info(f"🔍 Scraping: {city}, {county}")
        
        try:
            businesses = scraper.search_and_enrich(
                query=query,
                location=location,
                enrich_websites=self.enrich
            )
            
            # If no results, retry with simpler location (city, Romania) 
            # Some cities don't return results when county is included
            if len(businesses) == 0:
                logger.info(f"  🔄 Retrying with simpler location: {city}, Romania")
                location_simple = f"{city}, Romania"
                businesses = scraper.search_and_enrich(
                    query=query,
                    location=location_simple,
                    enrich_websites=self.enrich
                )
            
            # Filter businesses to only those actually in the target city
            filtered_businesses = []
            for biz in businesses:
                if self._business_matches_city(biz, city, county):
                    if not biz.county:
                        biz.county = county
                    if not biz.city:
                        biz.city = city
                    filtered_businesses.append(biz)
                else:
                    logger.debug(f"  ⚠️ Filtered out '{biz.name}' - address '{biz.address}' doesn't match {city}")
            
            filtered_count = len(businesses) - len(filtered_businesses)
            if filtered_count > 0:
                logger.info(f"  📍 Filtered {filtered_count} businesses not in {city}")
            
            logger.info(f"  ✅ Found {len(filtered_businesses)} businesses in {city}")
            return filtered_businesses
            return businesses
            
        except Exception as e:
            logger.error(f"  ❌ Error scraping {city}: {e}")
            return []
    
    def scrape_county(self, county_data: Dict, progress: Dict) -> int:
        """
        Scrape all cities in a county.
        
        Args:
            county_data: County info with cities list
            progress: Progress tracking dict
            
        Returns:
            Total businesses found in county
        """
        county_name = county_data['name']
        cities = county_data['cities']
        
        # Get already completed cities for this county
        completed_cities = set(progress.get('completed_cities', {}).get(county_name, []))
        cities_to_scrape = [c for c in cities if c not in completed_cities]
        
        if not cities_to_scrape:
            logger.info(f"✅ County {county_name} already completed")
            return 0
        
        logger.info(f"\n{'='*60}")
        logger.info(f"🏛️  COUNTY: {county_name}")
        logger.info(f"   Cities: {len(cities_to_scrape)} remaining (of {len(cities)} total)")
        logger.info(f"{'='*60}")
        
        progress['current_county'] = county_name
        
        total_found = 0
        
        with GoogleMapsScraper(headless=self.headless) as scraper:
            for city in cities_to_scrape:
                if self.stop_requested:
                    logger.warning(f"⏹️ Stopping after {city}")
                    break
                
                progress['current_city'] = city
                self._save_progress(progress)
                
                businesses = self.scrape_city(city, county_name, scraper)
                
                if businesses:
                    total_found += len(businesses)
                    county_total = self._append_businesses(county_name, businesses)
                    progress['total_businesses'] = progress.get('total_businesses', 0) + len(businesses)
                
                # Mark city as completed
                if county_name not in progress['completed_cities']:
                    progress['completed_cities'][county_name] = []
                progress['completed_cities'][county_name].append(city)
                self._save_progress(progress)
                
                # Random delay between cities (2-5 seconds)
                delay = 2 + (hash(city) % 30) / 10  # 2-5 seconds
                time.sleep(delay)
        
        # Mark county as completed if all cities done
        if not self.stop_requested:
            progress['completed_counties'].append(county_name)
            progress['stats'][county_name] = total_found
            self._save_progress(progress)
            logger.info(f"✅ Completed {county_name}: {total_found} businesses")
        
        return total_found
    
    def scrape(self, counties: List[str] = None, resume: bool = True):
        """
        Main scraping method.
        
        Args:
            counties: List of county names to scrape (None = all)
            resume: Resume from previous progress
        """
        progress = self._load_progress() if resume else {
            "started_at": datetime.now().isoformat(),
            "last_updated": None,
            "completed_counties": [],
            "completed_cities": {},
            "current_county": None,
            "current_city": None,
            "failed": [],
            "total_businesses": 0,
            "stats": {}
        }
        
        if not progress.get('started_at'):
            progress['started_at'] = datetime.now().isoformat()
        
        # Get counties to scrape
        counties_to_scrape = self.get_counties_to_scrape(counties)
        
        # Filter out already completed counties
        completed = set(progress.get('completed_counties', []))
        counties_to_scrape = [c for c in counties_to_scrape if c['name'] not in completed]
        
        logger.info(f"\n{'='*60}")
        logger.info(f"🇷🇴 ROMANIA FUNERAL COMPANY SCRAPER")
        logger.info(f"{'='*60}")
        logger.info(f"Counties to scrape: {len(counties_to_scrape)}")
        logger.info(f"Already completed: {len(completed)}")
        logger.info(f"Headless mode: {self.headless}")
        logger.info(f"Website enrichment: {self.enrich}")
        logger.info(f"{'='*60}\n")
        
        total_businesses = progress.get('total_businesses', 0)
        
        for county_data in counties_to_scrape:
            if self.stop_requested:
                break
            
            found = self.scrape_county(county_data, progress)
            total_businesses += found
        
        # Final summary
        logger.info(f"\n{'='*60}")
        logger.info(f"📊 SCRAPING SUMMARY")
        logger.info(f"{'='*60}")
        logger.info(f"Total businesses found: {progress.get('total_businesses', 0)}")
        logger.info(f"Counties completed: {len(progress.get('completed_counties', []))}")
        logger.info(f"Status: {'INTERRUPTED' if self.stop_requested else 'COMPLETED'}")
        logger.info(f"{'='*60}\n")
        
        self._save_progress(progress)
        return progress


def main():
    parser = argparse.ArgumentParser(
        description='Scrape funeral companies across Romania from Google Maps'
    )
    parser.add_argument(
        '--county', type=str, 
        help='Single county to scrape (e.g., "Timiș")'
    )
    parser.add_argument(
        '--counties', type=str,
        help='Comma-separated list of counties (e.g., "Timiș,Arad,Bihor")'
    )
    parser.add_argument(
        '--all', action='store_true',
        help='Scrape all Romania'
    )
    parser.add_argument(
        '--resume', action='store_true',
        help='Resume from previous progress'
    )
    parser.add_argument(
        '--no-headless', action='store_true',
        help='Show browser window (useful for debugging)'
    )
    parser.add_argument(
        '--enrich', action='store_true',
        help='Enrich data from company websites (slower)'
    )
    parser.add_argument(
        '--list-counties', action='store_true',
        help='List all available counties and exit'
    )
    parser.add_argument(
        '--status', action='store_true',
        help='Show current scraping progress and exit'
    )
    
    args = parser.parse_args()
    
    # List counties
    if args.list_counties:
        with open(CITIES_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("\n📋 Available counties:\n")
        for county in data['counties']:
            cities = ", ".join(county['cities'][:3])
            if len(county['cities']) > 3:
                cities += f" (+{len(county['cities'])-3} more)"
            print(f"  • {county['name']}: {cities}")
        print(f"\nTotal: {len(data['counties'])} counties")
        return
    
    # Show status
    if args.status:
        if PROGRESS_FILE.exists():
            with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
                progress = json.load(f)
            print("\n📊 Scraping Progress:\n")
            print(f"Started: {progress.get('started_at', 'N/A')}")
            print(f"Last updated: {progress.get('last_updated', 'N/A')}")
            print(f"Total businesses: {progress.get('total_businesses', 0)}")
            print(f"Completed counties: {len(progress.get('completed_counties', []))}")
            if progress.get('completed_counties'):
                print(f"  {', '.join(progress['completed_counties'])}")
            print(f"Current: {progress.get('current_county', 'N/A')} / {progress.get('current_city', 'N/A')}")
            if progress.get('stats'):
                print("\n📈 Per-county stats:")
                for county, count in progress['stats'].items():
                    print(f"  {county}: {count} businesses")
        else:
            print("No scraping progress found. Run --all or --county to start.")
        return
    
    # Determine counties to scrape
    counties_filter = None
    
    if args.county:
        counties_filter = [args.county]
    elif args.counties:
        counties_filter = [c.strip() for c in args.counties.split(',')]
    elif not args.all and not args.resume:
        parser.print_help()
        print("\n⚠️ Specify --county, --counties, --all, or --resume")
        return
    
    # Run scraper
    scraper = RomaniaScraper(
        headless=not args.no_headless,
        enrich=args.enrich
    )
    
    scraper.scrape(counties=counties_filter, resume=args.resume or args.all)


if __name__ == "__main__":
    main()
