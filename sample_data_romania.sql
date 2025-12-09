-- Additional Sample Data for Romania Funeral Directory
-- Adds sample companies in multiple cities across Romania
-- All entries marked as [SAMPLE] in description

-- First, update existing Timișoara locations
UPDATE locations 
SET city = 'Timișoara', county = 'Timiș', county_id = (SELECT id FROM counties WHERE slug = 'timis');

-- ============================================
-- BUCUREȘTI
-- ============================================
INSERT INTO companies (name, slug, motto, description, fiscal_code, website, is_verified, is_non_stop) VALUES
('Funerare București Central', 'funerare-bucuresti-central', 'Profesionalism în cele mai grele momente', '[SAMPLE] Date de test - nu este o firmă reală', 'RO11111111', 'https://example.com/buc-central', true, true),
('Casa Eternității București', 'casa-eternitatii-bucuresti', 'Cu grijă și respect', '[SAMPLE] Date de test - nu este o firmă reală', 'RO11111112', 'https://example.com/eternitate-buc', true, false),
('Memorial Sector 1', 'memorial-sector-1', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'RO11111113', NULL, false, false);

INSERT INTO locations (company_id, address, city, county, county_id, type) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-bucuresti-central'), 'Calea Victoriei 100, Sector 1', 'București', 'București', (SELECT id FROM counties WHERE slug = 'bucuresti'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'casa-eternitatii-bucuresti'), 'Bulevardul Unirii 50, Sector 3', 'București', 'București', (SELECT id FROM counties WHERE slug = 'bucuresti'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'memorial-sector-1'), 'Strada Aviatorilor 25, Sector 1', 'București', 'București', (SELECT id FROM counties WHERE slug = 'bucuresti'), 'headquarters');

INSERT INTO contacts (company_id, type, value, is_primary) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-bucuresti-central'), 'phone_mobile', '0721 111 111', true),
((SELECT id FROM companies WHERE slug = 'funerare-bucuresti-central'), 'email', 'contact@buc-central-sample.ro', false),
((SELECT id FROM companies WHERE slug = 'casa-eternitatii-bucuresti'), 'phone_mobile', '0722 222 222', true),
((SELECT id FROM companies WHERE slug = 'memorial-sector-1'), 'phone_landline', '021 123 4567', true);

INSERT INTO services (company_id, service_tag) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-bucuresti-central'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-bucuresti-central'), 'cremation'),
((SELECT id FROM companies WHERE slug = 'funerare-bucuresti-central'), 'coffins'),
((SELECT id FROM companies WHERE slug = 'funerare-bucuresti-central'), 'bureaucracy'),
((SELECT id FROM companies WHERE slug = 'casa-eternitatii-bucuresti'), 'transport'),
((SELECT id FROM companies WHERE slug = 'casa-eternitatii-bucuresti'), 'wake_house'),
((SELECT id FROM companies WHERE slug = 'casa-eternitatii-bucuresti'), 'religious'),
((SELECT id FROM companies WHERE slug = 'memorial-sector-1'), 'monuments'),
((SELECT id FROM companies WHERE slug = 'memorial-sector-1'), 'flowers');

-- ============================================
-- CLUJ
-- ============================================
INSERT INTO companies (name, slug, motto, description, fiscal_code, website, is_verified, is_non_stop) VALUES
('Servicii Funerare Cluj', 'servicii-funerare-cluj', 'Tradiție și compasiune', '[SAMPLE] Date de test - nu este o firmă reală', 'RO22222221', 'https://example.com/funerare-cluj', true, true),
('Casa Păcii Cluj-Napoca', 'casa-pacii-cluj', 'Liniște în suflet', '[SAMPLE] Date de test - nu este o firmă reală', 'RO22222222', NULL, true, false);

INSERT INTO locations (company_id, address, city, county, county_id, type) VALUES
((SELECT id FROM companies WHERE slug = 'servicii-funerare-cluj'), 'Strada Memorandumului 21, Cluj-Napoca', 'Cluj-Napoca', 'Cluj', (SELECT id FROM counties WHERE slug = 'cluj'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'casa-pacii-cluj'), 'Bulevardul 21 Decembrie 45, Cluj-Napoca', 'Cluj-Napoca', 'Cluj', (SELECT id FROM counties WHERE slug = 'cluj'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'casa-pacii-cluj'), 'Strada Republicii 10, Turda', 'Turda', 'Cluj', (SELECT id FROM counties WHERE slug = 'cluj'), 'wake_house');

