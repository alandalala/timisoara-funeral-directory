"""Quick test: scrape only 5 businesses to verify data integrity."""
from tools.maps_scraper import GoogleMapsScraper
import logging

# Enable DEBUG logging to see coordinate extraction method
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')

print("Starting test scrape (5 businesses only)...")

scraper = GoogleMapsScraper(headless=False)  # Non-headless so we can see what's happening
scraper.start()

# Do search - STOP after finding 5 businesses
print("Searching (limited to 5 businesses)...")
results = scraper.search('servicii funerare', 'București, București, Romania', skip_names=set(), max_results=5)

print(f"\n{'='*60}")
print(f"Collected {len(results)} total, showing first 5:")
print(f"{'='*60}\n")

# Validate coordinates are unique and in București bounds (lat ~44.3-44.6, lng ~25.9-26.3)
bucuresti_bounds = {'lat_min': 44.3, 'lat_max': 44.6, 'lng_min': 25.9, 'lng_max': 26.3}
coord_issues = []

for i, r in enumerate(results[:5]):
    print(f"{i+1}. {r.name}")
    print(f"   Phone: {r.phone}")
    print(f"   Website: {r.website}")
    print(f"   Lat/Lng: {r.latitude}, {r.longitude}")
    print(f"   PlaceID: {r.place_id[:40] if r.place_id else 'None'}...")
    
    # Check if coordinates are within București bounds
    if r.latitude and r.longitude:
        in_bounds = (bucuresti_bounds['lat_min'] <= r.latitude <= bucuresti_bounds['lat_max'] and
                     bucuresti_bounds['lng_min'] <= r.longitude <= bucuresti_bounds['lng_max'])
        if not in_bounds:
            coord_issues.append(f"{r.name}: ({r.latitude}, {r.longitude}) - outside București")
            print(f"   ⚠️  OUTSIDE BUCUREȘTI BOUNDS!")
        else:
            print(f"   ✅ In București bounds")
    else:
        coord_issues.append(f"{r.name}: No coordinates")
        print(f"   ⚠️  NO COORDINATES!")
    print()

scraper.stop()

print(f"{'='*60}")
if coord_issues:
    print(f"❌ {len(coord_issues)} coordinate issues found:")
    for issue in coord_issues:
        print(f"   - {issue}")
else:
    print("✅ All coordinates valid and within București bounds!")
print(f"{'='*60}")
