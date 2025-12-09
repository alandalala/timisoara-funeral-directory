-- Comprehensive Sample Data for Romania Funeral Directory
-- Multiple real cities per county
-- All entries marked as [SAMPLE] in description

-- First, update existing Timișoara locations
UPDATE locations 
SET city = 'Timișoara', county = 'Timiș', county_id = (SELECT id FROM counties WHERE slug = 'timis');

-- ============================================
-- TIMIȘ - Additional cities
-- ============================================
INSERT INTO companies (name, slug, motto, description, fiscal_code, website, is_verified, is_non_stop) VALUES
('Funerare Lugoj', 'funerare-lugoj', 'Servicii de încredere', '[SAMPLE] Date de test - nu este o firmă reală', 'ROTM000001', NULL, true, false),
('Casa Funerară Sânnicolau Mare', 'casa-funerara-sannicolau', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'ROTM000002', NULL, false, false),
('Servicii Funerare Jimbolia', 'servicii-funerare-jimbolia', 'Aproape de comunitate', '[SAMPLE] Date de test - nu este o firmă reală', 'ROTM000003', NULL, true, false),
('Funerare Făget', 'funerare-faget', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'ROTM000004', NULL, false, true);

INSERT INTO locations (company_id, address, city, county, county_id, type) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-lugoj'), 'Strada Timisorii 45, Lugoj', 'Lugoj', 'Timiș', (SELECT id FROM counties WHERE slug = 'timis'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'casa-funerara-sannicolau'), 'Strada Republicii 12, Sânnicolau Mare', 'Sânnicolau Mare', 'Timiș', (SELECT id FROM counties WHERE slug = 'timis'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'servicii-funerare-jimbolia'), 'Strada Lorena 8, Jimbolia', 'Jimbolia', 'Timiș', (SELECT id FROM counties WHERE slug = 'timis'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-faget'), 'Strada Principală 23, Făget', 'Făget', 'Timiș', (SELECT id FROM counties WHERE slug = 'timis'), 'headquarters');

INSERT INTO contacts (company_id, type, value, is_primary) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-lugoj'), 'phone_mobile', '0756 001 001', true),
((SELECT id FROM companies WHERE slug = 'casa-funerara-sannicolau'), 'phone_mobile', '0756 001 002', true),
((SELECT id FROM companies WHERE slug = 'servicii-funerare-jimbolia'), 'phone_mobile', '0756 001 003', true),
((SELECT id FROM companies WHERE slug = 'funerare-faget'), 'phone_mobile', '0756 001 004', true);

INSERT INTO services (company_id, service_tag) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-lugoj'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-lugoj'), 'coffins'),
((SELECT id FROM companies WHERE slug = 'casa-funerara-sannicolau'), 'transport'),
((SELECT id FROM companies WHERE slug = 'servicii-funerare-jimbolia'), 'transport'),
((SELECT id FROM companies WHERE slug = 'servicii-funerare-jimbolia'), 'flowers'),
((SELECT id FROM companies WHERE slug = 'funerare-faget'), 'transport');

-- ============================================
-- BUCUREȘTI & ILFOV
-- ============================================
INSERT INTO companies (name, slug, motto, description, fiscal_code, website, is_verified, is_non_stop) VALUES
('Funerare București Central', 'funerare-bucuresti-central', 'Profesionalism în cele mai grele momente', '[SAMPLE] Date de test - nu este o firmă reală', 'ROB0000001', 'https://example.com/buc-central', true, true),
('Casa Eternității Sector 3', 'casa-eternitatii-sector3', 'Cu grijă și respect', '[SAMPLE] Date de test - nu este o firmă reală', 'ROB0000002', NULL, true, false),
('Memorial Sector 6', 'memorial-sector-6', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'ROB0000003', NULL, false, false),
('Funerare Voluntari', 'funerare-voluntari', 'Servicii complete Ilfov', '[SAMPLE] Date de test - nu este o firmă reală', 'ROB0000004', NULL, true, false),
('Casa Păcii Buftea', 'casa-pacii-buftea', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'ROB0000005', NULL, false, true),
('Servicii Funerare Popești-Leordeni', 'funerare-popesti', 'Mereu alături', '[SAMPLE] Date de test - nu este o firmă reală', 'ROB0000006', NULL, true, false),
('Funerare Otopeni', 'funerare-otopeni', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'ROB0000007', NULL, false, false),
('Memorial Bragadiru', 'memorial-bragadiru', 'Tradiție și respect', '[SAMPLE] Date de test - nu este o firmă reală', 'ROB0000008', NULL, true, true);

