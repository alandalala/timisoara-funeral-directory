"""
Automated scrape + import workflow for all Romanian counties.
Runs unattended: scrape county → import to Supabase → next county → repeat

Usage:
    python scrape_and_import.py --all              # Process all counties
    python scrape_and_import.py --county "Bihor"   # Single county
    python scrape_and_import.py --all --no-headless  # Debug mode
"""
import json
import logging
import time
import argparse
from pathlib import Path
from datetime import datetime
from scrape_romania import RomaniaScraper, CITIES_FILE, OUTPUT_DIR
from import_googlemaps import import_googlemaps_json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

WORKFLOW_PROGRESS_FILE = Path(__file__).parent / "data" / "workflow_progress.json"
COUNTY_DELAY_SECONDS = 10  # Pause between counties to avoid rate limits


class AutomatedWorkflow:
    """Orchestrates scraping and importing for all Romanian counties."""
    
    def __init__(self, headless: bool = True, enrich: bool = True):
        self.headless = headless
        self.enrich = enrich
        self.progress = self._load_progress()
        self.stop_requested = False
    
    def _load_progress(self) -> dict:
        """Load workflow progress from file."""
        if WORKFLOW_PROGRESS_FILE.exists():
            with open(WORKFLOW_PROGRESS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "started_at": datetime.now().isoformat(),
            "imported_counties": [],
            "import_stats": {}
        }
    
    def _save_progress(self):
        """Save workflow progress to file."""
        self.progress["last_updated"] = datetime.now().isoformat()
        WORKFLOW_PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(WORKFLOW_PROGRESS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.progress, f, indent=2, ensure_ascii=False)
        logger.info(f"💾 Workflow progress saved to {WORKFLOW_PROGRESS_FILE}")
    
    def _get_county_file(self, county_name: str) -> Path:
        """Get the output JSON file path for a county."""
        slug = county_name.lower().replace(' ', '_').replace('-', '_')
        # Normalize Romanian characters
        replacements = [('ș', 's'), ('ț', 't'), ('ă', 'a'), ('â', 'a'), ('î', 'i')]
        for char, repl in replacements:
            slug = slug.replace(char, repl)
        return OUTPUT_DIR / f"maps_{slug}.json"
    
    def _get_all_counties(self) -> list:
        """Load all counties from config file."""
        with open(CITIES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)['counties']
    
    def run(self, counties: list = None, resume: bool = True):
        """
        Run full workflow: scrape + import for each county.
        
        Args:
            counties: List of county names to process. None = all counties.
            resume: Skip already imported counties.
        """
        all_counties = self._get_all_counties()
        
        # Filter to specific counties if provided
        if counties:
            all_counties = [c for c in all_counties if c['name'] in counties]
            if not all_counties:
                logger.error(f"No matching counties found for: {counties}")
                return
        
        # Filter out already imported counties (if resume=True)
        imported = set(self.progress.get('imported_counties', []))
        if resume:
            pending = [c for c in all_counties if c['name'] not in imported]
        else:
            pending = all_counties
        
        total_counties = len(all_counties)
        already_done = len(imported)
        to_process = len(pending)
        
        logger.info(f"\n{'='*60}")
        logger.info(f"🇷🇴 AUTOMATED WORKFLOW STARTING")
        logger.info(f"{'='*60}")
        logger.info(f"Total counties: {total_counties}")
        logger.info(f"Already imported: {already_done}")
        logger.info(f"To process: {to_process}")
        logger.info(f"{'='*60}\n")
        
        if to_process == 0:
            logger.info("✅ All counties already imported!")
            return
        
        for idx, county_data in enumerate(pending, 1):
            county_name = county_data['name']
            
            logger.info(f"\n{'='*60}")
            logger.info(f"📍 COUNTY {idx}/{to_process}: {county_name}")
            logger.info(f"{'='*60}")
            
            # Step 1: Scrape the county (skip if already scraped)
            county_file = self._get_county_file(county_name)
            if county_file.exists():
                logger.info(f"📁 Found existing data: {county_file.name} - skipping scrape")
                success = True
            else:
                success = self._scrape_county(county_name)
            
            if self.stop_requested:
                logger.warning("🛑 Stop requested - saving progress and exiting")
                self._save_progress()
                break
            
            if not success:
                logger.error(f"❌ Scraping failed for {county_name}, skipping import")
                continue
            
            # Step 2: Import to Supabase
            import_result = self._import_county(county_name)
            
            if import_result:
                # Mark as imported only on success
                self.progress['imported_counties'].append(county_name)
                self.progress['import_stats'][county_name] = import_result
                self._save_progress()
                
                logger.info(f"✅ {county_name} complete: {import_result['success']} imported, "
                           f"{import_result['failed']} failed, {import_result['skipped']} skipped")
            
            # Delay between counties to avoid rate limits
            if idx < to_process:
                logger.info(f"⏳ Waiting {COUNTY_DELAY_SECONDS}s before next county...")
                time.sleep(COUNTY_DELAY_SECONDS)
        
        # Final summary
        self._print_summary()
    
    def _scrape_county(self, county_name: str) -> bool:
        """Scrape a single county. Returns True on success."""
        try:
            logger.info(f"🔍 Scraping {county_name}...")
            
            # Create new scraper instance for each county (fresh browser)
            scraper = RomaniaScraper(headless=self.headless, enrich=self.enrich)
            scraper.scrape(counties=[county_name], resume=True)
            
            if scraper.stop_requested:
                self.stop_requested = True
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error scraping {county_name}: {e}")
            return False
    
    def _import_county(self, county_name: str) -> dict:
        """Import a county's data to Supabase. Returns result dict or None on failure."""
        county_file = self._get_county_file(county_name)
        
        if not county_file.exists():
            logger.warning(f"⚠️ No data file found: {county_file}")
            return None
        
        try:
            logger.info(f"📤 Importing {county_name} to Supabase...")
            result = import_googlemaps_json(str(county_file), dry_run=False)
            return result
            
        except Exception as e:
            logger.error(f"❌ Error importing {county_name}: {e}")
            return None
    
    def _print_summary(self):
        """Print final workflow summary."""
        imported = self.progress.get('imported_counties', [])
        stats = self.progress.get('import_stats', {})
        
        total_success = sum(s.get('success', 0) for s in stats.values())
        total_failed = sum(s.get('failed', 0) for s in stats.values())
        total_skipped = sum(s.get('skipped', 0) for s in stats.values())
        
        logger.info(f"\n{'='*60}")
        logger.info(f"📊 WORKFLOW SUMMARY")
        logger.info(f"{'='*60}")
        logger.info(f"Counties imported: {len(imported)}/42")
        logger.info(f"Total businesses imported: {total_success}")
        logger.info(f"Total failed: {total_failed}")
        logger.info(f"Total skipped: {total_skipped}")
        logger.info(f"{'='*60}")
        
        if len(imported) == 42:
            logger.info("🎉 ALL COUNTIES COMPLETE!")
        else:
            remaining = 42 - len(imported)
            logger.info(f"📋 Remaining: {remaining} counties")


