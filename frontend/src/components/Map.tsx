'use client';

import { useEffect, useState } from 'react';
import { Company } from '@/types';

// Romanian city coordinates (approximate centers)
const CITY_COORDINATES: Record<string, [number, number]> = {
  // Timiș
  'Timișoara': [45.7489, 21.2087],
  'Lugoj': [45.6867, 21.9033],
  'Buziaș': [45.6500, 21.6000],
  'Jimbolia': [45.7933, 20.7167],
  'Sânnicolau Mare': [46.0667, 20.6333],
  'Giroc': [45.7333, 21.2500],
  'Dumbrăvița': [45.7833, 21.2333],
  'Ghiroda': [45.7667, 21.2833],
  // Arad
  'Arad': [46.1667, 21.3167],
  'Ineu': [46.4333, 21.8333],
  'Lipova': [46.0833, 21.6833],
  'Chișineu-Criș': [46.5333, 21.5167],
  'Pâncota': [46.3333, 21.7000],
  'Șicula': [46.3667, 21.5833],
  'Ghioroc': [46.1500, 21.5167],
  // Bihor
  'Oradea': [47.0722, 21.9211],
  'Salonta': [46.8000, 21.6500],
  'Beiuș': [46.6667, 22.3500],
  'Marghita': [47.3500, 22.3333],
  'Aleșd': [47.0667, 22.4000],
  'Vad': [47.0333, 22.2333],
  // Cluj
  'Cluj-Napoca': [46.7712, 23.6236],
  'Turda': [46.5667, 23.7833],
  'Dej': [47.1333, 23.8833],
  'Câmpia Turzii': [46.5500, 23.8833],
  'Gherla': [47.0333, 23.9000],
  'Huedin': [46.8667, 23.0333],
  // Brașov
  'Brașov': [45.6427, 25.5887],
  'Făgăraș': [45.8500, 24.9667],
  'Săcele': [45.6167, 25.6833],
  'Codlea': [45.7000, 25.4500],
  'Zărnești': [45.5667, 25.3333],
  // Constanța
  'Constanța': [44.1598, 28.6348],
  'Mangalia': [43.8167, 28.5833],
  'Medgidia': [44.2500, 28.2667],
  'Năvodari': [44.3167, 28.6167],
  'Cernavodă': [44.3333, 28.0333],
  'Eforie': [44.0500, 28.6333],
  // București
  'București': [44.4268, 26.1025],
  // Iași
  'Iași': [47.1585, 27.6014],
  'Pașcani': [47.2500, 26.7167],
  'Hârlău': [47.4333, 26.9000],
  'Târgu Frumos': [47.2167, 27.0167],
  // Ilfov
  'Voluntari': [44.4833, 26.1667],
  'Popești-Leordeni': [44.3833, 26.1667],
  'Buftea': [44.5667, 25.9500],
  'Otopeni': [44.5500, 26.0667],
  'Bragadiru': [44.3833, 26.0167],
  'Pantelimon': [44.4500, 26.2000],
};

// Default center of Romania
const ROMANIA_CENTER: [number, number] = [45.9432, 25.0094];
const DEFAULT_ZOOM = 7;

// Bounds type for map viewport
export interface MapBounds {
  north: number;
  south: number;
  east: number;
  west: number;
}

// Get coordinates for a company - exported for use in filtering
export const getCompanyCoords = (company: Company): [number, number] | null => {
  const location = company.locations?.[0];
  if (!location) return null;

  // Check if we have direct latitude/longitude columns (preferred)
  if (location.latitude && location.longitude) {
    return [location.latitude, location.longitude];
  }

  // Fallback: Check if we have geo_point in GeoJSON format
  if (location.geo_point?.coordinates) {
    return [location.geo_point.coordinates[1], location.geo_point.coordinates[0]];
  }

  // Try to get from city name
  if (location.city && CITY_COORDINATES[location.city]) {
    return CITY_COORDINATES[location.city];
  }

  return null;
};

// Get coordinates with offset for map display (to avoid overlapping markers)
export const getCompanyCoordsWithOffset = (company: Company, index: number = 0): [number, number] | null => {
  const baseCoords = getCompanyCoords(company);
  if (!baseCoords) return null;
  
  const location = company.locations?.[0];
  
  // If we have exact coordinates (lat/lng or geo_point), use it as-is
  if (location?.latitude && location?.longitude) {
    return baseCoords;
  }
  if (location?.geo_point?.coordinates) {
    return baseCoords;
  }
  
  // For city fallback coordinates, add a small offset based on company id/index
  // to spread out markers that would otherwise overlap
  // Offset is ~200-500m in a circular pattern
  const seed = company.id ? parseInt(company.id.replace(/\D/g, '').slice(-4) || '0', 10) : index;
  const angle = (seed * 137.5) % 360; // Golden angle for good distribution
  const radius = 0.003 + (seed % 5) * 0.001; // ~300-800m offset
  
  const offsetLat = radius * Math.cos(angle * Math.PI / 180);
  const offsetLng = radius * Math.sin(angle * Math.PI / 180);
  
  return [baseCoords[0] + offsetLat, baseCoords[1] + offsetLng];
};