INSERT INTO locations (company_id, address, city, county, county_id, type) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-bucuresti-central'), 'Calea Victoriei 100', 'București', 'București', (SELECT id FROM counties WHERE slug = 'bucuresti'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'casa-eternitatii-sector3'), 'Bulevardul Unirii 50', 'București', 'București', (SELECT id FROM counties WHERE slug = 'bucuresti'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'memorial-sector-6'), 'Strada Drumul Taberei 25', 'București', 'București', (SELECT id FROM counties WHERE slug = 'bucuresti'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-voluntari'), 'Șoseaua Afumați 78', 'Voluntari', 'Ilfov', (SELECT id FROM counties WHERE slug = 'ilfov'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'casa-pacii-buftea'), 'Strada Studioului 15', 'Buftea', 'Ilfov', (SELECT id FROM counties WHERE slug = 'ilfov'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-popesti'), 'Șoseaua Oltenitei 120', 'Popești-Leordeni', 'Ilfov', (SELECT id FROM counties WHERE slug = 'ilfov'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-otopeni'), 'Calea Bucureștilor 45', 'Otopeni', 'Ilfov', (SELECT id FROM counties WHERE slug = 'ilfov'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'memorial-bragadiru'), 'Strada Libertății 30', 'Bragadiru', 'Ilfov', (SELECT id FROM counties WHERE slug = 'ilfov'), 'headquarters');

INSERT INTO contacts (company_id, type, value, is_primary) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-bucuresti-central'), 'phone_mobile', '0721 111 111', true),
((SELECT id FROM companies WHERE slug = 'casa-eternitatii-sector3'), 'phone_mobile', '0721 111 112', true),
((SELECT id FROM companies WHERE slug = 'memorial-sector-6'), 'phone_mobile', '0721 111 113', true),
((SELECT id FROM companies WHERE slug = 'funerare-voluntari'), 'phone_mobile', '0721 111 114', true),
((SELECT id FROM companies WHERE slug = 'casa-pacii-buftea'), 'phone_mobile', '0721 111 115', true),
((SELECT id FROM companies WHERE slug = 'funerare-popesti'), 'phone_mobile', '0721 111 116', true),
((SELECT id FROM companies WHERE slug = 'funerare-otopeni'), 'phone_mobile', '0721 111 117', true),
((SELECT id FROM companies WHERE slug = 'memorial-bragadiru'), 'phone_mobile', '0721 111 118', true);

INSERT INTO services (company_id, service_tag) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-bucuresti-central'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-bucuresti-central'), 'cremation'),
((SELECT id FROM companies WHERE slug = 'funerare-bucuresti-central'), 'coffins'),
((SELECT id FROM companies WHERE slug = 'casa-eternitatii-sector3'), 'transport'),
((SELECT id FROM companies WHERE slug = 'casa-eternitatii-sector3'), 'wake_house'),
((SELECT id FROM companies WHERE slug = 'memorial-sector-6'), 'monuments'),
((SELECT id FROM companies WHERE slug = 'funerare-voluntari'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-voluntari'), 'bureaucracy'),
((SELECT id FROM companies WHERE slug = 'casa-pacii-buftea'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-popesti'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-popesti'), 'coffins'),
((SELECT id FROM companies WHERE slug = 'funerare-otopeni'), 'transport'),
((SELECT id FROM companies WHERE slug = 'memorial-bragadiru'), 'transport'),
((SELECT id FROM companies WHERE slug = 'memorial-bragadiru'), 'religious');

-- ============================================
-- CLUJ
-- ============================================
INSERT INTO companies (name, slug, motto, description, fiscal_code, website, is_verified, is_non_stop) VALUES
('Servicii Funerare Cluj-Napoca', 'funerare-cluj-napoca', 'Tradiție și compasiune', '[SAMPLE] Date de test - nu este o firmă reală', 'ROCJ000001', NULL, true, true),
('Casa Păcii Turda', 'casa-pacii-turda', 'Liniște în suflet', '[SAMPLE] Date de test - nu este o firmă reală', 'ROCJ000002', NULL, true, false),
('Funerare Dej', 'funerare-dej', 'Alături de familie', '[SAMPLE] Date de test - nu este o firmă reală', 'ROCJ000003', NULL, false, false),
('Memorial Câmpia Turzii', 'memorial-campia-turzii', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'ROCJ000004', NULL, true, false),
('Funerare Gherla', 'funerare-gherla', 'Cu respect', '[SAMPLE] Date de test - nu este o firmă reală', 'ROCJ000005', NULL, false, true),
('Casa Funerară Huedin', 'funerare-huedin', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'ROCJ000006', NULL, true, false);

INSERT INTO locations (company_id, address, city, county, county_id, type) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-cluj-napoca'), 'Strada Memorandumului 21', 'Cluj-Napoca', 'Cluj', (SELECT id FROM counties WHERE slug = 'cluj'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'casa-pacii-turda'), 'Piața Republicii 15', 'Turda', 'Cluj', (SELECT id FROM counties WHERE slug = 'cluj'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-dej'), 'Strada 1 Mai 45', 'Dej', 'Cluj', (SELECT id FROM counties WHERE slug = 'cluj'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'memorial-campia-turzii'), 'Strada Laminoriștilor 12', 'Câmpia Turzii', 'Cluj', (SELECT id FROM counties WHERE slug = 'cluj'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-gherla'), 'Strada Bobâlna 8', 'Gherla', 'Cluj', (SELECT id FROM counties WHERE slug = 'cluj'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-huedin'), 'Strada Horea 33', 'Huedin', 'Cluj', (SELECT id FROM counties WHERE slug = 'cluj'), 'headquarters');

