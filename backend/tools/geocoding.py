"""
Geocoding Tool - Convert addresses to coordinates using Nominatim (OpenStreetMap).
Free, no API key required.
"""
import requests
import time
from typing import Optional, Tuple
from config.settings import USER_AGENT

# Hardcoded city center coordinates for Romanian cities (guaranteed fallback)
CITY_COORDINATES = {
    'timișoara': (45.7538355, 21.2257474),
    'timisoara': (45.7538355, 21.2257474),
    'bucurești': (44.4268, 26.1025),
    'bucuresti': (44.4268, 26.1025),
    'bucharest': (44.4268, 26.1025),
    'cluj-napoca': (46.7712, 23.6236),
    'cluj': (46.7712, 23.6236),
    'iași': (47.1585, 27.6014),
    'iasi': (47.1585, 27.6014),
    'constanța': (44.1598, 28.6348),
    'constanta': (44.1598, 28.6348),
    'craiova': (44.3302, 23.7949),
    'brașov': (45.6427, 25.5887),
    'brasov': (45.6427, 25.5887),
    'galați': (45.4353, 28.0080),
    'galati': (45.4353, 28.0080),
    'ploiești': (44.9366, 26.0134),
    'ploiesti': (44.9366, 26.0134),
    'oradea': (47.0465, 21.9189),
    'brăila': (45.2692, 27.9575),
    'braila': (45.2692, 27.9575),
    'arad': (46.1866, 21.3123),
    'pitești': (44.8565, 24.8692),
    'pitesti': (44.8565, 24.8692),
    'sibiu': (45.7983, 24.1256),
    'bacău': (46.5670, 26.9146),
    'bacau': (46.5670, 26.9146),
    'târgu mureș': (46.5386, 24.5579),
    'targu mures': (46.5386, 24.5579),
    'baia mare': (47.6567, 23.5850),
    'buzău': (45.1500, 26.8333),
    'buzau': (45.1500, 26.8333),
    'botoșani': (47.7486, 26.6694),
    'botosani': (47.7486, 26.6694),
    'satu mare': (47.7928, 22.8856),
    'râmnicu vâlcea': (45.1047, 24.3693),
    'ramnicu valcea': (45.1047, 24.3693),
    'drobeta-turnu severin': (44.6369, 22.6597),
    'suceava': (47.6514, 26.2556),
    'piatra neamț': (46.9275, 26.3658),
    'piatra neamt': (46.9275, 26.3658),
    'târgu jiu': (45.0378, 23.2736),
    'targu jiu': (45.0378, 23.2736),
    'focșani': (45.6967, 27.1833),
    'focsani': (45.6967, 27.1833),
    'tulcea': (45.1667, 28.8000),
    'reșița': (45.3006, 21.8894),
    'resita': (45.3006, 21.8894),
    'târgoviște': (44.9253, 25.4567),
    'targoviste': (44.9253, 25.4567),
    'mediaș': (46.1667, 24.3500),
    'medias': (46.1667, 24.3500),
    'giurgiu': (43.9037, 25.9699),
    'deva': (45.8833, 22.9000),
    'hunedoara': (45.7500, 22.9167),
    'zalău': (47.1833, 23.0500),
    'zalau': (47.1833, 23.0500),
    'alba iulia': (46.0667, 23.5833),
    'bistrița': (47.1333, 24.5000),
    'bistrita': (47.1333, 24.5000),
    'vaslui': (46.6333, 27.7333),
    'slobozia': (44.5667, 27.3667),
    'călărași': (44.2000, 27.3333),
    'calarasi': (44.2000, 27.3333),
    'alexandria': (43.9833, 25.3333),
    'miercurea ciuc': (46.3500, 25.8000),
    'sfântu gheorghe': (45.8667, 25.7833),
    'sfantu gheorghe': (45.8667, 25.7833),
}


