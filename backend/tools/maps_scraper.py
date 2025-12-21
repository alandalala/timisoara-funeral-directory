"""
Google Maps Scraper - Extracts funeral company data from Google Maps.
Uses Playwright for browser automation. Free, no API costs.
"""
import json
import re
import time
import logging
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from urllib.parse import urlparse, quote

from playwright.sync_api import sync_playwright, Page, Browser, TimeoutError as PlaywrightTimeout

# Import geocoding for coordinate fallback
try:
    from tools.geocoding import GeocodingTool
    GEOCODING_AVAILABLE = True
except ImportError:
    GEOCODING_AVAILABLE = False

logger = logging.getLogger(__name__)

# City coordinates for geo-locked Google Maps searches
# Using @lat,lng,zoom format locks the map viewport to prevent wrong-city results
CITY_COORDINATES = {
    # București
    'bucurești': {'lat': 44.4268, 'lng': 26.1025, 'zoom': 12},
    'bucharest': {'lat': 44.4268, 'lng': 26.1025, 'zoom': 12},
    'bucuresti': {'lat': 44.4268, 'lng': 26.1025, 'zoom': 12},
    # Major cities
    'timișoara': {'lat': 45.7489, 'lng': 21.2087, 'zoom': 13},
    'timisoara': {'lat': 45.7489, 'lng': 21.2087, 'zoom': 13},
    'cluj-napoca': {'lat': 46.7712, 'lng': 23.6236, 'zoom': 13},
    'cluj': {'lat': 46.7712, 'lng': 23.6236, 'zoom': 13},
    'iași': {'lat': 47.1585, 'lng': 27.6014, 'zoom': 13},
    'iasi': {'lat': 47.1585, 'lng': 27.6014, 'zoom': 13},
    'constanța': {'lat': 44.1598, 'lng': 28.6348, 'zoom': 13},
    'constanta': {'lat': 44.1598, 'lng': 28.6348, 'zoom': 13},
    'craiova': {'lat': 44.3302, 'lng': 23.7949, 'zoom': 13},
    'brașov': {'lat': 45.6427, 'lng': 25.5887, 'zoom': 13},
    'brasov': {'lat': 45.6427, 'lng': 25.5887, 'zoom': 13},
    'galați': {'lat': 45.4353, 'lng': 28.0080, 'zoom': 13},
    'galati': {'lat': 45.4353, 'lng': 28.0080, 'zoom': 13},
    'ploiești': {'lat': 44.9365, 'lng': 26.0254, 'zoom': 13},
    'ploiesti': {'lat': 44.9365, 'lng': 26.0254, 'zoom': 13},
    'oradea': {'lat': 47.0722, 'lng': 21.9217, 'zoom': 13},
    'brăila': {'lat': 45.2692, 'lng': 27.9575, 'zoom': 13},
    'braila': {'lat': 45.2692, 'lng': 27.9575, 'zoom': 13},
    'arad': {'lat': 46.1866, 'lng': 21.3123, 'zoom': 13},
    'pitești': {'lat': 44.8565, 'lng': 24.8692, 'zoom': 13},
    'pitesti': {'lat': 44.8565, 'lng': 24.8692, 'zoom': 13},
    'sibiu': {'lat': 45.7983, 'lng': 24.1256, 'zoom': 13},
    'bacău': {'lat': 46.5670, 'lng': 26.9146, 'zoom': 13},
    'bacau': {'lat': 46.5670, 'lng': 26.9146, 'zoom': 13},
    'târgu mureș': {'lat': 46.5386, 'lng': 24.5579, 'zoom': 13},
    'targu mures': {'lat': 46.5386, 'lng': 24.5579, 'zoom': 13},
    'baia mare': {'lat': 47.6567, 'lng': 23.5850, 'zoom': 13},
    'buzău': {'lat': 45.1500, 'lng': 26.8333, 'zoom': 13},
    'buzau': {'lat': 45.1500, 'lng': 26.8333, 'zoom': 13},
    'botoșani': {'lat': 47.7487, 'lng': 26.6694, 'zoom': 13},
    'botosani': {'lat': 47.7487, 'lng': 26.6694, 'zoom': 13},
    'satu mare': {'lat': 47.7926, 'lng': 22.8859, 'zoom': 13},
    'râmnicu vâlcea': {'lat': 45.0997, 'lng': 24.3693, 'zoom': 13},
    'ramnicu valcea': {'lat': 45.0997, 'lng': 24.3693, 'zoom': 13},
    'suceava': {'lat': 47.6635, 'lng': 26.2732, 'zoom': 13},
    'piatra neamț': {'lat': 46.9275, 'lng': 26.3708, 'zoom': 13},
    'piatra neamt': {'lat': 46.9275, 'lng': 26.3708, 'zoom': 13},
    'drobeta-turnu severin': {'lat': 44.6269, 'lng': 22.6566, 'zoom': 13},
    'târgu jiu': {'lat': 45.0378, 'lng': 23.2743, 'zoom': 13},
    'targu jiu': {'lat': 45.0378, 'lng': 23.2743, 'zoom': 13},
    'târgoviște': {'lat': 44.9254, 'lng': 25.4567, 'zoom': 13},
    'targoviste': {'lat': 44.9254, 'lng': 25.4567, 'zoom': 13},
    'focșani': {'lat': 45.6947, 'lng': 27.1858, 'zoom': 13},
    'focsani': {'lat': 45.6947, 'lng': 27.1858, 'zoom': 13},
    'bistrița': {'lat': 47.1325, 'lng': 24.5008, 'zoom': 13},
    'bistrita': {'lat': 47.1325, 'lng': 24.5008, 'zoom': 13},
    'reșița': {'lat': 45.3008, 'lng': 21.8893, 'zoom': 13},
    'resita': {'lat': 45.3008, 'lng': 21.8893, 'zoom': 13},
    'tulcea': {'lat': 45.1780, 'lng': 28.8003, 'zoom': 13},
    'călărași': {'lat': 44.2048, 'lng': 27.3331, 'zoom': 13},
    'calarasi': {'lat': 44.2048, 'lng': 27.3331, 'zoom': 13},
    'hunedoara': {'lat': 45.7500, 'lng': 22.9000, 'zoom': 13},
    'deva': {'lat': 45.8833, 'lng': 22.9000, 'zoom': 13},
    'alba iulia': {'lat': 46.0667, 'lng': 23.5833, 'zoom': 13},
    'giurgiu': {'lat': 43.9037, 'lng': 25.9699, 'zoom': 13},
    'slobozia': {'lat': 44.5644, 'lng': 27.3664, 'zoom': 13},
    'vaslui': {'lat': 46.6407, 'lng': 27.7276, 'zoom': 13},
    'alexandria': {'lat': 43.9710, 'lng': 25.3316, 'zoom': 13},
    'zalău': {'lat': 47.1918, 'lng': 23.0635, 'zoom': 13},
    'zalau': {'lat': 47.1918, 'lng': 23.0635, 'zoom': 13},
    'sfântu gheorghe': {'lat': 45.8667, 'lng': 25.7833, 'zoom': 13},
    'sfantu gheorghe': {'lat': 45.8667, 'lng': 25.7833, 'zoom': 13},
    'miercurea ciuc': {'lat': 46.3597, 'lng': 25.8042, 'zoom': 13},
    'slatina': {'lat': 44.4304, 'lng': 24.3630, 'zoom': 13},
    'mediaș': {'lat': 46.1667, 'lng': 24.3500, 'zoom': 14},
    'medias': {'lat': 46.1667, 'lng': 24.3500, 'zoom': 14},
}

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