INSERT INTO contacts (company_id, type, value, is_primary) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-cluj-napoca'), 'phone_mobile', '0744 222 001', true),
((SELECT id FROM companies WHERE slug = 'casa-pacii-turda'), 'phone_mobile', '0744 222 002', true),
((SELECT id FROM companies WHERE slug = 'funerare-dej'), 'phone_mobile', '0744 222 003', true),
((SELECT id FROM companies WHERE slug = 'memorial-campia-turzii'), 'phone_mobile', '0744 222 004', true),
((SELECT id FROM companies WHERE slug = 'funerare-gherla'), 'phone_mobile', '0744 222 005', true),
((SELECT id FROM companies WHERE slug = 'funerare-huedin'), 'phone_mobile', '0744 222 006', true);

INSERT INTO services (company_id, service_tag) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-cluj-napoca'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-cluj-napoca'), 'cremation'),
((SELECT id FROM companies WHERE slug = 'funerare-cluj-napoca'), 'repatriation'),
((SELECT id FROM companies WHERE slug = 'casa-pacii-turda'), 'transport'),
((SELECT id FROM companies WHERE slug = 'casa-pacii-turda'), 'wake_house'),
((SELECT id FROM companies WHERE slug = 'funerare-dej'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-dej'), 'coffins'),
((SELECT id FROM companies WHERE slug = 'memorial-campia-turzii'), 'monuments'),
((SELECT id FROM companies WHERE slug = 'funerare-gherla'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-huedin'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-huedin'), 'religious');

-- ============================================
-- IAȘI
-- ============================================
INSERT INTO companies (name, slug, motto, description, fiscal_code, website, is_verified, is_non_stop) VALUES
('Funerare Moldova Iași', 'funerare-iasi-central', 'Respect pentru cei dragi', '[SAMPLE] Date de test - nu este o firmă reală', 'ROIS000001', NULL, true, true),
('Casa Funerară Pașcani', 'funerare-pascani', 'Cu demnitate', '[SAMPLE] Date de test - nu este o firmă reală', 'ROIS000002', NULL, true, false),
('Servicii Funerare Hârlău', 'funerare-harlau', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'ROIS000003', NULL, false, false),
('Memorial Târgu Frumos', 'memorial-targu-frumos', 'Tradiție moldovenească', '[SAMPLE] Date de test - nu este o firmă reală', 'ROIS000004', NULL, true, false),
('Funerare Podu Iloaiei', 'funerare-podu-iloaiei', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'ROIS000005', NULL, false, true);

INSERT INTO locations (company_id, address, city, county, county_id, type) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-iasi-central'), 'Bulevardul Ștefan cel Mare 88', 'Iași', 'Iași', (SELECT id FROM counties WHERE slug = 'iasi'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-pascani'), 'Strada Gării 25', 'Pașcani', 'Iași', (SELECT id FROM counties WHERE slug = 'iasi'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-harlau'), 'Strada Cuza Vodă 12', 'Hârlău', 'Iași', (SELECT id FROM counties WHERE slug = 'iasi'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'memorial-targu-frumos'), 'Strada Petru Rareș 45', 'Târgu Frumos', 'Iași', (SELECT id FROM counties WHERE slug = 'iasi'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-podu-iloaiei'), 'Strada Principală 8', 'Podu Iloaiei', 'Iași', (SELECT id FROM counties WHERE slug = 'iasi'), 'headquarters');

INSERT INTO contacts (company_id, type, value, is_primary) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-iasi-central'), 'phone_mobile', '0766 333 001', true),
((SELECT id FROM companies WHERE slug = 'funerare-pascani'), 'phone_mobile', '0766 333 002', true),
((SELECT id FROM companies WHERE slug = 'funerare-harlau'), 'phone_mobile', '0766 333 003', true),
((SELECT id FROM companies WHERE slug = 'memorial-targu-frumos'), 'phone_mobile', '0766 333 004', true),
((SELECT id FROM companies WHERE slug = 'funerare-podu-iloaiei'), 'phone_mobile', '0766 333 005', true);

