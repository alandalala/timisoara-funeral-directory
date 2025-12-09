# 📋 Next Steps Checklist

**Last Updated:** December 9, 2025

Track your progress by checking off completed items!

---

## Priority 1: Database Setup ⏱️ ~15 min

- [ ] Create a Supabase project at [supabase.com](https://supabase.com)
  - Name: `funeral-directory`
  - Region: Europe (Frankfurt)
- [ ] Run `database_schema.sql` in Supabase SQL Editor
- [ ] Verify all 6 tables are created:
  - [ ] companies
  - [ ] locations
  - [ ] services
  - [ ] contacts
  - [ ] reports
  - [ ] removal_requests
- [ ] Copy API credentials:
  - [ ] Project URL
  - [ ] Anon public key
  - [ ] Service role key

---

## Priority 2: Environment Configuration ⏱️ ~10 min

- [ ] Create `backend/.env` file with:
  ```
  SUPABASE_URL=your_supabase_url
  SUPABASE_SERVICE_KEY=your_service_role_key
  OPENAI_API_KEY=your_openai_key
  FIRECRAWL_API_KEY=your_firecrawl_key
  ```
- [ ] Create `frontend/.env.local` file with:
  ```
  NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
  NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
  ```
- [ ] Test backend connection: `python backend/verify_setup.py`
- [ ] Test frontend connection: `npm run dev` in frontend folder

---

## Priority 3: Test Backend Pipeline ⏱️ ~30 min

- [ ] Add seed URLs to `backend/data/seed_urls.json`
  - Find 5-10 funeral home websites in Timișoara
- [ ] (Optional) Download DSP authorization PDF
- [ ] Run test scrape: `python backend/main.py`
- [ ] Verify data appears in Supabase tables

---

## Priority 4: Build Frontend Pages ⏱️ ~4-6 hours

### Components to Build:
- [ ] `CompanyCard` - Display company info with motto and badges
- [ ] `CompanyCardSkeleton` - Loading state placeholder
- [ ] `SearchInput` - Debounced search field
- [ ] `FilterPanel` - Service filters & verification toggle
- [ ] `ServiceBadge` - Service tag display
- [ ] `MapContainer` - Leaflet map wrapper
- [ ] `MapController` - Marker rendering & clustering

### Pages to Build:
- [ ] Homepage (`/`) - Directory listing with search
- [ ] Company Profile (`/company/[slug]`) - Detail page
- [ ] About (`/about`) - Project information
- [ ] Request Removal (`/request-removal`) - GDPR compliance form

### SEO:
- [ ] JSON-LD structured data
- [ ] Dynamic metadata generation
- [ ] Sitemap.xml generation
- [ ] robots.txt

---

## Priority 5: API Routes ⏱️ ~2-3 hours

- [ ] `GET /api/companies` - Paginated, filtered listing
- [ ] `GET /api/companies/[slug]` - Single company details
- [ ] `GET /api/locations/nearby` - Geospatial search
- [ ] `POST /api/reports` - User feedback submission
- [ ] `POST /api/removal-request` - GDPR erasure request

---

## Priority 6: Testing ⏱️ ~3-4 hours

- [ ] Backend unit tests (pytest)
- [ ] Frontend component tests
- [ ] E2E tests (Playwright)
- [ ] Integration tests

---

## Priority 7: Deployment ⏱️ ~2 hours

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

## Notes

_Add any notes or blockers here:_

- 

