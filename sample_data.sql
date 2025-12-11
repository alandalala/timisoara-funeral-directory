-- ============================================================================
-- COMPREHENSIVE SAMPLE DATA - ALL ROMANIA (42 COUNTIES)
-- Romania Funeral Services Directory
-- ============================================================================
-- IMPORTANT: All data marked with [SAMPLE] is for testing purposes only
-- These are NOT real companies!
-- ============================================================================

-- ============================================================================
-- CLEANUP: Delete existing sample data before inserting new data
-- ============================================================================
DELETE FROM services WHERE company_id IN (SELECT id FROM companies WHERE description LIKE '%[SAMPLE]%');
DELETE FROM contacts WHERE company_id IN (SELECT id FROM companies WHERE description LIKE '%[SAMPLE]%');
DELETE FROM locations WHERE company_id IN (SELECT id FROM companies WHERE description LIKE '%[SAMPLE]%');
DELETE FROM companies WHERE description LIKE '%[SAMPLE]%';

-- ============================================================================
-- INSERT COUNTIES (if not exists)
-- ============================================================================
INSERT INTO counties (name, slug, region) VALUES
('Alba', 'alba', 'Transilvania'),
('Arad', 'arad', 'Vest'),
('Argeș', 'arges', 'Muntenia'),
('Bacău', 'bacau', 'Moldova'),
('Bihor', 'bihor', 'Vest'),
('Bistrița-Năsăud', 'bistrita-nasaud', 'Transilvania'),
('Botoșani', 'botosani', 'Moldova'),
('Brăila', 'braila', 'Muntenia'),
('Brașov', 'brasov', 'Transilvania'),
('București', 'bucuresti', 'București-Ilfov'),
('Buzău', 'buzau', 'Muntenia'),
('Caraș-Severin', 'caras-severin', 'Vest'),
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
('Maramureș', 'maramures', 'Transilvania'),
('Mehedinți', 'mehedinti', 'Oltenia'),
('Mureș', 'mures', 'Transilvania'),
('Neamț', 'neamt', 'Moldova'),
('Olt', 'olt', 'Oltenia'),
('Prahova', 'prahova', 'Muntenia'),
('Satu Mare', 'satu-mare', 'Transilvania'),
('Sălaj', 'salaj', 'Transilvania'),
('Sibiu', 'sibiu', 'Transilvania'),
('Suceava', 'suceava', 'Moldova'),
('Teleorman', 'teleorman', 'Muntenia'),
('Timiș', 'timis', 'Vest'),
('Tulcea', 'tulcea', 'Dobrogea'),
('Vaslui', 'vaslui', 'Moldova'),
('Vâlcea', 'valcea', 'Oltenia'),
('Vrancea', 'vrancea', 'Moldova')
ON CONFLICT (slug) DO NOTHING;

-- ============================================================================
-- TIMIȘ COUNTY COMPANIES
-- ============================================================================
INSERT INTO companies (name, slug, motto, description, fiscal_code, website, is_verified, is_non_stop) VALUES
('Funerare Timișoara Central', 'funerare-timisoara-central', 'Servicii complete non-stop', '[SAMPLE] Date de test - nu este o firmă reală', 'ROTM100001', NULL, true, true),
('Funerare Lugoj', 'funerare-lugoj', 'Cu respect și demnitate', '[SAMPLE] Date de test - nu este o firmă reală', 'ROTM100002', NULL, true, false),
('Casa Funerară Buziș', 'funerare-buzias', 'Liniște și pace', '[SAMPLE] Date de test - nu este o firmă reală', 'ROTM100003', NULL, true, false),
('Funerare Jimbolia', 'funerare-jimbolia', 'Tradiție și grijă', '[SAMPLE] Date de test - nu este o firmă reală', 'ROTM100008', NULL, true, true),
('Funerare Sânnicolau Mare', 'funerare-sannicolau-mare', 'Respect pentru cei dragi', '[SAMPLE] Date de test - nu este o firmă reală', 'ROTM100010', NULL, true, false),
('Funerare Giroc', 'funerare-giroc', 'Profesionalism', '[SAMPLE] Date de test - nu este o firmă reală', 'ROTM100011', NULL, true, false),
('Memorial Dumbrăvița', 'funerare-dumbravita', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'ROTM100012', NULL, false, false),
('Casa Funerară Ghiroda', 'funerare-ghiroda', 'Alături de familie', '[SAMPLE] Date de test - nu este o firmă reală', 'ROTM100013', NULL, true, false);

