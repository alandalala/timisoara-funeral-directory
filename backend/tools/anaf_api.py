"""
ANAF API Tool - Romanian Tax Authority public API for company verification.

Uses the official ANAF API to get company details from CUI (fiscal code).
API docs: https://static.anaf.ro/static/10/Anaf/Informatii_R/documentatie_SW_v9.txt
"""
import requests
from datetime import datetime
from typing import Optional
import time
import re


class ANAFTool:
    """Tool to query ANAF API for company information by CUI."""
    
    BASE_URL = "https://webservicesp.anaf.ro/api/PlatitorTvaRest/api/v9/ws/tva"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        self._last_request_time = 0
    
    def _rate_limit(self):
        """Ensure at least 1 second between requests."""
        elapsed = time.time() - self._last_request_time
        if elapsed < 1.0:
            time.sleep(1.0 - elapsed)
        self._last_request_time = time.time()
    
    def _clean_cui(self, cui: str) -> Optional[int]:
        """Extract numeric CUI from various formats."""
        if not cui:
            return None
        # Remove RO prefix, spaces, dashes
        cleaned = re.sub(r'[^0-9]', '', str(cui))
        if cleaned:
            return int(cleaned)
        return None
    
    def lookup_company(self, cui: str) -> dict:
        """
        Look up company details by CUI.
        
        Args:
            cui: Company fiscal code (CUI/CIF), with or without RO prefix
            
        Returns:
            dict with company info or error
        """
        numeric_cui = self._clean_cui(cui)
        if not numeric_cui:
            return {'success': False, 'error': 'Invalid CUI format'}
        
        self._rate_limit()
        
        today = datetime.now().strftime('%Y-%m-%d')
        payload = [{"cui": numeric_cui, "data": today}]
        
        try:
            response = self.session.post(self.BASE_URL, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('found') and len(data['found']) > 0:
                company = data['found'][0]
                
                # Extract relevant fields
                general = company.get('date_generale', {})
                address = company.get('adresa_sediu_social', {}) or company.get('adresa_domiciliu_fiscal', {})
                
                return {
                    'success': True,
                    'cui': numeric_cui,
                    'name': general.get('denumire', ''),
                    'registration_number': general.get('nrRegCom', ''),
                    'status': general.get('stare_inregistrare', ''),
                    'address': self._format_address(address),
                    'city': address.get('denumire_Localitate', ''),
                    'county': address.get('denumire_Judet', ''),
                    'is_active': general.get('stare_inregistrare', '').upper() == 'INREGISTRAT',
                    'raw': company
                }
            else:
                return {
                    'success': False,
                    'error': f'CUI {numeric_cui} not found in ANAF database',
                    'cui': numeric_cui
                }
                
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f'ANAF API error: {str(e)}',
                'cui': numeric_cui
            }
    
    def _format_address(self, addr: dict) -> str:
        """Format address from ANAF response."""
        parts = []
        if addr.get('dstrada'):
            parts.append(addr['dstrada'])
        if addr.get('dnumar'):
            parts.append(f"Nr. {addr['dnumar']}")
        if addr.get('denumire_Localitate'):
            parts.append(addr['denumire_Localitate'])
        if addr.get('denumire_Judet'):
            parts.append(f"Jud. {addr['denumire_Judet']}")
        return ', '.join(parts) if parts else ''
    
    def lookup_batch(self, cui_list: list) -> list:
        """
        Look up multiple companies at once (max 100 per request).
        
        Args:
            cui_list: List of CUI strings
            
        Returns:
            List of company info dicts
        """
        results = []
        
        # Process in batches of 100
        for i in range(0, len(cui_list), 100):
            batch = cui_list[i:i+100]
            self._rate_limit()
            
            today = datetime.now().strftime('%Y-%m-%d')
            payload = [{"cui": self._clean_cui(cui), "data": today} 
                      for cui in batch if self._clean_cui(cui)]
            
            if not payload:
                continue
                
            try:
                response = self.session.post(self.BASE_URL, json=payload, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                for company in data.get('found', []):
                    general = company.get('date_generale', {})
                    address = company.get('adresa_sediu_social', {}) or {}
                    
                    results.append({
                        'success': True,
                        'cui': general.get('cui'),
                        'name': general.get('denumire', ''),
                        'city': address.get('denumire_Localitate', ''),
                        'county': address.get('denumire_Judet', ''),
                        'is_active': general.get('stare_inregistrare', '').upper() == 'INREGISTRAT'
                    })
                    
            except requests.exceptions.RequestException as e:
                print(f"Batch lookup error: {e}")
                
        return results


# Quick test
if __name__ == "__main__":
    anaf = ANAFTool()
    
    # Test with Subin Funerare's CUI
    print("Testing ANAF API with CUI 1810870 (Servicii Funerare SRL)...")
    result = anaf.lookup_company("1810870")
    
    if result['success']:
        print(f"✅ Found: {result['name']}")
        print(f"   CUI: {result['cui']}")
        print(f"   Status: {result['status']}")
        print(f"   Address: {result['address']}")
        print(f"   City: {result['city']}")
        print(f"   County: {result['county']}")
        print(f"   Active: {result['is_active']}")
    else:
        print(f"❌ Error: {result['error']}")
