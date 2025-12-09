"""
Utility functions for data processing and validation.
"""
import re
import time
import random
from typing import Optional, Tuple
from config.settings import MIN_DELAY_SECONDS, MAX_DELAY_SECONDS


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
    """
    delay = random.uniform(MIN_DELAY_SECONDS, MAX_DELAY_SECONDS)
    time.sleep(delay)


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
