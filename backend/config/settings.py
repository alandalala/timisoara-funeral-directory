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

# Scraper Settings - Human-like behavior
MIN_DELAY_SECONDS = 3
MAX_DELAY_SECONDS = 8
REQUEST_TIMEOUT = 30

# Rotating User Agents (realistic browser signatures)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
]

# Legacy single user agent (for backwards compatibility)
USER_AGENT = USER_AGENTS[0]

# Agent Settings
LLM_PROVIDER = "ollama"  # "openai" or "ollama"
OLLAMA_BASE_URL = "http://192.168.50.212:11434"
OLLAMA_MODEL = "qwen3:32b"
LLM_MODEL = "gpt-4o"  # Fallback for OpenAI
LLM_TEMPERATURE = 0.1
MAX_TOKENS = 4000

# Database Settings
BATCH_SIZE = 10

# File Paths
DSP_PDF_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "dsp_authorized_list.pdf")
SEED_URLS_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "seed_urls.json")

# Search Queries - expanded for better coverage
SEARCH_QUERIES = [
    # Core funeral terms
    "funerare timisoara",
    "servicii funerare timisoara",
    "pompe funebre timisoara",
    "firma pompe funebre timisoara",
    "casa funerara timisoara",
    "agentie funerara timisoara",
    # County-level searches
    "servicii funerare timis",
    "pompe funebre judetul timis",
    # Service-specific
    "repatriere decedat timisoara",
    "transport funerar timisoara",
    "sicrie timisoara",
    "coroane funerare timisoara",
    "inmormantare timisoara",
    # Alternative spellings/terms
    "servicii mortuare timisoara",
    "capela mortuara timisoara",
    "firma funerara timisoara",
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
