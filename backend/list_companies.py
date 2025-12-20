"""List companies in the database"""
from tools.supabase_tool import SupabaseTool

db = SupabaseTool()
result = db.client.table('companies').select('name, website').execute()
print(f"\nTotal companies: {len(result.data)}\n")
for c in result.data:
    print(f"- {c['name']} ({c['website']})")
