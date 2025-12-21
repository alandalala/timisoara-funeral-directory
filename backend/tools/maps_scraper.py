"""
Google Maps Scraper - Extracts funeral company data from Google Maps.
Uses Playwright for browser automation. Free, no API costs.
"""
import json
import re
import time
import logging
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright, Page, Browser, TimeoutError as PlaywrightTimeout

logger = logging.getLogger(__name__)

# Keywords that indicate a legitimate funeral business
FUNERAL_KEYWORDS = [
    'funerar', 'funerare', 'funebre', 'funeral',
    'pompe funebre', 'casa funerară', 'casa funerara',
    'înmormântare', 'inmormantare', 'înhumare',
    'deces', 'decedat',
    'capelă', 'capela', 'priveghi',
    'sicri', 'sicriu',
]

# Keywords that indicate NON-funeral businesses (excluded unless has funeral keyword)
EXCLUDED_KEYWORDS = [
    # Flower shops
    'florărie', 'florarie', 'florar', 'flori ', 'floré', 'flore ',
    # Cemeteries (not service providers)
    'cimitir', 'cimitirul',
    # Monument/stone sellers
    'monument', 'monumente', 'pietr', 'marmur', 'granit',
    # Vending machines
    'automat de', 'self-service', 'self service',
    # Generic unrelated
    'speed', 'transport marfa',
]

# Categories from Google Maps that are NOT funeral services
EXCLUDED_CATEGORIES = [
    'florist', 'florărie', 'flower',
    'cemetery', 'cimitir',
    'stone', 'marble', 'granite', 'monument',
]


# Keywords that ALWAYS exclude a business (even if funeral keywords present)
ALWAYS_EXCLUDE_KEYWORDS = [
    'monument', 'monumente', 'pietr', 'marmur', 'granit',
]


def is_funeral_business(name: str, category: str = None) -> bool:
    """
    Check if a business is a legitimate funeral service provider.
    
    Logic:
    1. ALWAYS exclude monument/stone sellers (even if they have 'funerare' in name)
    2. Include if category contains funeral keywords (e.g., flower shop with 'pompe funebre' category)
    3. Include if name contains funeral keywords
    4. Exclude if name has excluded keywords (florist, cemetery, etc.)
    
    Args:
        name: Business name
        category: Google Maps category (optional)
        
    Returns:
        True if likely a funeral business, False otherwise
    """
    name_lower = name.lower()
    category_lower = (category or '').lower()
    
    # FIRST: Always exclude monument/stone sellers - they are NOT funeral service providers
    for keyword in ALWAYS_EXCLUDE_KEYWORDS:
        if keyword in name_lower:
            logger.debug(f"Excluding '{name}' - monument/stone seller")
            return False
    
    # SECOND: Check if category indicates funeral service (trust Google's category)
    # This catches flower shops that ALSO do funerals (category will say 'pompe funebre')
    for keyword in FUNERAL_KEYWORDS:
        if keyword in category_lower:
            return True
    
    # THIRD: Check if name contains funeral keywords
    for keyword in FUNERAL_KEYWORDS:
        if keyword in name_lower:
            return True
    
    # FOURTH: Exclude if name has excluded keywords without funeral keywords
    for keyword in EXCLUDED_KEYWORDS:
        if keyword in name_lower:
            logger.debug(f"Excluding '{name}' - matched excluded keyword: {keyword}")
            return False
    
    # FIFTH: Is the category explicitly non-funeral?
    for cat in EXCLUDED_CATEGORIES:
        if cat in category_lower:
            logger.debug(f"Excluding '{name}' - matched excluded category: {cat}")
            return False
    
    # Default: Include (might be a funeral business with unusual name)
    return True


@dataclass
class MapsBusinessData:
    """Data extracted from Google Maps for a business."""
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    county: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    business_hours: Optional[Dict] = None
    is_non_stop: bool = False
    category: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    place_id: Optional[str] = None
    # Website-extracted data
    email: Optional[str] = None
    fiscal_code: Optional[str] = None
    description: Optional[str] = None
    services: List[str] = None
    
    def __post_init__(self):
        if self.services is None:
            self.services = []


