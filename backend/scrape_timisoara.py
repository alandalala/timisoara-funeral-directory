"""
Comprehensive Timișoara funeral companies scraper with detailed logging.
"""
import sys
import logging
from pathlib import Path
from datetime import datetime

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from main import FuneralDirectoryScraper

# Create timestamped log file
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = f"scrape_timisoara_{timestamp}.log"

# Setup detailed logging to file
file_handler = logging.FileHandler(log_filename, encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Get root logger and add handlers
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
root_logger.handlers = []  # Clear existing handlers
root_logger.addHandler(file_handler)
root_logger.addHandler(console_handler)

logger = logging.getLogger(__name__)

def main():
    logger.info("=" * 70)
    logger.info("TIMIȘOARA FUNERAL DIRECTORY - COMPREHENSIVE SCRAPE")
    logger.info(f"Log file: {log_filename}")
    logger.info("=" * 70)
    logger.info("")
    logger.info("Validation rules:")
    logger.info("  - Location must be in Timișoara or Timiș county")
    logger.info("  - Companies with >5 phone numbers are filtered (likely directories)")
    logger.info("  - Address will be geocoded with street-level precision when possible")
    logger.info("")
    
    # Initialize scraper
    scraper = FuneralDirectoryScraper()
    
    # Run with search mode to find all funeral homes in Timișoara
    logger.info("Starting search for funeral homes in Timișoara...")
    logger.info("")
    
    # Search for more results (20 to get a good sample)
    scraper.run(search_mode=True, max_results=20)
    
    logger.info("")
    logger.info("=" * 70)
    logger.info(f"Scraping completed. Full log saved to: {log_filename}")
    logger.info("=" * 70)

if __name__ == "__main__":
    main()
