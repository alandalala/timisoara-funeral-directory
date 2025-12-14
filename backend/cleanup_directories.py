"""Test directory detection logic"""
import sys
sys.path.insert(0, '.')

def test_directory_detection():
    """Test the _is_directory_site logic"""
    
    # Simulate extracted data from different sites
    test_cases = [
        # (extracted_data, url, expected_is_directory)
        (
            {'company_name': 'Timisoreni.ro', 'phones': ['0256123456'] * 29},
            'https://www.timisoreni.ro/info/pompe_funebre/',
            True,  # Directory - many phones, /info/ path, known domain
        ),
        (
            {'company_name': 'Subin Funerare', 'phones': ['0256123456', '0723456789']},
            'https://funeraretimisoara.ro/',
            False,  # Real company
        ),
        (
            {'company_name': 'SC SERVICII FUNERARE S.R.L.', 'phones': ['0256111222']},
            'https://serviciifunerare-timisoara.ro/',
            False,  # Real company
        ),
        (
            {'company_name': 'Lista Pompe Funebre Online', 'phones': ['0256111222']},
            'https://example.ro/firme/funerare/',
            True,  # Directory - name pattern + URL pattern
        ),
        (
            {'company_name': 'Pompe Funebre Timisoara', 'phones': ['0256123456'] * 10},
            'https://pompefunebre.ro/',
            True,  # Directory - too many phones
        ),
    ]
    
    from urllib.parse import urlparse
    
    def is_directory_site(extracted, url):
        phones = extracted.get('phones', [])
        if len(phones) > 5:
            return True, f"too many phones ({len(phones)})"
        
        company_name = extracted.get('company_name', '').lower()
        directory_name_patterns = [
            '.ro', '.com', '.net',
            'info', 'portal', 'online', 'lista', 'director',
            'firme', 'companies', 'ghid',
        ]
        if any(pattern in company_name for pattern in directory_name_patterns):
            return True, f"name pattern"
        
        parsed_url = urlparse(url)
        path = parsed_url.path.lower()
        directory_url_patterns = [
            '/info/', '/listings/', '/directory/', '/catalog/',
            '/firme/', '/companies/', '/lista/', '/list/',
            '/results/', '/search/', '/categorie/', '/category/',
            '/pompe_funebre/', '/servicii_funerare/',
        ]
        if any(pattern in path for pattern in directory_url_patterns):
            return True, f"URL pattern '{path}'"
        
        domain = parsed_url.netloc.lower().replace('www.', '')
        directory_domains = [
            'timisoreni.ro', 'oradeni.ro', 'clujeni.ro', 'bucuresteni.ro',
        ]
        if domain in directory_domains:
            return True, f"known domain '{domain}'"
        
        return False, "real company"
    
    print("Testing directory detection:\n")
    
    for extracted, url, expected in test_cases:
        is_dir, reason = is_directory_site(extracted, url)
        status = "PASS" if is_dir == expected else "FAIL"
        print(f"[{status}] {extracted['company_name'][:30]}")
        print(f"       URL: {url}")
        print(f"       Expected: {'directory' if expected else 'company'}")
        print(f"       Got: {'directory' if is_dir else 'company'} ({reason})")
        print()

if __name__ == '__main__':
    test_directory_detection()
