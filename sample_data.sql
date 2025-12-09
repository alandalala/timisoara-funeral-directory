-- Sample Test Data for Timișoara Funeral Directory
-- NOTE: All entries are marked as "Sample" in the description field

-- Insert sample companies
INSERT INTO companies (name, slug, motto, description, fiscal_code, website, is_verified, is_non_stop) VALUES
('Casa Funerară Eternal', 'casa-funerara-eternal', 'Alături de dumneavoastră în momentele grele', '[SAMPLE] Date de test - nu este o firmă reală', 'RO12345678', 'https://example.com/eternal', true, true),
('Servicii Funerare Pace', 'servicii-funerare-pace', 'Cu respect și demnitate', '[SAMPLE] Date de test - nu este o firmă reală', 'RO23456789', 'https://example.com/pace', true, false),
('Memorial Timișoara', 'memorial-timisoara', 'Tradiție și profesionalism', '[SAMPLE] Date de test - nu este o firmă reală', 'RO34567890', 'https://example.com/memorial', false, false),
('Funerare Non-Stop TM', 'funerare-non-stop-tm', NULL, '[SAMPLE] Date de test - nu este o firmă reală', 'RO45678901', NULL, true, true),
('Casa Doliului', 'casa-doliului', 'Compasiune în fiecare gest', '[SAMPLE] Date de test - nu este o firmă reală', 'RO56789012', 'https://example.com/doliu', false, false);

-- Insert locations for each company
INSERT INTO locations (company_id, address, type) VALUES
((SELECT id FROM companies WHERE slug = 'casa-funerara-eternal'), 'Strada Memorandumului 15, Timișoara 300045', 'headquarters'),
((SELECT id FROM companies WHERE slug = 'servicii-funerare-pace'), 'Bulevardul Revoluției 89, Timișoara 300034', 'headquarters'),
((SELECT id FROM companies WHERE slug = 'servicii-funerare-pace'), 'Strada Fabric 22, Timișoara 300123', 'wake_house'),
((SELECT id FROM companies WHERE slug = 'memorial-timisoara'), 'Calea Aradului 45, Timișoara 300222', 'headquarters'),
((SELECT id FROM companies WHERE slug = 'funerare-non-stop-tm'), 'Strada Circumvalațiunii 78, Timișoara 300456', 'headquarters'),
((SELECT id FROM companies WHERE slug = 'casa-doliului'), 'Piața Unirii 10, Timișoara 300001', 'headquarters');

-- Insert contacts
INSERT INTO contacts (company_id, type, value, is_primary) VALUES
-- Eternal
((SELECT id FROM companies WHERE slug = 'casa-funerara-eternal'), 'phone_mobile', '0756 123 456', true),
((SELECT id FROM companies WHERE slug = 'casa-funerara-eternal'), 'phone_landline', '0256 123 456', false),
((SELECT id FROM companies WHERE slug = 'casa-funerara-eternal'), 'email', 'contact@eternal-sample.ro', false),
-- Pace
((SELECT id FROM companies WHERE slug = 'servicii-funerare-pace'), 'phone_mobile', '0744 987 654', true),
((SELECT id FROM companies WHERE slug = 'servicii-funerare-pace'), 'email', 'office@pace-sample.ro', false),
-- Memorial
((SELECT id FROM companies WHERE slug = 'memorial-timisoara'), 'phone_landline', '0256 789 012', true),
((SELECT id FROM companies WHERE slug = 'memorial-timisoara'), 'phone_mobile', '0722 345 678', false),
-- Non-Stop
((SELECT id FROM companies WHERE slug = 'funerare-non-stop-tm'), 'phone_mobile', '0733 111 222', true),
((SELECT id FROM companies WHERE slug = 'funerare-non-stop-tm'), 'phone_mobile', '0733 333 444', false),
-- Doliului
((SELECT id FROM companies WHERE slug = 'casa-doliului'), 'phone_mobile', '0755 555 666', true),
((SELECT id FROM companies WHERE slug = 'casa-doliului'), 'email', 'info@doliu-sample.ro', false);

-- Insert services
INSERT INTO services (company_id, service_tag) VALUES
-- Eternal (full service)
((SELECT id FROM companies WHERE slug = 'casa-funerara-eternal'), 'transport'),
((SELECT id FROM companies WHERE slug = 'casa-funerara-eternal'), 'cremation'),
((SELECT id FROM companies WHERE slug = 'casa-funerara-eternal'), 'coffins'),
((SELECT id FROM companies WHERE slug = 'casa-funerara-eternal'), 'flowers'),
((SELECT id FROM companies WHERE slug = 'casa-funerara-eternal'), 'bureaucracy'),
((SELECT id FROM companies WHERE slug = 'casa-funerara-eternal'), 'religious'),
-- Pace
((SELECT id FROM companies WHERE slug = 'servicii-funerare-pace'), 'transport'),
((SELECT id FROM companies WHERE slug = 'servicii-funerare-pace'), 'wake_house'),
((SELECT id FROM companies WHERE slug = 'servicii-funerare-pace'), 'coffins'),
((SELECT id FROM companies WHERE slug = 'servicii-funerare-pace'), 'bureaucracy'),
-- Memorial
((SELECT id FROM companies WHERE slug = 'memorial-timisoara'), 'monuments'),
((SELECT id FROM companies WHERE slug = 'memorial-timisoara'), 'coffins'),
((SELECT id FROM companies WHERE slug = 'memorial-timisoara'), 'flowers'),
-- Non-Stop
((SELECT id FROM companies WHERE slug = 'funerare-non-stop-tm'), 'transport'),
((SELECT id FROM companies WHERE slug = 'funerare-non-stop-tm'), 'repatriation'),
((SELECT id FROM companies WHERE slug = 'funerare-non-stop-tm'), 'embalming'),
((SELECT id FROM companies WHERE slug = 'funerare-non-stop-tm'), 'bureaucracy'),
-- Doliului
((SELECT id FROM companies WHERE slug = 'casa-doliului'), 'wake_house'),
((SELECT id FROM companies WHERE slug = 'casa-doliului'), 'religious'),
((SELECT id FROM companies WHERE slug = 'casa-doliului'), 'flowers');
