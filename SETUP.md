# Quick Setup Guide

## What Has Been Created

### ✅ Phase 1.1: Repository Structure (COMPLETED)
- Git repository with proper .gitignore
- Project folder structure (frontend/ and backend/)
- Comprehensive README.md

### ✅ Phase 1.3: Frontend (COMPLETED)
- Next.js 14 with App Router and TypeScript
- Tailwind CSS configured
- shadcn/ui components installed (card, button, badge, input, dialog, skeleton)
- Supabase client setup
- TypeScript types defined
- Dependencies: leaflet, react-leaflet, lucide-react

### ✅ Phase 1.4: Backend (COMPLETED)
- Python project structure
- requirements.txt with all dependencies
- Pydantic models for data validation
- Configuration management
- Utility functions (phone normalization, slugify, etc.)
- Tools implemented:
  - DSPVerificationTool (cross-references with official list)
  - FirecrawlExtractorTool (web scraping)
  - LLMExtractorTool (AI data extraction)
  - SupabaseTool (database operations)
- Main orchestration script (main.py)

### 🔲 Phase 1.2: Database Setup (NEXT STEP)
SQL schema file created but needs to be executed in Supabase.

---

## Next Steps to Complete Setup

### Step 1: Set Up Supabase Database

1. **Create a Supabase project:**
   - Go to https://supabase.com
   - Create a new project
   - Wait for provisioning to complete

2. **Execute the database schema:**
   - Open Supabase SQL Editor
   - Copy contents of `database_schema.sql`
   - Execute the SQL script
   - Verify all tables are created

3. **Get your credentials:**
   - Project Settings → API
   - Copy `Project URL`
   - Copy `anon/public key`
   - Copy `service_role key` (for backend only)

### Step 2: Configure Environment Variables

**Backend** (create `backend/.env`):
```bash
SUPABASE_URL=your_project_url
SUPABASE_SERVICE_KEY=your_service_role_key
OPENAI_API_KEY=your_openai_api_key
FIRECRAWL_API_KEY=your_firecrawl_api_key
```

**Frontend** (create `frontend/.env.local`):
```bash
NEXT_PUBLIC_SUPABASE_URL=your_project_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
```

### Step 3: Set Up Backend Python Environment

```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

### Step 4: Add Seed URLs

Edit `backend/data/seed_urls.json` and add funeral home URLs:

```json
[
  "https://serviciifunerare-timisoara.ro/",
  "https://casafuneraramara.ro/",
  "https://www.funeraliatm.ro/",
  "https://angelshousefuneral.ro/"
]
```

### Step 5: Download DSP Authorization List (Optional but Recommended)

1. Download from: https://www.dsptimis.ro/public/data_files/media/comparimente/avize-autorizatii/
2. Save as `backend/data/dsp_authorized_list.pdf`
3. This enables verification of authorized funeral homes

### Step 6: Test the Backend Scraper

```powershell
cd backend
.venv\Scripts\activate
python main.py
```

The scraper will:
- Load seed URLs
- Scrape each website
- Extract structured data with AI
- Verify against DSP list
- Store in Supabase

### Step 7: Run the Frontend

```powershell
cd frontend
npm run dev
```

Visit http://localhost:3000

---

## Project Structure

```
timisoara-funeral-directory/
├── backend/
│   ├── agents/           # CrewAI agents (to be implemented)
│   ├── tools/            # ✅ Implemented tools
│   │   ├── dsp_verification.py
│   │   ├── firecrawl_extractor.py
│   │   ├── llm_extractor.py
│   │   └── supabase_tool.py
│   ├── config/
│   │   └── settings.py   # ✅ Configuration
│   ├── data/
│   │   ├── seed_urls.json
│   │   └── dsp_authorized_list.pdf (download this)
│   ├── models.py         # ✅ Pydantic models
│   ├── utils.py          # ✅ Utility functions
│   ├── main.py           # ✅ Main orchestrator
│   └── requirements.txt  # ✅ Dependencies
│
├── frontend/
│   ├── src/
│   │   ├── app/          # Next.js pages (to be created)
│   │   ├── components/   # React components (to be created)
│   │   │   └── ui/       # ✅ shadcn/ui components
│   │   ├── lib/
│   │   │   ├── supabase.ts  # ✅ Supabase client
│   │   │   └── utils.ts     # ✅ Utility functions
│   │   └── types/
│   │       └── index.ts     # ✅ TypeScript types
│   └── package.json      # ✅ Dependencies installed
│
├── database_schema.sql   # ✅ SQL schema
├── .gitignore           # ✅ Git ignore rules
└── README.md            # ✅ Project documentation
```

---

## API Keys You'll Need

1. **Supabase** (free tier available): https://supabase.com
2. **OpenAI API** (for GPT-4o): https://platform.openai.com/api-keys
3. **Firecrawl API** (for web scraping): https://firecrawl.dev

---

## What's Next After Setup

Once the infrastructure is running, continue with:

- **Phase 2**: Implement CrewAI agents (Scout, Analyst, Auditor)
- **Phase 3**: Build frontend components and pages
- **Phase 4**: Create API routes
- **Phase 5**: Add tests
- **Phase 6**: Deploy to production
- **Phase 7**: Complete documentation

---

## Troubleshooting

### Backend Issues

**"ModuleNotFoundError"**: Activate the virtual environment
```powershell
cd backend
.venv\Scripts\activate
```

**"API key not found"**: Check your `.env` file in the backend folder

**"Supabase connection failed"**: Verify your SUPABASE_URL and SUPABASE_SERVICE_KEY

### Frontend Issues

**"Missing Supabase environment variables"**: Create `.env.local` in the frontend folder

**"Module not found"**: Run `npm install` in the frontend folder

**Port already in use**: Change port with `npm run dev -- -p 3001`

---

## Current Implementation Status

| Component | Status | Notes |
|-----------|--------|-------|
| Repository Structure | ✅ Complete | All folders and config files |
| Backend Models | ✅ Complete | Pydantic validation models |
| Backend Tools | ✅ Complete | All 4 tools implemented |
| Backend Orchestrator | ✅ Complete | main.py ready to run |
| Database Schema | ✅ Created | Needs execution in Supabase |
| Frontend Scaffold | ✅ Complete | Next.js with all dependencies |
| Frontend Components | 🔲 Pending | Phase 3 |
| Frontend Pages | 🔲 Pending | Phase 3 |
| API Routes | 🔲 Pending | Phase 4 |
| Tests | 🔲 Pending | Phase 5 |
| Deployment | 🔲 Pending | Phase 6 |

---

## Support

If you encounter issues:
1. Check this SETUP.md file
2. Review the main README.md
3. Check the task list in Developer_Task_List_Funeral_Directory.md
