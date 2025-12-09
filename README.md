# Timișoara Funeral Services Directory

A semantic web directory for funeral services in Timișoara, Romania, featuring AI-powered data extraction, DSP verification, and a high-performance Next.js frontend.

## 🏗️ Tech Stack

- **Frontend**: Next.js 14 (App Router), TypeScript, Tailwind CSS, shadcn/ui
- **Backend**: Python, CrewAI, Firecrawl, Playwright
- **Database**: Supabase (PostgreSQL + PostGIS)
- **Deployment**: Vercel (Frontend), GitHub Actions (Backend Scraper)

## 📋 Features

- 🤖 **AI-Powered Data Extraction**: Autonomous agents extract company mottos and ethos statements
- ✅ **DSP Verification**: Cross-reference with official authorization list from Direcția de Sănătate Publică
- 🗺️ **Interactive Map**: Geospatial search with PostGIS
- 🔍 **Semantic Filtering**: Filter by service philosophy, not just price or location
- 📱 **Mobile-First**: Responsive design with one-tap calling
- 🔒 **GDPR Compliant**: Data minimization and erasure requests supported

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ 
- Python 3.11+
- Supabase account
- OpenAI API key
- Firecrawl API key

### Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env.local
# Add your Supabase credentials to .env.local
npm run dev
```

### Backend Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # On Windows
# source .venv/bin/activate  # On Unix
pip install -r requirements.txt
playwright install chromium
cp .env.example .env
# Add your API keys to .env
python main.py
```

## 📊 Database Schema

The project uses PostgreSQL with PostGIS extension for geospatial queries:

- **companies**: Core business entities with mottos and verification status
- **locations**: Physical addresses with geography points
- **services**: Service offerings (cremation, repatriation, etc.)
- **contacts**: Phone, email, and other contact methods

See `docs/schema.sql` for full DDL.

## 🤖 Scraper Architecture

The data acquisition pipeline uses CrewAI agents:

1. **Scout Agent**: Discovers funeral homes from search queries
2. **Analyst Agent**: Extracts structured data using LLMs
3. **Auditor Agent**: Validates and deduplicates before database insertion

## 📝 Environment Variables

### Frontend (.env.local)
```
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
```

### Backend (.env)
```
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_KEY=your_service_role_key
OPENAI_API_KEY=your_openai_key
FIRECRAWL_API_KEY=your_firecrawl_key
```

## 🧪 Testing

```bash
# Frontend tests
cd frontend
npm run test

# Backend tests
cd backend
pytest
```

## 📦 Deployment

### Frontend
The frontend auto-deploys to Vercel on push to main branch.

### Backend Scraper
Runs weekly via GitHub Actions (Sundays at midnight).

## 📖 Documentation

- [Architecture Blueprint](docs/architecture.md)
- [API Documentation](docs/api.md)
- [Contributing Guidelines](CONTRIBUTING.md)

## ⚖️ Legal & Ethics

This project adheres to:
- GDPR data protection regulations
- Robots.txt compliance
- Rate limiting to avoid server overload
- Transparent user-agent identification

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please read CONTRIBUTING.md first.

## 📧 Contact

For data removal requests or inquiries: contact@funeraldirectory.ro
