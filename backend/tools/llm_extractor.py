"""
LLM Extraction Tool - Uses OpenAI to extract structured data from markdown.
"""
from typing import Dict, Optional
import json
from openai import OpenAI
from config.settings import OPENAI_API_KEY, LLM_MODEL, LLM_TEMPERATURE


class LLMExtractorTool:
    """
    Tool to extract structured data from website markdown using LLM.
    """
    
    def __init__(self, api_key: str = OPENAI_API_KEY):
        if not api_key:
            raise ValueError("OPENAI_API_KEY must be set")
        
        self.client = OpenAI(api_key=api_key)
        self.model = LLM_MODEL
    
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
  "address": "Physical address if mentioned",
  "services": ["Array of service keywords. Valid values: transport, repatriation, cremation, embalming, wake_house, coffins, flowers, bureaucracy, religious, monuments"],
  "is_non_stop": "Boolean, true if '24/7', 'Non-Stop', '24 de ore', or similar mentioned",
  "fiscal_code": "Romanian CUI/fiscal code if mentioned (format: CUI 12345678 or RO12345678)",
  "description": "Brief description of the company (2-3 sentences)"
}

Important rules:
1. A motto is philosophical/emotional, not descriptive
2. Extract ALL phone numbers found
3. Only use service keywords from the valid list
4. Return valid JSON only, no additional text"""

        user_prompt = f"""Website URL: {url}

Website Content (Markdown):
{markdown_content[:8000]}

Extract the company information as JSON."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=LLM_TEMPERATURE,
                response_format={"type": "json_object"}
            )
            
            result_text = response.choices[0].message.content
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
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=10
            )
            
            result = response.choices[0].message.content.strip().upper()
            return result == "MOTTO"
            
        except Exception as e:
            print(f"Error validating motto: {e}")
            return False