INSERT INTO services (company_id, service_tag) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-iasi-central'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-iasi-central'), 'embalming'),
((SELECT id FROM companies WHERE slug = 'funerare-pascani'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-pascani'), 'coffins'),
((SELECT id FROM companies WHERE slug = 'funerare-harlau'), 'transport'),
((SELECT id FROM companies WHERE slug = 'memorial-targu-frumos'), 'monuments'),
((SELECT id FROM companies WHERE slug = 'funerare-podu-iloaiei'), 'transport');

-- ============================================
-- CONSTANȚA
-- ============================================
INSERT INTO companies (name, slug, motto, description, fiscal_code, website, is_verified, is_non_stop) VALUES
('Funerare Litoral Constanța', 'funerare-constanta', 'Alături de familie', '[SAMPLE] Date de test - nu este o firmă reală', 'ROCT000001', NULL, true, true),
('Casa Funerară Mangalia', 'funerare-mangalia', 'Pe malul mării', '[SAMPLE] Date de test - nu este o firmă reală', 'ROCT000002', NULL, true, false),
('Servicii Funerare Medgidia', 'funerare-medgidia', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'ROCT000003', NULL, false, false),
('Memorial Năvodari', 'memorial-navodari', 'Cu respect', '[SAMPLE] Date de test - nu este o firmă reală', 'ROCT000004', NULL, true, false),
('Funerare Cernavodă', 'funerare-cernavoda', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'ROCT000005', NULL, false, true),
('Casa Păcii Eforie', 'funerare-eforie', 'Liniște', '[SAMPLE] Date de test - nu este o firmă reală', 'ROCT000006', NULL, true, false);

INSERT INTO locations (company_id, address, city, county, county_id, type) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-constanta'), 'Bulevardul Tomis 150', 'Constanța', 'Constanța', (SELECT id FROM counties WHERE slug = 'constanta'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-mangalia'), 'Strada Portului 25', 'Mangalia', 'Constanța', (SELECT id FROM counties WHERE slug = 'constanta'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-medgidia'), 'Strada Republicii 45', 'Medgidia', 'Constanța', (SELECT id FROM counties WHERE slug = 'constanta'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'memorial-navodari'), 'Strada Industriilor 12', 'Năvodari', 'Constanța', (SELECT id FROM counties WHERE slug = 'constanta'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-cernavoda'), 'Strada Saligny 8', 'Cernavodă', 'Constanța', (SELECT id FROM counties WHERE slug = 'constanta'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-eforie'), 'Strada Republicii 33', 'Eforie Sud', 'Constanța', (SELECT id FROM counties WHERE slug = 'constanta'), 'headquarters');

INSERT INTO contacts (company_id, type, value, is_primary) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-constanta'), 'phone_mobile', '0788 444 001', true),
((SELECT id FROM companies WHERE slug = 'funerare-mangalia'), 'phone_mobile', '0788 444 002', true),
((SELECT id FROM companies WHERE slug = 'funerare-medgidia'), 'phone_mobile', '0788 444 003', true),
((SELECT id FROM companies WHERE slug = 'memorial-navodari'), 'phone_mobile', '0788 444 004', true),
((SELECT id FROM companies WHERE slug = 'funerare-cernavoda'), 'phone_mobile', '0788 444 005', true),
((SELECT id FROM companies WHERE slug = 'funerare-eforie'), 'phone_mobile', '0788 444 006', true);

INSERT INTO services (company_id, service_tag) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-constanta'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-constanta'), 'repatriation'),
((SELECT id FROM companies WHERE slug = 'funerare-mangalia'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-mangalia'), 'wake_house'),
((SELECT id FROM companies WHERE slug = 'funerare-medgidia'), 'transport'),
((SELECT id FROM companies WHERE slug = 'memorial-navodari'), 'monuments'),
((SELECT id FROM companies WHERE slug = 'funerare-cernavoda'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-eforie'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-eforie'), 'flowers');

-- ============================================
-- BRAȘOV
-- ============================================
INSERT INTO companies (name, slug, motto, description, fiscal_code, website, is_verified, is_non_stop) VALUES
('Casa Funerară Brașov', 'funerare-brasov', 'Demnitate și respect', '[SAMPLE] Date de test - nu este o firmă reală', 'ROBV000001', NULL, true, true),
('Servicii Funerare Făgăraș', 'funerare-fagaras', 'Sub munți', '[SAMPLE] Date de test - nu este o firmă reală', 'ROBV000002', NULL, true, false),
('Memorial Săcele', 'memorial-sacele', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'ROBV000003', NULL, false, false),
('Funerare Codlea', 'funerare-codlea', 'Tradiție', '[SAMPLE] Date de test - nu este o firmă reală', 'ROBV000004', NULL, true, false),
('Casa Păcii Râșnov', 'funerare-rasnov', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'ROBV000005', NULL, false, true),
('Funerare Zărnești', 'funerare-zarnesti', 'La poalele Pietrei Craiului', '[SAMPLE] Date de test - nu este o firmă reală', 'ROBV000006', NULL, true, false);

INSERT INTO locations (company_id, address, city, county, county_id, type) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-brasov'), 'Strada Republicii 35', 'Brașov', 'Brașov', (SELECT id FROM counties WHERE slug = 'brasov'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-fagaras'), 'Strada Negoiu 12', 'Făgăraș', 'Brașov', (SELECT id FROM counties WHERE slug = 'brasov'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'memorial-sacele'), 'Strada Brașovului 45', 'Săcele', 'Brașov', (SELECT id FROM counties WHERE slug = 'brasov'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-codlea'), 'Strada Lungă 78', 'Codlea', 'Brașov', (SELECT id FROM counties WHERE slug = 'brasov'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-rasnov'), 'Strada Cetății 15', 'Râșnov', 'Brașov', (SELECT id FROM counties WHERE slug = 'brasov'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-zarnesti'), 'Strada Mitropolit Ioan Metianu 22', 'Zărnești', 'Brașov', (SELECT id FROM counties WHERE slug = 'brasov'), 'headquarters');

INSERT INTO contacts (company_id, type, value, is_primary) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-brasov'), 'phone_mobile', '0722 555 001', true),
((SELECT id FROM companies WHERE slug = 'funerare-fagaras'), 'phone_mobile', '0722 555 002', true),
((SELECT id FROM companies WHERE slug = 'memorial-sacele'), 'phone_mobile', '0722 555 003', true),
((SELECT id FROM companies WHERE slug = 'funerare-codlea'), 'phone_mobile', '0722 555 004', true),
((SELECT id FROM companies WHERE slug = 'funerare-rasnov'), 'phone_mobile', '0722 555 005', true),
((SELECT id FROM companies WHERE slug = 'funerare-zarnesti'), 'phone_mobile', '0722 555 006', true);

INSERT INTO services (company_id, service_tag) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-brasov'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-brasov'), 'cremation'),
((SELECT id FROM companies WHERE slug = 'funerare-brasov'), 'embalming'),
((SELECT id FROM companies WHERE slug = 'funerare-fagaras'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-fagaras'), 'coffins'),
((SELECT id FROM companies WHERE slug = 'memorial-sacele'), 'monuments'),
((SELECT id FROM companies WHERE slug = 'funerare-codlea'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-rasnov'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-zarnesti'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-zarnesti'), 'religious');

-- ============================================
-- SIBIU
-- ============================================
INSERT INTO companies (name, slug, motto, description, fiscal_code, website, is_verified, is_non_stop) VALUES
('Funerare Sibiu Central', 'funerare-sibiu', 'Disponibili 24/7', '[SAMPLE] Date de test - nu este o firmă reală', 'ROSB000001', NULL, true, true),
('Casa Funerară Mediaș', 'funerare-medias', 'Cu grijă', '[SAMPLE] Date de test - nu este o firmă reală', 'ROSB000002', NULL, true, false),
('Servicii Funerare Cisnădie', 'funerare-cisnadie', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'ROSB000003', NULL, false, false),
('Memorial Agnita', 'memorial-agnita', 'Tradiție săsească', '[SAMPLE] Date de test - nu este o firmă reală', 'ROSB000004', NULL, true, false),
('Funerare Dumbrăveni', 'funerare-dumbraveni', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'ROSB000005', NULL, false, true);

INSERT INTO locations (company_id, address, city, county, county_id, type) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-sibiu'), 'Strada Nicolae Bălcescu 40', 'Sibiu', 'Sibiu', (SELECT id FROM counties WHERE slug = 'sibiu'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-medias'), 'Strada Greweln 15', 'Mediaș', 'Sibiu', (SELECT id FROM counties WHERE slug = 'sibiu'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-cisnadie'), 'Strada Cetății 8', 'Cisnădie', 'Sibiu', (SELECT id FROM counties WHERE slug = 'sibiu'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'memorial-agnita'), 'Strada Mare 22', 'Agnita', 'Sibiu', (SELECT id FROM counties WHERE slug = 'sibiu'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-dumbraveni'), 'Strada Republicii 5', 'Dumbrăveni', 'Sibiu', (SELECT id FROM counties WHERE slug = 'sibiu'), 'headquarters');

INSERT INTO contacts (company_id, type, value, is_primary) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-sibiu'), 'phone_mobile', '0744 666 001', true),
((SELECT id FROM companies WHERE slug = 'funerare-medias'), 'phone_mobile', '0744 666 002', true),
((SELECT id FROM companies WHERE slug = 'funerare-cisnadie'), 'phone_mobile', '0744 666 003', true),
((SELECT id FROM companies WHERE slug = 'memorial-agnita'), 'phone_mobile', '0744 666 004', true),
((SELECT id FROM companies WHERE slug = 'funerare-dumbraveni'), 'phone_mobile', '0744 666 005', true);

INSERT INTO services (company_id, service_tag) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-sibiu'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-sibiu'), 'cremation'),
((SELECT id FROM companies WHERE slug = 'funerare-medias'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-medias'), 'wake_house'),
((SELECT id FROM companies WHERE slug = 'funerare-cisnadie'), 'transport'),
((SELECT id FROM companies WHERE slug = 'memorial-agnita'), 'monuments'),
((SELECT id FROM companies WHERE slug = 'funerare-dumbraveni'), 'transport');

-- ============================================
-- DOLJ (Craiova)
-- ============================================
INSERT INTO companies (name, slug, motto, description, fiscal_code, website, is_verified, is_non_stop) VALUES
('Servicii Funerare Craiova', 'funerare-craiova', 'Cu drag pentru Oltenia', '[SAMPLE] Date de test - nu este o firmă reală', 'RODJ000001', NULL, true, true),
('Casa Funerară Băilești', 'funerare-bailesti', 'Aproape de comunitate', '[SAMPLE] Date de test - nu este o firmă reală', 'RODJ000002', NULL, true, false),
('Funerare Calafat', 'funerare-calafat', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'RODJ000003', NULL, false, false),
('Memorial Filiași', 'memorial-filiasi', 'Tradiție oltenească', '[SAMPLE] Date de test - nu este o firmă reală', 'RODJ000004', NULL, true, false),
('Funerare Segarcea', 'funerare-segarcea', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'RODJ000005', NULL, false, true);

INSERT INTO locations (company_id, address, city, county, county_id, type) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-craiova'), 'Calea București 50', 'Craiova', 'Dolj', (SELECT id FROM counties WHERE slug = 'dolj'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-bailesti'), 'Strada Victoriei 25', 'Băilești', 'Dolj', (SELECT id FROM counties WHERE slug = 'dolj'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-calafat'), 'Strada Traian 12', 'Calafat', 'Dolj', (SELECT id FROM counties WHERE slug = 'dolj'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'memorial-filiasi'), 'Strada Oltului 8', 'Filiași', 'Dolj', (SELECT id FROM counties WHERE slug = 'dolj'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-segarcea'), 'Strada Unirii 15', 'Segarcea', 'Dolj', (SELECT id FROM counties WHERE slug = 'dolj'), 'headquarters');

