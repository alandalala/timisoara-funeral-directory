"""Fix missing rating/review_count in companies metadata from scraped data."""
import json
from tools.supabase_tool import SupabaseTool

def normalize_name(name: str) -> str:
    """Normalize company name for matching."""
    import unicodedata
    name = unicodedata.normalize('NFKD', name)
    name = name.encode('ascii', 'ignore').decode('ascii')
    return name.lower().strip()

def main():
    db = SupabaseTool()
    
    # Load original scraped data
    data = json.load(open('maps_timisoara_enriched.json', encoding='utf-8'))
    
    # Create a map of normalized name -> rating info
    rating_map = {}
    for item in data:
        if item.get('rating') and item.get('name'):
            key = normalize_name(item['name'])
            rating_map[key] = {
                'rating': item['rating'],
                'review_count': item.get('review_count', 0),
                'category': item.get('category'),
                'source': 'google_maps'
            }
    
    print(f'Found {len(rating_map)} companies with ratings in JSON')
    
    # Get all companies
    result = db.client.table('companies').select('id, name, metadata').execute()
    print(f'Found {len(result.data)} companies in database')
    
    updated = 0
    for company in result.data:
        current_meta = company.get('metadata') or {}
        if not current_meta.get('rating'):
            # Try to match
            key = normalize_name(company['name'])
            rating_info = rating_map.get(key)
            
            if rating_info:
                new_meta = {**current_meta, **rating_info}
                db.client.table('companies').update({
                    'metadata': new_meta
                }).eq('id', company['id']).execute()
                updated += 1
                print(f'  Updated: {company["name"][:40]} -> {rating_info["rating"]} stars')
    
    print(f'\nUpdated {updated} companies with ratings')

if __name__ == '__main__':
    main()
