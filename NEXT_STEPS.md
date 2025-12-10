# 📋 Next Steps Checklist

**Last Updated:** December 10, 2025  
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

## Priority 3: Database Schema Update for Romania-wide Coverage ⏱️ ~20 min ✅ COMPLETE

- [x] Add `city` and `county` (județ) fields to locations table ✅
- [x] Create `counties` reference table with all 41 Romanian counties + Bucharest ✅
- [x] Add indexes for city/county queries ✅
- [x] Run schema update in Supabase SQL Editor ✅
- [x] Import sample data (56 companies across 10 counties) ✅

---

## Priority 4: Location-Based Search UI ⏱️ ~2-3 hours ✅ COMPLETE

### Components Built:
- [x] County dropdown selector (searchable) ✅
- [x] City dropdown filter (searchable) ✅
- [x] Reset filters button ✅
- [x] Results count with location display ✅
- [x] Updated page title to "România" ✅

---

## Priority 5: Build Remaining Frontend Pages ⏱️ ~4-6 hours ✅ COMPLETE

### Components:
- [x] `CompanyCard` - Company listing card ✅
- [x] `CompanyCardSkeleton` - Loading skeleton ✅
- [x] `SearchInput` - Search field ✅
- [x] `Map` - Leaflet map with markers and popups ✅

### Pages:
- [x] Homepage (`/`) - Directory listing with map/grid toggle ✅
- [x] Company Profile (`/company/[slug]`) - Full detail page ✅
- [x] Not Found page for companies ✅

### Map Features:
- [x] Interactive Leaflet map with OpenStreetMap ✅
- [x] Map/List toggle view on homepage ✅
- [x] Mini-map on company detail pages ✅
- [x] Clickable markers with company popups ✅
- [x] Google Maps integration links ✅

---

## Priority 6: SEO & Meta Tags ⏱️ ~2 hours ✅ COMPLETE

- [x] Global metadata in layout.tsx ✅
- [x] Dynamic metadata per company page ✅
- [x] JSON-LD LocalBusiness structured data (FuneralHome schema) ✅
- [x] sitemap.xml auto-generated from database ✅
- [x] robots.txt ✅
- [x] Canonical URLs ✅
- [x] OpenGraph & Twitter cards ✅
- [x] Romanian language (lang="ro") ✅

---

## Priority 7: API Routes ⏱️ ~2-3 hours ✅ COMPLETE

- [x] `GET /api/companies` - Paginated, filtered by location ✅
- [x] `GET /api/companies/[slug]` - Single company details ✅
- [x] `GET /api/counties` - List all counties ✅
- [x] `GET /api/cities?county=X` - List cities in a county ✅
- [x] `POST /api/reports` - User feedback submission ✅
- [x] `POST /api/removal-request` - GDPR erasure request ✅
- [ ] **RUN `reports_schema.sql` in Supabase** (optional - for reports/removal tables)

---

## Priority 8: Backend Scraper for Romania ⏱️ ~2-3 hours 🔜 NEXT

- [ ] Add seed URLs organized by county
- [ ] Update scraper to extract city/county from addresses
- [ ] Add geocoding for coordinates (lat/lng)
- [ ] Set up Python virtual environment
- [ ] Install backend dependencies
- [ ] Run scraper for multiple cities

---

## Priority 9: Additional Pages ⏱️ ~2-3 hours ✅ COMPLETE

- [x] About (`/despre`) - Project information ✅
- [x] Contact (`/contact`) - Contact form ✅
- [x] GDPR Removal Request (`/eliminare`) - Removal request form ✅
- [ ] Homepage by County (`/judet/[county]`) - e.g., `/judet/timis` (optional)
- [ ] Homepage by City (`/judet/[county]/[city]`) - e.g., `/judet/timis/timisoara` (optional)

---

## Priority 10: Testing ⏱️ ~3-4 hours 🔜 NEXT

- [ ] Backend unit tests (pytest)
- [ ] Frontend component tests
- [ ] E2E tests (Playwright)
- [ ] Integration tests

---

## Priority 11: Deployment ⏱️ ~2 hours

- [ ] Deploy frontend to Vercel
- [ ] Configure environment variables
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

