"""Check all companies in database"""
from tools.supabase_tool import SupabaseTool

def main():
    db = SupabaseTool()
    result = db.client.table('companies').select('name, is_verified').execute()
    
    print(f"\n{'='*60}")
    print(f"Total companies: {len(result.data)}")
    print(f"{'='*60}")
    
    verified = 0
    for c in result.data:
        status = "✅ VERIFIED" if c.get('is_verified') else "❌ Not verified"
        print(f"  {c['name'][:40]:40} | {status}")
        if c.get('is_verified'):
            verified += 1
    
    print(f"{'='*60}")
    print(f"Verified: {verified}/{len(result.data)}")

if __name__ == "__main__":
    main()