INSERT INTO contacts (company_id, type, value, is_primary) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-craiova'), 'phone_mobile', '0755 777 001', true),
((SELECT id FROM companies WHERE slug = 'funerare-bailesti'), 'phone_mobile', '0755 777 002', true),
((SELECT id FROM companies WHERE slug = 'funerare-calafat'), 'phone_mobile', '0755 777 003', true),
((SELECT id FROM companies WHERE slug = 'memorial-filiasi'), 'phone_mobile', '0755 777 004', true),
((SELECT id FROM companies WHERE slug = 'funerare-segarcea'), 'phone_mobile', '0755 777 005', true);

INSERT INTO services (company_id, service_tag) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-craiova'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-craiova'), 'coffins'),
((SELECT id FROM companies WHERE slug = 'funerare-bailesti'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-bailesti'), 'flowers'),
((SELECT id FROM companies WHERE slug = 'funerare-calafat'), 'transport'),
((SELECT id FROM companies WHERE slug = 'memorial-filiasi'), 'monuments'),
((SELECT id FROM companies WHERE slug = 'funerare-segarcea'), 'transport');

-- ============================================
-- BIHOR (Oradea)
-- ============================================
INSERT INTO companies (name, slug, motto, description, fiscal_code, website, is_verified, is_non_stop) VALUES
('Funerare Crișana Oradea', 'funerare-oradea', 'Servicii complete', '[SAMPLE] Date de test - nu este o firmă reală', 'ROBH000001', NULL, true, true),
('Casa Funerară Salonta', 'funerare-salonta', 'Cu respect', '[SAMPLE] Date de test - nu este o firmă reală', 'ROBH000002', NULL, true, false),
('Servicii Funerare Marghita', 'funerare-marghita', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'ROBH000003', NULL, false, false),
('Memorial Beiuș', 'memorial-beius', 'Tradiție și grijă', '[SAMPLE] Date de test - nu este o firmă reală', 'ROBH000004', NULL, true, false),
('Funerare Aleșd', 'funerare-alesd', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'ROBH000005', NULL, false, true);

INSERT INTO locations (company_id, address, city, county, county_id, type) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-oradea'), 'Strada Republicii 80', 'Oradea', 'Bihor', (SELECT id FROM counties WHERE slug = 'bihor'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-salonta'), 'Strada Libertății 25', 'Salonta', 'Bihor', (SELECT id FROM counties WHERE slug = 'bihor'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-marghita'), 'Strada Republicii 12', 'Marghita', 'Bihor', (SELECT id FROM counties WHERE slug = 'bihor'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'memorial-beius'), 'Strada Horea 8', 'Beiuș', 'Bihor', (SELECT id FROM counties WHERE slug = 'bihor'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-alesd'), 'Strada Bobâlna 15', 'Aleșd', 'Bihor', (SELECT id FROM counties WHERE slug = 'bihor'), 'headquarters');

