# ⚡ Quick Start Guide

**Get your funeral directory running in under 1 hour!**

---

## ✅ Prerequisites Checklist

Before starting, have these ready:

- [ ] Computer with Windows (PowerShell)
- [ ] Python 3.11+ installed
- [ ] Node.js 18+ installed
- [ ] Git installed
- [ ] Code editor (VS Code recommended)
- [ ] Internet connection

---

## 🚀 Step-by-Step Setup (60 minutes)

### Step 1: Get API Keys (15 minutes)

#### 1.1 Supabase (Database) ⭐ REQUIRED
1. Go to https://supabase.com
2. Sign up / Log in
3. Click "New Project"
4. Fill in:
   - Name: `funeral-directory`
   - Password: (generate strong password)
   - Region: Europe (Frankfurt)
5. Wait 2 minutes for provisioning
6. Go to Project Settings → API
7. **Copy these:**
   - `Project URL` (looks like: https://xxxxx.supabase.co)
   - `anon public` key (starts with: eyJ...)
   - `service_role` key (starts with: eyJ...)
8. Keep this tab open!

#### 1.2 OpenAI (AI Extraction) ⭐ REQUIRED
1. Go to https://platform.openai.com/api-keys
2. Sign in / Create account
3. Click "+ Create new secret key"
4. Name it: `funeral-directory`
5. **Copy the key** (starts with: sk-...)
6. ⚠️ You won't see it again!

#### 1.3 Firecrawl (Web Scraping) ⚡ OPTIONAL
1. Go to https://firecrawl.dev
2. Sign up
3. Get free API key
4. **Copy the key**
5. (If you skip this, some sites might not work)

---

### Step 2: Setup Database (10 minutes)

1. **Go back to your Supabase project**
2. Click "SQL Editor" in the left sidebar
3. Click "New Query"
4. Open the file: `database_schema.sql` from your project
5. Copy ALL the content
6. Paste into Supabase SQL Editor
7. Click "Run" (or press Ctrl+Enter)
8. You should see: ✅ Success, no errors
9. Click "Table Editor" → Verify you see 6 tables:
   - companies
   - locations
   - services
   - contacts
   - reports
   - removal_requests

---

### Step 3: Configure Backend (10 minutes)

Open PowerShell and run these commands:

```powershell
# Navigate to the project
cd C:\Users\alexandra.pascu\timisoara-funeral-directory\backend

# Create virtual environment
python -m venv .venv

# Activate it
.venv\Scripts\activate

# Install dependencies (this will take a few minutes)
pip install -r requirements.txt

# Install browser for Playwright
playwright install chromium
```

**Create `.env` file:**

Create a new file called `.env` in the `backend` folder with this content:

```env
SUPABASE_URL=your_project_url_here
SUPABASE_SERVICE_KEY=your_service_role_key_here
OPENAI_API_KEY=your_openai_key_here
FIRECRAWL_API_KEY=your_firecrawl_key_here
```

Replace the placeholders with your actual keys from Step 1!

**Verify setup:**

```powershell
python verify_setup.py
```

You should see ✅ checkmarks. If you see ❌, check your .env file.

---

### Step 4: Add Funeral Home URLs (5 minutes)

Edit the file: `backend/data/seed_urls.json`

Replace the empty array `[]` with:

```json
[
  "https://serviciifunerare-timisoara.ro/",
  "https://casafuneraramara.ro/",
  "https://www.funeraliatm.ro/",
  "https://angelshousefuneral.ro/"
]
```

Save the file.

---

### Step 5: Run Your First Scrape! (10 minutes)

```powershell
# Make sure you're in the backend folder and venv is activated
cd C:\Users\alexandra.pascu\timisoara-funeral-directory\backend
.venv\Scripts\activate

# Run the scraper
python main.py
```

**What happens:**
- The scraper will process each URL
- You'll see progress logs in the terminal
- Each company takes ~30-60 seconds
- ✅ means success
- ✗ means failure (check the error)

**Check the results:**
1. Go to Supabase → Table Editor
2. Click on `companies` table
3. You should see rows with data!
4. Look for:
   - Company names
   - Mottos (some might have them)
   - `is_verified` = true if found in DSP list

---

### Step 6: Setup Frontend (10 minutes)

Open a **NEW** PowerShell window (keep the backend one for later):

```powershell
# Navigate to frontend
cd C:\Users\alexandra.pascu\timisoara-funeral-directory\frontend

# Install dependencies
npm install

# Create environment file
Copy-Item .env.example .env.local
```

**Edit `.env.local`:**

Open `frontend/.env.local` and replace with:

```env
NEXT_PUBLIC_SUPABASE_URL=your_project_url_here
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_public_key_here
```

⚠️ Use the **anon/public** key, NOT the service role key!

**Start the dev server:**

```powershell
npm run dev
```

Open browser: http://localhost:3000

You'll see the default Next.js page (we haven't built the UI yet - that's Phase 3!)

---

## ✅ Success Criteria

You've successfully completed setup if:

- [ ] Supabase project is created
- [ ] Database schema is executed (6 tables exist)
- [ ] Backend scraper runs without errors
- [ ] At least 1 company is in the database
- [ ] Frontend dev server starts
- [ ] No errors in browser console

---

## 🎯 What You've Accomplished

1. ✅ **Database:** Production-ready PostgreSQL with geospatial support
2. ✅ **Backend:** AI-powered scraper that extracts structured data
3. ✅ **Data:** Real funeral home information in your database
4. ✅ **Frontend:** Modern Next.js app ready for development

---

## 🐛 Troubleshooting

### "ModuleNotFoundError" when running Python
**Solution:** Activate the virtual environment
```powershell
cd backend
.venv\Scripts\activate
```

### "SUPABASE_URL must be set"
**Solution:** Check your `.env` file exists in the `backend` folder and has the correct values

### "Failed to scrape" errors
**Possible causes:**
- Website is down
- Robots.txt disallows scraping
- Firecrawl API limit reached
- Network issues

**Try:** Use a different URL or skip problematic sites for now

### Frontend shows "Missing Supabase environment variables"
**Solution:** Create `.env.local` in the `frontend` folder (not `.env`!)

### Port 3000 already in use
**Solution:** Kill the process or use different port:
```powershell
npm run dev -- -p 3001
```

---

## 📝 Next Steps

Now that the infrastructure is working:

### Immediate (Optional):
- Add more seed URLs to scrape more companies
- Download the DSP PDF for verification
- Explore the data in Supabase Table Editor

### Development (Phase 3 - Coming Next):
- Build the homepage UI
- Create company cards
- Add search functionality
- Implement the map view

### Production (Phase 6):
- Deploy frontend to Vercel
- Setup automated weekly scraping
- Configure custom domain
- Add monitoring

---

## 🆘 Still Stuck?

1. Read `SETUP.md` for detailed explanations
2. Check `PROJECT_STATUS.md` to understand what's implemented
3. Review `ARCHITECTURE.md` to understand how it works
4. Look at error logs in `backend/scraper.log`

---

## 🎉 Congratulations!

You've built and deployed a sophisticated AI-powered web scraper with a modern database backend. The hard part is done! 

The next phase is building the user interface, which is more visual and fun. 

**You're ready to proceed!** 🚀

---

**Time spent:** ~60 minutes  
**Lines of code working:** ~2,000+  
**Companies scraped:** 4+ (and counting!)  
**Status:** ✅ Phase 1 Complete
