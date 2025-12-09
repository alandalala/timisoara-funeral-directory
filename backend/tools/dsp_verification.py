"""
DSP Verification Tool - Cross-references companies with official authorization list.
"""
import os
from typing import List, Dict, Optional
from pypdf import PdfReader
from thefuzz import fuzz
from models import DSPRecord
from config.settings import DSP_PDF_PATH


class DSPVerificationTool:
    """
    Tool to verify funeral companies against the DSP Timis authorization list.
    """
    
    def __init__(self, pdf_path: str = DSP_PDF_PATH):
        self.pdf_path = pdf_path
        self.dsp_records: List[DSPRecord] = []
        self._load_dsp_data()
    
    def _load_dsp_data(self):
        """
        Load and parse the DSP authorization PDF.
        """
        if not os.path.exists(self.pdf_path):
            print(f"Warning: DSP PDF not found at {self.pdf_path}")
            print("Verification will be skipped. Download from:")
            print("https://www.dsptimis.ro/public/data_files/media/comparimente/avize-autorizatii/")
            return
        
        try:
            reader = PdfReader(self.pdf_path)
            full_text = ""
            
            for page in reader.pages:
                full_text += page.extract_text()
            
            # Parse the text to extract company records
            self._parse_dsp_text(full_text)
            
            print(f"Loaded {len(self.dsp_records)} authorized companies from DSP list")
            
        except Exception as e:
            print(f"Error loading DSP PDF: {e}")
    
    def _parse_dsp_text(self, text: str):
        """
        Parse DSP PDF text to extract company records.
        
        The DSP list typically has format like:
        1. SC COMPANY NAME SRL - CUI: 12345678 - Address
        """
        import re
        
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or len(line) < 10:
                continue
            
            # Try to extract company name (usually starts with SC or SRL pattern)
            if 'SC ' in line.upper() or 'SRL' in line.upper():
                # Extract CUI if present
                cui_match = re.search(r'CUI[:\s]*(\d{2,10})', line, re.IGNORECASE)
                cui = cui_match.group(1) if cui_match else None
                
                # Clean up company name
                company_name = line
                # Remove numbering (e.g., "1.", "2.")
                company_name = re.sub(r'^\d+\.?\s*', '', company_name)
                # Extract just the company name part (before CUI or address)
                if cui_match:
                    company_name = line[:cui_match.start()].strip()
                
                # Clean common patterns
                company_name = re.sub(r'\s*-\s*CUI.*', '', company_name, flags=re.IGNORECASE)
                company_name = company_name.strip(' ,-')
                
                if company_name and len(company_name) > 5:
                    record = DSPRecord(
                        legal_name=company_name,
                        cui=cui,
                        address=None  # Could be extracted if format is consistent
                    )
                    self.dsp_records.append(record)
    
    def verify_company(self, company_name: str, cui: Optional[str] = None) -> Dict:
        """
        Verify if a company is in the DSP authorization list.
        
        Args:
            company_name: Company name to verify
            cui: Optional fiscal code for exact matching
        
        Returns:
            Dict with verification result:
            {
                "is_verified": bool,
                "official_name": str (if verified),
                "verification_source": str,
                "match_score": int (0-100)
            }
        """
        if not self.dsp_records:
            return {
                "is_verified": False,
                "verification_source": "DSP_list_not_available"
            }
        
        best_match_score = 0
        best_match_record = None
        
        for record in self.dsp_records:
            # Exact CUI match has highest priority
            if cui and record.cui and cui == record.cui:
                return {
                    "is_verified": True,
                    "official_name": record.legal_name,
                    "verification_source": "DSP_Timis_2024",
                    "match_score": 100,
                    "match_method": "cui_exact"
                }
            
            # Fuzzy name matching
            similarity = fuzz.ratio(
                company_name.lower(),
                record.legal_name.lower()
            )
            
            if similarity > best_match_score:
                best_match_score = similarity
                best_match_record = record
        
        # Consider it verified if similarity is above 85%
        if best_match_score >= 85:
            return {
                "is_verified": True,
                "official_name": best_match_record.legal_name,
                "verification_source": "DSP_Timis_2024",
                "match_score": best_match_score,
                "match_method": "name_fuzzy"
            }
        
        return {
            "is_verified": False,
            "match_score": best_match_score,
            "closest_match": best_match_record.legal_name if best_match_record else None
        }
    
    def get_all_authorized_companies(self) -> List[DSPRecord]:
        """
        Get list of all authorized companies.
        """
        return self.dsp_records
