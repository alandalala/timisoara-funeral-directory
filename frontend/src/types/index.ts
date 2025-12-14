/**
 * TypeScript type definitions for the funeral directory.
 */

export interface Company {
  id: string;
  name: string;
  slug: string;
  motto?: string | null;
  description?: string | null;
  fiscal_code?: string | null;
  website?: string | null;
  facebook_url?: string | null;
  instagram_url?: string | null;
  is_verified: boolean;
  is_non_stop: boolean;
  founded_year?: number | null;
  metadata?: Record<string, any>;
  created_at: string;
  updated_at: string;
  
  // Relations
  contacts?: Contact[];
  services?: Service[];
  locations?: Location[];
  reviews?: Review[];
  review_summary?: ReviewSummary | null;
}

export interface Contact {
  id: string;
  company_id: string;
  type: 'phone_mobile' | 'phone_landline' | 'email' | 'fax';
  value: string;
  is_primary: boolean;
  created_at: string;
}

export interface Location {
  id: string;
  company_id: string;
  address: string;
  city?: string | null;
  county?: string | null;
  county_id?: number | null;
  latitude?: number | null;
  longitude?: number | null;
  geo_point?: {
    type: 'Point';
    coordinates: [number, number]; // [longitude, latitude]
  };
  type: 'headquarters' | 'wake_house' | 'showroom';
  created_at: string;
}

export interface County {
  id: number;
  name: string;
  slug: string;
  region?: string | null;
}

export interface Service {
  id: string;
  company_id: string;
  service_tag: string;
  created_at: string;
}

export interface Report {
  id: string;
  company_id: string;
  issue_type: string;
  description?: string | null;
  requester_email?: string | null;
  status: 'pending' | 'reviewed' | 'resolved';
  created_at: string;
}

export interface RemovalRequest {
  id: string;
  company_id: string;
  requester_email: string;
  status: 'pending' | 'approved' | 'rejected' | 'completed';
  created_at: string;
}

export interface Review {
  id: string;
  company_id: string;
  source: 'google' | 'facebook' | 'manual';
  author_name?: string | null;
  author_location?: string | null;
  rating?: number | null;
  content?: string | null;
  sentiment_tags?: string[] | null;
  review_date?: string | null;
  source_url?: string | null;
  is_featured: boolean;
  created_at: string;
}

export interface ReviewSummary {
  id: string;
  company_id: string;
  total_reviews: number;
  average_rating?: number | null;
  google_rating?: number | null;
  facebook_rating?: number | null;
  top_sentiment_tags?: string[] | null;
  last_scraped_at?: string | null;
  created_at: string;
  updated_at: string;
}

// Sentiment tag labels for display
export const SENTIMENT_LABELS: Record<string, { ro: string; icon: string }> = {
  'profesionalism': { ro: 'Profesionalism', icon: '✓' },
  'raspuns_rapid': { ro: 'Răspuns Rapid', icon: '✓' },
  'empatie': { ro: 'Empatie', icon: '✓' },
  'preturi_corecte': { ro: 'Prețuri Corecte', icon: '✓' },
  'comunicare': { ro: 'Comunicare Bună', icon: '✓' },
  'punctualitate': { ro: 'Punctualitate', icon: '✓' },
  'respect': { ro: 'Respect', icon: '✓' },
  'calitate': { ro: 'Calitate Servicii', icon: '✓' },
  'disponibilitate': { ro: 'Disponibilitate', icon: '✓' },
  'curatenie': { ro: 'Curățenie', icon: '✓' },
};

