"""
Supabase Database Tool - Handles all database operations.
"""
from typing import List, Dict, Optional
from supabase import create_client, Client
from config.settings import SUPABASE_URL, SUPABASE_SERVICE_KEY
from models import Company, Location, Contact
from utils import slugify
import json


class SupabaseTool:
    """
    Tool for interacting with Supabase database.
    """
    
    def __init__(self):
        if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
            raise ValueError("Supabase credentials must be set in environment")
        
        self.client: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    
    def upsert_company(self, company: Company) -> Dict:
        """
        Insert or update a company in the database.
        Uses fiscal_code, website, or phone numbers for matching existing records.
        
        Returns:
            Dict with 'success', 'company_id', 'action' (inserted/updated/duplicate)
        """
        try:
            # Generate slug from company name
            slug = slugify(company.name)
            
            # Check if company already exists
            existing_company = None
            
            # Check by fiscal_code
            if company.fiscal_code:
                result = self.client.table('companies').select('*').eq('fiscal_code', company.fiscal_code).execute()
                if result.data:
                    existing_company = result.data[0]
                    print(f"Found existing company by fiscal_code: {company.fiscal_code}")
            
            # Check by website
            if not existing_company and company.website:
                result = self.client.table('companies').select('*').eq('website', company.website).execute()
                if result.data:
                    existing_company = result.data[0]
                    print(f"Found existing company by website: {company.website}")
            
            # Check by phone numbers (duplicate detection)
            if not existing_company and company.contacts:
                for contact in company.contacts:
                    if contact.type in ('phone_mobile', 'phone_landline'):
                        # Normalize phone for comparison
                        phone_value = contact.value.replace(' ', '').replace('-', '').replace('.', '')
                        
                        # Search in contacts table
                        result = self.client.table('contacts').select(
                            'company_id, value'
                        ).in_('type', ['phone_mobile', 'phone_landline']).execute()
                        
                        for existing_contact in result.data or []:
                            existing_phone = existing_contact['value'].replace(' ', '').replace('-', '').replace('.', '')
                            if phone_value == existing_phone:
                                # Found matching phone - get the company
                                comp_result = self.client.table('companies').select('*').eq(
                                    'id', existing_contact['company_id']
                                ).execute()
                                if comp_result.data:
                                    existing_company = comp_result.data[0]
                                    print(f"Found existing company by phone: {contact.value} -> {existing_company['name']}")
                                    break
                    if existing_company:
                        break
            
            # Prepare company data
            company_data = {
                'name': company.name,
                'slug': slug,
                'motto': company.motto,
                'description': company.description,
                'fiscal_code': company.fiscal_code,
                'website': company.website,
                'is_verified': company.is_verified,
                'is_non_stop': company.is_non_stop,
                'founded_year': company.founded_year,
            }
            
            # Add social media URLs if available (requires DB columns)
            if company.facebook_url:
                company_data['facebook_url'] = company.facebook_url
            if company.instagram_url:
                company_data['instagram_url'] = company.instagram_url
            
            if existing_company:
                # Update existing
                company_id = existing_company['id']
                
                self.client.table('companies').update(company_data).eq('id', company_id).execute()
                
                # Delete old relations (will re-insert)
                self.client.table('contacts').delete().eq('company_id', company_id).execute()
                self.client.table('services').delete().eq('company_id', company_id).execute()
                self.client.table('locations').delete().eq('company_id', company_id).execute()
                
                action = 'updated'
            else:
                # Insert new
                result = self.client.table('companies').insert(company_data).execute()
                company_id = result.data[0]['id']
                action = 'inserted'
            
            # Insert contacts
            for contact in company.contacts:
                contact_data = {
                    'company_id': company_id,
                    'type': contact.type,
                    'value': contact.value,
                    'is_primary': contact.is_primary
                }
                self.client.table('contacts').insert(contact_data).execute()
            
            # Insert services
            for service_tag in company.services:
                service_data = {
                    'company_id': company_id,
                    'service_tag': service_tag
                }
                self.client.table('services').insert(service_data).execute()
            
            # Insert locations
            for location in company.locations:
                location_data = {
                    'company_id': company_id,
                    'address': location.address,
                    'city': location.city,
                    'county': location.county,
                    'type': location.type
                }
                
                # Add coordinates if available (both as separate columns and geo_point)
                if location.latitude and location.longitude:
                    location_data['latitude'] = location.latitude
                    location_data['longitude'] = location.longitude
                    location_data['geo_point'] = f'POINT({location.longitude} {location.latitude})'
                
                self.client.table('locations').insert(location_data).execute()
            
            print(f"✓ Company '{company.name}' {action} successfully (ID: {company_id})")
            
            return {
                'success': True,
                'company_id': company_id,
                'action': action
            }
            
        except Exception as e:
            print(f"✗ Error upserting company '{company.name}': {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_company_by_slug(self, slug: str) -> Optional[Dict]:
        """
        Get a company by slug with all related data.
        """
        try:
            result = self.client.table('companies').select(
                '*, contacts(*), services(*), locations(*)'
            ).eq('slug', slug).execute()
            
            if result.data:
                return result.data[0]
            return None
            
        except Exception as e:
            print(f"Error fetching company by slug: {e}")
            return None
    
    def check_duplicate(self, fiscal_code: Optional[str] = None, 
                       phone: Optional[str] = None) -> Optional[Dict]:
        """
        Check if a company already exists based on fiscal code or phone.
        
        Returns:
            Existing company dict if found, None otherwise
        """
        try:
            if fiscal_code:
                result = self.client.table('companies').select('*').eq(
                    'fiscal_code', fiscal_code
                ).execute()
                
                if result.data:
                    return result.data[0]
            
            if phone:
                # Check in contacts table
                result = self.client.table('contacts').select(
                    'company_id, companies(*)'
                ).eq('value', phone).execute()
                
                if result.data:
                    return result.data[0]['companies']
            
            return None
            
        except Exception as e:
            print(f"Error checking duplicates: {e}")
            return None
    
    def get_all_companies(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """
        Get all companies with pagination.
        """
        try:
            result = self.client.table('companies').select(
                '*, contacts(*), services(*), locations(*)'
            ).range(offset, offset + limit - 1).execute()
            
            return result.data
            
        except Exception as e:
            print(f"Error fetching companies: {e}")
            return []
    
    def get_statistics(self) -> Dict:
        """
        Get database statistics.
        """
        try:
            total_companies = self.client.table('companies').select('id', count='exact').execute()
            verified_companies = self.client.table('companies').select(
                'id', count='exact'
            ).eq('is_verified', True).execute()
            
            return {
                'total_companies': total_companies.count,
                'verified_companies': verified_companies.count,
                'verification_rate': (verified_companies.count / total_companies.count * 100) if total_companies.count > 0 else 0
            }
            
        except Exception as e:
            print(f"Error fetching statistics: {e}")
            return {}
