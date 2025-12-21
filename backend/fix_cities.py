"""Fix bad city data in the database."""
from tools.supabase_tool import SupabaseTool
import re

tool = SupabaseTool()
result = tool.client.table('locations').select('id, city, address').execute()

# Find records with numbers in city (bad data)
bad = [r for r in result.data if r['city'] and any(c.isdigit() for c in r['city'])]

print(f"Found {len(bad)} cities with numbers (likely bad data)")

def extract_city(address):
    """Extract correct city from address - usually before postal code."""
    if not address:
        return None
    # Pattern: City PostalCode at end, like 'Craiova 200142' or 'Galați 800402'
    match = re.search(r',\s*([A-Za-zăâîșțĂÂÎȘȚ\s\-]+)\s+\d{6}', address)
    if match:
        return match.group(1).strip()
    # Try pattern without comma
    match = re.search(r'([A-Za-zăâîșțĂÂÎȘȚ\s\-]+)\s+\d{6}', address)
    if match:
        city = match.group(1).strip()
        # Skip if it looks like a street
        if not any(x in city.lower() for x in ['strada', 'bulevardul', 'calea', 'str.']):
            return city
    return None

fixed = 0
failed = []
for r in bad:
    correct_city = extract_city(r['address'])
    if correct_city:
        print(f"Fixing: '{r['city']}' -> '{correct_city}'")
        tool.client.table('locations').update({'city': correct_city}).eq('id', r['id']).execute()
        fixed += 1
    else:
        failed.append(r)
        print(f"Could not auto-fix: {r['city']}")

print(f"\nFixed {fixed} of {len(bad)} records")

if failed:
    print("\nRecords that need manual review:")
    for r in failed:
        print(f"  ID: {r['id']}")
        print(f"    City: {r['city']}")
        print(f"    Address: {r['address']}")
        print()
