"""Fix Subin Funerare verification status"""
from tools.supabase_tool import SupabaseTool
from tools.dsp_verification import DSPVerificationTool

def main():
    db = SupabaseTool()
    dsp = DSPVerificationTool()
    
    # Get Subin Funerare
    result = db.client.table('companies').select('*').ilike('name', '%subin%').execute()
    if result.data:
        company = result.data[0]
        print(f"Found: {company['name']} (ID: {company['id']})")
        print(f"Currently verified: {company.get('is_verified', False)}")
        
        # Verify
        verify_result = dsp.verify_company(
            company['name'], 
            company.get('city', ''), 
            company.get('county', '')
        )
        print(f"Verification result: {verify_result}")
        
        # Update in DB
        update = db.client.table('companies').update({
            'is_verified': verify_result['is_verified']
        }).eq('id', company['id']).execute()
        print(f"✅ Updated Subin Funerare in database!")
        print(f"   is_verified: {verify_result['is_verified']}")
        print(f"   official_name: {verify_result.get('official_name')}")
        print(f"   match_method: {verify_result.get('match_method')}")
    else:
        print("Subin Funerare not found in database")

if __name__ == "__main__":
    main()
