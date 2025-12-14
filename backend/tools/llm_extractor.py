"""
LLM Extraction Tool - Uses Ollama (local) or OpenAI to extract structured data from markdown.
"""
from typing import Dict, Optional
import json
import requests
from config.settings import (
    OPENAI_API_KEY, LLM_MODEL, LLM_TEMPERATURE,
    LLM_PROVIDER, OLLAMA_BASE_URL, OLLAMA_MODEL
)


class LLMExtractorTool:
    """
    Tool to extract structured data from website markdown using LLM.
    Supports both local Ollama and OpenAI backends.
    """
    
    def __init__(self, provider: str = LLM_PROVIDER, api_key: str = OPENAI_API_KEY):
        self.provider = provider
        
        if provider == "openai":
            if not api_key:
                raise ValueError("OPENAI_API_KEY must be set for OpenAI provider")
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key)
            self.model = LLM_MODEL
        elif provider == "ollama":
            self.base_url = OLLAMA_BASE_URL
            self.model = OLLAMA_MODEL
        else:
            raise ValueError(f"Unknown LLM provider: {provider}")
    
    def extract_company_data(self, markdown_content: str, url: str) -> Dict:
        """
        Extract structured company data from markdown content.
        
        Args:
            markdown_content: Website content in markdown format
            url: Source URL
        
        Returns:
            Dict with extracted data matching Company model structure
        """
        system_prompt = """You are an expert data analyst for the funeral industry. 
Your task is to extract structured information from funeral home website content.

Extract the following JSON object:
{
  "company_name": "Official company name (required)",
  "motto": "Short inspirational phrase representing company ethos. Look for:
           - Quoted text in hero sections
           - Italicized mission statements  
           - Text explicitly labeled as 'Motto' or 'Deviza'
           Return null if none found. Do NOT mistake service descriptions for mottos.
           Must be under 200 characters.",
  "phones": ["Array of phone numbers found"],
  "email": "Primary contact email",
  "address": "Full physical address if mentioned",
  "city": "City name (e.g., Timișoara, București, Cluj-Napoca). Extract from address or location info.",
  "county": "Romanian county/județ (e.g., Timiș, București, Cluj, Arad, Bihor). Infer from city if not explicit.",
  "services": ["Array of service keywords. Valid values: transport, repatriation, cremation, embalming, wake_house, coffins, flowers, bureaucracy, religious, monuments"],
  "is_non_stop": "Boolean, true if '24/7', 'Non-Stop', '24 de ore', or similar mentioned",
  "founded_year": "Year the company was founded (integer, e.g., 2010). Look for 'din anul', 'fondată în', 'activă din', 'experiență din'. Return null if not found.",
  "fiscal_code": "Romanian CUI/CIF fiscal code. IMPORTANT: Look carefully for patterns like:
                  - 'CUI: 12345678' or 'CUI 12345678'
                  - 'CIF: 12345678' or 'CIF 12345678' 
                  - 'Cod fiscal: 12345678'
                  - 'RO12345678' (VAT format)
                  - 'J35/1234/2010' (trade register number, extract just the CUI if nearby)
                  Usually found in footer, contact page, or 'Despre noi' sections.
                  Return just the number (6-10 digits) without 'RO' prefix.",
  "facebook_url": "Facebook page URL if found (e.g., https://facebook.com/company)",
  "instagram_url": "Instagram profile URL if found (e.g., https://instagram.com/company)",
  "description": "Brief description of the company (2-3 sentences)"
}

Important rules:
1. A motto is philosophical/emotional, not descriptive
2. Extract ALL phone numbers found
3. Only use service keywords from the valid list
4. CUI/CIF is critical - search the entire content carefully for it
5. Return valid JSON only, no additional text"""

        # Model has 32768 token context (~4 chars/token), leave room for prompt + response
        max_content_chars = 50000
        
        user_prompt = f"""Website URL: {url}

Website Content (Markdown):
{markdown_content[:max_content_chars]}

IMPORTANT: Look carefully for email addresses - they often appear on Contact pages or in footer sections.
Common patterns: name@domain.ro, contact@company.ro, office@company.ro

Extract the company information as JSON."""

        try:
            if self.provider == "ollama":
                result_text = self._call_ollama(system_prompt, user_prompt)
            else:
                result_text = self._call_openai(system_prompt, user_prompt)
            
            extracted_data = json.loads(result_text)
            
            # Add source URL
            extracted_data['url'] = url
            
            return {
                'success': True,
                'data': extracted_data
            }
            
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON from LLM response: {e}")
            return {
                'success': False,
                'error': 'Invalid JSON from LLM'
            }
        except Exception as e:
            print(f"Error extracting data with LLM: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _call_ollama(self, system_prompt: str, user_prompt: str) -> str:
        """Call Ollama API and return response text."""
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": full_prompt,
                "stream": False,
                "format": "json"
            },
            timeout=120
        )
        response.raise_for_status()
        return response.json()["response"]
    
    def _call_openai(self, system_prompt: str, user_prompt: str) -> str:
        """Call OpenAI API and return response text."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=LLM_TEMPERATURE,
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content
    
    def validate_motto(self, text: str) -> bool:
        """
        Use LLM to validate if a text is truly a motto or just a description.
        
        Returns:
            True if it's a valid motto, False otherwise
        """
        if not text or len(text) > 200:
            return False
        
        prompt = f"""Is the following text a company motto/slogan/ethos statement, or just a regular description?

Text: "{text}"

A motto is:
- Short and memorable
- Philosophical or emotional
- Represents core values
- Often poetic or inspirational

A description is:
- Factual information
- List of services
- Contact details
- General information

Answer with only "MOTTO" or "DESCRIPTION"."""

        try:
            if self.provider == "ollama":
                response = requests.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False
                    },
                    timeout=60
                )
                response.raise_for_status()
                result = response.json()["response"].strip().upper()
            else:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0,
                    max_tokens=10
                )
                result = response.choices[0].message.content.strip().upper()
            
            return "MOTTO" in result
            
        except Exception as e:
            print(f"Error validating motto: {e}")
            return False
