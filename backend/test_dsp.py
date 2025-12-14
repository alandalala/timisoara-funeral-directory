"""Test DSP Scraper and Verification"""
from tools.dsp_verification import DSPVerificationTool

def test_verification():
    verifier = DSPVerificationTool()
    
    print("DSP Authorized Companies:")
    for c in verifier.authorized_companies:
        print(f"  - {c['name']}")
    
    print("\n\nTesting verification of scraped companies:")
    test_names = [
        "SERVICII FUNERARE S.R.L.",
        "Subin Funerare",
        "SC DENISALEX SRL",
        "OBELISC SRL",
    ]
    
    for name in test_names:
        result = verifier.verify_company(name, county='TM')
        status = "[OK]" if result['is_verified'] else "[X]"
        print(f"\n{name}")
        print(f"  {status} Score: {result['match_score']}%")
        if result.get('official_name'):
            print(f"  Matched: {result['official_name']}")
        elif result.get('closest_match'):
            print(f"  Closest: {result['closest_match']}")

if __name__ == '__main__':
    test_verification()
