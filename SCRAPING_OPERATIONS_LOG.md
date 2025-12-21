# Scraping Operations Log

## 2025-12-21: București Rescrape with Optimizations

### Operations Performed

1. **Cleared existing București data**
   - Deleted: `backend/data/scraped/maps_bucuresti.json`
   - Reason: Test new optimizations with fresh data

2. **Ran optimized București scrape**
   - Command: `python scrape_romania.py --county "București"`
   - Duration: ~8 minutes (15:47:57 - 15:56:09)
   - Mode: Headless browser

### Optimizations Applied (implemented earlier this session)

| Optimization | Description |
|-------------|-------------|
| **Search order reordered** | Changed from "funerare" → "pompe funebre" → "servicii funerare" to "servicii funerare" → "pompe funebre" → "funerare" (most natural term first) |
| **Removed 4th redundant search** | Previously ran extra "funerare {city}, Romania" search for county capitals - no longer needed with geo-locked URLs |
| **Added skip_names parameter** | `search()` method now accepts set of already-scraped names to skip extraction |
| **Name normalization** | `normalize_name()` function strips emojis, normalizes diacritics (ă→a, â→a, î→i, ș→s, ț→t), removes SRL/S.R.L. suffixes |

### Results

| Metric | Value |
|--------|-------|
| **Total unique businesses found** | 117 |
| **Businesses saved** | 103 |
| **Filtered (wrong location)** | 14 |
| **Searches performed** | 3 |

### Search Breakdown

| Search Term | Results Found | New Extracted | Skipped (duplicates) |
|-------------|--------------|---------------|---------------------|
| "servicii funerare" | 88 cards | 84 new | 4 skipped |
| "pompe funebre" | 83 cards | 31 new | 52 skipped |
| "funerare" | 88 cards | 2 new | 86 skipped |

### Efficiency Gains

**Before optimization (previous run):**
- ~250 extractions total across 4 searches
- ~102 unique businesses saved
- ~148 redundant extractions (~6 minutes wasted)

**After optimization:**
- ~117 extractions total across 3 searches
- 103 unique businesses saved
- Skipped ~133 redundant extractions via `[SKIP] Already scraped` logs
- **Time saved: ~5-6 minutes per city**

### Issues Identified

#### ⚠️ False Positive: "Giurgiului" street vs "Giurgiu" city

**Problem:** The location filter incorrectly rejects businesses on "Șoseaua Giurgiului" (a major street in București) because it matches the "giurgiu" city keyword.

**Affected businesses:**
- Servicii Funerare Mirgal (Șoseaua Giurgiului 31, București) - ❌ Incorrectly filtered
- Servicii funerare non stop - Stefy - ❌ Incorrectly filtered  
- Servicii funerare sector 4 - ❌ Incorrectly filtered
- DANI IMPEX - ❌ Incorrectly filtered

**Root cause:** The `search()` method in `maps_scraper.py` checks if card snippet contains city names, but "giurgiului" (genitive form of Giurgiu, used in street names) triggers the "giurgiu" city filter.

**Fix needed:** Update filter to distinguish between:
- "Giurgiu" as standalone word (city) → filter out
- "Giurgiului" in street names → allow

### Files Modified

1. `backend/tools/maps_scraper.py`:
   - Added `normalize_name()` function
   - Added `skip_names` parameter to `search()` method
   - Added skip logic before extraction

2. `backend/scrape_romania.py`:
   - Reordered search terms
   - Removed 4th redundant search for county capitals
   - Updated to pass `skip_names` to `scraper.search()`
   - Added name normalization for deduplication

### Next Steps

1. **Fix Giurgiului street filter** - Distinguish street names from city names
2. **Verify Mirgal is captured** - After fix, confirm business is included
3. **Full Romania scrape** - Run optimized scraper across all counties
