# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added - Phase 1: Infrastructure (2025-12-08)

#### Backend
- Python project structure with organized folders (agents, tools, config, data)
- Pydantic models for data validation (Company, Contact, Location, Service)
- DSPVerificationTool for cross-referencing with official authorization list
- FirecrawlExtractorTool for website scraping with markdown conversion
- LLMExtractorTool for AI-powered structured data extraction using GPT-4o
- SupabaseTool for database operations with upsert and deduplication
- Utility functions: phone normalization, slugify, CUI extraction, robots.txt checking
- Main orchestration script (main.py) implementing the full scraping pipeline
- Comprehensive configuration management with environment variables
- requirements.txt with all necessary dependencies
- Logging system with file and console output
- Rate limiting and ethical scraping features

#### Frontend
- Next.js 14 with App Router, TypeScript, and Tailwind CSS
- shadcn/ui component library integration (Card, Button, Badge, Input, Dialog, Skeleton)
- Supabase client setup with TypeScript types
- Complete type definitions for all database entities
- Service taxonomy with bilingual labels (Romanian/English)
- Leaflet and react-leaflet for mapping functionality
- lucide-react for icons
- Utility functions for class name merging

#### Database
- PostgreSQL schema with PostGIS extension for geospatial queries
- Six tables: companies, locations, services, contacts, reports, removal_requests
- Row Level Security (RLS) policies for data protection
- Performance indexes including GIST index for geospatial queries
- Automatic timestamp updates with triggers
- Foreign key constraints and check constraints for data integrity

#### DevOps & Documentation
- .gitignore for Python and Node.js projects
- Comprehensive README.md with project overview
- SETUP.md with detailed setup instructions
- CONTRIBUTING.md with contribution guidelines
- PROJECT_STATUS.md with current implementation status
- GitHub Actions workflow for weekly automated scraping
- Environment configuration templates (.env.example)

#### Features
- AI-powered motto extraction with validation
- DSP verification for authorized funeral homes
- GDPR-compliant data minimization
- Robots.txt compliance
- Phone number normalization for Romanian numbers
- Fiscal code (CUI) extraction and validation
- Multi-source data fusion strategy
- Deduplication based on fiscal code and phone numbers

### Security
- Row Level Security (RLS) on all Supabase tables
- Service role separation (public vs. service_role keys)
- Environment variable protection (.gitignore)
- Transparent user-agent identification
- Rate limiting to prevent server overload

---

## [0.1.0] - 2025-12-08

### Project Initialization
- Created project repository structure
- Established development environment
- Defined technical architecture
- Completed Phase 1: Infrastructure Setup

---

## Future Releases

### [0.2.0] - Planned
- Frontend components implementation
- Homepage with company directory
- Company profile pages
- Interactive map view
- Search and filter functionality

### [0.3.0] - Planned
- API routes implementation
- GDPR removal request workflow
- User feedback system
- SEO optimizations (JSON-LD, sitemap)

### [0.4.0] - Planned
- Testing suite (unit, integration, E2E)
- Performance optimizations
- Accessibility improvements
- Mobile optimizations

### [1.0.0] - Planned
- Production deployment
- Custom domain configuration
- Monitoring and analytics
- Full documentation
- Public launch
