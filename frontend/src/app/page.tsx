'use client';

import { useEffect, useState } from 'react';
import dynamic from 'next/dynamic';
import { supabase } from '@/lib/supabase';
import { Company, County } from '@/types';
import { CompanyCard } from '@/components/CompanyCard';
import { CompanyCardSkeleton } from '@/components/CompanyCardSkeleton';
import { Input } from '@/components/ui/input';

// Dynamic import for Map to avoid SSR issues
const Map = dynamic(() => import('@/components/Map').then(mod => ({ default: mod.Map })), {
  ssr: false,
  loading: () => (
    <div className="h-[400px] bg-slate-100 rounded-lg flex items-center justify-center">
      <div className="text-slate-500">Se încarcă harta...</div>
    </div>
  ),
});

export default function Home() {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [counties, setCounties] = useState<County[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCounty, setSelectedCounty] = useState<string>('');
  const [countySearchQuery, setCountySearchQuery] = useState('');
  const [showCountyDropdown, setShowCountyDropdown] = useState(false);
  const [selectedCity, setSelectedCity] = useState<string>('');
  const [citySearchQuery, setCitySearchQuery] = useState('');
  const [showCityDropdown, setShowCityDropdown] = useState(false);
  const [showVerifiedOnly, setShowVerifiedOnly] = useState(false);
  const [viewMode, setViewMode] = useState<'grid' | 'map'>('grid');
  const [selectedMapCompany, setSelectedMapCompany] = useState<Company | null>(null);

  // Filter counties based on search query
  const filteredCounties = counties.filter(county =>
    county.name.toLowerCase().includes(countySearchQuery.toLowerCase())
  );

  // Get unique cities from current companies based on selected county
  const availableCities = [...new Set(
    companies
      .flatMap(c => c.locations || [])
      .filter(loc => !selectedCounty || loc.county === selectedCounty)
      .map(loc => loc.city)
      .filter(Boolean)
  )].sort();

  // Filter cities based on search query
  const filteredCities = availableCities.filter(city =>
    city?.toLowerCase().includes(citySearchQuery.toLowerCase())
  );

  useEffect(() => {
    fetchCounties();
    fetchCompanies();
  }, []);

  async function fetchCounties() {
    try {
      const { data, error } = await supabase
        .from('counties')
        .select('*')
        .order('name');

      if (error) throw error;
      setCounties(data || []);
    } catch (error) {
      console.error('Error fetching counties:', error);
    }
  }

  async function fetchCompanies() {
    setLoading(true);
    try {
      const { data, error } = await supabase
        .from('companies')
        .select(`
          *,
          contacts (*),
          services (*),
          locations (*)
        `)
        .order('name');

      if (error) throw error;
      setCompanies(data || []);
    } catch (error) {
      console.error('Error fetching companies:', error);
    } finally {
      setLoading(false);
    }
  }

  const filteredCompanies = companies.filter((company) => {
    // Filter by name search
    const matchesSearch = company.name
      .toLowerCase()
      .includes(searchQuery.toLowerCase());
    
    // Filter by verification status
    const matchesVerified = showVerifiedOnly ? company.is_verified : true;
    
    // Filter by county (exact match if selected, or partial match if searching)
    const matchesCounty = selectedCounty
      ? company.locations?.some(loc => loc.county === selectedCounty)
      : countySearchQuery
        ? company.locations?.some(loc => 
            loc.county?.toLowerCase().includes(countySearchQuery.toLowerCase())
          )
        : true;
    
    // Filter by city (exact match if selected, or partial match if searching)
    const matchesCity = selectedCity
      ? company.locations?.some(loc => loc.city === selectedCity)
      : citySearchQuery
        ? company.locations?.some(loc => 
            loc.city?.toLowerCase().includes(citySearchQuery.toLowerCase())
          )
        : true;
    return matchesSearch && matchesVerified && matchesCounty && matchesCity;
  });

  // Handle county selection
  const handleCountySelect = (county: string) => {
    setSelectedCounty(county);
    setCountySearchQuery(county);
    setShowCountyDropdown(false);
    // Reset city when county changes
    setSelectedCity('');
    setCitySearchQuery('');
  };

  // Clear county selection
  const clearCountySelection = () => {
    setSelectedCounty('');
    setCountySearchQuery('');
    setSelectedCity('');
    setCitySearchQuery('');
  };

  // Handle city selection
  const handleCitySelect = (city: string) => {
    setSelectedCity(city);
    setCitySearchQuery(city);
    setShowCityDropdown(false);
  };

  // Clear city selection
  const clearCitySelection = () => {
    setSelectedCity('');
    setCitySearchQuery('');
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-slate-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-6xl mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-slate-900">
            🕯️ Director Servicii Funerare România
          </h1>
          <p className="text-slate-600 mt-2">
            Găsește servicii funerare verificate în toată România
          </p>
        </div>
      </header>

      {/* Search & Filters */}
      <div className="max-w-6xl mx-auto px-4 py-6">
        <div className="bg-white rounded-lg shadow-sm p-4 mb-6">
          {/* Location filters row */}
          <div className="flex flex-col md:flex-row gap-4 mb-4">
            <div className="flex-1 relative">
              <label className="block text-sm font-medium text-slate-700 mb-1">
                📍 Județ
              </label>
              <div className="relative">
                <input
                  type="text"
                  value={countySearchQuery}
                  onChange={(e) => {
                    setCountySearchQuery(e.target.value);
                    setSelectedCounty('');
                    setShowCountyDropdown(true);
                  }}
                  onFocus={() => setShowCountyDropdown(true)}
                  placeholder="Caută județ..."
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
                {selectedCounty && (
                  <button
                    onClick={clearCountySelection}
                    className="absolute right-2 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
                  >
                    ✕
                  </button>
                )}
                {showCountyDropdown && filteredCounties.length > 0 && !selectedCounty && (
                  <div className="absolute z-20 w-full mt-1 bg-white border border-slate-300 rounded-lg shadow-lg max-h-60 overflow-y-auto">
                    <button
                      onClick={() => {
                        setSelectedCounty('');
                        setCountySearchQuery('');
                        setShowCountyDropdown(false);
                      }}
                      className="w-full px-3 py-2 text-left hover:bg-slate-100 text-slate-500"
                    >
                      Toate județele
                    </button>
                    {filteredCounties.map((county) => (
                      <button
                        key={county.id}
                        onClick={() => handleCountySelect(county.name)}
                        className="w-full px-3 py-2 text-left hover:bg-slate-100"
                      >
                        {county.name}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </div>
            <div className="flex-1 relative">
              <label className="block text-sm font-medium text-slate-700 mb-1">
                🏙️ Oraș
              </label>
              <div className="relative">
                <input
                  type="text"
                  value={citySearchQuery}
                  onChange={(e) => {
                    setCitySearchQuery(e.target.value);
                    setSelectedCity('');
                    setShowCityDropdown(true);
                  }}
                  onFocus={() => setShowCityDropdown(true)}
                  placeholder="Caută oraș..."
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  disabled={availableCities.length === 0}
                />
                {selectedCity && (
                  <button
                    onClick={clearCitySelection}
                    className="absolute right-2 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
                  >
                    ✕
                  </button>
                )}
                {showCityDropdown && filteredCities.length > 0 && !selectedCity && (
                  <div className="absolute z-10 w-full mt-1 bg-white border border-slate-300 rounded-lg shadow-lg max-h-60 overflow-y-auto">
                    <button
                      onClick={() => {
                        setSelectedCity('');
                        setCitySearchQuery('');
                        setShowCityDropdown(false);
                      }}
                      className="w-full px-3 py-2 text-left hover:bg-slate-100 text-slate-500"
                    >
                      Toate orașele
                    </button>
                    {filteredCities.map((city) => (
                      <button
                        key={city}
                        onClick={() => handleCitySelect(city!)}
                        className="w-full px-3 py-2 text-left hover:bg-slate-100"
                      >
                        {city}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Click outside to close dropdowns */}
          {(showCountyDropdown || showCityDropdown) && (
            <div
              className="fixed inset-0 z-0"
              onClick={() => {
                setShowCountyDropdown(false);
                setShowCityDropdown(false);
              }}
            />
          )}

          {/* Search and filters row */}
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1">
              <Input
                type="text"
                placeholder="Caută după nume..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full"
              />
            </div>
            <button
              onClick={() => setShowVerifiedOnly(!showVerifiedOnly)}
              className={`px-4 py-2 rounded-lg border transition-colors ${
                showVerifiedOnly
                  ? 'bg-green-100 border-green-500 text-green-700'
                  : 'bg-white border-slate-300 text-slate-600 hover:bg-slate-50'
              }`}
            >
              ✅ Doar verificate
            </button>
            {(selectedCounty || countySearchQuery || selectedCity || citySearchQuery || searchQuery || showVerifiedOnly) && (
              <button
                onClick={() => {
                  setSelectedCounty('');
                  setCountySearchQuery('');
                  setSelectedCity('');
                  setCitySearchQuery('');
                  setSearchQuery('');
                  setShowVerifiedOnly(false);
                }}
                className="px-4 py-2 rounded-lg border border-red-300 text-red-600 hover:bg-red-50 transition-colors"
              >
                ✕ Resetează filtrele
              </button>
            )}
          </div>
        </div>

        {/* Results count and location indicator */}
        <div className="mb-4 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div className="text-slate-600">
            {loading ? (
              <span>Se încarcă...</span>
            ) : (
              <span>
                {filteredCompanies.length} {filteredCompanies.length === 1 ? 'firmă găsită' : 'firme găsite'}
                {selectedCounty && ` în ${selectedCounty}`}
                {!selectedCounty && countySearchQuery && ` (județ: "${countySearchQuery}")`}
                {selectedCity && `, ${selectedCity}`}
                {!selectedCity && citySearchQuery && ` (oraș: "${citySearchQuery}")`}
              </span>
            )}
          </div>
          
          {/* View Toggle */}
          <div className="flex gap-2">
            <button
              onClick={() => setViewMode('grid')}
              className={`px-4 py-2 rounded-lg border transition-colors flex items-center gap-2 ${
                viewMode === 'grid'
                  ? 'bg-blue-100 border-blue-500 text-blue-700'
                  : 'bg-white border-slate-300 text-slate-600 hover:bg-slate-50'
              }`}
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
              </svg>
              Listă
            </button>
            <button
              onClick={() => setViewMode('map')}
              className={`px-4 py-2 rounded-lg border transition-colors flex items-center gap-2 ${
                viewMode === 'map'
                  ? 'bg-blue-100 border-blue-500 text-blue-700'
                  : 'bg-white border-slate-300 text-slate-600 hover:bg-slate-50'
              }`}
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
              </svg>
              Hartă
            </button>
          </div>
        </div>

        {/* Map View */}
        {viewMode === 'map' && (
          <div className="mb-6">
            <Map 
              companies={filteredCompanies}
              selectedCompany={selectedMapCompany}
              onCompanySelect={(company) => setSelectedMapCompany(company)}
              height="500px"
              showAllMarkers={true}
            />
            {selectedMapCompany && (
              <div className="mt-4 p-4 bg-white rounded-lg shadow-sm border">
                <div className="flex items-start justify-between">
                  <div>
                    <h3 className="font-semibold text-lg">{selectedMapCompany.name}</h3>
                    {selectedMapCompany.locations?.[0] && (
                      <p className="text-slate-600 text-sm">
                        📍 {selectedMapCompany.locations[0].address}, {selectedMapCompany.locations[0].city}
                      </p>
                    )}
                    {selectedMapCompany.contacts?.[0] && (
                      <a 
                        href={`tel:${selectedMapCompany.contacts[0].value}`}
                        className="text-blue-600 hover:underline text-sm"
                      >
                        📞 {selectedMapCompany.contacts[0].value}
                      </a>
                    )}
                  </div>
                  <div className="flex gap-2">
                    <a
                      href={`/company/${selectedMapCompany.slug}`}
                      className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm"
                    >
                      Vezi detalii
                    </a>
                    <button
                      onClick={() => setSelectedMapCompany(null)}
                      className="px-3 py-2 border border-slate-300 rounded-lg hover:bg-slate-50 text-sm"
                    >
                      ✕
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Company Grid */}
        {viewMode === 'grid' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {loading ? (
              // Loading skeletons
              <>
                <CompanyCardSkeleton />
                <CompanyCardSkeleton />
                <CompanyCardSkeleton />
                <CompanyCardSkeleton />
                <CompanyCardSkeleton />
                <CompanyCardSkeleton />
              </>
            ) : filteredCompanies.length > 0 ? (
              filteredCompanies.map((company) => (
                <CompanyCard key={company.id} company={company} />
              ))
            ) : (
              <div className="col-span-full text-center py-12">
                <p className="text-slate-500 text-lg">
                  {companies.length === 0
                    ? '📭 Nu există încă firme în baza de date. Rulează scraper-ul pentru a adăuga date.'
                    : '🔍 Nicio firmă nu corespunde criteriilor de căutare.'}
                </p>
                {(selectedCounty || selectedCity) && companies.length > 0 && (
                  <button
                    onClick={() => {
                      setSelectedCounty('');
                      setSelectedCity('');
                    }}
                    className="mt-4 text-blue-600 hover:underline"
                  >
                    Caută în toată România
                  </button>
                )}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Footer */}
      <footer className="bg-white border-t mt-12 py-8">
        <div className="max-w-6xl mx-auto px-4">
          {/* Navigation Links */}
          <div className="flex flex-wrap justify-center gap-6 mb-6">
            <a href="/despre" className="text-slate-600 hover:text-blue-600 transition-colors">
              Despre Noi
            </a>
            <a href="/contact" className="text-slate-600 hover:text-blue-600 transition-colors">
              Contact
            </a>
            <a href="/eliminare" className="text-slate-600 hover:text-blue-600 transition-colors">
              Solicită Ștergerea Datelor
            </a>
          </div>
          
          {/* Copyright */}
          <div className="text-center text-slate-500">
            <p>© 2025 Director Servicii Funerare România</p>
            <p className="text-sm mt-2">
              Datele sunt verificate cu listele DSP din fiecare județ.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
