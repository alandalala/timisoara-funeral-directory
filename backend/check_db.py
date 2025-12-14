"""Check DB status and DSP verification"""
from tools.supabase_tool import SupabaseTool
from tools.dsp_verification import DSPVerificationTool

db = SupabaseTool()
v = DSPVerificationTool()

# Check companies and their locations
companies = db.client.table('companies').select('id,name,is_verified').execute()
locations = db.client.table('locations').select('company_id,city,county').execute()

# Create location lookup
loc_by_company = {}
for loc in locations.data:
    loc_by_company[loc['company_id']] = loc

print("Companies, Locations, and DSP verification:")
for c in companies.data:
    name = c['name']
    company_id = c['id']
    loc = loc_by_company.get(company_id, {})
    city = loc.get('city', 'N/A')
    county = loc.get('county', 'N/A')
    
    db_verified = "DB:YES" if c['is_verified'] else "DB:NO"
    
    # Test verification without county filter (like we're getting 0% in scraper)
    result_no_county = v.verify_company(name)
    
    # Test with county
    result_with_county = v.verify_company(name, county=county)
    
    print(f"\n{name}")
    print(f"  Location: {city}, {county}")
    print(f"  {db_verified}")
    print(f"  DSP (no county filter): score={result_no_county.get('match_score')}%")
    print(f"  DSP (with county={county}): score={result_with_county.get('match_score')}%")
