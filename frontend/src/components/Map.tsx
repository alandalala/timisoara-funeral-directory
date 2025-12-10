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

interface MapProps {
  companies: Company[];
  selectedCompany?: Company | null;
  onCompanySelect?: (company: Company) => void;
  height?: string;
  showAllMarkers?: boolean;
}

export function Map({ 
  companies, 
  selectedCompany, 
  onCompanySelect,
  height = '400px',
  showAllMarkers = true 
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
  />;
}

// Separate component to handle dynamic imports
function MapContent({ 
  companies, 
  selectedCompany, 
  onCompanySelect,
  height,
  showAllMarkers 
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

  const { MapContainer, TileLayer, Marker, Popup } = MapComponents;

  // Get coordinates for a company
  const getCompanyCoords = (company: Company): [number, number] | null => {
    const location = company.locations?.[0];
    if (!location) return null;

    // Check if we have geo_point
    if (location.geo_point?.coordinates) {
      return [location.geo_point.coordinates[1], location.geo_point.coordinates[0]];
    }

    // Try to get from city name
    if (location.city && CITY_COORDINATES[location.city]) {
      return CITY_COORDINATES[location.city];
    }

    return null;
  };

  // Filter companies with valid coordinates
  const companiesWithCoords = companies
    .map(company => ({
      company,
      coords: getCompanyCoords(company)
    }))
    .filter(item => item.coords !== null) as { company: Company; coords: [number, number] }[];

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
                <div className="min-w-[200px]">
                  <h3 className="font-semibold text-sm mb-1">{company.name}</h3>
                  {location && (
                    <p className="text-xs text-gray-600 mb-2">
                      {location.address}, {location.city}
                    </p>
                  )}
                  {company.contacts?.[0] && (
                    <a 
                      href={`tel:${company.contacts[0].value}`}
                      className="text-xs text-blue-600 hover:underline"
                    >
                      📞 {company.contacts[0].value}
                    </a>
                  )}
                  <div className="mt-2 flex gap-2">
                    <a
                      href={`/company/${company.slug}`}
                      className="inline-block text-xs px-3 py-1.5 rounded hover:opacity-90"
                      style={{ backgroundColor: '#2563eb', color: '#ffffff' }}
                    >
                      Vezi detalii →
                    </a>
                    {location && (
                      <a
                        href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(
                          `${location.address}, ${location.city}, Romania`
                        )}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-block text-xs px-3 py-1.5 rounded hover:opacity-90"
                        style={{ backgroundColor: '#16a34a', color: '#ffffff' }}
                      >
                        📍 Maps
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
              <div className="min-w-[200px]">
                <h3 className="font-semibold text-sm mb-1">{selectedCompany.name}</h3>
                {selectedCompany.locations?.[0] && (
                  <p className="text-xs text-gray-600">
                    {selectedCompany.locations[0].address}, {selectedCompany.locations[0].city}
                  </p>
                )}
              </div>
            </Popup>
          </Marker>
        )}

        <MapUpdater center={center} zoom={zoom} />
      </MapContainer>
    </div>
  );
}

// Component to update map view when props change
function MapUpdater({ center, zoom }: { center: [number, number]; zoom: number }) {
  const [useMapHook, setUseMapHook] = useState<any>(null);

  useEffect(() => {
    import('react-leaflet').then((mod) => {
      setUseMapHook(() => mod.useMap);
    });
  }, []);

  useEffect(() => {
    if (useMapHook) {
      const MapUpdaterInner = () => {
        const map = useMapHook();
        useEffect(() => {
          map.setView(center, zoom);
        }, [center, zoom, map]);
        return null;
      };
      // We can't actually render this here, so we handle it differently
    }
  }, [useMapHook, center, zoom]);

  return null;
}

export { CITY_COORDINATES, ROMANIA_CENTER };
