"""Update is_verified flag for existing companies in DB"""
from tools.supabase_tool import SupabaseTool
from tools.dsp_verification import DSPVerificationTool

def update_verification_status():
    db = SupabaseTool()
    verifier = DSPVerificationTool()
    
    # Get all companies with their locations
    companies = db.client.table('companies').select('id,name').execute()
    locations = db.client.table('locations').select('company_id,county').execute()
    
    # Create location lookup
    county_by_company = {}
    for loc in locations.data:
        county_by_company[loc['company_id']] = loc.get('county')
    
    updated = 0
    verified = 0
    
    print("Updating verification status for all companies...\n")
    
    for company in companies.data:
        company_id = company['id']
        name = company['name']
        county = county_by_company.get(company_id)
        
        # Verify against DSP
        result = verifier.verify_company(name, county=county)
        is_verified = result.get('is_verified', False)
        
        # Update database
        db.client.table('companies').update({
            'is_verified': is_verified
        }).eq('id', company_id).execute()
        
        status = "VERIFIED" if is_verified else "not verified"
        score = result.get('match_score', 0)
        print(f"{name}")
        print(f"  County: {county or 'N/A'}")
        print(f"  -> {status} (score: {score}%)")
        
        if is_verified:
            print(f"     Matched: {result.get('official_name', 'N/A')}")
            verified += 1
        print()
        
        updated += 1
    
    print(f"\n{'='*50}")
    print(f"Updated {updated} companies")
    print(f"Verified: {verified}")
    print(f"Not verified: {updated - verified}")

if __name__ == '__main__':
    update_verification_status()