class GoogleMapsScraper:
    """
    Scrapes business data from Google Maps search results.
    Extracts comprehensive info from business panels and optionally their websites.
    """
    
    def __init__(self, headless: bool = True, slow_mo: int = 100):
        """
        Initialize the scraper.
        
        Args:
            headless: Run browser in headless mode (no visible window)
            slow_mo: Slow down actions by this many ms (helps avoid detection)
        """
        self.headless = headless
        self.slow_mo = slow_mo
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.playwright = None
        
    def __enter__(self):
        self.start()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        
    def start(self):
        """Start the browser."""
        logger.info("Starting browser...")
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            slow_mo=self.slow_mo
        )
        self.page = self.browser.new_page(
            viewport={'width': 1920, 'height': 1080},
            locale='ro-RO'
        )
        # Set Romanian language preference
        self.page.set_extra_http_headers({
            'Accept-Language': 'ro-RO,ro;q=0.9,en;q=0.8'
        })
        logger.info("Browser started")
        
    def stop(self):
        """Stop the browser."""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        logger.info("Browser stopped")
    
    def _check_for_single_result(self) -> Optional[Dict]:
        """
        Check if Google Maps opened a single business panel directly.
        This happens when searching for a specific business name or
        when there's only one result in a small town.
        
        Returns:
            Basic info dict if single business found, None otherwise
        """
        try:
            # Check for business title in the detail panel (not in search results)
            # This selector matches the title when a business page is open directly
            title_selectors = [
                'h1.DUwDvf',  # Business name header
                'h1.fontHeadlineLarge',  # Alternative header
            ]
            
            for selector in title_selectors:
                try:
                    title_elem = self.page.locator(selector).first
                    if title_elem.is_visible(timeout=2000):
                        name = title_elem.text_content()
                        if name:
                            # Verify this is a single business view, not a list
                            # by checking if there's NO results feed
                            feed = self.page.locator('[role="feed"]')
                            if feed.count() == 0:
                                logger.info(f"Detected single business result: {name}")
                                return {'name': name.strip(), 'element': None, 'is_single_result': True}
                except:
                    continue
            
            return None
        except Exception as e:
            logger.debug(f"Single result check failed: {e}")
            return None
    
    def _handle_consent(self):
        """Handle Google cookie consent popup."""
        try:
            # Look for consent button (Romanian or English)
            consent_selectors = [
                'button:has-text("Acceptă tot")',
                'button:has-text("Accept all")',
                'button:has-text("Accept")',
                '[aria-label="Accept all"]',
                'form[action*="consent"] button',
            ]
            
            for selector in consent_selectors:
                try:
                    button = self.page.locator(selector).first
                    if button.is_visible(timeout=2000):
                        button.click()
                        logger.info("Accepted cookie consent")
                        time.sleep(1)
                        return True
                except:
                    continue
            return False
        except Exception as e:
            logger.debug(f"No consent popup or error: {e}")
            return False
    
    def search(self, query: str, location: str) -> List[MapsBusinessData]:
        """
        Search Google Maps and extract all business data.
        
        Args:
            query: Search term (e.g., "servicii funerare")
            location: Location (e.g., "Timișoara")
            
        Returns:
            List of MapsBusinessData objects
        """
        search_term = f"{query} {location}"
        url = f"https://www.google.com/maps/search/{search_term.replace(' ', '+')}"
        
        logger.info(f"Searching Google Maps: {search_term}")
        self.page.goto(url, wait_until='domcontentloaded', timeout=30000)
        
        # Handle consent popup
        self._handle_consent()
        
        # Wait for results to load (give Maps time to render)
        time.sleep(4)
        
        # Check if Google Maps opened a single business directly (no list)
        single_business = self._check_for_single_result()
        if single_business:
            logger.info("Google Maps showed single business directly")
            businesses = [single_business]
        else:
            # Scroll results to load all businesses
            businesses = self._scroll_and_collect_results()
        
        logger.info(f"Found {len(businesses)} businesses")
        
        # Extract detailed info for each business
        detailed_businesses = []
        for i, basic_info in enumerate(businesses):
            logger.info(f"Extracting details for [{i+1}/{len(businesses)}]: {basic_info.get('name', 'Unknown')}")
            try:
                detailed = self._extract_business_details(basic_info)
                if detailed:
                    detailed_businesses.append(detailed)
                time.sleep(1)  # Delay between extractions
            except Exception as e:
                logger.error(f"Error extracting details: {e}")
                continue
        
        return detailed_businesses
    
    def _scroll_and_collect_results(self) -> List[Dict]:
        """Scroll the results panel and collect all business cards."""
        businesses = []
        seen_names = set()
        skipped_count = 0
        
        # Find the scrollable results container
        results_selector = '[role="feed"]'
        
        try:
            self.page.wait_for_selector(results_selector, timeout=10000)
        except PlaywrightTimeout:
            logger.warning("Could not find results feed, trying alternative selectors")
            # Try alternative approach - look for business cards directly
            results_selector = '.Nv2PK'
        
        scroll_attempts = 0
        max_scrolls = 30  # Increased from 20
        no_new_count = 0
        last_height = 0
        
        while scroll_attempts < max_scrolls:
            # Get current business cards
            cards = self.page.locator('.Nv2PK').all()
            
            new_found = 0
            for card in cards:
                try:
                    name_elem = card.locator('.qBF1Pd').first
                    name = name_elem.text_content() if name_elem.count() > 0 else None
                    
                    if name and name not in seen_names:
                        seen_names.add(name)
                        
                        # Try to get category early for filtering
                        category = None
                        try:
                            category_elem = card.locator('.W4Efsd .W4Efsd span span').first
                            if category_elem.count() > 0:
                                category = category_elem.text_content()
                        except:
                            pass
                        
                        # Filter out non-funeral businesses
                        if not is_funeral_business(name, category):
                            skipped_count += 1
                            logger.info(f"  [SKIP] Not a funeral business: {name}")
                            continue
                        
                        new_found += 1
                        
                        # Extract basic info from card
                        basic_info = {'name': name, 'element': card, 'category': category}
                        
                        # Try to get rating
                        try:
                            rating_elem = card.locator('.MW4etd').first
                            if rating_elem.count() > 0:
                                rating_text = rating_elem.text_content()
                                basic_info['rating'] = float(rating_text.replace(',', '.'))
                        except:
                            pass
                        
                        businesses.append(basic_info)
                except Exception as e:
                    continue
            
            scroll_attempts += 1
            logger.info(f"Scroll {scroll_attempts}: Found {new_found} new funeral businesses (total: {len(businesses)}, skipped: {skipped_count})")
            
            if new_found == 0:
                no_new_count += 1
                if no_new_count >= 5:  # Increased from 3 - give more chances to load
                    # Check if we've hit the "end of results" marker
                    try:
                        end_marker = self.page.locator('span.HlvSq').first
                        if end_marker.count() > 0:
                            logger.info("Reached end of results")
                            break
                    except:
                        pass
                    # No new results after 5 scrolls and no end marker, we're done
                    break
            else:
                no_new_count = 0
            
            # Scroll down in the results panel - try multiple methods
            try:
                feed = self.page.locator(results_selector).first
                # Get current scroll position
                current_height = feed.evaluate('el => el.scrollTop')
                # Scroll by a larger amount
                feed.evaluate('el => el.scrollTop = el.scrollTop + 1000')
                # Also try scrolling to the last card to ensure it loads
                if len(cards) > 0:
                    try:
                        cards[-1].scroll_into_view_if_needed()
                    except:
                        pass
            except:
                # Alternative scroll method
                self.page.keyboard.press('End')
            
            # Wait longer for results to load (Google Maps can be slow)
            time.sleep(2.0)  # Increased from 1.5
        
        logger.info(f"Collection complete: {len(businesses)} funeral businesses, {skipped_count} non-funeral skipped")
        return businesses
    
    def _extract_business_details(self, basic_info: Dict) -> Optional[MapsBusinessData]:
        """Click on a business card and extract all details from the panel."""
        try:
            # Click the business card to open details panel (skip if single result - already open)
            is_single_result = basic_info.get('is_single_result', False)
            card = basic_info.get('element')
            if card and not is_single_result:
                card.click()
                time.sleep(2)
            
            # Wait for details panel to load
            self.page.wait_for_selector('[role="main"]', timeout=5000)
            
            data = MapsBusinessData(
                name=basic_info.get('name', 'Unknown'),
                rating=basic_info.get('rating'),
                category=basic_info.get('category')
            )
            
            # Extract from URL (contains coordinates)
            try:
                url = self.page.url
                coord_match = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', url)
                if coord_match:
                    data.latitude = float(coord_match.group(1))
                    data.longitude = float(coord_match.group(2))
                
                # Extract place ID
                place_match = re.search(r'place/[^/]+/([^/]+)', url)
                if place_match:
                    data.place_id = place_match.group(1)
            except:
                pass
            
            # Extract address
            try:
                address_button = self.page.locator('[data-item-id="address"] .Io6YTe').first
                if address_button.count() > 0:
                    full_address = address_button.text_content()
                    data.address = full_address
                    
                    # Parse city/county from address
                    self._parse_address(data, full_address)
            except:
                pass
            
            # Extract phone
            try:
                phone_button = self.page.locator('[data-item-id^="phone:"] .Io6YTe').first
                if phone_button.count() > 0:
                    data.phone = phone_button.text_content()
            except:
                pass
            
            # Extract website
            try:
                website_button = self.page.locator('[data-item-id="authority"] .Io6YTe').first
                if website_button.count() > 0:
                    data.website = website_button.text_content()
                    # Clean up website URL
                    if data.website and not data.website.startswith('http'):
                        data.website = 'https://' + data.website
            except:
                pass
            
            # Extract business hours
            try:
                hours_button = self.page.locator('[data-item-id="oh"] .Io6YTe').first
                if hours_button.count() > 0:
                    hours_text = hours_button.text_content()
                    if hours_text:
                        hours_lower = hours_text.lower()
                        # Check for non-stop indicators in Romanian and English
                        non_stop_indicators = [
                            'non-stop', 'nonstop', 'non stop',
                            '24 de ore', '24 ore', '24h', '24/7',
                            'deschis 24', 'open 24',
                            'deschis non', 'open non'
                        ]
                        if any(indicator in hours_lower for indicator in non_stop_indicators):
                            data.is_non_stop = True
                        data.business_hours = {'text': hours_text}
            except:
                pass
            
            # Also check for non-stop in other page elements (sometimes shown differently)
            if not data.is_non_stop:
                try:
                    page_text = self.page.locator('.fontBodyMedium').all_text_contents()
                    page_text_combined = ' '.join(page_text).lower()
                    non_stop_indicators = ['non-stop', 'nonstop', '24 de ore', '24/7', 'deschis 24']
                    if any(indicator in page_text_combined for indicator in non_stop_indicators):
                        data.is_non_stop = True
                except:
                    pass
            
            # Extract review count - try multiple selectors
            try:
                # Try the review count from the header area (shows as "X recenzii" or "X reviews")
                review_selectors = [
                    '[jsaction*="review"] span[aria-label*="recenzii"]',
                    '[jsaction*="review"] span[aria-label*="reviews"]',
                    'button[jsaction*="review"] span',
                    '.F7nice span[aria-label]',
                    'span[aria-label*="recenzii"]',
                    'span[aria-label*="reviews"]',
                ]
                
                for selector in review_selectors:
                    try:
                        reviews_elem = self.page.locator(selector).first
                        if reviews_elem.count() > 0:
                            # Try aria-label first
                            review_text = reviews_elem.get_attribute('aria-label')
                            if not review_text:
                                review_text = reviews_elem.text_content()
                            if review_text:
                                # Extract number from text like "123 de recenzii" or "(123)"
                                match = re.search(r'(\d[\d.,]*)', review_text.replace('.', '').replace(',', ''))
                                if match:
                                    data.review_count = int(match.group(1))
                                    break
                    except:
                        continue
                
                # Also try to get review count from the text near rating
                if not data.review_count:
                    try:
                        # Look for pattern like "4.5 (123)" near rating
                        rating_area = self.page.locator('.F7nice').first
                        if rating_area.count() > 0:
                            text = rating_area.text_content()
                            match = re.search(r'\((\d+)\)', text)
                            if match:
                                data.review_count = int(match.group(1))
                    except:
                        pass
            except:
                pass
            
            return data
            
        except Exception as e:
            logger.error(f"Error extracting business details: {e}")
            return MapsBusinessData(name=basic_info.get('name', 'Unknown'))
    
    def _parse_address(self, data: MapsBusinessData, full_address: str):
        """Parse Romanian address to extract city and county."""
        # Romanian address format often: "Street, Number, City, County PostalCode"
        # Or: "Street, Number, City PostalCode"
        
        # Common Timiș county cities
        timis_cities = ['timișoara', 'timisoara', 'lugoj', 'sânnicolau mare', 'jimbolia', 
                        'buziaș', 'făget', 'recaș', 'deta', 'gătaia']
        
        address_lower = full_address.lower()
        
        # Check for Timiș county indicators
        if 'timiș' in address_lower or 'timis' in address_lower:
            data.county = 'Timiș'
        
        # Check for city
        for city in timis_cities:
            if city in address_lower:
                data.city = city.title()
                data.county = 'Timiș'
                break
        
        # If still no city, try to extract from address parts
        if not data.city:
            parts = full_address.split(',')
            if len(parts) >= 3:
                # Street indicators that should NOT be in city names
                street_indicators = [
                    'str.', 'strada', 'calea', 'bulevardul', 'b-dul', 'bd.', 
                    'aleea', 'piața', 'piata', 'șoseaua', 'soseaua', 'intrarea',
                    'bloc', 'nr.', 'et.', 'ap.', 'sector'
                ]
                # Usually city is second-to-last or third-to-last
                for part in reversed(parts[:-1]):
                    part = part.strip()
                    part_lower = part.lower()
                    # Skip if it looks like a postal code
                    if re.match(r'^\d{5,6}$', part):
                        continue
                    # Skip if it contains street indicators (not a city name)
                    if any(indicator in part_lower for indicator in street_indicators):
                        continue
                    # Skip if it starts with a number (likely a street number or address)
                    if re.match(r'^\d', part):
                        continue
                    data.city = part
                    break
    
    def enrich_from_website(self, business: MapsBusinessData) -> MapsBusinessData:
        """
        Visit the business website and extract additional data.
        
        Args:
            business: Business data with website URL
            
        Returns:
            Enriched business data
        """
        if not business.website:
            return business
        
        try:
            logger.info(f"Enriching from website: {business.website}")
            
            # Navigate to website
            self.page.goto(business.website, wait_until='domcontentloaded', timeout=15000)
            time.sleep(2)
            
            # Get page content
            content = self.page.content()
            text_content = self.page.locator('body').text_content()
            
            # Extract email
            email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            emails = re.findall(email_pattern, content)
            excluded_emails = ['example.com', 'domain.com', 'email.com', 'wixpress.com', 'sentry.io']
            valid_emails = [e for e in emails if not any(ex in e.lower() for ex in excluded_emails)]
            if valid_emails:
                business.email = valid_emails[0]
            
            # Extract CUI/CIF (Romanian fiscal code)
            cui_patterns = [
                r'(?:CUI|CIF|C\.U\.I\.|C\.I\.F\.|Cod\s*(?:unic|fiscal))[:\s]*(?:RO)?(\d{6,10})',
                r'(?:RO)(\d{6,10})',
                r'(?:cod\s*identificare|inregistrare)[:\s]*(?:RO)?(\d{6,10})',
            ]
            for pattern in cui_patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    business.fiscal_code = match.group(1)
                    break
            
            # Extract meta description
            try:
                meta_desc = self.page.locator('meta[name="description"]').first
                if meta_desc.count() > 0:
                    business.description = meta_desc.get_attribute('content')
            except:
                pass
            
            # Extract services from common patterns
            services = self._extract_services(text_content)
            if services:
                business.services = services
            
            logger.info(f"  Found: email={business.email}, CUI={business.fiscal_code}, services={len(business.services)}")
            
        except Exception as e:
            logger.warning(f"Error enriching from website: {e}")
        
        return business
    
    def _extract_services(self, text: str) -> List[str]:
        """Extract funeral services from page text."""
        services = []
        
        # Common Romanian funeral service keywords
        service_keywords = [
            'transport funerar', 'transport decedat',
            'îmbălsămare', 'imbalsamare', 'tanatopraxie',
            'sicriu', 'sicrie', 'coșciug',
            'coroană', 'coroane', 'aranjamente florale', 'flori',
            'cruce', 'cruci', 'monument', 'monumente',
            'înmormântare', 'inmormantare', 'înhumare',
            'incinerare', 'crematoriu', 'cremație',
            'priveghi', 'capelă', 'capela',
            'servicii complete', 'pachet funerar',
            'acte deces', 'documente', 'formalități',
            'repatriere', 'transport internațional',
        ]
        
        text_lower = text.lower()
        for keyword in service_keywords:
            if keyword in text_lower:
                # Capitalize properly
                service = keyword.replace('ă', 'a').replace('â', 'a').replace('î', 'i').replace('ș', 's').replace('ț', 't')
                service = keyword.title()
                if service not in services:
                    services.append(service)
        
        return services[:15]  # Limit to 15 services
    
    def search_and_enrich(self, query: str, location: str, enrich_websites: bool = True) -> List[MapsBusinessData]:
        """
        Complete pipeline: search Maps, extract details, optionally enrich from websites.
        
        Args:
            query: Search term
            location: Location name
            enrich_websites: Whether to visit websites for extra data
            
        Returns:
            List of fully enriched business data
        """
        # Search and get basic + Maps details
        businesses = self.search(query, location)
        
        if enrich_websites:
            logger.info(f"\nEnriching {len(businesses)} businesses from their websites...")
            for i, business in enumerate(businesses):
                if business.website:
                    logger.info(f"[{i+1}/{len(businesses)}] Enriching: {business.name}")
                    self.enrich_from_website(business)
                    time.sleep(2)  # Delay between website visits
        
        return businesses
    
    def save_to_json(self, businesses: List[MapsBusinessData], filepath: str):
        """Save scraped data to JSON file."""
        data = [asdict(b) for b in businesses]
        # Remove 'element' field which isn't serializable
        for d in data:
            d.pop('element', None)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Saved {len(businesses)} businesses to {filepath}")


