"""
Utility functions for data processing and validation.
Includes human-like behavior simulation for ethical web scraping.
"""
import re
import time
import random
from typing import Optional, Tuple
from config.settings import MIN_DELAY_SECONDS, MAX_DELAY_SECONDS, USER_AGENTS


def normalize_phone_number(phone: str) -> Tuple[str, str]:
    """
    Normalize Romanian phone number to E.164 format.
    Returns (normalized_number, type) where type is 'mobile' or 'landline'
    """
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    
    # Handle Romanian formats
    if digits.startswith('40'):
        digits = digits[2:]  # Remove country code
    elif digits.startswith('0'):
        digits = digits[1:]  # Remove leading 0
    
    # Determine type based on Romanian numbering plan
    # Mobile: 7XX (where XX is mobile prefix like 72, 73, 74, 75, 76, 77, 78, 79)
    # Landline: starts with area code (e.g., 256 for Timișoara)
    
    phone_type = 'landline'
    if digits.startswith('7'):
        phone_type = 'mobile'
    
    # Ensure it's a valid length (9-10 digits for Romanian numbers)
    if len(digits) < 9 or len(digits) > 10:
        raise ValueError(f"Invalid phone number length: {digits}")
    
    # Return normalized format (with leading 0 for local format)
    normalized = '0' + digits if not digits.startswith('0') else digits
    
    return normalized, phone_type