INSERT INTO contacts (company_id, type, value, is_primary) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-oradea'), 'phone_mobile', '0766 888 001', true),
((SELECT id FROM companies WHERE slug = 'funerare-salonta'), 'phone_mobile', '0766 888 002', true),
((SELECT id FROM companies WHERE slug = 'funerare-marghita'), 'phone_mobile', '0766 888 003', true),
((SELECT id FROM companies WHERE slug = 'memorial-beius'), 'phone_mobile', '0766 888 004', true),
((SELECT id FROM companies WHERE slug = 'funerare-alesd'), 'phone_mobile', '0766 888 005', true);

INSERT INTO services (company_id, service_tag) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-oradea'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-oradea'), 'repatriation'),
((SELECT id FROM companies WHERE slug = 'funerare-salonta'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-salonta'), 'coffins'),
((SELECT id FROM companies WHERE slug = 'funerare-marghita'), 'transport'),
((SELECT id FROM companies WHERE slug = 'memorial-beius'), 'monuments'),
((SELECT id FROM companies WHERE slug = 'funerare-alesd'), 'transport');

-- ============================================
-- ARAD
-- ============================================
INSERT INTO companies (name, slug, motto, description, fiscal_code, website, is_verified, is_non_stop) VALUES
('Casa Memorială Arad', 'funerare-arad', 'În memoria celor dragi', '[SAMPLE] Date de test - nu este o firmă reală', 'ROAR000001', NULL, true, true),
('Funerare Ineu', 'funerare-ineu', 'Cu compasiune', '[SAMPLE] Date de test - nu este o firmă reală', 'ROAR000002', NULL, true, false),
('Servicii Funerare Lipova', 'funerare-lipova', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'ROAR000003', NULL, false, false),
('Memorial Pecica', 'memorial-pecica', 'Tradiție', '[SAMPLE] Date de test - nu este o firmă reală', 'ROAR000004', NULL, true, false),
('Funerare Chișineu-Criș', 'funerare-chisineu-cris', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'ROAR000005', NULL, false, true);

INSERT INTO locations (company_id, address, city, county, county_id, type) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-arad'), 'Bulevardul Revoluției 75', 'Arad', 'Arad', (SELECT id FROM counties WHERE slug = 'arad'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-ineu'), 'Strada Republicii 20', 'Ineu', 'Arad', (SELECT id FROM counties WHERE slug = 'arad'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-lipova'), 'Strada Nicolae Bălcescu 15', 'Lipova', 'Arad', (SELECT id FROM counties WHERE slug = 'arad'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'memorial-pecica'), 'Strada Principală 8', 'Pecica', 'Arad', (SELECT id FROM counties WHERE slug = 'arad'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-chisineu-cris'), 'Strada Libertății 12', 'Chișineu-Criș', 'Arad', (SELECT id FROM counties WHERE slug = 'arad'), 'headquarters');

