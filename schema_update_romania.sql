-- Schema Update for Romania-wide Coverage
-- Run this in Supabase SQL Editor

-- 1. Create counties reference table
CREATE TABLE IF NOT EXISTS counties (
  id SERIAL PRIMARY KEY,
  name TEXT UNIQUE NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  region TEXT -- e.g., 'Transilvania', 'Moldova', 'Muntenia', etc.
);

-- 2. Add city and county fields to locations table
ALTER TABLE locations 
ADD COLUMN IF NOT EXISTS city TEXT,
ADD COLUMN IF NOT EXISTS county TEXT,
ADD COLUMN IF NOT EXISTS county_id INTEGER REFERENCES counties(id);

-- 3. Create indexes for location-based queries
CREATE INDEX IF NOT EXISTS idx_locations_city ON locations(city);
CREATE INDEX IF NOT EXISTS idx_locations_county ON locations(county);
CREATE INDEX IF NOT EXISTS idx_locations_county_id ON locations(county_id);

-- 4. Insert all Romanian counties
INSERT INTO counties (name, slug, region) VALUES
('Alba', 'alba', 'Transilvania'),
('Arad', 'arad', 'Banat'),
('Argeș', 'arges', 'Muntenia'),
('Bacău', 'bacau', 'Moldova'),
('Bihor', 'bihor', 'Crișana'),
('Bistrița-Năsăud', 'bistrita-nasaud', 'Transilvania'),
('Botoșani', 'botosani', 'Moldova'),
('Brașov', 'brasov', 'Transilvania'),
('Brăila', 'braila', 'Muntenia'),
('București', 'bucuresti', 'București-Ilfov'),
('Buzău', 'buzau', 'Muntenia'),
('Caraș-Severin', 'caras-severin', 'Banat'),
('Călărași', 'calarasi', 'Muntenia'),
('Cluj', 'cluj', 'Transilvania'),
('Constanța', 'constanta', 'Dobrogea'),
('Covasna', 'covasna', 'Transilvania'),
('Dâmbovița', 'dambovita', 'Muntenia'),
('Dolj', 'dolj', 'Oltenia'),
('Galați', 'galati', 'Moldova'),
('Giurgiu', 'giurgiu', 'Muntenia'),
('Gorj', 'gorj', 'Oltenia'),
('Harghita', 'harghita', 'Transilvania'),
('Hunedoara', 'hunedoara', 'Transilvania'),
('Ialomița', 'ialomita', 'Muntenia'),
('Iași', 'iasi', 'Moldova'),
('Ilfov', 'ilfov', 'București-Ilfov'),
('Maramureș', 'maramures', 'Maramureș'),
('Mehedinți', 'mehedinti', 'Oltenia'),
('Mureș', 'mures', 'Transilvania'),
('Neamț', 'neamt', 'Moldova'),
('Olt', 'olt', 'Oltenia'),
('Prahova', 'prahova', 'Muntenia'),
('Satu Mare', 'satu-mare', 'Crișana'),
('Sălaj', 'salaj', 'Transilvania'),
('Sibiu', 'sibiu', 'Transilvania'),
('Suceava', 'suceava', 'Moldova'),
('Teleorman', 'teleorman', 'Muntenia'),
('Timiș', 'timis', 'Banat'),
('Tulcea', 'tulcea', 'Dobrogea'),
('Vaslui', 'vaslui', 'Moldova'),
('Vâlcea', 'valcea', 'Oltenia'),
('Vrancea', 'vrancea', 'Moldova')
ON CONFLICT (slug) DO NOTHING;

-- 5. Enable RLS on counties table
ALTER TABLE counties ENABLE ROW LEVEL SECURITY;

-- 6. Public read access for counties
CREATE POLICY "Allow public read access on counties" ON counties FOR SELECT USING (true);

-- 7. Update existing sample data with Timiș county
UPDATE locations 
SET city = 'Timișoara', county = 'Timiș', county_id = (SELECT id FROM counties WHERE slug = 'timis')
WHERE address LIKE '%Timișoara%';
