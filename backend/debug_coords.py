"""Debug: Find coordinates in Google Maps panel HTML."""
from playwright.sync_api import sync_playwright
import time
import re
import json

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    # Navigate to search results first (like the scraper does)
    page.goto('https://www.google.com/maps/search/servicii+funerare/@44.4268,26.1025,14z')
    time.sleep(3)
    
    # Handle consent
    try:
        accept_btn = page.locator('button[aria-label*="Acceptă"]').first
        if accept_btn.count() > 0:
            accept_btn.click()
            print("Accepted consent")
            time.sleep(3)
    except:
        pass
    
    # Click first business card
    cards = page.locator('.Nv2PK').all()
    if cards:
        name_elem = cards[0].locator('.qBF1Pd').first
        name = name_elem.text_content() if name_elem.count() > 0 else 'Unknown'
        print(f"\nClicking on: {name}")
        
        cards[0].click()
        time.sleep(3)  # Wait for panel to fully load
        
        print(f"\nSearching for coordinates in page content...")
        
        # Get page content
        html = page.content()
        
        # Look for lat/lng patterns in page source
        # Google embeds data in various JSON-like formats
        patterns = [
            r'\[(-?44\.\d{4,}),\s*(-?26\.\d{4,})\]',  # Array format in București area
            r'"lat":\s*(-?44\.\d+).*?"lng":\s*(-?26\.\d+)',  # Object format
            r'@(-?44\.\d+),(-?26\.\d+)',  # URL format
        ]
        
        all_coords = []
        for pattern in patterns:
            matches = re.findall(pattern, html)
            for match in matches:
                lat, lng = float(match[0]), float(match[1])
                if (44.3 < lat < 44.6) and (25.9 < lng < 26.4):  # București bounds
                    all_coords.append((lat, lng))
        
        # Remove duplicates and sort
        unique_coords = list(set(all_coords))
        print(f"\nFound {len(unique_coords)} unique coordinate pairs in București area:")
        for lat, lng in sorted(unique_coords)[:10]:
            print(f"  ({lat}, {lng})")
        
        # Also check the address element location
        print("\n=== Check visible elements ===")
        addr_elem = page.locator('[data-item-id="address"] .Io6YTe').first
        if addr_elem.count() > 0:
            addr = addr_elem.text_content()
            print(f"Address: {addr}")
        
        # The business title
        title = page.locator('h1.DUwDvf').first
        if title.count() > 0:
            print(f"Title: {title.text_content()}")
    
    browser.close()
