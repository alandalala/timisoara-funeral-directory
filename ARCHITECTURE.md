# Architecture Diagram

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    FUNERAL DIRECTORY SYSTEM                      │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                        DATA ACQUISITION                           │
│                         (Backend - Python)                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌────────────┐    ┌──────────────┐    ┌─────────────┐         │
│  │   SCOUT    │───▶│   ANALYST    │───▶│   AUDITOR   │         │
│  │  (Discover)│    │  (Extract)   │    │  (Validate) │         │
│  └────────────┘    └──────────────┘    └─────────────┘         │
│        │                   │                    │                │
│        │                   │                    │                │
│        ▼                   ▼                    ▼                │
│  ┌──────────────────────────────────────────────────┐           │
│  │              TOOLS LAYER                          │           │
│  ├──────────────────────────────────────────────────┤           │
│  │ • DSPVerificationTool (PDF parsing, fuzzy match) │           │
│  │ • FirecrawlExtractor  (HTML → Markdown)          │           │
│  │ • LLMExtractor        (GPT-4o extraction)        │           │
│  │ • SupabaseTool        (Database operations)      │           │
│  └──────────────────────────────────────────────────┘           │
│                                                                   │
└───────────────────────────┬───────────────────────────────────────┘
                            │
                            ▼
                 ┌────────────────────┐
                 │    SUPABASE DB     │
                 │   (PostgreSQL)     │
                 ├────────────────────┤
                 │ • companies        │
                 │ • locations (+GIS) │
                 │ • services         │
                 │ • contacts         │
                 │ • reports          │
                 └────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│                      USER INTERFACE                               │
│                    (Frontend - Next.js 14)                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌───────────────┐  ┌──────────────┐  ┌────────────────┐       │
│  │   Homepage    │  │   Company    │  │    Map View    │       │
│  │  (Directory)  │  │   Profile    │  │  (Geospatial)  │       │
│  └───────────────┘  └──────────────┘  └────────────────┘       │
│                                                                   │
│  ┌────────────────────────────────────────────────────┐         │
│  │            COMPONENTS LAYER                         │         │
│  ├────────────────────────────────────────────────────┤         │
│  │ • CompanyCard    (display company info)            │         │
│  │ • SearchInput    (debounced search)                │         │
│  │ • FilterPanel    (service/verification filters)    │         │
│  │ • MapController  (Leaflet integration)             │         │
│  └────────────────────────────────────────────────────┘         │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘

                            │
                            ▼
                  ┌──────────────────┐
                  │      USERS       │
                  │  (Bereaved       │
                  │   Families)      │
                  └──────────────────┘
```

---

## Data Flow

```
1. SCRAPING PIPELINE:

   Seed URLs → Firecrawl → Markdown
                              ↓
                         GPT-4o Analysis
                              ↓
                     Structured JSON Data
                              ↓
                    DSP Verification Check
                              ↓
                   Data Validation (Pydantic)
                              ↓
                  Deduplication Check (CUI/Phone)
                              ↓
                    Supabase Upsert (Insert/Update)


2. USER QUERY FLOW:

   User Search → Next.js Server Component
                        ↓
                 Supabase Query (with PostGIS for geo)
                        ↓
                 Render Results (SSR/ISR)
                        ↓
                 Client Interaction (Search, Filter)
                        ↓
                 Dynamic Updates (Client-side)