-- TIMIȘ LOCATIONS
INSERT INTO locations (company_id, address, city, county, county_id, type) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-timisoara-central'), 'Strada Victoriei 100', 'Timișoara', 'Timiș', (SELECT id FROM counties WHERE slug = 'timis'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-lugoj'), 'Strada Cernei 15', 'Lugoj', 'Timiș', (SELECT id FROM counties WHERE slug = 'timis'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-buzias'), 'Strada Principală 20', 'Buziaș', 'Timiș', (SELECT id FROM counties WHERE slug = 'timis'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-jimbolia'), 'Strada Republicii 45', 'Jimbolia', 'Timiș', (SELECT id FROM counties WHERE slug = 'timis'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-sannicolau-mare'), 'Strada Libertății 12', 'Sânnicolau Mare', 'Timiș', (SELECT id FROM counties WHERE slug = 'timis'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-giroc'), 'Strada Principală 5', 'Giroc', 'Timiș', (SELECT id FROM counties WHERE slug = 'timis'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-dumbravita'), 'Strada Pădurii 8', 'Dumbrăvița', 'Timiș', (SELECT id FROM counties WHERE slug = 'timis'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-ghiroda'), 'Strada Mare 22', 'Ghiroda', 'Timiș', (SELECT id FROM counties WHERE slug = 'timis'), 'headquarters');

-- TIMIȘ CONTACTS
INSERT INTO contacts (company_id, type, value, is_primary) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-timisoara-central'), 'phone_mobile', '0756 100 001', true),
((SELECT id FROM companies WHERE slug = 'funerare-lugoj'), 'phone_mobile', '0756 100 002', true),
((SELECT id FROM companies WHERE slug = 'funerare-buzias'), 'phone_mobile', '0756 100 003', true),
((SELECT id FROM companies WHERE slug = 'funerare-jimbolia'), 'phone_mobile', '0756 100 004', true),
((SELECT id FROM companies WHERE slug = 'funerare-sannicolau-mare'), 'phone_mobile', '0756 100 005', true),
((SELECT id FROM companies WHERE slug = 'funerare-giroc'), 'phone_mobile', '0756 100 006', true),
((SELECT id FROM companies WHERE slug = 'funerare-dumbravita'), 'phone_mobile', '0756 100 007', true),
((SELECT id FROM companies WHERE slug = 'funerare-ghiroda'), 'phone_mobile', '0756 100 008', true);