def normalize_name(name: str) -> str:
    """
    Normalize a business name for deduplication.
    Strips emojis, extra whitespace, normalizes case, removes common variations.
    
    Args:
        name: Original business name
        
    Returns:
        Normalized name for comparison
    """
    import unicodedata
    
    if not name:
        return ""
    
    # Convert to lowercase
    normalized = name.lower().strip()
    
    # Remove emojis and special symbols (keep Romanian diacritics)
    # This regex removes emoji ranges while preserving letters/numbers
    normalized = re.sub(r'[\U0001F300-\U0001F9FF\U00002600-\U000027BF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF]', '', normalized)
    
    # Normalize Romanian diacritics (ă->a, â->a, î->i, ș->s, ț->t)
    diacritic_map = {
        'ă': 'a', 'â': 'a', 'î': 'i', 'ș': 's', 'ț': 't',
        'Ă': 'a', 'Â': 'a', 'Î': 'i', 'Ș': 's', 'Ț': 't',
        'ş': 's', 'ţ': 't',  # Old-style diacritics
    }
    for diac, repl in diacritic_map.items():
        normalized = normalized.replace(diac, repl)
    
    # Remove common suffixes/prefixes that vary
    normalized = re.sub(r'\b(srl|s\.r\.l|s\.r\.l\.|sa|s\.a|s\.a\.)\b', '', normalized)
    
    # Normalize whitespace (multiple spaces to single)
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    
    # Remove punctuation except spaces
    normalized = re.sub(r'[^\w\s]', '', normalized)
    
    return normalized.strip()


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
    # Coordinate quality: 'exact' (street number), 'approximate' (street only), 'none' (failed)
    coord_quality: Optional[str] = None
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
    
    def __init__(self, headless: bool = True, slow_mo: int = 100, geocode: bool = True):
        """
        Initialize the scraper.
        
        Args:
            headless: Run browser in headless mode (no visible window)
            slow_mo: Slow down actions by this many ms (helps avoid detection)
            geocode: If True, geocode addresses during extraction (slow but accurate).
                     If False, skip geocoding for speed - run batch geocoding later.
        """
        self.headless = headless
        self.slow_mo = slow_mo
        self.geocode = geocode
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
    
    def search(self, query: str, location: str, skip_names: set = None, max_results: int = None) -> List[MapsBusinessData]:
        """
        Search Google Maps and extract all business data.
        Uses coordinate-locked URLs to prevent wrong-city results.
        
        Args:
            query: Search term (e.g., "servicii funerare")
            location: Location (e.g., "Timișoara")
            skip_names: Set of normalized business names to skip (already scraped in previous searches)
            max_results: Maximum number of businesses to extract (None = use city-based defaults)
            
        Returns:
            List of MapsBusinessData objects
        """
        if skip_names is None:
            skip_names = set()
            
        # Extract city name from location (e.g., "București, București" -> "bucurești")
        city_name = location.split(',')[0].strip().lower()
        
        # Get coordinates for this city
        coords = CITY_COORDINATES.get(city_name)
        
        if coords:
            # Use coordinate-locked URL - this prevents Google from showing results from other cities
            search_term = quote(query)
            url = f"https://www.google.com/maps/search/{search_term}/@{coords['lat']},{coords['lng']},{coords['zoom']}z"
            logger.info(f"Searching Google Maps (geo-locked): {query} in {city_name} @ {coords['lat']},{coords['lng']}")
        else:
            # Fallback to text search if city not in coordinates database
            search_term = f"{query} {location}"
            url = f"https://www.google.com/maps/search/{search_term.replace(' ', '+')}"
            logger.warning(f"City '{city_name}' not in coordinates database, using text search: {search_term}")
        
        self.page.goto(url, wait_until='domcontentloaded', timeout=30000)
        
        # Handle consent popup
        self._handle_consent()
        
        # Wait for results to load (give Maps time to render)
        time.sleep(2.0)  # Reduced from 4s
        
        # Check if Google Maps opened a single business directly (no list)
        single_business = self._check_for_single_result()
        if single_business:
            logger.info("Google Maps showed single business directly")
            businesses = [single_business]
        else:
            # Scroll results to load all businesses
            # Use provided max_results, or city-based default
            if max_results is None:
                # București (2M+ population) needs higher limit than other cities
                scroll_limit = 150 if 'bucuresti' in location.lower() or 'bucurești' in location.lower() else 50
            else:
                scroll_limit = max_results
            businesses = self._scroll_and_collect_results(max_results=scroll_limit)
        
        logger.info(f"Found {len(businesses)} businesses")
        
        # Major Romanian city names and neighborhoods for early filtering
        # If searching in one city but business name/card mentions another, likely wrong location
        MAJOR_CITIES = [
            'timișoara', 'timisoara', 'cluj', 'iași', 'iasi', 'constanța', 'constanta',
            'craiova', 'brașov', 'brasov', 'galați', 'galati', 'ploiești', 'ploiesti',
            'oradea', 'brăila', 'braila', 'arad', 'pitești', 'pitesti', 'sibiu',
            'bacău', 'bacau', 'târgu mureș', 'targu mures', 'baia mare', 'buzău', 'buzau',
            'botoșani', 'botosani', 'satu mare', 'suceava', 'piatra neamț', 'piatra neamt',
            'drobeta', 'focșani', 'focsani', 'tulcea', 'hunedoara', 'deva', 'alba iulia',
            'vaslui', 'giurgiu', 'slobozia', 'călărași', 'calarasi', 'alexandria',
            'mehala',  # Timișoara neighborhood
        ]
        
        # County-to-city mapping for address-based filtering
        # If we see "Timiș" county in address but searching in București, skip it
        COUNTY_INDICATORS = {
            'timiș': 'timișoara', 'timis': 'timișoara',
            'cluj': 'cluj',
            'iași': 'iași', 'iasi': 'iași',
            'brașov': 'brașov', 'brasov': 'brașov',
            'sibiu': 'sibiu',
            'constanța': 'constanța', 'constanta': 'constanța',
            'bihor': 'oradea',
            'arad': 'arad',
            'dolj': 'craiova',
            'prahova': 'ploiești',
            'galați': 'galați', 'galati': 'galați',
            'argeș': 'pitești', 'arges': 'pitești',
            'bacău': 'bacău', 'bacau': 'bacău',
            'mureș': 'târgu mureș', 'mures': 'târgu mureș',
            'maramureș': 'baia mare', 'maramures': 'baia mare',
            'suceava': 'suceava',
            'neamț': 'piatra neamț', 'neamt': 'piatra neamț',
            'hunedoara': 'hunedoara',
            'alba': 'alba iulia',
        }
        
        # Extract target city from query for filtering
        query_lower = query.lower()
        location_lower = location.lower()
        
        def is_city_match(city_name: str, text: str) -> bool:
            """
            Check if city_name appears as a standalone word in text.
            Avoids false positives like 'giurgiului' (street) matching 'giurgiu' (city).
            
            Romanian street names often use genitive forms:
            - Giurgiu → Giurgiului (Șoseaua Giurgiului)
            - Timișoara → Timișoarei
            - Craiova → Craiovei
            """
            # Use word boundary regex to match whole words only
            # \b doesn't work well with Romanian chars, so we check manually
            import re
            # Match city_name only if it's:
            # - at start/end of string, OR
            # - surrounded by non-letter characters (space, comma, etc.)
            # This excludes "giurgiului", "timișoarei" etc.
            pattern = r'(?<![a-zA-ZăâîșțĂÂÎȘȚ])' + re.escape(city_name) + r'(?![a-zA-ZăâîșțĂÂÎȘȚ])'
            return bool(re.search(pattern, text, re.IGNORECASE))
        
        # Extract detailed info for each business, with early filtering
        detailed_businesses = []
        for i, basic_info in enumerate(businesses):
            name = basic_info.get('name', 'Unknown')
            name_lower = name.lower()
            card_snippet = basic_info.get('card_snippet', '').lower()
            
            # Early filter: skip if name mentions a different major city
            skip_reason = None
            for city_name in MAJOR_CITIES:
                if is_city_match(city_name, name_lower):
                    # Check if this city is in our search location
                    if not is_city_match(city_name, location_lower) and not is_city_match(city_name, query_lower):
                        skip_reason = f"name mentions {city_name}"
                        break
            
            # Also check card snippet (contains address info visible in search results)
            if not skip_reason and card_snippet:
                # Check for city names in snippet
                for city_name in MAJOR_CITIES:
                    if is_city_match(city_name, card_snippet):
                        if not is_city_match(city_name, location_lower) and not is_city_match(city_name, query_lower):
                            skip_reason = f"card shows {city_name}"
                            break
                
                # Check for county indicators
                if not skip_reason:
                    for county, city in COUNTY_INDICATORS.items():
                        if is_city_match(county, card_snippet):
                            if not is_city_match(city, location_lower) and not is_city_match(city, query_lower):
                                skip_reason = f"card shows {county} county"
                                break
            
            if skip_reason:
                logger.info(f"  [SKIP] Wrong location ({skip_reason}): {name}")
                continue
            
            # Skip businesses already seen in previous searches (saves extraction time)
            normalized_name = normalize_name(name)
            if normalized_name in skip_names:
                logger.info(f"  [SKIP] Already scraped: {name}")
                continue
            
            logger.info(f"Extracting details for [{i+1}/{len(businesses)}]: {name}")
            try:
                detailed = self._extract_business_details(basic_info)
                if detailed:
                    detailed_businesses.append(detailed)
                time.sleep(0.3)  # Reduced from 1s - fast mode
            except Exception as e:
                logger.error(f"Error extracting details: {e}")
                continue
        
        return detailed_businesses
    
    def _scroll_and_collect_results(self, max_results: int = 50) -> List[Dict]:
        """Scroll the results panel and collect all business cards.
        
        Args:
            max_results: Maximum number of businesses to collect per search query.
                        Google Maps loads businesses beyond the visible map area,
                        so we cap results to avoid collecting irrelevant businesses.
        """
        businesses = []
        seen_names = set()
        skipped_count = 0
        
        # Recovery file to save progress during collection (prevents total data loss)
        recovery_file = Path(__file__).parent.parent / "data" / "scrape_recovery.json"
        
        def save_recovery():
            """Save collected names for recovery if scrape fails."""
            try:
                recovery_data = {
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'collected_count': len(businesses),
                    'names': [b.get('name', 'Unknown') for b in businesses]
                }
                with open(recovery_file, 'w', encoding='utf-8') as f:
                    json.dump(recovery_data, f, ensure_ascii=False, indent=2)
            except Exception as e:
                logger.debug(f"Could not save recovery file: {e}")
        
        # Find the scrollable results container
        results_selector = '[role="feed"]'
        
        try:
            self.page.wait_for_selector(results_selector, timeout=10000)
        except PlaywrightTimeout:
            logger.warning("Could not find results feed, trying alternative selectors")
            # Try alternative approach - look for business cards directly
            results_selector = '.Nv2PK'
        
        scroll_attempts = 0
        max_scrolls = 30  # Reduced - Google loads results from wider area as you scroll
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
                        
                        # Try to get category and card snippet (contains address info) early for filtering
                        category = None
                        card_snippet = ""
                        try:
                            # Get all text from the card info area (contains category, address, etc.)
                            info_elems = card.locator('.W4Efsd').all()
                            for info_elem in info_elems:
                                try:
                                    text = info_elem.text_content()
                                    if text:
                                        card_snippet += " " + text
                                except:
                                    pass
                            
                            # Get category specifically
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
                        basic_info = {'name': name, 'element': card, 'category': category, 'card_snippet': card_snippet}
                        
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
            
            # Save recovery after each scroll (prevents total data loss)
            if len(businesses) > 0 and scroll_attempts % 3 == 0:  # Every 3 scrolls
                save_recovery()
            
            # Stop if we've collected enough results - Google loads businesses from wider areas as you scroll
            if len(businesses) >= max_results:
                logger.info(f"Reached max results limit ({max_results}). Stopping collection.")
                save_recovery()  # Final save before exit
                break
            
            if new_found == 0:
                no_new_count += 1
                if no_new_count >= 2:  # Stop after 2 consecutive scrolls with 0 new results
                    logger.info(f"No new results for {no_new_count} consecutive scrolls. Reached end of results")
                    save_recovery()  # Final save before exit
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
            
            # Wait for results to load
            time.sleep(1.0)  # Reduced from 2s
        
        logger.info(f"Collection complete: {len(businesses)} funeral businesses, {skipped_count} non-funeral skipped")
        return businesses
    
    def _extract_business_details(self, basic_info: Dict) -> Optional[MapsBusinessData]:
        """Click on a business card and extract all details from the panel."""
        try:
            expected_name = basic_info.get('name', 'Unknown')
            
            # Click the business card to open details panel (skip if single result - already open)
            is_single_result = basic_info.get('is_single_result', False)
            card = basic_info.get('element')
            
            if card and not is_single_result:
                # Click and wait for the correct panel to load
                # Try up to 2 times if the panel doesn't show the right business
                for attempt in range(2):
                    card.click()
                    time.sleep(0.5)  # Initial wait for click to register
                    
                    # Wait for the h1 title to appear with correct business name
                    max_wait = 4.0
                    wait_interval = 0.2
                    waited = 0
                    panel_loaded = False
                    
                    while waited < max_wait:
                        time.sleep(wait_interval)
                        waited += wait_interval
                        
                        try:
                            panel_title = self.page.locator('h1.DUwDvf').first
                            if panel_title.count() > 0:
                                panel_name = panel_title.text_content()
                                if panel_name:
                                    # Normalize both names for comparison
                                    panel_clean = panel_name.strip().lower()
                                    expected_clean = expected_name.strip().lower()
                                    # Check if they match (or are very similar - first 20 chars)
                                    if panel_clean == expected_clean or panel_clean[:20] == expected_clean[:20]:
                                        panel_loaded = True
                                        break
                        except:
                            pass
                    
                    if panel_loaded:
                        time.sleep(0.3)  # Reduced from 0.5s
                        break
                    elif attempt == 0:
                        # First attempt failed, try scrolling the card into view and clicking again
                        try:
                            card.scroll_into_view_if_needed()
                        except:
                            pass
                        time.sleep(0.3)
                
                # If still not loaded after retries, wait longer and hope for the best
                if not panel_loaded:
                    time.sleep(2.0)
            
            # Wait for details panel to load
            self.page.wait_for_selector('[role="main"]', timeout=5000)
            
            # Wait for address element to be populated (confirms full panel load)
            try:
                for _ in range(10):  # Max 2 seconds
                    addr_elem = self.page.locator('[data-item-id="address"] .Io6YTe').first
                    if addr_elem.count() > 0 and addr_elem.text_content():
                        break
                    time.sleep(0.2)
            except:
                pass
            
            data = MapsBusinessData(
                name=basic_info.get('name', 'Unknown'),
                rating=basic_info.get('rating'),
                category=basic_info.get('category')
            )
            
            # Extract place_id from URL first (this is reliable)
            try:
                url = self.page.url
                place_id_match = re.search(r'!1s(0x[0-9a-fA-F]+:[0-9a-fA-Fx]+)', url)
                if place_id_match:
                    data.place_id = place_id_match.group(1)
                else:
                    place_match = re.search(r'/data=.*?!1s([^!]+)', url)
                    if place_match:
                        data.place_id = place_match.group(1)
            except:
                pass
            
            # Extract address FIRST - we need this for geocoding
            try:
                address_button = self.page.locator('[data-item-id="address"] .Io6YTe').first
                if address_button.count() > 0:
                    full_address = address_button.text_content()
                    data.address = full_address
                    
                    # Parse city/county from address
                    self._parse_address(data, full_address)
            except:
                pass
            
            # Extract coordinates via GEOCODING the address (most reliable method)
            # Skip if self.geocode=False for speed - can batch geocode later
            coord_method = None
            
            if self.geocode and data.address and GEOCODING_AVAILABLE:
                try:
                    from tools.geocoding import has_street_number
                    geocoder = GeocodingTool()
                    coords = geocoder.geocode(
                        address=data.address,
                        city=data.city,
                        county=data.county,
                        company_name=data.name
                    )
                    if coords:
                        data.latitude, data.longitude = coords
                        coord_method = "geocoding"
                        # Track coordinate quality based on address completeness
                        if has_street_number(data.address):
                            data.coord_quality = "exact"
                        else:
                            data.coord_quality = "approximate"
                            logger.warning(f"Address without street number: {data.address}")
                except Exception as e:
                    logger.debug(f"Geocoding failed: {e}")
            
            # Fallback: URL coordinates (less reliable - may be viewport center)
            if not coord_method:
                try:
                    url = self.page.url
                    coord_match = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', url)
                    if coord_match:
                        data.latitude = float(coord_match.group(1))
                        data.longitude = float(coord_match.group(2))
                        coord_method = "url_pattern (fallback)"
                        data.coord_quality = "approximate"  # URL coords are viewport, not exact
                except:
                    pass
            
            # Log which method worked
            if coord_method:
                logger.debug(f"Coordinates via {coord_method}: ({data.latitude}, {data.longitude})")
            else:
                logger.warning(f"No coordinates found for: {data.name}")
                data.coord_quality = "none"
            
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
        # Romanian address format: "Street, Number, City, County PostalCode" or "Street, City PostalCode"
        
        address_lower = full_address.lower()
        
        # All Romanian counties with their common name variations
        ROMANIAN_COUNTIES = {
            'alba': 'Alba',
            'arad': 'Arad', 
            'argeș': 'Argeș', 'arges': 'Argeș',
            'bacău': 'Bacău', 'bacau': 'Bacău',
            'bihor': 'Bihor',
            'bistrița-năsăud': 'Bistrița-Năsăud', 'bistrita-nasaud': 'Bistrița-Năsăud', 'bistrița': 'Bistrița-Năsăud', 'bistrita': 'Bistrița-Năsăud',
            'botoșani': 'Botoșani', 'botosani': 'Botoșani',
            'brăila': 'Brăila', 'braila': 'Brăila',
            'brașov': 'Brașov', 'brasov': 'Brașov',
            'bucurești': 'București', 'bucuresti': 'București', 'bucharest': 'București',
            'buzău': 'Buzău', 'buzau': 'Buzău',
            'călărași': 'Călărași', 'calarasi': 'Călărași',
            'caraș-severin': 'Caraș-Severin', 'caras-severin': 'Caraș-Severin',
            'cluj': 'Cluj',
            'constanța': 'Constanța', 'constanta': 'Constanța',
            'covasna': 'Covasna',
            'dâmbovița': 'Dâmbovița', 'dambovita': 'Dâmbovița',
            'dolj': 'Dolj',
            'galați': 'Galați', 'galati': 'Galați',
            'giurgiu': 'Giurgiu',
            'gorj': 'Gorj',
            'harghita': 'Harghita',
            'hunedoara': 'Hunedoara',
            'ialomița': 'Ialomița', 'ialomita': 'Ialomița',
            'iași': 'Iași', 'iasi': 'Iași',
            'ilfov': 'Ilfov',
            'maramureș': 'Maramureș', 'maramures': 'Maramureș',
            'mehedinți': 'Mehedinți', 'mehedinti': 'Mehedinți',
            'mureș': 'Mureș', 'mures': 'Mureș',
            'neamț': 'Neamț', 'neamt': 'Neamț',
            'olt': 'Olt',
            'prahova': 'Prahova',
            'sălaj': 'Sălaj', 'salaj': 'Sălaj',
            'satu mare': 'Satu Mare',
            'sibiu': 'Sibiu',
            'suceava': 'Suceava',
            'teleorman': 'Teleorman',
            'timiș': 'Timiș', 'timis': 'Timiș',
            'tulcea': 'Tulcea',
            'vâlcea': 'Vâlcea', 'valcea': 'Vâlcea',
            'vaslui': 'Vaslui',
            'vrancea': 'Vrancea',
        }
        
        # Detect county from address
        for county_variant, county_name in ROMANIAN_COUNTIES.items():
            if county_variant in address_lower:
                data.county = county_name
                break
        
        # Special handling for București (often just has "București" or "Sector X")
        if 'sector' in address_lower and not data.county:
            data.county = 'București'
            data.city = 'București'
        
        # If address contains "București" anywhere, set city/county
        if 'bucureș' in address_lower or 'bucures' in address_lower:
            data.county = 'București'
            if not data.city:
                data.city = 'București'
        
        # Try to extract city from address parts
        if not data.city:
            parts = full_address.split(',')
            if len(parts) >= 2:
                # Street indicators that should NOT be in city names
                street_indicators = [
                    'str.', 'strada', 'calea', 'bulevardul', 'b-dul', 'bd.', 
                    'aleea', 'piața', 'piata', 'șoseaua', 'soseaua', 'șos.', 'sos.',
                    'intrarea', 'fundătura', 'fundatura', 'drumul', 'pasaj',
                    'bloc', 'bl.', 'nr.', 'et.', 'ap.', 'sector', 'sc.',
                    'parter', 'subsol', 'etaj', 'mansardă', 'mansarda'
                ]
                # Usually city is second-to-last or third-to-last part
                for part in reversed(parts[:-1]):
                    part = part.strip()
                    part_lower = part.lower()
                    # Skip if it looks like a postal code (5-6 digits)
                    if re.match(r'^\d{5,6}$', part):
                        continue
                    # Skip if it's mostly a number with optional letters (street number)
                    if re.match(r'^\d+[a-zA-Z]?$', part):
                        continue
                    # Skip if it STARTS with a number (likely street number: "29A" or "bloc 5")
                    if re.match(r'^\d', part):
                        continue
                    # Skip if it contains street indicators (not a city name)
                    if any(indicator in part_lower for indicator in street_indicators):
                        continue
                    # Skip county names (already captured)
                    if part_lower in ROMANIAN_COUNTIES:
                        continue
                    # Skip if too short (likely abbreviation) or too long (likely street name)
                    if len(part) < 3 or len(part) > 30:
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