def slugify(text: str) -> str:
    """
    Convert text to URL-friendly slug.
    """
    # Convert to lowercase
    text = text.lower()
    
    # Replace Romanian characters
    replacements = {
        'ă': 'a', 'â': 'a', 'î': 'i', 'ș': 's', 'ț': 't',
        'ş': 's', 'ţ': 't'  # Old cedilla forms
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    # Remove non-alphanumeric characters (except hyphens)
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    
    # Replace spaces and multiple hyphens with single hyphen
    text = re.sub(r'[\s-]+', '-', text)
    
    # Remove leading/trailing hyphens
    text = text.strip('-')
    
    return text


def rate_limit_delay():
    """
    Introduce a random delay between requests to avoid overwhelming servers.
    Uses variable timing to mimic human browsing patterns.
    """
    delay = random.uniform(MIN_DELAY_SECONDS, MAX_DELAY_SECONDS)
    time.sleep(delay)


def human_delay(action_type: str = "page_load"):
    """
    Introduce human-like delays based on action type.
    Different actions have different typical human response times.
    
    Args:
        action_type: Type of action - 'page_load', 'click', 'scroll', 'read', 'between_sites'
    """
    delays = {
        'page_load': (2, 5),       # Time to wait for page to load
        'click': (0.5, 1.5),       # Time between clicks
        'scroll': (1, 3),          # Time to scroll and scan content
        'read': (3, 8),            # Time to read content
        'between_sites': (5, 15),  # Longer pause between different websites
        'form_fill': (1, 3),       # Time to fill a form field
    }
    
    min_delay, max_delay = delays.get(action_type, (2, 5))
    
    # Add occasional longer pauses (10% chance) to simulate distraction
    if random.random() < 0.1:
        max_delay *= 2
    
    delay = random.uniform(min_delay, max_delay)
    time.sleep(delay)


def get_random_user_agent() -> str:
    """
    Get a random realistic browser user agent.
    Rotates between common browsers to avoid detection.
    """
    return random.choice(USER_AGENTS)


def get_human_headers(referer: Optional[str] = None) -> dict:
    """
    Generate realistic HTTP headers that mimic a real browser.
    
    Args:
        referer: Optional referer URL (previous page visited)
    
    Returns:
        Dict of HTTP headers
    """
    headers = {
        'User-Agent': get_random_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'ro-RO,ro;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none' if not referer else 'same-origin',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
    }
    
    if referer:
        headers['Referer'] = referer
    
    return headers


class HumanBehaviorSimulator:
    """
    Simulates human browsing behavior for ethical web scraping.
    Tracks session state and varies behavior patterns.
    """
    
    def __init__(self):
        self.session_start = time.time()
        self.pages_visited = 0
        self.last_request_time = 0
        self.current_user_agent = get_random_user_agent()
        self.last_referer = None
    
    def before_request(self, url: str) -> dict:
        """
        Call before making a request. Returns headers and applies delays.
        
        Args:
            url: The URL about to be requested
        
        Returns:
            Dict of headers to use for the request
        """
        # Ensure minimum time between requests
        if self.last_request_time > 0:
            elapsed = time.time() - self.last_request_time
            if elapsed < MIN_DELAY_SECONDS:
                time.sleep(MIN_DELAY_SECONDS - elapsed + random.uniform(0.5, 2))
        
        # Apply human-like delay
        if self.pages_visited == 0:
            human_delay('page_load')
        elif self._is_different_domain(url):
            human_delay('between_sites')
            # Occasionally rotate user agent when switching sites
            if random.random() < 0.3:
                self.current_user_agent = get_random_user_agent()
        else:
            delay_type = random.choice(['click', 'scroll', 'read'])
            human_delay(delay_type)
        
        # Get headers
        headers = get_human_headers(self.last_referer)
        headers['User-Agent'] = self.current_user_agent
        
        return headers
    
    def after_request(self, url: str, success: bool = True):
        """
        Call after a request completes. Updates session state.
        
        Args:
            url: The URL that was requested
            success: Whether the request was successful
        """
        self.last_request_time = time.time()
        self.pages_visited += 1
        self.last_referer = url if success else self.last_referer
        
        # Simulate reading time after successful page load
        if success:
            human_delay('read')
    
    def _is_different_domain(self, url: str) -> bool:
        """Check if URL is on a different domain than last referer."""
        if not self.last_referer:
            return True
        
        from urllib.parse import urlparse
        current_domain = urlparse(url).netloc
        last_domain = urlparse(self.last_referer).netloc
        
        return current_domain != last_domain
    
    def take_break(self):
        """
        Simulate a coffee break (longer pause).
        Call this periodically during long scraping sessions.
        """
        break_duration = random.uniform(30, 120)
        print(f"Taking a {break_duration:.0f}s break to simulate human behavior...")
        time.sleep(break_duration)
        
        # Rotate user agent after break
        self.current_user_agent = get_random_user_agent()
    
    def should_take_break(self) -> bool:
        """
        Determine if it's time for a break based on pages visited.
        Humans typically take breaks every 20-30 pages.
        """
        return self.pages_visited > 0 and self.pages_visited % random.randint(20, 30) == 0


def extract_cui_from_text(text: str) -> Optional[str]:
    """
    Extract Romanian fiscal code (CUI) from text.
    Looks for patterns like "CUI: 12345678" or "RO12345678"
    """
    # Pattern 1: CUI: followed by digits
    match = re.search(r'CUI[:\s]*(\d{2,10})', text, re.IGNORECASE)
    if match:
        return match.group(1)
    
    # Pattern 2: RO followed by digits
    match = re.search(r'RO\s*(\d{2,10})', text, re.IGNORECASE)
    if match:
        return match.group(1)
    
    # Pattern 3: J followed by department code and number (e.g., J35/1234/2010)
    match = re.search(r'J\d{2}/(\d+)/\d{4}', text)
    if match:
        return match.group(1)
    
    return None


def check_robots_txt(url: str) -> bool:
    """
    Check if a URL is allowed by robots.txt.
    Returns True if allowed, False if disallowed.
    """
    from urllib.parse import urlparse, urljoin
    from urllib.robotparser import RobotFileParser
    
    try:
        parsed = urlparse(url)
        robots_url = urljoin(f"{parsed.scheme}://{parsed.netloc}", "/robots.txt")
        
        rp = RobotFileParser()
        rp.set_url(robots_url)
        rp.read()
        
        return rp.can_fetch("*", url)
    except Exception as e:
        # If we can't fetch robots.txt, assume it's allowed
        print(f"Could not check robots.txt for {url}: {e}")
        return True


def is_valid_email(email: str) -> bool:
    """
    Validate email format.
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def clean_text(text: str) -> str:
    """
    Clean and normalize text by removing extra whitespace.
    """
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)
    # Remove leading/trailing whitespace
    text = text.strip()
    return text
