"""Fix missing lat/lng in locations table from scraped data."""
import json
from tools.supabase_tool import SupabaseTool

def main():
    db = SupabaseTool()
    
    # Load original scraped data
    data = json.load(open('maps_timisoara_enriched.json', encoding='utf-8'))
    
    # Create a map of address -> (lat, lng)
    coords_map = {}
    for item in data:
        if item.get('latitude') and item.get('longitude') and item.get('address'):
            coords_map[item['address']] = (item['latitude'], item['longitude'])
    
    print(f'Found {len(coords_map)} addresses with coordinates in JSON')
    
    # Get all locations
    result = db.client.table('locations').select('id, address, latitude, longitude').execute()
    print(f'Found {len(result.data)} locations in database')
    
    updated = 0
    for loc in result.data:
        if not loc.get('latitude') and loc.get('address'):
            # Try exact match
            coords = coords_map.get(loc['address'])
            if coords:
                db.client.table('locations').update({
                    'latitude': coords[0],
                    'longitude': coords[1]
                }).eq('id', loc['id']).execute()
                updated += 1
                print(f'  Updated: {loc["address"][:50]}')
    
    print(f'\nUpdated {updated} locations with coordinates')

if __name__ == '__main__':
    main()
