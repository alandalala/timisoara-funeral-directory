"""
Process URLs one by one with detailed logging.
"""
import sys
import logging
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from main import FuneralDirectoryScraper

# Setup logging
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = f"scrape_batch_{timestamp}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# URLs to process (excluding directories and already processed)
urls = [
    "https://serviciifunerare-timisoara.ro/",
    "https://funeraretimisoara.ro/",
    "http://servicii-funerare-timisoara.ro/",
    "https://funerarotim.ro/",
    "https://www.denisalex.ro/",
    "https://obelisc.ro/",
]

logger.info("=" * 70)
logger.info("BATCH SCRAPING - Timișoara Funeral Companies")
logger.info(f"Log file: {log_filename}")
logger.info(f"URLs to process: {len(urls)}")
logger.info("=" * 70)

scraper = FuneralDirectoryScraper()

for i, url in enumerate(urls, 1):
    logger.info(f"\n[{i}/{len(urls)}] Processing: {url}")
    try:
        result = scraper.process_url(url)
        if result:
            logger.info(f"[{i}/{len(urls)}] SUCCESS: {url}")
        else:
            logger.info(f"[{i}/{len(urls)}] FAILED/SKIPPED: {url}")
    except Exception as e:
        logger.error(f"[{i}/{len(urls)}] ERROR: {url} - {e}")

logger.info("\n" + "=" * 70)
logger.info("BATCH COMPLETE")
logger.info(f"Processed: {scraper.stats['processed']}")
logger.info(f"Success: {scraper.stats['success']}")
logger.info(f"Failed: {scraper.stats['failed']}")
logger.info(f"Verified: {scraper.stats['verified']}")
logger.info("=" * 70)