-- TIMIȘ SERVICES
-- Funerare Timișoara Central - ALL SERVICES (full-service provider)
INSERT INTO services (company_id, service_tag) VALUES
-- Documentation & Legal
((SELECT id FROM companies WHERE slug = 'funerare-timisoara-central'), 'death_certificate'),
((SELECT id FROM companies WHERE slug = 'funerare-timisoara-central'), 'death_registration'),
((SELECT id FROM companies WHERE slug = 'funerare-timisoara-central'), 'permits'),
((SELECT id FROM companies WHERE slug = 'funerare-timisoara-central'), 'funeral_aid'),
-- Body Care & Storage
((SELECT id FROM companies WHERE slug = 'funerare-timisoara-central'), 'embalming'),
((SELECT id FROM companies WHERE slug = 'funerare-timisoara-central'), 'body_preparation'),
((SELECT id FROM companies WHERE slug = 'funerare-timisoara-central'), 'refrigeration'),
-- Transport & Logistics
((SELECT id FROM companies WHERE slug = 'funerare-timisoara-central'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-timisoara-central'), 'transport_long'),
((SELECT id FROM companies WHERE slug = 'funerare-timisoara-central'), 'repatriation'),
((SELECT id FROM companies WHERE slug = 'funerare-timisoara-central'), 'pallbearers'),
-- Products
((SELECT id FROM companies WHERE slug = 'funerare-timisoara-central'), 'coffins'),
((SELECT id FROM companies WHERE slug = 'funerare-timisoara-central'), 'urns'),
((SELECT id FROM companies WHERE slug = 'funerare-timisoara-central'), 'textiles'),
((SELECT id FROM companies WHERE slug = 'funerare-timisoara-central'), 'crosses'),
-- Ritual Essentials
((SELECT id FROM companies WHERE slug = 'funerare-timisoara-central'), 'coliva'),
((SELECT id FROM companies WHERE slug = 'funerare-timisoara-central'), 'liturgical_items'),
((SELECT id FROM companies WHERE slug = 'funerare-timisoara-central'), 'mourning_items'),
-- Ceremony & Venue
((SELECT id FROM companies WHERE slug = 'funerare-timisoara-central'), 'wake_house'),
((SELECT id FROM companies WHERE slug = 'funerare-timisoara-central'), 'church_service'),
((SELECT id FROM companies WHERE slug = 'funerare-timisoara-central'), 'flowers'),
((SELECT id FROM companies WHERE slug = 'funerare-timisoara-central'), 'music'),
-- Catering & Alms
((SELECT id FROM companies WHERE slug = 'funerare-timisoara-central'), 'food_packages'),
((SELECT id FROM companies WHERE slug = 'funerare-timisoara-central'), 'catering'),
((SELECT id FROM companies WHERE slug = 'funerare-timisoara-central'), 'restaurant'),
((SELECT id FROM companies WHERE slug = 'funerare-timisoara-central'), 'memorial_services'),
-- Cemetery Works
((SELECT id FROM companies WHERE slug = 'funerare-timisoara-central'), 'monuments'),
((SELECT id FROM companies WHERE slug = 'funerare-timisoara-central'), 'crypts'),
((SELECT id FROM companies WHERE slug = 'funerare-timisoara-central'), 'photo_ceramics'),
-- Legacy services
((SELECT id FROM companies WHERE slug = 'funerare-timisoara-central'), 'cremation'),
((SELECT id FROM companies WHERE slug = 'funerare-timisoara-central'), 'bureaucracy'),
((SELECT id FROM companies WHERE slug = 'funerare-timisoara-central'), 'religious'),

-- Funerare Lugoj - ALL SERVICES (full-service provider)
-- Documentation & Legal
((SELECT id FROM companies WHERE slug = 'funerare-lugoj'), 'death_certificate'),
((SELECT id FROM companies WHERE slug = 'funerare-lugoj'), 'death_registration'),
((SELECT id FROM companies WHERE slug = 'funerare-lugoj'), 'permits'),
((SELECT id FROM companies WHERE slug = 'funerare-lugoj'), 'funeral_aid'),
-- Body Care & Storage
((SELECT id FROM companies WHERE slug = 'funerare-lugoj'), 'embalming'),
((SELECT id FROM companies WHERE slug = 'funerare-lugoj'), 'body_preparation'),
((SELECT id FROM companies WHERE slug = 'funerare-lugoj'), 'refrigeration'),
-- Transport & Logistics
((SELECT id FROM companies WHERE slug = 'funerare-lugoj'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-lugoj'), 'transport_long'),
((SELECT id FROM companies WHERE slug = 'funerare-lugoj'), 'repatriation'),
((SELECT id FROM companies WHERE slug = 'funerare-lugoj'), 'pallbearers'),
-- Products
((SELECT id FROM companies WHERE slug = 'funerare-lugoj'), 'coffins'),
((SELECT id FROM companies WHERE slug = 'funerare-lugoj'), 'urns'),
((SELECT id FROM companies WHERE slug = 'funerare-lugoj'), 'textiles'),
((SELECT id FROM companies WHERE slug = 'funerare-lugoj'), 'crosses'),
-- Ritual Essentials
((SELECT id FROM companies WHERE slug = 'funerare-lugoj'), 'coliva'),
((SELECT id FROM companies WHERE slug = 'funerare-lugoj'), 'liturgical_items'),
((SELECT id FROM companies WHERE slug = 'funerare-lugoj'), 'mourning_items'),
-- Ceremony & Venue
((SELECT id FROM companies WHERE slug = 'funerare-lugoj'), 'wake_house'),
((SELECT id FROM companies WHERE slug = 'funerare-lugoj'), 'church_service'),
((SELECT id FROM companies WHERE slug = 'funerare-lugoj'), 'flowers'),
((SELECT id FROM companies WHERE slug = 'funerare-lugoj'), 'music'),
-- Catering & Alms
((SELECT id FROM companies WHERE slug = 'funerare-lugoj'), 'food_packages'),
((SELECT id FROM companies WHERE slug = 'funerare-lugoj'), 'catering'),
((SELECT id FROM companies WHERE slug = 'funerare-lugoj'), 'restaurant'),
((SELECT id FROM companies WHERE slug = 'funerare-lugoj'), 'memorial_services'),
-- Cemetery Works
((SELECT id FROM companies WHERE slug = 'funerare-lugoj'), 'monuments'),
((SELECT id FROM companies WHERE slug = 'funerare-lugoj'), 'crypts'),
((SELECT id FROM companies WHERE slug = 'funerare-lugoj'), 'photo_ceramics'),
-- Legacy services
((SELECT id FROM companies WHERE slug = 'funerare-lugoj'), 'cremation'),
((SELECT id FROM companies WHERE slug = 'funerare-lugoj'), 'bureaucracy'),
((SELECT id FROM companies WHERE slug = 'funerare-lugoj'), 'religious'),

-- Other Timiș companies (basic services)
((SELECT id FROM companies WHERE slug = 'funerare-jimbolia'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-jimbolia'), 'religious');

-- ============================================================================
-- ARAD COUNTY COMPANIES
-- ============================================================================
INSERT INTO companies (name, slug, motto, description, fiscal_code, website, is_verified, is_non_stop) VALUES
('Funerare Arad Central', 'funerare-arad-central', 'Servicii complete 24/7', '[SAMPLE] Date de test - nu este o firmă reală', 'ROAR100001', NULL, true, true),
('Casa Funerară Ineu', 'funerare-ineu', 'Tradiție și respect', '[SAMPLE] Date de test - nu este o firmă reală', 'ROAR100002', NULL, true, false),
('Funerare Lipova', 'funerare-lipova', 'Cu demnitate', '[SAMPLE] Date de test - nu este o firmă reală', 'ROAR100003', NULL, true, false),
('Servicii Funerare Chișineu-Criș', 'funerare-chisineu-cris', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'ROAR100004', NULL, false, false),
('Funerare Pâncota', 'funerare-pancota', 'Aproape de comunitate', '[SAMPLE] Date de test - nu este o firmă reală', 'ROAR100005', NULL, true, false),
('Casa Funerară Șicula', 'funerare-sicula', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'ROAR100006', NULL, false, false),
('Funerare Ghioroc', 'funerare-ghioroc', 'Cu compasiune', '[SAMPLE] Date de test - nu este o firmă reală', 'ROAR100007', NULL, true, false);

-- ARAD LOCATIONS
INSERT INTO locations (company_id, address, city, county, county_id, type) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-arad-central'), 'Bulevardul Revoluției 50', 'Arad', 'Arad', (SELECT id FROM counties WHERE slug = 'arad'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-ineu'), 'Strada Principală 10', 'Ineu', 'Arad', (SELECT id FROM counties WHERE slug = 'arad'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-lipova'), 'Strada Libertății 25', 'Lipova', 'Arad', (SELECT id FROM counties WHERE slug = 'arad'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-chisineu-cris'), 'Strada Mare 8', 'Chișineu-Criș', 'Arad', (SELECT id FROM counties WHERE slug = 'arad'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-pancota'), 'Strada Victoriei 15', 'Pâncota', 'Arad', (SELECT id FROM counties WHERE slug = 'arad'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-sicula'), 'Strada Centrală 3', 'Șicula', 'Arad', (SELECT id FROM counties WHERE slug = 'arad'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-ghioroc'), 'Strada Primăverii 7', 'Ghioroc', 'Arad', (SELECT id FROM counties WHERE slug = 'arad'), 'headquarters');

-- ARAD CONTACTS
INSERT INTO contacts (company_id, type, value, is_primary) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-arad-central'), 'phone_mobile', '0757 200 001', true),
((SELECT id FROM companies WHERE slug = 'funerare-ineu'), 'phone_mobile', '0757 200 002', true),
((SELECT id FROM companies WHERE slug = 'funerare-lipova'), 'phone_mobile', '0757 200 003', true),
((SELECT id FROM companies WHERE slug = 'funerare-chisineu-cris'), 'phone_mobile', '0757 200 004', true),
((SELECT id FROM companies WHERE slug = 'funerare-pancota'), 'phone_mobile', '0757 200 005', true),
((SELECT id FROM companies WHERE slug = 'funerare-sicula'), 'phone_mobile', '0757 200 006', true),
((SELECT id FROM companies WHERE slug = 'funerare-ghioroc'), 'phone_mobile', '0757 200 007', true);

-- ARAD SERVICES
INSERT INTO services (company_id, service_tag) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-arad-central'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-arad-central'), 'coffins'),
((SELECT id FROM companies WHERE slug = 'funerare-arad-central'), 'religious'),
((SELECT id FROM companies WHERE slug = 'funerare-ineu'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-lipova'), 'coffins');

-- ============================================================================
-- BIHOR COUNTY COMPANIES
-- ============================================================================
INSERT INTO companies (name, slug, motto, description, fiscal_code, website, is_verified, is_non_stop) VALUES
('Funerare Oradea Central', 'funerare-oradea-central', 'Servicii profesionale non-stop', '[SAMPLE] Date de test - nu este o firmă reală', 'ROBH100001', NULL, true, true),
('Casa Funerară Salonta', 'funerare-salonta', 'Respect și tradiție', '[SAMPLE] Date de test - nu este o firmă reală', 'ROBH100002', NULL, true, false),
('Funerare Beiuș', 'funerare-beius', 'Cu grijă pentru familie', '[SAMPLE] Date de test - nu este o firmă reală', 'ROBH100003', NULL, true, false),
('Servicii Funerare Marghita', 'funerare-marghita', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'ROBH100004', NULL, false, false),
('Funerare Aleșd', 'funerare-alesd', 'Tradiție locală', '[SAMPLE] Date de test - nu este o firmă reală', 'ROBH100005', NULL, true, false),
('Memorial Vad', 'funerare-vad', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'ROBH100006', NULL, false, false);

-- BIHOR LOCATIONS
INSERT INTO locations (company_id, address, city, county, county_id, type) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-oradea-central'), 'Strada Republicii 80', 'Oradea', 'Bihor', (SELECT id FROM counties WHERE slug = 'bihor'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-salonta'), 'Strada Libertății 30', 'Salonta', 'Bihor', (SELECT id FROM counties WHERE slug = 'bihor'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-beius'), 'Strada Horea 12', 'Beiuș', 'Bihor', (SELECT id FROM counties WHERE slug = 'bihor'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-marghita'), 'Strada Crișului 5', 'Marghita', 'Bihor', (SELECT id FROM counties WHERE slug = 'bihor'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-alesd'), 'Strada Victoriei 18', 'Aleșd', 'Bihor', (SELECT id FROM counties WHERE slug = 'bihor'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-vad'), 'Strada Primăverii 2', 'Vad', 'Bihor', (SELECT id FROM counties WHERE slug = 'bihor'), 'headquarters');

-- BIHOR CONTACTS
INSERT INTO contacts (company_id, type, value, is_primary) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-oradea-central'), 'phone_mobile', '0759 300 001', true),
((SELECT id FROM companies WHERE slug = 'funerare-salonta'), 'phone_mobile', '0759 300 002', true),
((SELECT id FROM companies WHERE slug = 'funerare-beius'), 'phone_mobile', '0759 300 003', true),
((SELECT id FROM companies WHERE slug = 'funerare-marghita'), 'phone_mobile', '0759 300 004', true),
((SELECT id FROM companies WHERE slug = 'funerare-alesd'), 'phone_mobile', '0759 300 005', true),
((SELECT id FROM companies WHERE slug = 'funerare-vad'), 'phone_mobile', '0759 300 006', true);

-- BIHOR SERVICES
INSERT INTO services (company_id, service_tag) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-oradea-central'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-oradea-central'), 'coffins'),
((SELECT id FROM companies WHERE slug = 'funerare-oradea-central'), 'religious'),
((SELECT id FROM companies WHERE slug = 'funerare-salonta'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-beius'), 'coffins');

-- ============================================================================
-- CLUJ COUNTY COMPANIES
-- ============================================================================
INSERT INTO companies (name, slug, motto, description, fiscal_code, website, is_verified, is_non_stop) VALUES
('Funerare Cluj-Napoca Central', 'funerare-cluj-napoca-central', 'Servicii complete 24/7', '[SAMPLE] Date de test - nu este o firmă reală', 'ROCJ100001', NULL, true, true),
('Casa Funerară Turda', 'funerare-turda', 'Cu respect și tradiție', '[SAMPLE] Date de test - nu este o firmă reală', 'ROCJ100002', NULL, true, false),
('Funerare Dej', 'funerare-dej', 'Aproape de comunitate', '[SAMPLE] Date de test - nu este o firmă reală', 'ROCJ100003', NULL, true, false),
('Servicii Funerare Câmpia Turzii', 'funerare-campia-turzii', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'ROCJ100004', NULL, false, false),
('Funerare Gherla', 'funerare-gherla', 'Tradiție și grijă', '[SAMPLE] Date de test - nu este o firmă reală', 'ROCJ100005', NULL, true, false),
('Memorial Huedin', 'funerare-huedin', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'ROCJ100006', NULL, false, false);

-- CLUJ LOCATIONS
INSERT INTO locations (company_id, address, city, county, county_id, type) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-cluj-napoca-central'), 'Strada Memorandumului 25', 'Cluj-Napoca', 'Cluj', (SELECT id FROM counties WHERE slug = 'cluj'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-turda'), 'Strada Republicii 40', 'Turda', 'Cluj', (SELECT id FROM counties WHERE slug = 'cluj'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-dej'), 'Strada 1 Mai 15', 'Dej', 'Cluj', (SELECT id FROM counties WHERE slug = 'cluj'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-campia-turzii'), 'Strada Libertății 8', 'Câmpia Turzii', 'Cluj', (SELECT id FROM counties WHERE slug = 'cluj'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-gherla'), 'Strada Clujului 22', 'Gherla', 'Cluj', (SELECT id FROM counties WHERE slug = 'cluj'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-huedin'), 'Strada Horea 5', 'Huedin', 'Cluj', (SELECT id FROM counties WHERE slug = 'cluj'), 'headquarters');

-- CLUJ CONTACTS
INSERT INTO contacts (company_id, type, value, is_primary) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-cluj-napoca-central'), 'phone_mobile', '0764 400 001', true),
((SELECT id FROM companies WHERE slug = 'funerare-turda'), 'phone_mobile', '0764 400 002', true),
((SELECT id FROM companies WHERE slug = 'funerare-dej'), 'phone_mobile', '0764 400 003', true),
((SELECT id FROM companies WHERE slug = 'funerare-campia-turzii'), 'phone_mobile', '0764 400 004', true),
((SELECT id FROM companies WHERE slug = 'funerare-gherla'), 'phone_mobile', '0764 400 005', true),
((SELECT id FROM companies WHERE slug = 'funerare-huedin'), 'phone_mobile', '0764 400 006', true);

-- CLUJ SERVICES
INSERT INTO services (company_id, service_tag) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-cluj-napoca-central'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-cluj-napoca-central'), 'coffins'),
((SELECT id FROM companies WHERE slug = 'funerare-cluj-napoca-central'), 'religious'),
((SELECT id FROM companies WHERE slug = 'funerare-turda'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-dej'), 'coffins');

-- ============================================================================
-- BRAȘOV COUNTY COMPANIES
-- ============================================================================
INSERT INTO companies (name, slug, motto, description, fiscal_code, website, is_verified, is_non_stop) VALUES
('Funerare Brașov Central', 'funerare-brasov-central', 'Servicii profesionale non-stop', '[SAMPLE] Date de test - nu este o firmă reală', 'ROBV100001', NULL, true, true),
('Casa Funerară Făgăraș', 'funerare-fagaras', 'Tradiție și respect', '[SAMPLE] Date de test - nu este o firmă reală', 'ROBV100002', NULL, true, false),
('Funerare Săcele', 'funerare-sacele', 'Cu grijă pentru familie', '[SAMPLE] Date de test - nu este o firmă reală', 'ROBV100003', NULL, true, false),
('Servicii Funerare Codlea', 'funerare-codlea', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'ROBV100004', NULL, false, false),
('Funerare Zărnești', 'funerare-zarnesti', 'Aproape de comunitate', '[SAMPLE] Date de test - nu este o firmă reală', 'ROBV100005', NULL, true, false);

-- BRAȘOV LOCATIONS
INSERT INTO locations (company_id, address, city, county, county_id, type) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-brasov-central'), 'Strada Republicii 60', 'Brașov', 'Brașov', (SELECT id FROM counties WHERE slug = 'brasov'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-fagaras'), 'Strada Libertății 25', 'Făgăraș', 'Brașov', (SELECT id FROM counties WHERE slug = 'brasov'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-sacele'), 'Strada Principală 12', 'Săcele', 'Brașov', (SELECT id FROM counties WHERE slug = 'brasov'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-codlea'), 'Strada Mare 8', 'Codlea', 'Brașov', (SELECT id FROM counties WHERE slug = 'brasov'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-zarnesti'), 'Strada Morii 15', 'Zărnești', 'Brașov', (SELECT id FROM counties WHERE slug = 'brasov'), 'headquarters');

-- BRAȘOV CONTACTS
INSERT INTO contacts (company_id, type, value, is_primary) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-brasov-central'), 'phone_mobile', '0768 500 001', true),
((SELECT id FROM companies WHERE slug = 'funerare-fagaras'), 'phone_mobile', '0768 500 002', true),
((SELECT id FROM companies WHERE slug = 'funerare-sacele'), 'phone_mobile', '0768 500 003', true),
((SELECT id FROM companies WHERE slug = 'funerare-codlea'), 'phone_mobile', '0768 500 004', true),
((SELECT id FROM companies WHERE slug = 'funerare-zarnesti'), 'phone_mobile', '0768 500 005', true);

-- BRAȘOV SERVICES
INSERT INTO services (company_id, service_tag) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-brasov-central'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-brasov-central'), 'coffins'),
((SELECT id FROM companies WHERE slug = 'funerare-brasov-central'), 'religious'),
((SELECT id FROM companies WHERE slug = 'funerare-fagaras'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-sacele'), 'coffins');

-- ============================================================================
-- CONSTANȚA COUNTY COMPANIES
-- ============================================================================
INSERT INTO companies (name, slug, motto, description, fiscal_code, website, is_verified, is_non_stop) VALUES
('Funerare Constanța Central', 'funerare-constanta-central', 'Servicii complete 24/7', '[SAMPLE] Date de test - nu este o firmă reală', 'ROCT100001', NULL, true, true),
('Casa Funerară Mangalia', 'funerare-mangalia', 'Cu respect și tradiție', '[SAMPLE] Date de test - nu este o firmă reală', 'ROCT100002', NULL, true, false),
('Funerare Medgidia', 'funerare-medgidia', 'Aproape de comunitate', '[SAMPLE] Date de test - nu este o firmă reală', 'ROCT100003', NULL, true, false),
('Servicii Funerare Năvodari', 'funerare-navodari', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'ROCT100004', NULL, false, false),
('Funerare Cernavodă', 'funerare-cernavoda', 'Tradiție și grijă', '[SAMPLE] Date de test - nu este o firmă reală', 'ROCT100005', NULL, true, false),
('Memorial Eforie', 'funerare-eforie', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'ROCT100006', NULL, false, false);

-- CONSTANȚA LOCATIONS
INSERT INTO locations (company_id, address, city, county, county_id, type) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-constanta-central'), 'Bulevardul Tomis 100', 'Constanța', 'Constanța', (SELECT id FROM counties WHERE slug = 'constanta'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-mangalia'), 'Strada Rozelor 25', 'Mangalia', 'Constanța', (SELECT id FROM counties WHERE slug = 'constanta'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-medgidia'), 'Strada Republicii 40', 'Medgidia', 'Constanța', (SELECT id FROM counties WHERE slug = 'constanta'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-navodari'), 'Strada Mării 8', 'Năvodari', 'Constanța', (SELECT id FROM counties WHERE slug = 'constanta'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-cernavoda'), 'Strada Dunării 15', 'Cernavodă', 'Constanța', (SELECT id FROM counties WHERE slug = 'constanta'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-eforie'), 'Strada Primăverii 5', 'Eforie', 'Constanța', (SELECT id FROM counties WHERE slug = 'constanta'), 'headquarters');

