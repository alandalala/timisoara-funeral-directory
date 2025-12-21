"""Debug: Check why Jilava businesses are filtered."""
from tools.maps_scraper import MapsBusinessData
import unicodedata

# Test business similar to what we'd get from scraping
biz = MapsBusinessData(
    name='Poarta Raiului - Servicii Funerare Complete - Cimitirul Mierlari Jilava',
    address='DJ401 210A, Jilava 077120',
    city='Jilava',
    county='Ilfov'
)

print(f"Business: {biz.name}")
print(f"Address: {biz.address}")
print(f"City: {biz.city}")
print(f"County: {biz.county}")
print()

def normalize(s):
    n = unicodedata.normalize('NFD', s)
    return ''.join(c for c in n if unicodedata.category(c) != 'Mn').lower()

city = 'București'
county = 'București'

print(f"Searching for city='{city}', county='{county}'")
print()
print(f"Normalized address: '{normalize(biz.address)}'")
print(f"'bucuresti' in address: {'bucuresti' in normalize(biz.address)}")
print(f"'bucuresti' == city field: {normalize(biz.city) == 'bucuresti' if biz.city else False}")
print(f"'bucuresti' == county field: {normalize(biz.county) == 'bucuresti' if biz.county else False}")
print()

# This is why it's filtered - Jilava is in Ilfov county, not București
print("CONCLUSION:")
print("- Jilava is technically in Ilfov county, not București")
print("- The filtering is correct but may be too strict for border businesses")
print("- Options: 1) Include Ilfov in București scrape, or 2) Relax filtering for known București suburbs")
