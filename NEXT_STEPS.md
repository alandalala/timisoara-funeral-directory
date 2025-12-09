# 📋 Next Steps Checklist

**Last Updated:** December 9, 2025  
**Scope:** 🇷🇴 Funeral Services Directory for ALL of Romania

Track your progress by checking off completed items!

---

## Priority 1: Database Setup ⏱️ ~15 min ✅ COMPLETE

- [x] Create a Supabase project at [supabase.com](https://supabase.com) ✅
  - URL: `https://xhdizdharbtmngtlwhop.supabase.co`
- [x] Run `database_schema.sql` in Supabase SQL Editor ✅
- [x] Verify all 6 tables are created ✅
- [x] Copy API credentials ✅

---

## Priority 2: Environment Configuration ⏱️ ~10 min ✅ COMPLETE

- [x] Create `backend/.env` file ✅
- [x] Create `frontend/.env.local` file ✅
- [x] Add your OpenAI API key to `backend/.env` ✅
- [x] Test frontend connection ✅

---

## Priority 3: Database Schema Update for Romania-wide Coverage ⏱️ ~20 min 🔄 IN PROGRESS

- [x] Add `city` and `county` (județ) fields to locations table ✅ (schema_update_romania.sql created)
- [x] Create `counties` reference table with all 41 Romanian counties + Bucharest ✅
- [x] Add indexes for city/county queries ✅
- [ ] **RUN `schema_update_romania.sql` in Supabase SQL Editor**
- [ ] Verify counties table has 42 entries

---

## Priority 4: Location-Based Search UI ⏱️ ~2-3 hours

### Components to Build:
- [x] `LocationSelector` - County/City dropdown selector ✅ (built into homepage)
- [x] `CountyFilter` - Filter by județ ✅
- [x] City dropdown filter ✅
- [x] Reset filters button ✅
- [ ] `NearbySearch` - "Găsește în apropiere" using geolocation

### Homepage Updates:
- [x] Add county selector dropdown ✅
- [x] Add city search field ✅
- [x] Display results count with location ✅
- [ ] Show distance when using geolocation
- [x] Updated page title to "România" ✅

---

## Priority 5: Build Remaining Frontend Pages ⏱️ ~4-6 hours

### Components:
- [x] `CompanyCard` ✅
- [x] `CompanyCardSkeleton` ✅
- [x] `SearchInput` ✅
- [ ] `FilterPanel` - Service filters & verification toggle
- [ ] `MapContainer` - Leaflet map wrapper
- [ ] `MapController` - Marker rendering & clustering

### Pages:
- [x] Homepage (`/`) - Directory listing ✅
- [ ] Homepage by County (`/[county]`) - e.g., `/timis`, `/bucuresti`
- [ ] Homepage by City (`/[county]/[city]`) - e.g., `/timis/timisoara`
- [ ] Company Profile (`/company/[slug]`) - Detail page
- [ ] About (`/about`) - Project information
- [ ] Request Removal (`/request-removal`) - GDPR compliance form

---

## Priority 6: API Routes ⏱️ ~2-3 hours

- [ ] `GET /api/companies` - Paginated, filtered by location
- [ ] `GET /api/companies/[slug]` - Single company details
- [ ] `GET /api/locations/nearby` - Geospatial search by coordinates
- [ ] `GET /api/counties` - List all counties
- [ ] `GET /api/cities?county=X` - List cities in a county
- [ ] `POST /api/reports` - User feedback submission
- [ ] `POST /api/removal-request` - GDPR erasure request

---

## Priority 7: Backend Scraper for Romania ⏱️ ~2-3 hours

- [ ] Add seed URLs organized by county
- [ ] Update scraper to extract city/county from addresses
- [ ] Add geocoding for coordinates (lat/lng)
- [ ] Set up Python virtual environment
- [ ] Install backend dependencies
- [ ] Run scraper for multiple cities

---

## Priority 8: SEO for Location Pages ⏱️ ~2 hours

- [ ] Dynamic metadata per county/city
- [ ] JSON-LD LocalBusiness structured data
- [ ] Sitemap.xml with all location pages
- [ ] robots.txt
- [ ] Canonical URLs for location pages

---

## Priority 9: Testing ⏱️ ~3-4 hours

- [ ] Backend unit tests (pytest)
- [ ] Frontend component tests
- [ ] E2E tests (Playwright)
- [ ] Integration tests

---

## Priority 10: Deployment ⏱️ ~2 hours

- [ ] Deploy frontend to Vercel
- [ ] Configure GitHub Secrets for Actions
- [ ] Set up custom domain (optional)
- [ ] Add error monitoring (Sentry)
- [ ] Enable Vercel Analytics

---

## 🎉 Project Launch

- [ ] Final review and testing
- [ ] Go live!

---

## Romanian Counties Reference

All 41 counties + Bucharest:
```
Alba, Arad, Argeș, Bacău, Bihor, Bistrița-Năsăud, Botoșani, Brașov,
Brăila, București, Buzău, Caraș-Severin, Călărași, Cluj, Constanța,
Covasna, Dâmbovița, Dolj, Galați, Giurgiu, Gorj, Harghita, Hunedoara,
Ialomița, Iași, Ilfov, Maramureș, Mehedinți, Mureș, Neamț, Olt,
Prahova, Satu Mare, Sălaj, Sibiu, Suceava, Teleorman, Timiș,
Tulcea, Vaslui, Vâlcea, Vrancea
```

---

## Notes

_Add any notes or blockers here:_

- Project renamed from "Timișoara Funeral Directory" to "Romania Funeral Directory"