-- CONSTANȚA CONTACTS
INSERT INTO contacts (company_id, type, value, is_primary) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-constanta-central'), 'phone_mobile', '0241 600 001', true),
((SELECT id FROM companies WHERE slug = 'funerare-mangalia'), 'phone_mobile', '0241 600 002', true),
((SELECT id FROM companies WHERE slug = 'funerare-medgidia'), 'phone_mobile', '0241 600 003', true),
((SELECT id FROM companies WHERE slug = 'funerare-navodari'), 'phone_mobile', '0241 600 004', true),
((SELECT id FROM companies WHERE slug = 'funerare-cernavoda'), 'phone_mobile', '0241 600 005', true),
((SELECT id FROM companies WHERE slug = 'funerare-eforie'), 'phone_mobile', '0241 600 006', true);

-- CONSTANȚA SERVICES
INSERT INTO services (company_id, service_tag) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-constanta-central'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-constanta-central'), 'coffins'),
((SELECT id FROM companies WHERE slug = 'funerare-constanta-central'), 'religious'),
((SELECT id FROM companies WHERE slug = 'funerare-mangalia'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-medgidia'), 'coffins');

-- ============================================================================
-- BUCUREȘTI COMPANIES
-- ============================================================================
INSERT INTO companies (name, slug, motto, description, fiscal_code, website, is_verified, is_non_stop) VALUES
('Funerare București Sector 1', 'funerare-bucuresti-s1', 'Servicii profesionale non-stop', '[SAMPLE] Date de test - nu este o firmă reală', 'ROB100001', NULL, true, true),
('Casa Funerară București Sector 2', 'funerare-bucuresti-s2', 'Cu respect și tradiție', '[SAMPLE] Date de test - nu este o firmă reală', 'ROB100002', NULL, true, false),
('Funerare București Sector 3', 'funerare-bucuresti-s3', 'Aproape de comunitate', '[SAMPLE] Date de test - nu este o firmă reală', 'ROB100003', NULL, true, false),
('Servicii Funerare București Sector 4', 'funerare-bucuresti-s4', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'ROB100004', NULL, false, false),
('Funerare București Sector 5', 'funerare-bucuresti-s5', 'Tradiție și grijă', '[SAMPLE] Date de test - nu este o firmă reală', 'ROB100005', NULL, true, false),
('Memorial București Sector 6', 'funerare-bucuresti-s6', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'ROB100006', NULL, false, false);

-- BUCUREȘTI LOCATIONS
INSERT INTO locations (company_id, address, city, county, county_id, type) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-bucuresti-s1'), 'Calea Victoriei 100', 'București', 'București', (SELECT id FROM counties WHERE slug = 'bucuresti'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-bucuresti-s2'), 'Bulevardul Basarabia 50', 'București', 'București', (SELECT id FROM counties WHERE slug = 'bucuresti'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-bucuresti-s3'), 'Șoseaua Mihai Bravu 80', 'București', 'București', (SELECT id FROM counties WHERE slug = 'bucuresti'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-bucuresti-s4'), 'Bulevardul Metalurgiei 30', 'București', 'București', (SELECT id FROM counties WHERE slug = 'bucuresti'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-bucuresti-s5'), 'Calea Rahova 120', 'București', 'București', (SELECT id FROM counties WHERE slug = 'bucuresti'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-bucuresti-s6'), 'Bulevardul Iuliu Maniu 200', 'București', 'București', (SELECT id FROM counties WHERE slug = 'bucuresti'), 'headquarters');

