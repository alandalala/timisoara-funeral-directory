-- ============================================================================
-- UPDATE TIMIȘ COMPANIES WITH ALL SERVICES
-- Run this to add all service tags to the two main Timiș companies
-- ============================================================================

-- First, delete existing services for these companies to avoid duplicates
DELETE FROM services WHERE company_id IN (
  SELECT id FROM companies WHERE slug IN ('funerare-timisoara-central', 'funerare-lugoj')
);

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
((SELECT id FROM companies WHERE slug = 'funerare-timisoara-central'), 'religious');

-- Funerare Lugoj - ALL SERVICES (full-service provider)
INSERT INTO services (company_id, service_tag) VALUES
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
((SELECT id FROM companies WHERE slug = 'funerare-lugoj'), 'religious');

-- Verify the update
SELECT c.name, COUNT(s.id) as service_count
FROM companies c
LEFT JOIN services s ON s.company_id = c.id
WHERE c.slug IN ('funerare-timisoara-central', 'funerare-lugoj')
GROUP BY c.name;
