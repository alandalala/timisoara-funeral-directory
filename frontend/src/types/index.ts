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
  is_verified: boolean;
  is_non_stop: boolean;
  metadata?: Record<string, any>;
  created_at: string;
  updated_at: string;
  
  // Relations
  contacts?: Contact[];
  services?: Service[];
  locations?: Location[];
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
  geo_point?: {
    type: 'Point';
    coordinates: [number, number]; // [longitude, latitude]
  };
  type: 'headquarters' | 'wake_house' | 'showroom';
  created_at: string;
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

export type ServiceTag = 
  | 'transport'
  | 'repatriation'
  | 'cremation'
  | 'embalming'
  | 'wake_house'
  | 'coffins'
  | 'flowers'
  | 'bureaucracy'
  | 'religious'
  | 'monuments';

export const SERVICE_LABELS: Record<ServiceTag, { ro: string; en: string }> = {
  transport: { ro: 'Transport Funerar', en: 'Funeral Transport' },
  repatriation: { ro: 'Repatriere Internațională', en: 'International Repatriation' },
  cremation: { ro: 'Incinerare', en: 'Cremation' },
  embalming: { ro: 'Îmbălsămare', en: 'Embalming' },
  wake_house: { ro: 'Capelă / Cameră Mortuară', en: 'Wake House' },
  coffins: { ro: 'Sicrie', en: 'Coffins' },
  flowers: { ro: 'Aranjamente Florale', en: 'Flower Arrangements' },
  bureaucracy: { ro: 'Acte / Formalități', en: 'Paperwork/Bureaucracy' },
  religious: { ro: 'Servicii Religioase', en: 'Religious Services' },
  monuments: { ro: 'Monumente Funerare', en: 'Monuments' }
};