INSERT INTO contacts (company_id, type, value, is_primary) VALUES
((SELECT id FROM companies WHERE slug = 'servicii-funerare-cluj'), 'phone_mobile', '0744 333 333', true),
((SELECT id FROM companies WHERE slug = 'servicii-funerare-cluj'), 'email', 'office@funerare-cluj-sample.ro', false),
((SELECT id FROM companies WHERE slug = 'casa-pacii-cluj'), 'phone_mobile', '0755 444 444', true);

INSERT INTO services (company_id, service_tag) VALUES
((SELECT id FROM companies WHERE slug = 'servicii-funerare-cluj'), 'transport'),
((SELECT id FROM companies WHERE slug = 'servicii-funerare-cluj'), 'repatriation'),
((SELECT id FROM companies WHERE slug = 'servicii-funerare-cluj'), 'coffins'),
((SELECT id FROM companies WHERE slug = 'servicii-funerare-cluj'), 'bureaucracy'),
((SELECT id FROM companies WHERE slug = 'casa-pacii-cluj'), 'wake_house'),
((SELECT id FROM companies WHERE slug = 'casa-pacii-cluj'), 'religious'),
((SELECT id FROM companies WHERE slug = 'casa-pacii-cluj'), 'flowers');

-- ============================================
-- IAȘI
-- ============================================
INSERT INTO companies (name, slug, motto, description, fiscal_code, website, is_verified, is_non_stop) VALUES
('Funerare Moldova Iași', 'funerare-moldova-iasi', 'Respect pentru cei dragi', '[SAMPLE] Date de test - nu este o firmă reală', 'RO33333331', 'https://example.com/moldova-iasi', true, false),
('Eternal Rest Iași', 'eternal-rest-iasi', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'RO33333332', NULL, false, true);

INSERT INTO locations (company_id, address, city, county, county_id, type) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-moldova-iasi'), 'Bulevardul Ștefan cel Mare 88, Iași', 'Iași', 'Iași', (SELECT id FROM counties WHERE slug = 'iasi'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'eternal-rest-iasi'), 'Strada Păcurari 55, Iași', 'Iași', 'Iași', (SELECT id FROM counties WHERE slug = 'iasi'), 'headquarters');

INSERT INTO contacts (company_id, type, value, is_primary) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-moldova-iasi'), 'phone_mobile', '0766 555 555', true),
((SELECT id FROM companies WHERE slug = 'funerare-moldova-iasi'), 'phone_landline', '0232 123 456', false),
((SELECT id FROM companies WHERE slug = 'eternal-rest-iasi'), 'phone_mobile', '0777 666 666', true);

INSERT INTO services (company_id, service_tag) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-moldova-iasi'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-moldova-iasi'), 'embalming'),
((SELECT id FROM companies WHERE slug = 'funerare-moldova-iasi'), 'coffins'),
((SELECT id FROM companies WHERE slug = 'eternal-rest-iasi'), 'transport'),
((SELECT id FROM companies WHERE slug = 'eternal-rest-iasi'), 'wake_house'),
((SELECT id FROM companies WHERE slug = 'eternal-rest-iasi'), 'bureaucracy');

-- ============================================
-- CONSTANȚA
-- ============================================
INSERT INTO companies (name, slug, motto, description, fiscal_code, website, is_verified, is_non_stop) VALUES
('Funerare Litoral Constanța', 'funerare-litoral-constanta', 'Alături de familie', '[SAMPLE] Date de test - nu este o firmă reală', 'RO44444441', 'https://example.com/litoral-ct', true, true),
('Servicii Funerare Mamaia', 'servicii-funerare-mamaia', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'RO44444442', NULL, false, false);

INSERT INTO locations (company_id, address, city, county, county_id, type) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-litoral-constanta'), 'Bulevardul Tomis 150, Constanța', 'Constanța', 'Constanța', (SELECT id FROM counties WHERE slug = 'constanta'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'servicii-funerare-mamaia'), 'Strada Principală 30, Mamaia', 'Mamaia', 'Constanța', (SELECT id FROM counties WHERE slug = 'constanta'), 'headquarters');

