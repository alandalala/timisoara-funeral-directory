"""Clean up database and all progress files."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from tools.supabase_tool import SupabaseTool

# Clean database
print("🗑️ Cleaning database...")
tool = SupabaseTool()
client = tool.client

r2 = client.table('contacts').delete().neq('company_id', '00000000-0000-0000-0000-000000000000').execute()
print(f"  Deleted {len(r2.data)} contacts")

r3 = client.table('locations').delete().neq('company_id', '00000000-0000-0000-0000-000000000000').execute()
print(f"  Deleted {len(r3.data)} locations")

r4 = client.table('companies').delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
print(f"  Deleted {len(r4.data)} companies")

# Clean progress files
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

# Clean scraped data
scraped_dir = data_dir / "scraped"
if scraped_dir.exists():
    for f in scraped_dir.glob("maps_*.json"):
        f.unlink()
        print(f"  Deleted {f.name}")

print("\n✅ Cleanup complete!")
