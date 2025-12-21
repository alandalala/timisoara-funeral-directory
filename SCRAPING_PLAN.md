# Google Maps Scraping - Comprehensive Fix Plan

## The Problem

When manually searching "funerare bucurești" on Google Maps:
- Results are **only from București** 
- Scrolling to the end shows only local results
- Map is centered on București and shows businesses in that area

When our scraper searches:
- Results include businesses from Timișoara, Brașov, Giurgiu, etc.
- 100+ results when manually there are ~30-40
- Wrong-city businesses appear frequently

## Root Cause Analysis

### Why Manual Search Works Differently

1. **Map Viewport Binding**: Google Maps shows results based on the **visible map area**. When you search manually:
   - The map centers on București
   - Results are from businesses **visible on the map**
   - Scrolling the list doesn't change the map bounds

2. **Geolocation**: Your browser shares your location, influencing results

3. **Session/Cookies**: Google personalizes based on your search history

4. **URL Structure**: Manual search uses geographic bounds in the URL

### Why Our Scraper Gets Wrong Results

1. **Headless Browser Issues**:
   - No geolocation set → Google uses IP location
   - Different user agent → Different results
   - No cookies → No personalization

2. **URL Without Bounds**: We use:
   ```
   https://www.google.com/maps/search/funerare+București,+București,+Romania
   ```
   This doesn't lock the map to București bounds.

3. **Excessive Scrolling**: Google Maps loads "related" results from wider areas when you scroll beyond the initial set

---

## Solution Plan

### Phase 1: URL-Based Geographic Locking (Recommended First)

Use Google Maps URL with **explicit coordinates and zoom**:

```
https://www.google.com/maps/search/funerare/@44.4268,26.1025,12z
```

Where:
- `@44.4268,26.1025` = București center coordinates
- `12z` = zoom level (12 covers the city, 13 is tighter)

**City Coordinates Database**:
```python
CITY_COORDS = {
    'București': {'lat': 44.4268, 'lng': 26.1025, 'zoom': 12},
    'Cluj-Napoca': {'lat': 46.7712, 'lng': 23.6236, 'zoom': 13},
    'Timișoara': {'lat': 45.7489, 'lng': 21.2087, 'zoom': 13},
    'Iași': {'lat': 47.1585, 'lng': 27.6014, 'zoom': 13},
    'Constanța': {'lat': 44.1598, 'lng': 28.6348, 'zoom': 13},
    'Craiova': {'lat': 44.3302, 'lng': 23.7949, 'zoom': 13},
    'Brașov': {'lat': 45.6427, 'lng': 25.5887, 'zoom': 13},
    'Galați': {'lat': 45.4353, 'lng': 28.0080, 'zoom': 13},
    'Ploiești': {'lat': 44.9365, 'lng': 26.0254, 'zoom': 13},
    'Oradea': {'lat': 47.0722, 'lng': 21.9217, 'zoom': 13},
    # ... add all cities
}
```

### Phase 2: Viewport Verification

Before collecting results, verify the map is showing the right area:

```python
def verify_map_location(self, expected_city: str) -> bool:
    """Check if map is centered on expected city."""
    # Get current URL
    url = self.page.url
    
    # Extract coordinates from URL
    # Format: @44.4268,26.1025,12z
    import re
    match = re.search(r'@([\d.]+),([\d.]+),([\d.]+)z', url)
    if match:
        lat, lng, zoom = float(match.group(1)), float(match.group(2)), float(match.group(3))
        expected = CITY_COORDS.get(expected_city)
        if expected:
            # Check if within reasonable distance (0.1 degrees ≈ 11km)
            lat_diff = abs(lat - expected['lat'])
            lng_diff = abs(lng - expected['lng'])
            return lat_diff < 0.2 and lng_diff < 0.2
    return False
```

### Phase 3: Coordinate-Based Filtering

After extracting each business, verify its coordinates are within the city bounds:

```python
CITY_BOUNDS = {
    'București': {
        'min_lat': 44.35, 'max_lat': 44.55,
        'min_lng': 25.95, 'max_lng': 26.25
    },
    'Timișoara': {
        'min_lat': 45.70, 'max_lat': 45.80,
        'min_lng': 21.15, 'max_lng': 21.30
    },
    # ... etc
}

def is_in_city_bounds(self, lat: float, lng: float, city: str) -> bool:
    bounds = CITY_BOUNDS.get(city)
    if not bounds:
        return True  # No bounds defined, accept
    return (bounds['min_lat'] <= lat <= bounds['max_lat'] and
            bounds['min_lng'] <= lng <= bounds['max_lng'])
```

### Phase 4: Reduce Scroll Depth

Stop scrolling earlier - the initial results are the most relevant:

```python
max_results = 30  # For most cities
max_results = 50  # For București only
max_scrolls = 10  # Reduced from 30
```

### Phase 5: Non-Headless Debugging

Run with `headless=False` to see what's happening:

```python
# In maps_scraper.py
def __init__(self, headless: bool = False):  # Change default to False for debugging
```

Then watch:
1. Does the map center on the right city?
2. What results appear in the list?
3. Does scrolling load wrong-city results?

---

## Implementation Order

### Step 1: Quick Fix (30 min)
- [x] Add max_results limit (done)
- [ ] Use coordinate-based URLs instead of text search
- [ ] Reduce scroll depth to 10

### Step 2: URL with Coordinates (1 hour)
- [ ] Create CITY_COORDS dictionary for all Romanian cities
- [ ] Modify search() to use `@lat,lng,zoom` URL format
- [ ] Test with București manually

### Step 3: Coordinate Filtering (1 hour)
- [ ] Extract coordinates from business detail page
- [ ] Create CITY_BOUNDS for major cities
- [ ] Filter out businesses outside bounds
- [ ] Log skipped businesses with their actual coordinates

### Step 4: Verification (30 min)
- [ ] Add map viewport verification
- [ ] Add retry logic if map shows wrong area
- [ ] Test with 5 different cities

---

## Alternative Approaches

### Option A: Google Places API (Paid but Reliable)
- $17 per 1000 requests for Nearby Search
- Guaranteed correct results
- No scraping headaches
- Structured data

### Option B: Multiple Precise Searches
Instead of one broad search, do multiple targeted searches:
- "pompe funebre sector 1 bucurești"
- "pompe funebre sector 2 bucurești"
- "pompe funebre sector 3 bucurești"
- etc.

### Option C: Bounding Box in URL
Use the `!3m1!4b1!4m5!3m4` parameters that Google Maps uses:
```
/maps/search/funerare/@44.4268,26.1025,12z/data=!3m1!4b1
```

---

## Testing Checklist

After implementation:

- [ ] Search "funerare bucurești" - should return ONLY București businesses
- [ ] Check coordinates of all returned businesses - all should be 44.3-44.6 lat, 25.9-26.3 lng
- [ ] Search "funerare timișoara" - should NOT include București businesses
- [ ] Total results should match manual search count (~30-50, not 100+)
- [ ] No "Styx Funerare Mehala" in București results
- [ ] No "Giurgiu" addresses in București results

---

## Recommended Immediate Action

**Start with coordinate-based URLs** - this is the most impactful fix:

```python
# Current (broken):
url = f"https://www.google.com/maps/search/{query}+{location}"

# Fixed:
coords = CITY_COORDS.get(city_name, {'lat': 45.9432, 'lng': 24.9668, 'zoom': 6})
url = f"https://www.google.com/maps/search/{query}/@{coords['lat']},{coords['lng']},{coords['zoom']}z"
```

This single change should dramatically improve result accuracy.