INSERT INTO contacts (company_id, type, value, is_primary) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-litoral-constanta'), 'phone_mobile', '0788 777 777', true),
((SELECT id FROM companies WHERE slug = 'servicii-funerare-mamaia'), 'phone_mobile', '0799 888 888', true);

INSERT INTO services (company_id, service_tag) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-litoral-constanta'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-litoral-constanta'), 'repatriation'),
((SELECT id FROM companies WHERE slug = 'funerare-litoral-constanta'), 'cremation'),
((SELECT id FROM companies WHERE slug = 'servicii-funerare-mamaia'), 'coffins'),
((SELECT id FROM companies WHERE slug = 'servicii-funerare-mamaia'), 'flowers');

-- ============================================
-- BRAȘOV
-- ============================================
INSERT INTO companies (name, slug, motto, description, fiscal_code, website, is_verified, is_non_stop) VALUES
('Casa Funerară Brașov', 'casa-funerara-brasov', 'Demnitate și respect', '[SAMPLE] Date de test - nu este o firmă reală', 'RO55555551', 'https://example.com/funerare-brasov', true, false),
('Memorial Transilvania', 'memorial-transilvania', 'Tradiție în servicii funerare', '[SAMPLE] Date de test - nu este o firmă reală', 'RO55555552', NULL, true, true);

INSERT INTO locations (company_id, address, city, county, county_id, type) VALUES
((SELECT id FROM companies WHERE slug = 'casa-funerara-brasov'), 'Strada Republicii 35, Brașov', 'Brașov', 'Brașov', (SELECT id FROM counties WHERE slug = 'brasov'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'memorial-transilvania'), 'Bulevardul Eroilor 20, Brașov', 'Brașov', 'Brașov', (SELECT id FROM counties WHERE slug = 'brasov'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'memorial-transilvania'), 'Strada Lungă 100, Brașov', 'Brașov', 'Brașov', (SELECT id FROM counties WHERE slug = 'brasov'), 'wake_house');

INSERT INTO contacts (company_id, type, value, is_primary) VALUES
((SELECT id FROM companies WHERE slug = 'casa-funerara-brasov'), 'phone_mobile', '0722 999 111', true),
((SELECT id FROM companies WHERE slug = 'casa-funerara-brasov'), 'email', 'contact@brasov-sample.ro', false),
((SELECT id FROM companies WHERE slug = 'memorial-transilvania'), 'phone_mobile', '0733 999 222', true),
((SELECT id FROM companies WHERE slug = 'memorial-transilvania'), 'phone_landline', '0268 123 456', false);

INSERT INTO services (company_id, service_tag) VALUES
((SELECT id FROM companies WHERE slug = 'casa-funerara-brasov'), 'transport'),
((SELECT id FROM companies WHERE slug = 'casa-funerara-brasov'), 'coffins'),
((SELECT id FROM companies WHERE slug = 'casa-funerara-brasov'), 'monuments'),
((SELECT id FROM companies WHERE slug = 'memorial-transilvania'), 'transport'),
((SELECT id FROM companies WHERE slug = 'memorial-transilvania'), 'wake_house'),
((SELECT id FROM companies WHERE slug = 'memorial-transilvania'), 'religious'),
((SELECT id FROM companies WHERE slug = 'memorial-transilvania'), 'embalming');

-- ============================================
-- SIBIU
-- ============================================
INSERT INTO companies (name, slug, motto, description, fiscal_code, website, is_verified, is_non_stop) VALUES
('Funerare Sibiu NonStop', 'funerare-sibiu-nonstop', 'Disponibili 24/7', '[SAMPLE] Date de test - nu este o firmă reală', 'RO66666661', 'https://example.com/sibiu-nonstop', true, true);

INSERT INTO locations (company_id, address, city, county, county_id, type) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-sibiu-nonstop'), 'Strada Nicolae Bălcescu 40, Sibiu', 'Sibiu', 'Sibiu', (SELECT id FROM counties WHERE slug = 'sibiu'), 'headquarters');

INSERT INTO contacts (company_id, type, value, is_primary) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-sibiu-nonstop'), 'phone_mobile', '0744 111 333', true),
((SELECT id FROM companies WHERE slug = 'funerare-sibiu-nonstop'), 'phone_mobile', '0744 111 334', false);

