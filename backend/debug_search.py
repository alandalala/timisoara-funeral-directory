"""Debug search engines"""
import requests
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

query = "servicii funerare timisoara"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'ro-RO,ro;q=0.9,en;q=0.8',
}

# Test Bing
print("=== Testing Bing ===")
url = f"https://www.bing.com/search?q={quote_plus(query)}"
response = requests.get(url, headers=headers, timeout=30)
print(f"Status: {response.status_code}")
print(f"Content length: {len(response.text)}")

soup = BeautifulSoup(response.text, 'html.parser')

# Check what classes we can find
print("\nLooking for result containers...")
for cls in ['b_algo', 'b_results', 'b_content']:
    found = soup.find_all(class_=cls)
    print(f"  Class '{cls}': {len(found)} found")

# Try to find any links
print("\nAll links with .ro domain:")
for link in soup.find_all('a', href=True):
    href = link.get('href', '')
    if '.ro' in href and href.startswith('http'):
        print(f"  {href[:100]}")

# Save HTML for inspection
with open('debug_bing.html', 'w', encoding='utf-8') as f:
    f.write(response.text)
print("\nSaved HTML to debug_bing.html")