-- BUCUREȘTI CONTACTS
INSERT INTO contacts (company_id, type, value, is_primary) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-bucuresti-s1'), 'phone_mobile', '021 700 001', true),
((SELECT id FROM companies WHERE slug = 'funerare-bucuresti-s2'), 'phone_mobile', '021 700 002', true),
((SELECT id FROM companies WHERE slug = 'funerare-bucuresti-s3'), 'phone_mobile', '021 700 003', true),
((SELECT id FROM companies WHERE slug = 'funerare-bucuresti-s4'), 'phone_mobile', '021 700 004', true),
((SELECT id FROM companies WHERE slug = 'funerare-bucuresti-s5'), 'phone_mobile', '021 700 005', true),
((SELECT id FROM companies WHERE slug = 'funerare-bucuresti-s6'), 'phone_mobile', '021 700 006', true);

-- BUCUREȘTI SERVICES
INSERT INTO services (company_id, service_tag) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-bucuresti-s1'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-bucuresti-s1'), 'coffins'),
((SELECT id FROM companies WHERE slug = 'funerare-bucuresti-s1'), 'religious'),
((SELECT id FROM companies WHERE slug = 'funerare-bucuresti-s2'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-bucuresti-s3'), 'coffins');

-- ============================================================================
-- IAȘI COUNTY COMPANIES
-- ============================================================================
INSERT INTO companies (name, slug, motto, description, fiscal_code, website, is_verified, is_non_stop) VALUES
('Funerare Iași Central', 'funerare-iasi-central', 'Servicii complete 24/7', '[SAMPLE] Date de test - nu este o firmă reală', 'ROIS100001', NULL, true, true),
('Casa Funerară Pașcani', 'funerare-pascani', 'Cu respect și tradiție', '[SAMPLE] Date de test - nu este o firmă reală', 'ROIS100002', NULL, true, false),
('Funerare Hârlău', 'funerare-harlau', 'Aproape de comunitate', '[SAMPLE] Date de test - nu este o firmă reală', 'ROIS100003', NULL, true, false),
('Servicii Funerare Târgu Frumos', 'funerare-targu-frumos', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'ROIS100004', NULL, false, false);

-- IAȘI LOCATIONS
INSERT INTO locations (company_id, address, city, county, county_id, type) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-iasi-central'), 'Bulevardul Ștefan cel Mare 100', 'Iași', 'Iași', (SELECT id FROM counties WHERE slug = 'iasi'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-pascani'), 'Strada Gării 25', 'Pașcani', 'Iași', (SELECT id FROM counties WHERE slug = 'iasi'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-harlau'), 'Strada Cuza Vodă 12', 'Hârlău', 'Iași', (SELECT id FROM counties WHERE slug = 'iasi'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-targu-frumos'), 'Strada Petru Rareș 8', 'Târgu Frumos', 'Iași', (SELECT id FROM counties WHERE slug = 'iasi'), 'headquarters');