// Check if a company is within given bounds
export const isCompanyInBounds = (company: Company, bounds: MapBounds): boolean => {
  const coords = getCompanyCoords(company);
  if (!coords) return false;
  
  const [lat, lng] = coords;
  return lat >= bounds.south && lat <= bounds.north && 
         lng >= bounds.west && lng <= bounds.east;
};

interface MapProps {
  companies: Company[];
  selectedCompany?: Company | null;
  onCompanySelect?: (company: Company) => void;
  height?: string;
  showAllMarkers?: boolean;
  onBoundsChange?: (bounds: MapBounds) => void;
  disableAutoFit?: boolean;
}

export function Map({ 
  companies, 
  selectedCompany, 
  onCompanySelect,
  height = '400px',
  showAllMarkers = true,
  onBoundsChange,
  disableAutoFit = false
}: MapProps) {
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  if (!isMounted) {
    return (
      <div 
        style={{ height }} 
        className="bg-slate-100 rounded-lg flex items-center justify-center"
      >
        <div className="text-slate-500">Se încarcă harta...</div>
      </div>
    );
  }

  return <MapContent 
    companies={companies} 
    selectedCompany={selectedCompany}
    onCompanySelect={onCompanySelect}
    height={height}
    showAllMarkers={showAllMarkers}
    onBoundsChange={onBoundsChange}
    disableAutoFit={disableAutoFit}
  />;
}

