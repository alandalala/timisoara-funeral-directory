-- =============================================
-- Update Services Schema - Expanded Service Types
-- Run this in Supabase SQL Editor
-- =============================================

-- Update the service_tag enum to include all new services
-- First, let's see what we have and then add the new values

-- Note: PostgreSQL enums can't be easily modified, so we'll use VARCHAR instead
-- First, drop the constraint if it exists
ALTER TABLE services 
DROP CONSTRAINT IF EXISTS services_service_tag_check;

-- Now the service_tag column can accept any of these values:
-- 1. Documentation & Legal
--    death_certificate, death_registration, permits, funeral_aid
-- 2. Body Care & Storage  
--    embalming, body_preparation, refrigeration
-- 3. Transport & Logistics
--    transport, transport_long, repatriation, pallbearers
-- 4. Products
--    coffins, urns, textiles, crosses
-- 5. Ritual Essentials
--    coliva, liturgical_items, mourning_items
-- 6. Ceremony & Venue
--    wake_house, church_service, flowers, music
-- 7. Catering & Alms
--    food_packages, catering, restaurant, memorial_services
-- 8. Cemetery Works
--    monuments, crypts, photo_ceramics
-- Legacy: cremation, bureaucracy, religious

-- Add a check constraint for valid service tags
ALTER TABLE services
ADD CONSTRAINT services_service_tag_check 
CHECK (service_tag IN (
  -- Documentation & Legal
  'death_certificate', 'death_registration', 'permits', 'funeral_aid',
  -- Body Care & Storage
  'embalming', 'body_preparation', 'refrigeration',
  -- Transport & Logistics
  'transport', 'transport_long', 'repatriation', 'pallbearers',
  -- Products
  'coffins', 'urns', 'textiles', 'crosses',
  -- Ritual Essentials
  'coliva', 'liturgical_items', 'mourning_items',
  -- Ceremony & Venue
  'wake_house', 'church_service', 'flowers', 'music',
  -- Catering & Alms
  'food_packages', 'catering', 'restaurant', 'memorial_services',
  -- Cemetery Works
  'monuments', 'crypts', 'photo_ceramics',
  -- Legacy
  'cremation', 'bureaucracy', 'religious'
));

-- =============================================
-- Success message
-- =============================================
SELECT 'Services schema updated with 30 service types!' AS message;