-- IAȘI CONTACTS
INSERT INTO contacts (company_id, type, value, is_primary) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-iasi-central'), 'phone_mobile', '0232 800 001', true),
((SELECT id FROM companies WHERE slug = 'funerare-pascani'), 'phone_mobile', '0232 800 002', true),
((SELECT id FROM companies WHERE slug = 'funerare-harlau'), 'phone_mobile', '0232 800 003', true),
((SELECT id FROM companies WHERE slug = 'funerare-targu-frumos'), 'phone_mobile', '0232 800 004', true);

-- IAȘI SERVICES
INSERT INTO services (company_id, service_tag) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-iasi-central'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-iasi-central'), 'coffins'),
((SELECT id FROM companies WHERE slug = 'funerare-iasi-central'), 'religious'),
((SELECT id FROM companies WHERE slug = 'funerare-pascani'), 'transport');

-- ============================================================================
-- ILFOV COUNTY COMPANIES
-- ============================================================================
INSERT INTO companies (name, slug, motto, description, fiscal_code, website, is_verified, is_non_stop) VALUES
('Funerare Voluntari', 'funerare-voluntari', 'Servicii profesionale', '[SAMPLE] Date de test - nu este o firmă reală', 'ROIF100001', NULL, true, true),
('Casa Funerară Popești-Leordeni', 'funerare-popesti-leordeni', 'Cu respect și tradiție', '[SAMPLE] Date de test - nu este o firmă reală', 'ROIF100002', NULL, true, false),
('Funerare Buftea', 'funerare-buftea', 'Aproape de comunitate', '[SAMPLE] Date de test - nu este o firmă reală', 'ROIF100003', NULL, true, false),
('Servicii Funerare Otopeni', 'funerare-otopeni', 'Non-stop', '[SAMPLE] Date de test - nu este o firmă reală', 'ROIF100004', NULL, true, true),
('Funerare Bragadiru', 'funerare-bragadiru', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'ROIF100005', NULL, false, false),
('Memorial Pantelimon', 'funerare-pantelimon', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'ROIF100006', NULL, false, false);

