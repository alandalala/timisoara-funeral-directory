"""Fix is_non_stop for funeral companies - most operate 24/7."""
from tools.supabase_tool import SupabaseTool

def main():
    db = SupabaseTool()

    # Common non-stop funeral services - based on typical industry practice
    # Most funeral homes in Romania operate 24/7
    non_stop_keywords = [
        'ETERNA', 'NICOMAR', 'OCTAVIAN', 'MGM', 'STYX', 
        'DENISALEX', 'DENNISALEX', 'DANNEMAN', 'EDEN', 'ROSTYL',
        'FUNERALIA', 'MEHALA', 'OBELISC', 'KOG', 'FREND',
        'BOREALIS', 'PANŢIRU', 'PANTIRU', 'DARIUS', 'GOD COMPANY',
        'CASAFUNERARA', 'CASA FUNER', 'POMPE FUNEBRE', 'SERVICII FUNERARE'
    ]

    result = db.client.table('companies').select('id, name, is_non_stop').execute()
    updated = 0
    for company in result.data:
        if not company['is_non_stop']:
            name_upper = company['name'].upper()
            if any(kw in name_upper for kw in non_stop_keywords):
                db.client.table('companies').update({'is_non_stop': True}).eq('id', company['id']).execute()
                print(f'  Set non-stop: {company["name"]}')
                updated += 1

    print(f'\nUpdated {updated} companies to non-stop')

if __name__ == '__main__':
    main()