export type ServiceTag = 
  // 1. Documentation & Legal
  | 'death_certificate'      // Constatare deces & certificat medical
  | 'death_registration'     // Certificat deces de la primărie
  | 'permits'                // Autorizații sanitare și îngropare
  | 'funeral_aid'            // Dosar ajutor înmormântare
  // 2. Body Care & Storage
  | 'embalming'              // Îmbălsămare / Tanatopraxy
  | 'body_preparation'       // Toaletă, îmbrăcare, machiaj
  | 'refrigeration'          // Frigider mortuar
  // 3. Transport & Logistics
  | 'transport'              // Transport funerar local
  | 'transport_long'         // Transport funerar distanță lungă
  | 'repatriation'           // Repatriere internațională
  | 'pallbearers'            // Echipă purtători sicriu
  // 4. Products
  | 'coffins'                // Sicrie (economice, lux, zinc)
  | 'urns'                   // Urne pentru cremație
  | 'textiles'               // Perne, pături, căptușeli
  | 'crosses'                // Cruci de lemn
  // 5. Ritual Essentials
  | 'coliva'                 // Colivă și colaci
  | 'liturgical_items'       // Vin, ulei, tămâie, cărbune
  | 'mourning_items'         // Lumânări, icoane, batiste, prosoape
  // 6. Ceremony & Venue
  | 'wake_house'             // Capelă / Cameră mortuară
  | 'church_service'         // Serviciu religios la biserică
  | 'flowers'                // Coroane și aranjamente florale
  | 'music'                  // Cor sau fanfară
  // 7. Catering & Alms
  | 'food_packages'          // Pachete pomană
  | 'catering'               // Catering masă priveghi/praznic
  | 'restaurant'             // Rezervare restaurant
  | 'memorial_services'      // Parastase (40 zile, 6 luni, 1 an)
  // 8. Cemetery Works
  | 'monuments'              // Monumente granit/marmură
  | 'crypts'                 // Cripte și cavouri
  | 'photo_ceramics'         // Fotografii ceramice
  // Legacy (for backwards compatibility)
  | 'cremation'              // Incinerare
  | 'bureaucracy'            // Acte / Formalități (legacy)
  | 'religious';             // Servicii religioase (legacy)

export const SERVICE_LABELS: Record<ServiceTag, { ro: string; en: string }> = {
  // 1. Documentation & Legal
  death_certificate: { ro: 'Constatare Deces', en: 'Death Confirmation' },
  death_registration: { ro: 'Certificat Deces (Primărie)', en: 'Death Registration' },
  permits: { ro: 'Autorizații (Sanepid/Îngropare)', en: 'Burial Permits' },
  funeral_aid: { ro: 'Dosar Ajutor Înmormântare', en: 'Funeral Aid Filing' },
  // 2. Body Care & Storage
  embalming: { ro: 'Îmbălsămare / Tanatopraxy', en: 'Embalming' },
  body_preparation: { ro: 'Toaletă și Îmbrăcare', en: 'Body Preparation' },
  refrigeration: { ro: 'Frigider Mortuar', en: 'Refrigeration' },
  // 3. Transport & Logistics
  transport: { ro: 'Transport Funerar Local', en: 'Local Funeral Transport' },
  transport_long: { ro: 'Transport Distanță Lungă', en: 'Long Distance Transport' },
  repatriation: { ro: 'Repatriere Internațională', en: 'International Repatriation' },
  pallbearers: { ro: 'Echipă Purtători Sicriu', en: 'Pallbearers Team' },
  // 4. Products
  coffins: { ro: 'Sicrie', en: 'Coffins' },
  urns: { ro: 'Urne Cremație', en: 'Cremation Urns' },
  textiles: { ro: 'Textile Funerare', en: 'Funeral Textiles' },
  crosses: { ro: 'Cruci de Lemn', en: 'Wooden Crosses' },
  // 5. Ritual Essentials
  coliva: { ro: 'Colivă și Colaci', en: 'Ritual Foods' },
  liturgical_items: { ro: 'Articole Liturgice', en: 'Liturgical Items' },
  mourning_items: { ro: 'Lumânări, Icoane, Batiste', en: 'Mourning Items' },
  // 6. Ceremony & Venue
  wake_house: { ro: 'Capelă / Cameră Mortuară', en: 'Wake House/Chapel' },
  church_service: { ro: 'Serviciu la Biserică', en: 'Church Service' },
  flowers: { ro: 'Coroane și Flori', en: 'Wreaths & Flowers' },
  music: { ro: 'Cor / Fanfară', en: 'Choir/Band' },
  // 7. Catering & Alms
  food_packages: { ro: 'Pachete Pomană', en: 'Alms Packages' },
  catering: { ro: 'Catering Praznic', en: 'Memorial Catering' },
  restaurant: { ro: 'Rezervare Restaurant', en: 'Restaurant Booking' },
  memorial_services: { ro: 'Parastase (40 zile, 1 an)', en: 'Memorial Services' },
  // 8. Cemetery Works
  monuments: { ro: 'Monumente Funerare', en: 'Monuments' },
  crypts: { ro: 'Cripte și Cavouri', en: 'Crypts & Vaults' },
  photo_ceramics: { ro: 'Fotografii Ceramice', en: 'Photo Ceramics' },
  // Legacy
  cremation: { ro: 'Incinerare', en: 'Cremation' },
  bureaucracy: { ro: 'Acte / Formalități', en: 'Paperwork' },
  religious: { ro: 'Servicii Religioase', en: 'Religious Services' },
};
