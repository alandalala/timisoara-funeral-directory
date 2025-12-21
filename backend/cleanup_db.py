"""Clean up database and optionally progress files."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from tools.supabase_tool import SupabaseTool

def cleanup_database(keep_scraped_files: bool = True):
    """
    Clean up all company-related data from the database.
    
    Args:
        keep_scraped_files: If True, keeps the scraped JSON files (default)
    """
    # Clean database
    print("🗑️ Cleaning database...")
    tool = SupabaseTool()
    client = tool.client

    # Delete in order of dependencies (child tables first)
    try:
        r1 = client.table('review_summaries').delete().neq('company_id', '00000000-0000-0000-0000-000000000000').execute()
        print(f"  Deleted {len(r1.data)} review summaries")
    except Exception as e:
        print(f"  review_summaries: {e}")

    try:
        r2 = client.table('reviews').delete().neq('company_id', '00000000-0000-0000-0000-000000000000').execute()
        print(f"  Deleted {len(r2.data)} reviews")
    except Exception as e:
        print(f"  reviews: {e}")

    try:
        r3 = client.table('reports').delete().neq('company_id', '00000000-0000-0000-0000-000000000000').execute()
        print(f"  Deleted {len(r3.data)} reports")
    except Exception as e:
        print(f"  reports: {e}")

    try:
        r4 = client.table('removal_requests').delete().neq('company_id', '00000000-0000-0000-0000-000000000000').execute()
        print(f"  Deleted {len(r4.data)} removal requests")
    except Exception as e:
        print(f"  removal_requests: {e}")

    try:
        r5 = client.table('services').delete().neq('company_id', '00000000-0000-0000-0000-000000000000').execute()
        print(f"  Deleted {len(r5.data)} services")
    except Exception as e:
        print(f"  services: {e}")

    try:
        r6 = client.table('contacts').delete().neq('company_id', '00000000-0000-0000-0000-000000000000').execute()
        print(f"  Deleted {len(r6.data)} contacts")
    except Exception as e:
        print(f"  contacts: {e}")

    try:
        r7 = client.table('locations').delete().neq('company_id', '00000000-0000-0000-0000-000000000000').execute()
        print(f"  Deleted {len(r7.data)} locations")
    except Exception as e:
        print(f"  locations: {e}")

    try:
        r8 = client.table('companies').delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
        print(f"  Deleted {len(r8.data)} companies")
    except Exception as e:
        print(f"  companies: {e}")

    # Clean progress files (but NOT scraped data)
    data_dir = Path(__file__).parent / "data"
    progress_files = [
        data_dir / "workflow_progress.json",
        data_dir / "scrape_progress.json",
    ]

    print("\n🗑️ Cleaning progress files...")
    for f in progress_files:
        if f.exists():
            f.unlink()
            print(f"  Deleted {f.name}")
        else:
            print(f"  {f.name} not found")

    # Only clean scraped data if explicitly requested
    if not keep_scraped_files:
        scraped_dir = data_dir / "scraped"
        if scraped_dir.exists():
            print("\n🗑️ Cleaning scraped JSON files...")
            for f in scraped_dir.glob("maps_*.json"):
                f.unlink()
                print(f"  Deleted {f.name}")
    else:
        print("\n📁 Keeping scraped JSON files (use --clean-scraped to remove them)")

    print("\n✅ Database cleanup complete!")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Clean up database")
    parser.add_argument("--clean-scraped", action="store_true", 
                        help="Also delete scraped JSON files")
    args = parser.parse_args()
    
    cleanup_database(keep_scraped_files=not args.clean_scraped)