```

---

## Technology Stack by Layer

```
┌─────────────────────────────────────────────────────────────┐
│ LAYER                 │ TECHNOLOGIES                         │
├─────────────────────────────────────────────────────────────┤
│ Data Sources          │ • Funeral home websites             │
│                       │ • DSP Timiș authorization list PDF  │
│                       │ • Google Maps / ListaFirme          │
├─────────────────────────────────────────────────────────────┤
│ Web Scraping          │ • Firecrawl API                     │
│                       │ • Playwright (fallback)             │
│                       │ • Requests library                  │
├─────────────────────────────────────────────────────────────┤
│ AI/ML                 │ • OpenAI GPT-4o                     │
│                       │ • LangChain (potential)             │
│                       │ • CrewAI (agent orchestration)      │
├─────────────────────────────────────────────────────────────┤
│ Backend Logic         │ • Python 3.11+                      │
│                       │ • Pydantic (validation)             │
│                       │ • pypdf (PDF parsing)               │
│                       │ • thefuzz (fuzzy matching)          │
├─────────────────────────────────────────────────────────────┤
│ Database              │ • Supabase (managed PostgreSQL)     │
│                       │ • PostGIS (geospatial extension)    │
│                       │ • Row Level Security                │
├─────────────────────────────────────────────────────────────┤
│ Frontend Framework    │ • Next.js 14 (App Router)           │
│                       │ • React 18                          │
│                       │ • TypeScript                        │
├─────────────────────────────────────────────────────────────┤
│ UI/Styling            │ • Tailwind CSS                      │
│                       │ • shadcn/ui components              │
│                       │ • lucide-react (icons)              │
├─────────────────────────────────────────────────────────────┤
│ Mapping               │ • Leaflet                           │
│                       │ • react-leaflet                     │
│                       │ • OpenStreetMap tiles               │
├─────────────────────────────────────────────────────────────┤
│ Deployment            │ • Vercel (frontend hosting)         │
│                       │ • GitHub Actions (scraper cron)     │
│                       │ • Supabase (database hosting)       │
├─────────────────────────────────────────────────────────────┤
│ Monitoring            │ • Vercel Analytics                  │
│                       │ • Sentry (error tracking)           │
│                       │ • Custom logging                    │
└─────────────────────────────────────────────────────────────┘
```

---

## Database Schema (Simplified)

```
┌─────────────────────┐
│     companies       │
├─────────────────────┤
│ id (PK)             │
│ name                │
│ slug (unique)       │
│ motto               │◀─── AI-extracted!
│ fiscal_code         │
│ website             │
│ is_verified         │◀─── DSP-verified!
│ is_non_stop         │
└─────────────────────┘
         │
         │ 1:N
         │
    ┌────┴────┬────────────┬───────────┐
    │         │            │           │
    ▼         ▼            ▼           ▼
┌─────────┐ ┌──────────┐ ┌─────────┐ ┌──────────┐
│contacts │ │locations │ │services │ │ reports  │
├─────────┤ ├──────────┤ ├─────────┤ ├──────────┤
│ type    │ │ address  │ │ service │ │ issue    │
│ value   │ │ geo_point│ │ _tag    │ │ status   │
└─────────┘ └──────────┘ └─────────┘ └──────────┘
              (PostGIS)
```

---

## Security & Compliance

```
┌───────────────────────────────────────────────────────┐
│                  SECURITY LAYERS                       │
├───────────────────────────────────────────────────────┤
│                                                        │
│  1. AUTHENTICATION                                     │
│     • Supabase RLS (Row Level Security)               │
│     • Public: Read-only access                        │
│     • Service Role: Full access (backend only)        │
│                                                        │
│  2. DATA PROTECTION                                    │
│     • Environment variables (not in repo)             │
│     • .gitignore for sensitive files                  │
│     • No PII in public fields                         │
│                                                        │
│  3. GDPR COMPLIANCE                                    │
│     • Data minimization                               │
│     • Removal request workflow                        │
│     • Transparent data collection                     │
│                                                        │
│  4. ETHICAL SCRAPING                                   │
│     • Robots.txt compliance                           │
│     • Rate limiting (2-5s delays)                     │
│     • Transparent user-agent                          │
│     • Business data only (not personal)               │
│                                                        │
└───────────────────────────────────────────────────────┘
```

---

## Deployment Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    PRODUCTION SETUP                       │
└──────────────────────────────────────────────────────────┘

    ┌─────────────────┐
    │  GitHub Repo    │
    └────────┬────────┘
             │
      ┌──────┴──────┐
      │             │
      ▼             ▼
┌──────────┐  ┌─────────────┐
│  Vercel  │  │GitHub Actions│
│(Frontend)│  │  (Scraper)   │
└────┬─────┘  └──────┬──────┘
     │               │
     │               │
     └───────┬───────┘
             │
             ▼
      ┌─────────────┐
      │  Supabase   │
      │ (Database)  │
      └─────────────┘
             │
             ▼
      ┌─────────────┐
      │    Users    │
      └─────────────┘

• Frontend auto-deploys on git push
• Scraper runs weekly (cron schedule)
• Database is always-available (99.9% SLA)
```

---

## File Organization

```
Backend Structure:
backend/
├── agents/          # AI agent definitions
├── tools/           # Reusable tools (4 implemented)
├── config/          # Settings and environment
├── data/            # Seed URLs, DSP PDF
├── models.py        # Data models (Pydantic)
├── utils.py         # Helper functions
├── main.py          # Orchestrator
└── verify_setup.py  # Setup checker

Frontend Structure:
frontend/src/
├── app/             # Next.js pages (routes)
├── components/      # React components
│   └── ui/          # shadcn/ui primitives
├── lib/             # Utilities and clients
│   ├── supabase.ts  # DB client
│   └── utils.ts     # Helpers
└── types/           # TypeScript definitions
```

---

**This architecture enables:**
- ✅ Scalable data collection
- ✅ Intelligent extraction
- ✅ Fast, SEO-friendly frontend
- ✅ Geographic search capabilities
- ✅ Automated maintenance
- ✅ GDPR compliance
