-- Enable PostGIS extension for geospatial queries
CREATE EXTENSION IF NOT EXISTS postgis;

-- Companies table: Core business entities
CREATE TABLE IF NOT EXISTS companies (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  motto TEXT,
  description TEXT,
  fiscal_code TEXT UNIQUE,
  website TEXT,
  is_verified BOOLEAN DEFAULT FALSE,
  is_non_stop BOOLEAN DEFAULT FALSE,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Locations table: Physical addresses with geospatial data
CREATE TABLE IF NOT EXISTS locations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
  address TEXT NOT NULL,
  geo_point GEOGRAPHY(Point, 4326),
  type TEXT CHECK (type IN ('headquarters', 'wake_house', 'showroom')),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Services table: Service offerings
CREATE TABLE IF NOT EXISTS services (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
  service_tag TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Contacts table: Phone, email, and other contact methods
CREATE TABLE IF NOT EXISTS contacts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
  type TEXT CHECK (type IN ('phone_mobile', 'phone_landline', 'email', 'fax')),
  value TEXT NOT NULL,
  is_primary BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Reports table: User-submitted inaccuracy reports
CREATE TABLE IF NOT EXISTS reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
  issue_type TEXT NOT NULL,
  description TEXT,
  requester_email TEXT,
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'reviewed', 'resolved')),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Removal requests table: GDPR data removal requests
CREATE TABLE IF NOT EXISTS removal_requests (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
  requester_email TEXT NOT NULL,
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected', 'completed')),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_companies_slug ON companies(slug);
CREATE INDEX IF NOT EXISTS idx_companies_fiscal_code ON companies(fiscal_code);
CREATE INDEX IF NOT EXISTS idx_companies_is_verified ON companies(is_verified);
CREATE INDEX IF NOT EXISTS idx_locations_company_id ON locations(company_id);
CREATE INDEX IF NOT EXISTS idx_locations_geo_point ON locations USING GIST(geo_point);
CREATE INDEX IF NOT EXISTS idx_services_company_id ON services(company_id);
CREATE INDEX IF NOT EXISTS idx_services_service_tag ON services(service_tag);
CREATE INDEX IF NOT EXISTS idx_contacts_company_id ON contacts(company_id);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger to auto-update updated_at
CREATE TRIGGER update_companies_updated_at BEFORE UPDATE ON companies
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Row Level Security (RLS) Policies
ALTER TABLE companies ENABLE ROW LEVEL SECURITY;
ALTER TABLE locations ENABLE ROW LEVEL SECURITY;
ALTER TABLE services ENABLE ROW LEVEL SECURITY;
ALTER TABLE contacts ENABLE ROW LEVEL SECURITY;
ALTER TABLE reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE removal_requests ENABLE ROW LEVEL SECURITY;

-- Public read access
CREATE POLICY "Allow public read access on companies" ON companies FOR SELECT USING (true);
CREATE POLICY "Allow public read access on locations" ON locations FOR SELECT USING (true);
CREATE POLICY "Allow public read access on services" ON services FOR SELECT USING (true);
CREATE POLICY "Allow public read access on contacts" ON contacts FOR SELECT USING (true);

-- Service role full access (for backend scraper)
CREATE POLICY "Allow service role full access on companies" ON companies FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');
CREATE POLICY "Allow service role full access on locations" ON locations FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');
CREATE POLICY "Allow service role full access on services" ON services FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');
CREATE POLICY "Allow service role full access on contacts" ON contacts FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');

-- Reports: public can insert, service role can manage
CREATE POLICY "Allow public insert on reports" ON reports FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow service role full access on reports" ON reports FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');

-- Removal requests: similar to reports
CREATE POLICY "Allow public insert on removal_requests" ON removal_requests FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow service role full access on removal_requests" ON removal_requests FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');
