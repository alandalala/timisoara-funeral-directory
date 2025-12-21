"""Debug: Find the actual Directions button selector."""
from tools.maps_scraper import GoogleMapsScraper
import time

output = []

def log(msg):
    print(msg)
    output.append(msg)

scraper = GoogleMapsScraper(headless=False)
scraper.start()

# Navigate to a specific business
scraper.page.goto('https://www.google.com/maps/search/servicii+funerare/@44.4268,26.1025,14z')
time.sleep(4)

# Click first result
cards = scraper.page.locator('.Nv2PK').all()
if cards:
    cards[0].click()
    time.sleep(3)
    
    log("=== Looking for Directions button ===")
    
    # Try various selectors
    selectors_to_try = [
        'a[data-value="Directions"]',
        'a[href*="/dir//"]',
        'a[href*="dir"]',
        'button[data-item-id="directions"]',
        '[data-item-id="directions"]',
        'a[aria-label*="Directions"]',
        'a[aria-label*="Indicații"]',  # Romanian
        'button[aria-label*="Directions"]',
        'button[aria-label*="Indicații"]',
    ]
    
    for sel in selectors_to_try:
        try:
            elem = scraper.page.locator(sel).first
            if elem.count() > 0:
                href = elem.get_attribute('href')
                aria = elem.get_attribute('aria-label')
                log(f"✅ FOUND: {sel}")
                log(f"   href: {href}")
                log(f"   aria-label: {aria}")
            else:
                log(f"❌ Not found: {sel}")
        except Exception as e:
            log(f"❌ Error for {sel}: {e}")
    
    # Also look at all links with href containing 'dir'
    log("\n=== All links with 'dir' in href ===")
    all_links = scraper.page.locator('a[href]').all()
    for link in all_links[:30]:
        try:
            href = link.get_attribute('href')
            if href and 'dir' in href.lower():
                log(f"  {href[:150]}...")
        except:
            pass

scraper.stop()

# Write to file
with open('debug_output.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))