class GeocodingTool:
    """
    Geocode Romanian addresses using Nominatim API.
    """
    
    BASE_URL = "https://nominatim.openstreetmap.org/search"
    
    def __init__(self):
        self.last_request_time = 0
        self.min_delay = 1.0  # Nominatim requires 1 request per second max
    
    def _rate_limit(self):
        """Ensure we don't exceed rate limits."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_delay:
            time.sleep(self.min_delay - elapsed)
        self.last_request_time = time.time()
    
    def geocode(self, address: str, city: str = None, county: str = None, company_name: str = None) -> Optional[Tuple[float, float]]:
        """
        Geocode an address to lat/lng coordinates.
        
        Args:
            address: Street address
            city: City name (optional, improves accuracy)
            county: County/region name (optional)
            company_name: Company name to search for (optional, can find businesses)
        
        Returns:
            Tuple of (latitude, longitude) or None if not found
        """
        # Strategy 1: Try company name + city (businesses often indexed by name)
        if company_name and city:
            result = self._geocode_business(company_name, city)
            if result:
                return result
        
        # Strategy 2: Try full address
        if address and address.strip():
            self._rate_limit()
            
            # Build full address query
            parts = [address]
            if city:
                parts.append(city)
            parts.append("Romania")
            
            query = ", ".join(parts)
            
            try:
                params = {
                    'q': query,
                    'format': 'json',
                    'limit': 1,
                    'countrycodes': 'ro',
                    'addressdetails': 1
                }
                
                headers = {
                    'User-Agent': USER_AGENT
                }
                
                response = requests.get(self.BASE_URL, params=params, headers=headers, timeout=10)
                response.raise_for_status()
                
                results = response.json()
                
                if results and len(results) > 0:
                    lat = float(results[0]['lat'])
                    lon = float(results[0]['lon'])
                    print(f"  Geocoded address '{query}' -> ({lat}, {lon})")
                    return (lat, lon)
                else:
                    # Try to extract and geocode just the street name
                    street_result = self._geocode_street(address, city)
                    if street_result:
                        return street_result
                    print(f"  Address not found, trying city fallback...")
                    
            except Exception as e:
                print(f"  Geocoding error: {e}")
        
        # Strategy 3: Fall back to city coordinates (guaranteed for major cities)
        if city:
            return self._geocode_city(city, county)
        
        return None
    
    def _geocode_street(self, address: str, city: str) -> Optional[Tuple[float, float]]:
        """
        Try to extract and geocode just the street name from an address.
        Useful when full address with extra info (like landmarks) fails.
        """
        import re
        
        # Clean the address - remove parenthetical info, landmarks, etc.
        # "Calea Lugojului, Timisoara (fostul restaurant Trafic)" -> "Calea Lugojului"
        cleaned = re.sub(r'\([^)]*\)', '', address)  # Remove (...)
        cleaned = re.sub(r'\[[^\]]*\]', '', cleaned)  # Remove [...]
        cleaned = cleaned.split(',')[0].strip()  # Take first part before comma
        
        # Common Romanian street prefixes
        street_prefixes = [
            'strada', 'str.', 'str ', 'calea', 'bulevardul', 'bd.', 'bd ', 'b-dul',
            'aleea', 'piata', 'piața', 'splai', 'splaiul', 'drumul', 'intrarea'
        ]
        
        # Check if it looks like a street name
        has_street_prefix = any(cleaned.lower().startswith(p) for p in street_prefixes)
        
        if not has_street_prefix and not cleaned:
            return None
        
        # If no city provided, can't do street search
        if not city:
            return None
        
        self._rate_limit()
        
        # Try geocoding the street in the city
        query = f"{cleaned}, {city}, Romania"
        
        try:
            params = {
                'q': query,
                'format': 'json',
                'limit': 1,
                'countrycodes': 'ro',
                'addressdetails': 1
            }
            
            headers = {
                'User-Agent': USER_AGENT
            }
            
            response = requests.get(self.BASE_URL, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            results = response.json()
            
            if results and len(results) > 0:
                lat = float(results[0]['lat'])
                lon = float(results[0]['lon'])
                print(f"  Geocoded street '{cleaned}' in {city} -> ({lat}, {lon})")
                return (lat, lon)
            
            return None
            
        except Exception as e:
            print(f"  Street geocoding error: {e}")
            return None
    
    def _geocode_business(self, company_name: str, city: str) -> Optional[Tuple[float, float]]:
        """Try to find a business by name in Nominatim."""
        self._rate_limit()
        
        # Search for business name in city
        query = f"{company_name}, {city}, Romania"
        
        try:
            params = {
                'q': query,
                'format': 'json',
                'limit': 1,
                'countrycodes': 'ro'
            }
            
            headers = {
                'User-Agent': USER_AGENT
            }
            
            response = requests.get(self.BASE_URL, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            results = response.json()
            
            if results and len(results) > 0:
                lat = float(results[0]['lat'])
                lon = float(results[0]['lon'])
                print(f"  Found business '{company_name}' -> ({lat}, {lon})")
                return (lat, lon)
                
            return None
            
        except Exception as e:
            print(f"  Business search error: {e}")
            return None
    
    def _geocode_city(self, city: str, county: str = None) -> Optional[Tuple[float, float]]:
        """Fallback to geocode just the city - uses hardcoded coordinates if API fails."""
        # First check hardcoded coordinates (guaranteed to work)
        city_lower = city.lower().strip()
        if city_lower in CITY_COORDINATES:
            coords = CITY_COORDINATES[city_lower]
            print(f"  Using cached coordinates for '{city}' -> ({coords[0]}, {coords[1]})")
            return coords
        
        # Try Nominatim API
        self._rate_limit()
        
        # Just use city name without county prefix - works better with Nominatim
        query = f"{city}, Romania"
        
        try:
            params = {
                'q': query,
                'format': 'json',
                'limit': 1,
                'countrycodes': 'ro'
            }
            
            headers = {
                'User-Agent': USER_AGENT
            }
            
            response = requests.get(self.BASE_URL, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            results = response.json()
            
            if results and len(results) > 0:
                lat = float(results[0]['lat'])
                lon = float(results[0]['lon'])
                print(f"  Geocoded city '{city}' -> ({lat}, {lon})")
                return (lat, lon)
            
            # API returned no results - try without diacritics in hardcoded
            print(f"  City '{city}' not found in Nominatim or cache")
            return None
            
        except Exception as e:
            print(f"  City geocoding error: {e}")
            return None


# Singleton instance
_geocoder = None

def get_geocoder() -> GeocodingTool:
    global _geocoder
    if _geocoder is None:
        _geocoder = GeocodingTool()
    return _geocoder


def geocode_address(address: str, city: str = None, county: str = None, company_name: str = None) -> Optional[Tuple[float, float]]:
    """
    Convenience function to geocode an address.
    
    Args:
        address: Street address
        city: City name
        county: County name
        company_name: Company name (helps find businesses)
    
    Returns:
        Tuple of (latitude, longitude) or None
    """
    return get_geocoder().geocode(address, city, county, company_name)