INSERT INTO services (company_id, service_tag) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-sibiu-nonstop'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-sibiu-nonstop'), 'cremation'),
((SELECT id FROM companies WHERE slug = 'funerare-sibiu-nonstop'), 'coffins'),
((SELECT id FROM companies WHERE slug = 'funerare-sibiu-nonstop'), 'bureaucracy'),
((SELECT id FROM companies WHERE slug = 'funerare-sibiu-nonstop'), 'religious');

-- ============================================
-- CRAIOVA (Dolj)
-- ============================================
INSERT INTO companies (name, slug, motto, description, fiscal_code, website, is_verified, is_non_stop) VALUES
('Servicii Funerare Oltenia', 'servicii-funerare-oltenia', 'Cu drag pentru Oltenia', '[SAMPLE] Date de test - nu este o firmă reală', 'RO77777771', NULL, true, false);

INSERT INTO locations (company_id, address, city, county, county_id, type) VALUES
((SELECT id FROM companies WHERE slug = 'servicii-funerare-oltenia'), 'Calea București 50, Craiova', 'Craiova', 'Dolj', (SELECT id FROM counties WHERE slug = 'dolj'), 'headquarters');

INSERT INTO contacts (company_id, type, value, is_primary) VALUES
((SELECT id FROM companies WHERE slug = 'servicii-funerare-oltenia'), 'phone_mobile', '0755 222 444', true);

INSERT INTO services (company_id, service_tag) VALUES
((SELECT id FROM companies WHERE slug = 'servicii-funerare-oltenia'), 'transport'),
((SELECT id FROM companies WHERE slug = 'servicii-funerare-oltenia'), 'coffins'),
((SELECT id FROM companies WHERE slug = 'servicii-funerare-oltenia'), 'flowers'),
((SELECT id FROM companies WHERE slug = 'servicii-funerare-oltenia'), 'monuments');

-- ============================================
-- ORADEA (Bihor)
-- ============================================
INSERT INTO companies (name, slug, motto, description, fiscal_code, website, is_verified, is_non_stop) VALUES
('Funerare Crișana Oradea', 'funerare-crisana-oradea', 'Servicii complete', '[SAMPLE] Date de test - nu este o firmă reală', 'RO88888881', 'https://example.com/crisana', false, true);

INSERT INTO locations (company_id, address, city, county, county_id, type) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-crisana-oradea'), 'Strada Republicii 80, Oradea', 'Oradea', 'Bihor', (SELECT id FROM counties WHERE slug = 'bihor'), 'headquarters');

INSERT INTO contacts (company_id, type, value, is_primary) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-crisana-oradea'), 'phone_mobile', '0766 333 555', true);

INSERT INTO services (company_id, service_tag) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-crisana-oradea'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-crisana-oradea'), 'repatriation'),
((SELECT id FROM companies WHERE slug = 'funerare-crisana-oradea'), 'wake_house');

-- ============================================
-- ARAD
-- ============================================
INSERT INTO companies (name, slug, motto, description, fiscal_code, website, is_verified, is_non_stop) VALUES
('Casa Memorială Arad', 'casa-memoriala-arad', 'În memoria celor dragi', '[SAMPLE] Date de test - nu este o firmă reală', 'RO99999991', NULL, true, false);

INSERT INTO locations (company_id, address, city, county, county_id, type) VALUES
((SELECT id FROM companies WHERE slug = 'casa-memoriala-arad'), 'Bulevardul Revoluției 75, Arad', 'Arad', 'Arad', (SELECT id FROM counties WHERE slug = 'arad'), 'headquarters');

INSERT INTO contacts (company_id, type, value, is_primary) VALUES
((SELECT id FROM companies WHERE slug = 'casa-memoriala-arad'), 'phone_mobile', '0777 444 666', true),
((SELECT id FROM companies WHERE slug = 'casa-memoriala-arad'), 'email', 'contact@arad-sample.ro', false);

INSERT INTO services (company_id, service_tag) VALUES
((SELECT id FROM companies WHERE slug = 'casa-memoriala-arad'), 'transport'),
((SELECT id FROM companies WHERE slug = 'casa-memoriala-arad'), 'coffins'),
((SELECT id FROM companies WHERE slug = 'casa-memoriala-arad'), 'religious'),
((SELECT id FROM companies WHERE slug = 'casa-memoriala-arad'), 'bureaucracy');
