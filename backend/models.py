from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
import re


class Contact(BaseModel):
    """Contact information for a funeral company"""
    type: str = Field(..., description="Type of contact: phone_mobile, phone_landline, email, fax")
    value: str = Field(..., description="Contact value (phone number, email, etc.)")
    is_primary: bool = Field(default=False, description="Whether this is the primary contact")

    @field_validator('value')
    @classmethod
    def validate_contact_value(cls, v: str, info) -> str:
        """Validate contact values based on type"""
        contact_type = info.data.get('type')
        
        if contact_type in ['phone_mobile', 'phone_landline']:
            # Remove all non-digit characters
            digits_only = re.sub(r'\D', '', v)
            if not digits_only:
                raise ValueError("Phone number must contain digits")
            return digits_only
        
        elif contact_type == 'email':
            # Basic email validation
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
                raise ValueError("Invalid email format")
        
        return v


class Location(BaseModel):
    """Physical location of a funeral company"""
    address: str = Field(..., description="Full street address")
    city: Optional[str] = Field(None, description="City name")
    county: Optional[str] = Field(None, description="Romanian county/județ")
    latitude: Optional[float] = Field(None, description="Latitude coordinate")
    longitude: Optional[float] = Field(None, description="Longitude coordinate")
    type: str = Field(default="headquarters", description="Type: headquarters, wake_house, showroom")

    @field_validator('type')
    @classmethod
    def validate_location_type(cls, v: str) -> str:
        """Validate location type"""
        valid_types = ['headquarters', 'wake_house', 'showroom']
        if v not in valid_types:
            raise ValueError(f"Location type must be one of: {', '.join(valid_types)}")
        return v


class Company(BaseModel):
    """Funeral company entity"""
    name: str = Field(..., description="Official company name")
    motto: Optional[str] = Field(None, description="Company motto or ethos statement")
    description: Optional[str] = Field(None, description="Detailed company description")
    fiscal_code: Optional[str] = Field(None, description="Romanian fiscal code (CUI)")
    website: Optional[str] = Field(None, description="Company website URL")
    facebook_url: Optional[str] = Field(None, description="Facebook page URL")
    instagram_url: Optional[str] = Field(None, description="Instagram profile URL")
    is_verified: bool = Field(default=False, description="Whether company is DSP verified")
    is_non_stop: bool = Field(default=False, description="Whether company offers 24/7 service")
    founded_year: Optional[int] = Field(None, description="Year the company was founded")
    services: List[str] = Field(default_factory=list, description="List of service tags")
    contacts: List[Contact] = Field(default_factory=list, description="Contact information")
    locations: List[Location] = Field(default_factory=list, description="Physical locations")
    
    @field_validator('motto')
    @classmethod
    def validate_motto_length(cls, v: Optional[str]) -> Optional[str]:
        """Ensure motto is not too long"""
        if v and len(v) > 200:
            raise ValueError("Motto must be less than 200 characters")
        return v

    @field_validator('fiscal_code')
    @classmethod
    def validate_fiscal_code(cls, v: Optional[str]) -> Optional[str]:
        """Validate Romanian fiscal code format"""
        if v:
            # Remove 'RO' prefix if present
            v = v.replace('RO', '').strip()
            # Should be 2-10 digits
            if not re.match(r'^\d{2,10}$', v):
                raise ValueError("Invalid fiscal code format")
        return v

    @field_validator('services')
    @classmethod
    def validate_services(cls, v: List[str]) -> List[str]:
        """Validate service tags against allowed taxonomy"""
        valid_services = [
            'transport', 'repatriation', 'cremation', 'embalming',
            'wake_house', 'coffins', 'flowers', 'bureaucracy',
            'religious', 'monuments'
        ]
        
        for service in v:
            if service not in valid_services:
                raise ValueError(f"Invalid service tag: {service}. Must be one of: {', '.join(valid_services)}")
        
        return v


class ScrapedData(BaseModel):
    """Raw data extracted from website"""
    url: str = Field(..., description="Source URL")
    company_name: Optional[str] = Field(None, description="Extracted company name")
    motto: Optional[str] = Field(None, description="Extracted motto")
    phones: List[str] = Field(default_factory=list, description="Extracted phone numbers")
    email: Optional[str] = Field(None, description="Extracted email")
    address: Optional[str] = Field(None, description="Extracted address")
    services: List[str] = Field(default_factory=list, description="Extracted service keywords")
    is_non_stop: bool = Field(default=False, description="Whether 24/7 service mentioned")
    raw_content: Optional[str] = Field(None, description="Raw markdown content")
    extraction_timestamp: datetime = Field(default_factory=datetime.now, description="When data was extracted")


class DSPRecord(BaseModel):
    """Record from DSP authorization list"""
    legal_name: str = Field(..., description="Official legal name from DSP")
    cui: Optional[str] = Field(None, description="Fiscal code from DSP")
    address: Optional[str] = Field(None, description="Registered address from DSP")
    authorization_date: Optional[str] = Field(None, description="Date of authorization")