def scrape_city(city: str, query: str = "servicii funerare", headless: bool = True, 
                enrich: bool = True, output_file: str = None) -> List[MapsBusinessData]:
    """
    Convenience function to scrape funeral companies in a city.
    
    Args:
        city: City name (e.g., "Timișoara")
        query: Search term
        headless: Run headless
        enrich: Enrich from websites
        output_file: Optional JSON output file
        
    Returns:
        List of business data
    """
    with GoogleMapsScraper(headless=headless) as scraper:
        businesses = scraper.search_and_enrich(query, city, enrich_websites=enrich)
        
        if output_file:
            scraper.save_to_json(businesses, output_file)
        
        return businesses


if __name__ == "__main__":
    import argparse
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    parser = argparse.ArgumentParser(description='Scrape Google Maps for funeral companies')
    parser.add_argument('--city', type=str, default='Timișoara', help='City to search')
    parser.add_argument('--query', type=str, default='servicii funerare', help='Search query')
    parser.add_argument('--output', type=str, default='maps_results.json', help='Output JSON file')
    parser.add_argument('--no-headless', action='store_true', help='Show browser window')
    parser.add_argument('--no-enrich', action='store_true', help='Skip website enrichment')
    
    args = parser.parse_args()
    
    print(f"\n{'='*60}")
    print(f"Google Maps Scraper")
    print(f"{'='*60}")
    print(f"City: {args.city}")
    print(f"Query: {args.query}")
    print(f"Output: {args.output}")
    print(f"Headless: {not args.no_headless}")
    print(f"Enrich from websites: {not args.no_enrich}")
    print(f"{'='*60}\n")
    
    businesses = scrape_city(
        city=args.city,
        query=args.query,
        headless=not args.no_headless,
        enrich=not args.no_enrich,
        output_file=args.output
    )
    
    print(f"\n{'='*60}")
    print(f"RESULTS: Found {len(businesses)} businesses")
    print(f"{'='*60}")
    
    for b in businesses:
        print(f"\n{b.name}")
        print(f"  Address: {b.address}")
        print(f"  Phone: {b.phone}")
        print(f"  Website: {b.website}")
        print(f"  Email: {b.email}")
        print(f"  CUI: {b.fiscal_code}")
        print(f"  Rating: {b.rating} ({b.review_count} reviews)")