-- ILFOV LOCATIONS
INSERT INTO locations (company_id, address, city, county, county_id, type) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-voluntari'), 'Șoseaua Pipera 50', 'Voluntari', 'Ilfov', (SELECT id FROM counties WHERE slug = 'ilfov'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-popesti-leordeni'), 'Strada Oltenitei 100', 'Popești-Leordeni', 'Ilfov', (SELECT id FROM counties WHERE slug = 'ilfov'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-buftea'), 'Strada Studioului 25', 'Buftea', 'Ilfov', (SELECT id FROM counties WHERE slug = 'ilfov'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-otopeni'), 'Strada Aeroportului 8', 'Otopeni', 'Ilfov', (SELECT id FROM counties WHERE slug = 'ilfov'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-bragadiru'), 'Strada Alexandriei 200', 'Bragadiru', 'Ilfov', (SELECT id FROM counties WHERE slug = 'ilfov'), 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-pantelimon'), 'Șoseaua de Centură 30', 'Pantelimon', 'Ilfov', (SELECT id FROM counties WHERE slug = 'ilfov'), 'headquarters');

-- ILFOV CONTACTS
INSERT INTO contacts (company_id, type, value, is_primary) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-voluntari'), 'phone_mobile', '021 900 001', true),
((SELECT id FROM companies WHERE slug = 'funerare-popesti-leordeni'), 'phone_mobile', '021 900 002', true),
((SELECT id FROM companies WHERE slug = 'funerare-buftea'), 'phone_mobile', '021 900 003', true),
((SELECT id FROM companies WHERE slug = 'funerare-otopeni'), 'phone_mobile', '021 900 004', true),
((SELECT id FROM companies WHERE slug = 'funerare-bragadiru'), 'phone_mobile', '021 900 005', true),
((SELECT id FROM companies WHERE slug = 'funerare-pantelimon'), 'phone_mobile', '021 900 006', true);

-- ILFOV SERVICES
INSERT INTO services (company_id, service_tag) VALUES
((SELECT id FROM companies WHERE slug = 'funerare-voluntari'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-voluntari'), 'coffins'),
((SELECT id FROM companies WHERE slug = 'funerare-otopeni'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-otopeni'), 'religious');

-- ============================================================================
-- END OF SAMPLE DATA
-- ============================================================================