// Separate component to handle dynamic imports
function MapContent({ 
  companies, 
  selectedCompany, 
  onCompanySelect,
  height,
  showAllMarkers,
  onBoundsChange,
  disableAutoFit
}: MapProps) {
  const [MapComponents, setMapComponents] = useState<any>(null);

  useEffect(() => {
    // Dynamic import of react-leaflet to avoid SSR issues
    import('react-leaflet').then((mod) => {
      setMapComponents({
        MapContainer: mod.MapContainer,
        TileLayer: mod.TileLayer,
        Marker: mod.Marker,
        Popup: mod.Popup,
        useMap: mod.useMap,
        useMapEvents: mod.useMapEvents,
      });
    });
  }, []);

  if (!MapComponents) {
    return (
      <div 
        style={{ height }} 
        className="bg-slate-100 rounded-lg flex items-center justify-center"
      >
        <div className="text-slate-500">Se încarcă harta...</div>
      </div>
    );
  }

  const { MapContainer, TileLayer, Marker, Popup, useMapEvents, useMap } = MapComponents;

  // Component to track bounds changes
  function BoundsTracker() {
    const map = useMapEvents({
      moveend: () => {
        if (onBoundsChange) {
          const bounds = map.getBounds();
          onBoundsChange({
            north: bounds.getNorth(),
            south: bounds.getSouth(),
            east: bounds.getEast(),
            west: bounds.getWest(),
          });
        }
      },
    });
    
    // Report initial bounds on mount
    useEffect(() => {
      if (onBoundsChange) {
        // Small delay to ensure map is fully initialized
        const timer = setTimeout(() => {
          const bounds = map.getBounds();
          onBoundsChange({
            north: bounds.getNorth(),
            south: bounds.getSouth(),
            east: bounds.getEast(),
            west: bounds.getWest(),
          });
        }, 100);
        return () => clearTimeout(timer);
      }
    }, [map]);
    
    return null;
  }

  // Filter companies with valid coordinates and apply offset for display
  const companiesWithCoords = companies
    .map((company, index) => ({
      company,
      coords: getCompanyCoordsWithOffset(company, index)
    }))
    .filter(item => item.coords !== null) as { company: Company; coords: [number, number] }[];

  // Component to fit map bounds to show all companies
  function FitBoundsToCompanies() {
    const map = useMap();
    
    useEffect(() => {
      // Skip auto-fit if disabled (user has interacted with map)
      if (disableAutoFit) return;
      
      if (companiesWithCoords.length === 0) {
        // No companies, show all of Romania
        map.setView(ROMANIA_CENTER, DEFAULT_ZOOM);
        return;
      }
      
      if (companiesWithCoords.length === 1) {
        // Single company, center on it
        map.setView(companiesWithCoords[0].coords, 13);
        return;
      }
      
      // Multiple companies - fit bounds to show all
      const L = require('leaflet');
      const bounds = L.latLngBounds(companiesWithCoords.map(c => c.coords));
      map.fitBounds(bounds, { padding: [50, 50], maxZoom: 14 });
    }, [map, companiesWithCoords.length, disableAutoFit]);
    
    return null;
  }

  // Determine map center
  let center = ROMANIA_CENTER;
  let zoom = DEFAULT_ZOOM;

  if (selectedCompany) {
    const coords = getCompanyCoords(selectedCompany);
    if (coords) {
      center = coords;
      zoom = 13;
    }
  } else if (companiesWithCoords.length === 1) {
    center = companiesWithCoords[0].coords;
    zoom = 13;
  }

  // Create custom icon
  const createIcon = (isSelected: boolean) => {
    if (typeof window === 'undefined') return null;
    
    const L = require('leaflet');
    
    return L.divIcon({
      className: 'custom-marker',
      html: `<div style="
        background-color: ${isSelected ? '#dc2626' : '#2563eb'};
        width: 30px;
        height: 30px;
        border-radius: 50% 50% 50% 0;
        transform: rotate(-45deg);
        border: 3px solid white;
        box-shadow: 0 2px 5px rgba(0,0,0,0.3);
      "></div>`,
      iconSize: [30, 30],
      iconAnchor: [15, 30],
      popupAnchor: [0, -30],
    });
  };

  return (
    <div style={{ height }} className="rounded-lg overflow-hidden border border-slate-200">
      <MapContainer
        center={center}
        zoom={zoom}
        style={{ height: '100%', width: '100%' }}
        scrollWheelZoom={true}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        {showAllMarkers && companiesWithCoords.map(({ company, coords }) => {
          const isSelected = selectedCompany?.id === company.id;
          const location = company.locations?.[0];
          
          return (
            <Marker
              key={company.id}
              position={coords}
              icon={createIcon(isSelected)}
              eventHandlers={{
                click: () => onCompanySelect?.(company),
              }}
            >
              <Popup>
                <div className="min-w-[220px] p-1">
                  <h3 className="font-heading font-semibold text-navy text-sm mb-1.5">{company.name}</h3>
                  {location && location.address && (
                    <p className="text-xs text-slate mb-2 flex items-start gap-1.5">
                      <svg className="w-3.5 h-3.5 mt-0.5 text-slate/50 flex-shrink-0" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                      </svg>
                      <span>{location.address}, {location.city}</span>
                    </p>
                  )}
                  {company.contacts?.[0] && (
                    <a 
                      href={`tel:${company.contacts[0].value}`}
                      className="text-xs text-charcoal hover:text-navy transition-colors flex items-center gap-1.5 mb-3"
                    >
                      <svg className="w-3.5 h-3.5 text-sage" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/>
                      </svg>
                      <span className="font-medium">{company.contacts[0].value}</span>
                    </a>
                  )}
                  <div className="flex gap-2">
                    <a
                      href={`/company/${company.slug}`}
                      className="inline-flex items-center gap-1 text-xs px-3 py-1.5 rounded-lg font-medium transition-all hover:opacity-90"
                      style={{ backgroundColor: '#001D3D', color: '#ffffff' }}
                    >
                      Vezi detalii
                      <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                        <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
                      </svg>
                    </a>
                    {location && location.address && (
                      <a
                        href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(
                          `${location.address}, ${location.city}, Romania`
                        )}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-1 text-xs px-3 py-1.5 rounded-lg font-medium transition-all hover:opacity-90"
                        style={{ backgroundColor: '#606C38', color: '#ffffff' }}
                      >
                        <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 24 24">
                          <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                        </svg>
                        Maps
                      </a>
                    )}
                  </div>
                </div>
              </Popup>
            </Marker>
          );
        })}

        {/* Single marker for selected company if not showing all */}
        {!showAllMarkers && selectedCompany && getCompanyCoords(selectedCompany) && (
          <Marker
            position={getCompanyCoords(selectedCompany)!}
            icon={createIcon(true)}
          >
            <Popup>
              <div className="min-w-[200px] p-1">
                <h3 className="font-heading font-semibold text-navy text-sm mb-1.5">{selectedCompany.name}</h3>
                {selectedCompany.locations?.[0]?.address && (
                  <p className="text-xs text-slate flex items-start gap-1.5">
                    <svg className="w-3.5 h-3.5 mt-0.5 text-slate/50 flex-shrink-0" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                    </svg>
                    <span>{selectedCompany.locations[0].address}, {selectedCompany.locations[0].city}</span>
                  </p>
                )}
              </div>
            </Popup>
          </Marker>
        )}

        <BoundsTracker />
        <FitBoundsToCompanies />
      </MapContainer>
    </div>
  );
}

export { CITY_COORDINATES, ROMANIA_CENTER };
