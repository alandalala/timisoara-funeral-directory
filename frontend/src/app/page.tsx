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

// Normalize Romanian diacritics for search (ă→a, â→a, î→i, ș→s, ț→t)
function normalizeRomanian(text: string): string {
  return text
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '') // Remove diacritical marks
    .replace(/ă/g, 'a')
    .replace(/â/g, 'a')
    .replace(/î/g, 'i')
    .replace(/ș/g, 's')
    .replace(/ş/g, 's') // Alternative ș
    .replace(/ț/g, 't')
    .replace(/ţ/g, 't'); // Alternative ț
}

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

  // Filter counties based on search query (supports searching without diacritics)
  const filteredCounties = counties.filter(county =>
    normalizeRomanian(county.name).includes(normalizeRomanian(countySearchQuery))
  );

  // Get unique cities from current companies based on selected county
  const availableCities = [...new Set(
    companies
      .flatMap(c => c.locations || [])
      .filter(loc => !selectedCounty || loc.county === selectedCounty)
      .map(loc => loc.city)
      .filter(Boolean)
  )].sort();

  // Filter cities based on search query (supports searching without diacritics)
  const filteredCities = availableCities.filter(city =>
    normalizeRomanian(city || '').includes(normalizeRomanian(citySearchQuery))
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
    // Filter by name search (supports searching without diacritics)
    const matchesSearch = normalizeRomanian(company.name)
      .includes(normalizeRomanian(searchQuery));
    
    // Filter by verification status
    const matchesVerified = showVerifiedOnly ? company.is_verified : true;
    
    // Filter by county (exact match if selected, or partial match if searching)
    const matchesCounty = selectedCounty
      ? company.locations?.some(loc => loc.county === selectedCounty)
      : countySearchQuery
        ? company.locations?.some(loc => 
            normalizeRomanian(loc.county || '').includes(normalizeRomanian(countySearchQuery))
          )
        : true;
    
    // Filter by city (exact match if selected, or partial match if searching)
    const matchesCity = selectedCity
      ? company.locations?.some(loc => loc.city === selectedCity)
      : citySearchQuery
        ? company.locations?.some(loc => 
            normalizeRomanian(loc.city || '').includes(normalizeRomanian(citySearchQuery))
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
    <div className="min-h-screen bg-cream">
      {/* Header - Soft, welcoming */}
      <header className="bg-white shadow-soft border-b border-warm-grey" role="banner">
        <div className="max-w-6xl mx-auto px-4 py-8">
          <h1 className="text-3xl md:text-4xl font-heading text-charcoal">
            🕯️ Ghidul Tău de Încredere în Servicii Funerare
          </h1>
          <p className="text-slate mt-3 text-lg">
            Găsește servicii funerare verificate în toată România
          </p>
        </div>
      </header>

      {/* Main content area */}
      <main id="main-content" role="main" aria-label="Căutare servicii funerare">
      {/* Search & Filters - Soft card styling */}
      <div className="max-w-6xl mx-auto px-4 py-8">
        <section aria-label="Filtre de căutare" className="bg-white rounded-2xl shadow-soft border border-warm-grey p-6 mb-8">
          {/* Location filters row */}
          <div className="flex flex-col md:flex-row gap-4 mb-4">
            <div className="flex-1 relative">
              <label htmlFor="county-search" className="block text-sm font-medium text-charcoal mb-2">
                📍 Județ
              </label>
              <div className="relative">
                <input
                  id="county-search"
                  type="text"
                  value={countySearchQuery}
                  onChange={(e) => {
                    setCountySearchQuery(e.target.value);
                    setSelectedCounty('');
                    setShowCountyDropdown(true);
                  }}
                  onFocus={() => setShowCountyDropdown(true)}
                  placeholder="Caută județ..."
                  aria-label="Caută după județ"
                  aria-expanded={showCountyDropdown}
                  aria-autocomplete="list"
                  className="w-full px-4 py-3 border border-warm-grey rounded-xl input-glow"
                />
                {selectedCounty && (
                  <button
                    onClick={clearCountySelection}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-slate hover:text-charcoal transition-colors"
                  >
                    ✕
                  </button>
                )}
                {showCountyDropdown && filteredCounties.length > 0 && !selectedCounty && (
                  <div className="absolute z-20 w-full mt-2 bg-white border border-warm-grey rounded-xl shadow-soft-lg max-h-60 overflow-y-auto">
                    <button
                      onClick={() => {
                        setSelectedCounty('');
                        setCountySearchQuery('');
                        setShowCountyDropdown(false);
                      }}
                      className="w-full px-4 py-3 text-left hover:bg-cream text-slate transition-colors"
                    >
                      Toate județele
                    </button>
                    {filteredCounties.map((county) => (
                      <button
                        key={county.id}
                        onClick={() => handleCountySelect(county.name)}
                        className="w-full px-4 py-3 text-left hover:bg-cream transition-colors"
                      >
                        {county.name}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </div>
            <div className="flex-1 relative">
              <label htmlFor="city-search" className="block text-sm font-medium text-charcoal mb-2">
                🏙️ Oraș
              </label>
              <div className="relative">
                <input
                  id="city-search"
                  type="text"
                  value={citySearchQuery}
                  onChange={(e) => {
                    setCitySearchQuery(e.target.value);
                    setSelectedCity('');
                    setShowCityDropdown(true);
                  }}
                  onFocus={() => setShowCityDropdown(true)}
                  placeholder="Caută oraș..."
                  aria-label="Caută după oraș"
                  aria-expanded={showCityDropdown}
                  aria-autocomplete="list"
                  className="w-full px-4 py-3 border border-warm-grey rounded-xl input-glow disabled:bg-muted disabled:cursor-not-allowed"
                  disabled={availableCities.length === 0}
                />
                {selectedCity && (
                  <button
                    onClick={clearCitySelection}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-slate hover:text-charcoal transition-colors"
                  >
                    ✕
                  </button>
                )}
                {showCityDropdown && filteredCities.length > 0 && !selectedCity && (
                  <div className="absolute z-10 w-full mt-2 bg-white border border-warm-grey rounded-xl shadow-soft-lg max-h-60 overflow-y-auto">
                    <button
                      onClick={() => {
                        setSelectedCity('');
                        setCitySearchQuery('');
                        setShowCityDropdown(false);
                      }}
                      className="w-full px-4 py-3 text-left hover:bg-cream text-slate transition-colors"
                    >
                      Toate orașele
                    </button>
                    {filteredCities.map((city) => (
                      <button
                        key={city}
                        onClick={() => handleCitySelect(city!)}
                        className="w-full px-4 py-3 text-left hover:bg-cream transition-colors"
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
              <label htmlFor="name-search" className="sr-only">Caută după nume</label>
              <Input
                id="name-search"
                type="text"
                placeholder="Caută după nume..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                aria-label="Caută firmă după nume"
                className="w-full px-4 py-3 border-warm-grey rounded-xl focus:ring-navy/20 focus:border-navy"
              />
            </div>
            <button
              onClick={() => setShowVerifiedOnly(!showVerifiedOnly)}
              aria-pressed={showVerifiedOnly}
              className={`flex items-center gap-2 px-4 py-3 rounded-xl border font-medium transition-all ${
                showVerifiedOnly 
                  ? 'bg-sage text-white border-sage' 
                  : 'bg-white text-slate border-warm-grey hover:bg-cream'
              }`}
            >
              {showVerifiedOnly && (
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                </svg>
              )}
              Verificate DSP
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
                aria-label="Resetează toate filtrele"
                className="px-5 py-3 rounded-xl border border-rose/50 text-rose hover:bg-rose/5 btn-press"
              >
                ✕ Resetează filtrele
              </button>
            )}
          </div>
        </section>

        {/* Results count and location indicator */}
        <div className="mb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div className="text-slate">
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
          
          {/* View Toggle - Softer styling */}
          <div className="flex gap-2">
            <button
              onClick={() => setViewMode('grid')}
              className={`px-4 py-2.5 rounded-xl border btn-press flex items-center gap-2 ${
                viewMode === 'grid'
                  ? 'bg-navy/10 border-navy text-navy'
                  : 'bg-white border-warm-grey text-slate hover:bg-cream'
              }`}
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
              </svg>
              Listă
            </button>
            <button
              onClick={() => setViewMode('map')}
              className={`px-4 py-2.5 rounded-xl border btn-press flex items-center gap-2 ${
                viewMode === 'map'
                  ? 'bg-navy/10 border-navy text-navy'
                  : 'bg-white border-warm-grey text-slate hover:bg-cream'
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
          <div className="mb-8">
            <Map 
              companies={filteredCompanies}
              selectedCompany={selectedMapCompany}
              onCompanySelect={(company) => setSelectedMapCompany(company)}
              height="500px"
              showAllMarkers={true}
            />
            {selectedMapCompany && (
              <div className="mt-4 p-5 bg-white rounded-2xl shadow-soft border border-warm-grey">
                <div className="flex items-start justify-between">
                  <div>
                    <h3 className="font-heading text-xl text-charcoal">{selectedMapCompany.name}</h3>
                    {selectedMapCompany.locations?.[0] && (
                      <p className="text-slate text-sm mt-1">
                        📍 {selectedMapCompany.locations[0].address}, {selectedMapCompany.locations[0].city}
                      </p>
                    )}
                    {selectedMapCompany.contacts?.[0] && (
                      <a 
                        href={`tel:${selectedMapCompany.contacts[0].value}`}
                        className="text-navy hover:text-navy-dark text-sm inline-block mt-1"
                      >
                        📞 {selectedMapCompany.contacts[0].value}
                      </a>
                    )}
                  </div>
                  <div className="flex gap-2">
                    <a
                      href={`/company/${selectedMapCompany.slug}`}
                      className="px-5 py-2.5 bg-navy text-white rounded-xl hover:bg-navy-dark transition-colors text-sm font-medium"
                    >
                      Vezi detalii
                    </a>
                    <button
                      onClick={() => setSelectedMapCompany(null)}
                      className="px-4 py-2.5 border border-warm-grey rounded-xl hover:bg-cream transition-colors text-sm"
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
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-stagger">
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
              <div className="col-span-full text-center py-16 animate-fade-in">
                <p className="text-slate text-lg">
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
                    className="mt-4 text-navy hover:text-navy-dark link-animated"
                  >
                    Caută în toată România
                  </button>
                )}
              </div>
            )}
          </div>
        )}
      </div>
      </main>

      {/* Footer - Soft, supportive */}
      <footer className="bg-white border-t border-warm-grey mt-16 py-10" role="contentinfo">
        <div className="max-w-6xl mx-auto px-4">
          {/* Navigation Links */}
          <nav aria-label="Link-uri subsol" className="flex flex-wrap justify-center gap-8 mb-8">
            <a href="/despre" className="text-slate link-animated">
              Despre Noi
            </a>
            <a href="/contact" className="text-slate link-animated">
              Contact
            </a>
            <a href="/eliminare" className="text-slate link-animated">
              Solicită Ștergerea Datelor
            </a>
          </nav>
          
          {/* Copyright */}
          <div className="text-center text-slate">
            <p className="text-charcoal">© 2025 CăutareFunerare.ro</p>
            <p className="text-sm mt-2">
              Datele sunt verificate cu listele DSP din fiecare județ.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