INSERT INTO contacts (company_id, type, value, is_primary) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-arad'), 'phone_mobile', '0777 999 001', true),
((SELECT id FROM companies WHERE slug = 'funerare-ineu'), 'phone_mobile', '0777 999 002', true),
((SELECT id FROM companies WHERE slug = 'funerare-lipova'), 'phone_mobile', '0777 999 003', true),
((SELECT id FROM companies WHERE slug = 'memorial-pecica'), 'phone_mobile', '0777 999 004', true),
((SELECT id FROM companies WHERE slug = 'funerare-chisineu-cris'), 'phone_mobile', '0777 999 005', true);

INSERT INTO services (company_id, service_tag) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-arad'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-arad'), 'coffins'),
((SELECT id FROM companies WHERE slug = 'funerare-arad'), 'religious'),
((SELECT id FROM companies WHERE slug = 'funerare-ineu'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-lipova'), 'transport'),
((SELECT id FROM companies WHERE slug = 'memorial-pecica'), 'monuments'),
((SELECT id FROM companies WHERE slug = 'funerare-chisineu-cris'), 'transport');

-- ============================================
-- PRAHOVA (Ploiești)
-- ============================================
INSERT INTO companies (name, slug, motto, description, fiscal_code, website, is_verified, is_non_stop) VALUES
('Funerare Ploiești Central', 'funerare-ploiesti', 'Profesionalism', '[SAMPLE] Date de test - nu este o firmă reală', 'ROPH000001', NULL, true, true),
('Casa Funerară Câmpina', 'funerare-campina', 'La poalele munților', '[SAMPLE] Date de test - nu este o firmă reală', 'ROPH000002', NULL, true, false),
('Servicii Funerare Vălenii de Munte', 'funerare-valenii', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'ROPH000003', NULL, false, false),
('Memorial Sinaia', 'memorial-sinaia', 'În inima munților', '[SAMPLE] Date de test - nu este o firmă reală', 'ROPH000004', NULL, true, false),
('Funerare Bușteni', 'funerare-busteni', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'ROPH000005', NULL, false, true),
('Casa Păcii Azuga', 'funerare-azuga', 'Liniște montană', '[SAMPLE] Date de test - nu este o firmă reală', 'ROPH000006', NULL, true, false);

INSERT INTO locations (company_id, address, city, county, county_id, type) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-ploiesti'), 'Bulevardul Republicii 100', 'Ploiești', 'Prahova', (SELECT id FROM counties WHERE slug = 'prahova'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-campina'), 'Strada Griviței 25', 'Câmpina', 'Prahova', (SELECT id FROM counties WHERE slug = 'prahova'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-valenii'), 'Strada Nicolae Iorga 12', 'Vălenii de Munte', 'Prahova', (SELECT id FROM counties WHERE slug = 'prahova'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'memorial-sinaia'), 'Bulevardul Carol I 45', 'Sinaia', 'Prahova', (SELECT id FROM counties WHERE slug = 'prahova'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-busteni'), 'Strada Telecabinei 8', 'Bușteni', 'Prahova', (SELECT id FROM counties WHERE slug = 'prahova'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-azuga'), 'Strada Victoriei 15', 'Azuga', 'Prahova', (SELECT id FROM counties WHERE slug = 'prahova'), 'headquarters');

INSERT INTO contacts (company_id, type, value, is_primary) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-ploiesti'), 'phone_mobile', '0733 111 001', true),
((SELECT id FROM companies WHERE slug = 'funerare-campina'), 'phone_mobile', '0733 111 002', true),
((SELECT id FROM companies WHERE slug = 'funerare-valenii'), 'phone_mobile', '0733 111 003', true),
((SELECT id FROM companies WHERE slug = 'memorial-sinaia'), 'phone_mobile', '0733 111 004', true),
((SELECT id FROM companies WHERE slug = 'funerare-busteni'), 'phone_mobile', '0733 111 005', true),
((SELECT id FROM companies WHERE slug = 'funerare-azuga'), 'phone_mobile', '0733 111 006', true);

INSERT INTO services (company_id, service_tag) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-ploiesti'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-ploiesti'), 'cremation'),
((SELECT id FROM companies WHERE slug = 'funerare-campina'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-campina'), 'coffins'),
((SELECT id FROM companies WHERE slug = 'funerare-valenii'), 'transport'),
((SELECT id FROM companies WHERE slug = 'memorial-sinaia'), 'monuments'),
((SELECT id FROM companies WHERE slug = 'funerare-busteni'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-azuga'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-azuga'), 'religious');

-- ============================================
-- MUREȘ (Târgu Mureș)
-- ============================================
INSERT INTO companies (name, slug, motto, description, fiscal_code, website, is_verified, is_non_stop) VALUES
('Funerare Târgu Mureș', 'funerare-targu-mures', 'Cu respect', '[SAMPLE] Date de test - nu este o firmă reală', 'ROMS000001', NULL, true, true),
('Casa Funerară Sighișoara', 'funerare-sighisoara', 'Tradiție medievală', '[SAMPLE] Date de test - nu este o firmă reală', 'ROMS000002', NULL, true, false),
('Servicii Funerare Reghin', 'funerare-reghin', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'ROMS000003', NULL, false, false),
('Memorial Luduș', 'memorial-ludus', 'Cu grijă', '[SAMPLE] Date de test - nu este o firmă reală', 'ROMS000004', NULL, true, false),
('Funerare Sovata', 'funerare-sovata', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'ROMS000005', NULL, false, true);

INSERT INTO locations (company_id, address, city, county, county_id, type) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-targu-mures'), 'Piața Trandafirilor 50', 'Târgu Mureș', 'Mureș', (SELECT id FROM counties WHERE slug = 'mures'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-sighisoara'), 'Strada Cetății 15', 'Sighișoara', 'Mureș', (SELECT id FROM counties WHERE slug = 'mures'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-reghin'), 'Strada Petőfi Sándor 25', 'Reghin', 'Mureș', (SELECT id FROM counties WHERE slug = 'mures'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'memorial-ludus'), 'Strada Republicii 8', 'Luduș', 'Mureș', (SELECT id FROM counties WHERE slug = 'mures'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-sovata'), 'Strada Principală 12', 'Sovata', 'Mureș', (SELECT id FROM counties WHERE slug = 'mures'), 'headquarters');

INSERT INTO contacts (company_id, type, value, is_primary) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-targu-mures'), 'phone_mobile', '0755 222 001', true),
((SELECT id FROM companies WHERE slug = 'funerare-sighisoara'), 'phone_mobile', '0755 222 002', true),
((SELECT id FROM companies WHERE slug = 'funerare-reghin'), 'phone_mobile', '0755 222 003', true),
((SELECT id FROM companies WHERE slug = 'memorial-ludus'), 'phone_mobile', '0755 222 004', true),
((SELECT id FROM companies WHERE slug = 'funerare-sovata'), 'phone_mobile', '0755 222 005', true);

INSERT INTO services (company_id, service_tag) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-targu-mures'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-targu-mures'), 'embalming'),
((SELECT id FROM companies WHERE slug = 'funerare-sighisoara'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-sighisoara'), 'wake_house'),
((SELECT id FROM companies WHERE slug = 'funerare-reghin'), 'transport'),
((SELECT id FROM companies WHERE slug = 'memorial-ludus'), 'monuments'),
((SELECT id FROM companies WHERE slug = 'funerare-sovata'), 'transport');