def main():
    parser = argparse.ArgumentParser(
        description='Automated scrape + import workflow for Romanian funeral directory'
    )
    parser.add_argument('--county', help='Process a single county')
    parser.add_argument('--counties', nargs='+', help='Process multiple counties')
    parser.add_argument('--all', action='store_true', help='Process all 42 counties')
    parser.add_argument('--no-resume', action='store_true', help='Re-process already imported counties')
    parser.add_argument('--no-headless', action='store_true', help='Show browser (debug mode)')
    parser.add_argument('--no-enrich', action='store_true', help='Skip website enrichment')
    parser.add_argument('--status', action='store_true', help='Show current workflow status')
    
    args = parser.parse_args()
    
    # Status check
    if args.status:
        if WORKFLOW_PROGRESS_FILE.exists():
            with open(WORKFLOW_PROGRESS_FILE, 'r', encoding='utf-8') as f:
                progress = json.load(f)
            imported = progress.get('imported_counties', [])
            print(f"\n📊 Workflow Status:")
            print(f"   Counties imported: {len(imported)}/42")
            print(f"   Imported: {', '.join(imported) if imported else 'None'}")
        else:
            print("\n📊 No workflow progress found. Run with --all to start.")
        return
    
    # Determine counties to process
    counties = None
    if args.county:
        counties = [args.county]
    elif args.counties:
        counties = args.counties
    elif not args.all:
        parser.print_help()
        print("\n⚠️  Please specify --county, --counties, or --all")
        return
    
    # Run workflow
    workflow = AutomatedWorkflow(
        headless=not args.no_headless,
        enrich=not args.no_enrich
    )
    
    workflow.run(counties=counties, resume=not args.no_resume)


if __name__ == "__main__":
    main()
