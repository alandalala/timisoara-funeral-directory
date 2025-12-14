"""
DSP Verification Tool - Cross-references companies with official authorization list.
"""
import os
import json
import re
from typing import List, Dict, Optional, Tuple
from difflib import SequenceMatcher


class DSPVerificationTool:
    """
    Tool to verify funeral companies against DSP (Direcția de Sănătate Publică)
    authorization lists.
    """
    
    def __init__(self, dsp_data_path: str = None):
        self.dsp_data_path = dsp_data_path or os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            'data', 
            'dsp_authorized_companies.json'
        )
        self.authorized_companies = self._load_dsp_data()
    
    def _load_dsp_data(self) -> List[Dict]:
        """Load DSP authorized companies from JSON file."""
        if os.path.exists(self.dsp_data_path):
            with open(self.dsp_data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                companies = data.get('companies', [])
                print(f"Loaded {len(companies)} authorized companies from DSP list")
                return companies
        print(f"Warning: DSP data not found at {self.dsp_data_path}")
        print("Run DSP scraper first to populate the authorization list.")
        return []
    
    def _normalize_company_name(self, name: str) -> str:
        """Normalize company name for comparison."""
        if not name:
            return ""
        
        # Convert to uppercase
        normalized = name.upper()
        
        # Remove common prefixes/suffixes
        patterns_to_remove = [
            r'^SC\s+',      # SC prefix
            r'^S\.C\.\s*',  # S.C. prefix
            r'\s*S\.?R\.?L\.?\.?$',   # SRL suffix
            r'\s*S\.?A\.?\.?$',       # SA suffix
            r'\s*I\.?I\.?\.?$',       # II suffix
            r'\s*P\.?F\.?A\.?\.?$',   # PFA suffix
            r'\s*S\.?N\.?C\.?\.?$',   # SNC suffix
        ]
        
        for pattern in patterns_to_remove:
            normalized = re.sub(pattern, '', normalized, flags=re.IGNORECASE)
        
        # Remove punctuation and extra spaces
        normalized = re.sub(r'[^\w\s]', ' ', normalized)
        normalized = re.sub(r'\s+', ' ', normalized)
        normalized = normalized.strip()
        
        return normalized
    
    def _calculate_similarity(self, name1: str, name2: str) -> float:
        """Calculate similarity ratio between two company names."""
        norm1 = self._normalize_company_name(name1)
        norm2 = self._normalize_company_name(name2)
        
        if not norm1 or not norm2:
            return 0.0
        
        # Exact match after normalization
        if norm1 == norm2:
            return 1.0
        
        # Check if one contains the other
        if norm1 in norm2 or norm2 in norm1:
            shorter = min(len(norm1), len(norm2))
            longer = max(len(norm1), len(norm2))
            return shorter / longer
        
        # Use sequence matcher for fuzzy matching
        return SequenceMatcher(None, norm1, norm2).ratio()
    
    def _normalize_county(self, county: str) -> str:
        """Normalize county name for comparison (remove diacritics, etc.)."""
        if not county:
            return ""
        
        # Romanian diacritics mapping
        diacritics = {
            'ă': 'a', 'â': 'a', 'î': 'i', 'ș': 's', 'ț': 't',
            'Ă': 'A', 'Â': 'A', 'Î': 'I', 'Ș': 'S', 'Ț': 'T',
            'ş': 's', 'ţ': 't', 'Ş': 'S', 'Ţ': 'T',  # Old style diacritics
        }
        
        result = county
        for diac, replacement in diacritics.items():
            result = result.replace(diac, replacement)
        
        return result.upper().strip()

    def verify_company(self, company_name: str, county: str = None, 
                       threshold: float = 0.85) -> Dict:
        """
        Verify if a company is in the DSP authorization list.
        
        Args:
            company_name: Name of the company to verify
            county: Optional county filter (e.g., 'Timiș', 'TM')
            threshold: Minimum similarity score (0-1) to consider a match
            
        Returns:
            Dict with verification result
        """
        if not self.authorized_companies:
            return {
                "is_verified": False,
                "verification_source": "DSP_list_not_available",
                "match_score": 0
            }
        
        best_match = None
        best_score = 0.0
        
        # Normalize county for comparison
        county_normalized = self._normalize_county(county) if county else None
        
        for auth_company in self.authorized_companies:
            # Filter by county if specified
            if county_normalized:
                auth_county_normalized = self._normalize_county(auth_company.get('county', ''))
                auth_county_code = auth_company.get('county_code', '').upper()
                
                # Match on normalized county name or county code
                if county_normalized not in (auth_county_normalized, auth_county_code):
                    continue
            
            auth_name = auth_company.get('name', '')
            similarity = self._calculate_similarity(company_name, auth_name)
            
            if similarity > best_score:
                best_score = similarity
                best_match = auth_company
        
        is_verified = best_score >= threshold
        
        if is_verified and best_match:
            return {
                "is_verified": True,
                "official_name": best_match.get('name', ''),
                "verification_source": f"DSP_{best_match.get('county_code', 'RO')}",
                "match_score": int(best_score * 100),
                "authorization_number": best_match.get('authorization_number'),
                "match_method": "name_fuzzy"
            }
        
        return {
            "is_verified": False,
            "match_score": int(best_score * 100),
            "closest_match": best_match.get('name', '') if best_match else None
        }
    
    def get_all_authorized_companies(self) -> List[Dict]:
        """Get list of all authorized companies."""
        return self.authorized_companies
    
    def get_stats(self) -> Dict:
        """Get statistics about loaded DSP data."""
        if not self.authorized_companies:
            return {'total': 0, 'by_county': {}}
        
        by_county = {}
        for company in self.authorized_companies:
            county = company.get('county', 'Unknown')
            by_county[county] = by_county.get(county, 0) + 1
        
        return {
            'total': len(self.authorized_companies),
            'by_county': by_county
        }


def main():
    """Test the DSP verifier."""
    verifier = DSPVerificationTool()
    stats = verifier.get_stats()
    
    print(f"\nDSP Authorized Companies: {stats['total']}")
    print(f"By county: {stats['by_county']}")
    
    # Test verification
    test_companies = [
        "Subin Funerare",
        "DENISALEX SRL",
        "SC OBELISC SRL",
        "Casa Funerara Octavian",
        "ETERNA FUNERARE",
        "Random Company SRL",  # Should not match
    ]
    
    print("\n--- Verification Tests ---")
    for name in test_companies:
        result = verifier.verify_company(name, county='TM')
        status = "✓ VERIFIED" if result['is_verified'] else "✗ NOT VERIFIED"
        print(f"\n{name}")
        print(f"  {status} (score: {result['match_score']}%)")
        if result.get('official_name'):
            print(f"  Matched: {result['official_name']}")


if __name__ == '__main__':
    main()
