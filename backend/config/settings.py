"""
Configuration settings for the funeral directory scraper.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")

# Scraper Settings
USER_AGENT = "FuneralDirTimisoara/1.0 (+contact@funeraldirectory.ro)"
MIN_DELAY_SECONDS = 2
MAX_DELAY_SECONDS = 5
REQUEST_TIMEOUT = 30

# Agent Settings
LLM_MODEL = "gpt-4o"
LLM_TEMPERATURE = 0.1
MAX_TOKENS = 4000

# Database Settings
BATCH_SIZE = 10

# File Paths
DSP_PDF_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "dsp_authorized_list.pdf")
SEED_URLS_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "seed_urls.json")

# Search Queries
SEARCH_QUERIES = [
    "Servicii funerare Timisoara",
    "Pompe funebre Timis",
    "Repatrieri decedati Timisoara",
    "Casa funerara Timisoara",
]

# Service Taxonomy
SERVICE_TAXONOMY = {
    'transport': 'Transport Funerar',
    'repatriation': 'Repatriere Internațională',
    'cremation': 'Incinerare',
    'embalming': 'Îmbălsămare',
    'wake_house': 'Capelă / Cameră Mortuară',
    'coffins': 'Sicrie',
    'flowers': 'Aranjamente Florale',
    'bureaucracy': 'Acte / Formalități',
    'religious': 'Servicii Religioase',
    'monuments': 'Monumente Funerare',
}

# Validation
assert SUPABASE_URL, "SUPABASE_URL must be set in environment"
assert SUPABASE_SERVICE_KEY, "SUPABASE_SERVICE_KEY must be set in environment"
assert OPENAI_API_KEY, "OPENAI_API_KEY must be set in environment"
