'use client';

import { useEffect, useState, useRef, useMemo } from 'react';
import dynamic from 'next/dynamic';
import { supabase } from '@/lib/supabase';
import { Company, County } from '@/types';
import { CompanyCard } from '@/components/CompanyCard';
import { CompanyCardSkeleton } from '@/components/CompanyCardSkeleton';
import { Input } from '@/components/ui/input';
import { BottomSheet } from '@/components/BottomSheet';

// Dynamic import for Map to avoid SSR issues
const Map = dynamic(() => import('@/components/Map').then(mod => ({ default: mod.Map })), {
  ssr: false,
  loading: () => (
    <div className="h-[400px] bg-slate-100 rounded-lg flex items-center justify-center">
      <div className="text-slate-500">Se încarcă harta...</div>
    </div>
  ),
});

// Import map utilities for bounds filtering
import { MapBounds, isCompanyInBounds } from '@/components/Map';

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
  const [show24Only, setShow24Only] = useState(false);
  const [viewMode, setViewMode] = useState<'grid' | 'map' | 'split'>('grid');
  const [selectedMapCompany, setSelectedMapCompany] = useState<Company | null>(null);
  const [showMobileFilters, setShowMobileFilters] = useState(false);
  const [mapBounds, setMapBounds] = useState<MapBounds | null>(null);
  const [userInteractedWithMap, setUserInteractedWithMap] = useState(false);
  const [displayLimit, setDisplayLimit] = useState(6); // Initial number of companies to show
  const mapInitializedRef = useRef(false);
  const boundsChangeCountRef = useRef(0);

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
    
    // Read search parameter from URL
    const urlParams = new URLSearchParams(window.location.search);
    const searchParam = urlParams.get('search');
    if (searchParam) {
      setSearchQuery(searchParam);
    }
  }, []);

  // Clear map bounds when leaving split view
  useEffect(() => {
    if (viewMode !== 'split') {
      setMapBounds(null);
    }
  }, [viewMode]);

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
        `);

      if (error) throw error;
      
      // Shuffle companies randomly using Fisher-Yates algorithm
      const shuffled = [...(data || [])];
      for (let i = shuffled.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
      }
      
      setCompanies(shuffled);
    } catch (error) {
      console.error('Error fetching companies:', error);
    } finally {
      setLoading(false);
    }
  }

  // Memoized filtered and shuffled companies - only recalculates when dependencies change
  const filteredCompanies = useMemo(() => {
    // First filter
    const filtered = companies.filter((company) => {
      // Filter by name search (supports searching without diacritics)
      const matchesSearch = normalizeRomanian(company.name)
        .includes(normalizeRomanian(searchQuery));
      
      // Filter by verification status
      const matchesVerified = showVerifiedOnly ? company.is_verified : true;
      
      // Filter by 24/7 availability
      const matches24 = show24Only ? company.is_non_stop : true;
      
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
      return matchesSearch && matchesVerified && matches24 && matchesCounty && matchesCity;
    });
    
    // Then shuffle using Fisher-Yates algorithm
    const shuffled = [...filtered];
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
  }, [companies, searchQuery, selectedCounty, countySearchQuery, selectedCity, citySearchQuery, showVerifiedOnly, show24Only]);

  // For split view - always show all filtered companies
  // The map bounds filtering was causing issues where companies appeared on map but not in list
  const splitViewCompanies = filteredCompanies;

  // Check if any filters are active
  const hasActiveFilters = searchQuery || selectedCounty || countySearchQuery || selectedCity || citySearchQuery || showVerifiedOnly || show24Only;

  // Companies to display - limited if no filters, all if filters active
  const displayedCompanies = hasActiveFilters 
    ? filteredCompanies 
    : filteredCompanies.slice(0, displayLimit);

  // Check if there are more companies to show
  const hasMoreCompanies = !hasActiveFilters && displayLimit < filteredCompanies.length;

  // Reset display limit when filters change
  useEffect(() => {
    setDisplayLimit(6);
  }, [searchQuery, selectedCounty, selectedCity, showVerifiedOnly, show24Only]);

  // Reset map interaction flag when filters change
  useEffect(() => {
    setUserInteractedWithMap(false);
    boundsChangeCountRef.current = 0;
    mapInitializedRef.current = false;
  }, [searchQuery, selectedCounty, selectedCity, showVerifiedOnly, show24Only]);

  // Handle map bounds change - only count as user interaction after map has initialized
  const handleBoundsChange = (bounds: MapBounds) => {
    setMapBounds(bounds);
    
    // First 2 bounds changes are typically: initial load + auto-fit
    // Only after that do we consider it a user interaction
    boundsChangeCountRef.current += 1;
    if (boundsChangeCountRef.current > 2) {
      setUserInteractedWithMap(true);
    }
  };

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
      {/* Hero Section with Background Image */}
      <section 
        className="relative border-b-2 border-warm-grey/50"
        style={{
          backgroundImage: 'url("/hero-forest.jpg")',
          backgroundSize: 'cover',
          backgroundPosition: 'center',
        }}
      >
        {/* Light overlay - 40% for visible nature texture */}
        <div 
          className="absolute inset-0" 
          style={{ backgroundColor: 'rgba(255, 255, 255, 0.40)' }}
        ></div>
        
        {/* Content wrapper - positioned above overlay */}
        <div className="relative z-10">
          {/* Header with Title & Subtitle - NO border */}
          <header role="banner">
            <div className="max-w-6xl mx-auto px-4 py-16 md:py-20">
              <h1 className="text-3xl md:text-4xl lg:text-5xl font-heading text-navy">
                Ghidul Tău de Încredere în Servicii Funerare
              </h1>
              <p className="mt-4 text-lg md:text-xl max-w-2xl" style={{ color: '#001D3D' }}>
                Găsește servicii funerare verificate în toată România
              </p>
            </div>
          </header>

          {/* Search & Filters - Glassmorphism frosted glass */}
          <div className="max-w-6xl mx-auto px-4 py-8">
            <div 
              aria-label="Filtre de căutare" 
              className="rounded-3xl p-6 md:p-8 mb-8"
              style={{
                backgroundColor: 'rgba(255, 255, 255, 0.85)',
                backdropFilter: 'blur(12px)',
                WebkitBackdropFilter: 'blur(12px)',
                boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)',
                border: '1px solid rgba(255, 255, 255, 0.3)',
              }}
            >
            {/* Location filters row */}
            <div className="flex flex-col md:flex-row gap-4 mb-4">
              <div className="flex-1 relative">
                <label htmlFor="county-search" className="block text-sm font-medium text-charcoal mb-2">
                  Județ
                </label>
                <div className="relative">
                  {/* Map Pin Icon */}
                  <div className="absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none">
                    <svg className="w-5 h-5 text-slate/40" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                    </svg>
                  </div>
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
                  className="w-full pl-10 pr-4 py-3 border border-warm-grey rounded-xl bg-white/80 backdrop-blur-sm focus:border-sage focus:ring-2 focus:ring-sage/20 transition-all duration-200"
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
                Oraș
              </label>
              <div className="relative">
                {/* Building Icon for City */}
                <div className="absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none">
                  <svg className="w-5 h-5 text-slate/40" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M15 11V5l-3-3-3 3v2H3v14h18V11h-6zm-8 8H5v-2h2v2zm0-4H5v-2h2v2zm0-4H5V9h2v2zm6 8h-2v-2h2v2zm0-4h-2v-2h2v2zm0-4h-2V9h2v2zm0-4h-2V5h2v2zm6 12h-2v-2h2v2zm0-4h-2v-2h2v2z"/>
                  </svg>
                </div>
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
                  className="w-full pl-10 pr-4 py-3 border border-warm-grey rounded-xl bg-white/80 backdrop-blur-sm focus:border-sage focus:ring-2 focus:ring-sage/20 transition-all duration-200 disabled:bg-muted disabled:cursor-not-allowed"
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
            <div className="flex-1 relative">
              <label htmlFor="name-search" className="sr-only">Caută după nume</label>
              {/* Magnifying Glass Icon */}
              <div className="absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none z-10">
                <svg className="w-5 h-5 text-slate/40" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
              <Input
                id="name-search"
                type="text"
                placeholder="Caută după nume..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                aria-label="Caută firmă după nume"
                className="w-full pl-10 pr-4 py-3 border-warm-grey rounded-xl bg-white/80 backdrop-blur-sm focus:border-sage focus:ring-2 focus:ring-sage/20 transition-all duration-200"
              />
            </div>
            <button
              onClick={() => setShowVerifiedOnly(!showVerifiedOnly)}
              aria-pressed={showVerifiedOnly}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-full text-sm font-medium transition-all duration-200 ${
                showVerifiedOnly 
                  ? 'text-white shadow-md' 
                  : 'bg-slate-100 text-slate-600 border border-slate-200 hover:bg-slate-200'
              }`}
              style={showVerifiedOnly ? { backgroundColor: '#C1A050' } : {}}
            >
              {showVerifiedOnly ? (
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                </svg>
              ) : (
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              )}
              Verificate DSP
            </button>
            <button
              onClick={() => setShow24Only(!show24Only)}
              aria-pressed={show24Only}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-full text-sm font-medium transition-all duration-200 ${
                show24Only 
                  ? 'text-white shadow-md' 
                  : 'bg-slate-100 text-slate-600 border border-slate-200 hover:bg-slate-200'
              }`}
              style={show24Only ? { backgroundColor: '#C1A050' } : {}}
            >
              {show24Only ? (
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                </svg>
              ) : (
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              )}
              24/7
            </button>
            {(selectedCounty || countySearchQuery || selectedCity || citySearchQuery || searchQuery || showVerifiedOnly || show24Only) && (
              <button
                onClick={() => {
                  setSelectedCounty('');
                  setCountySearchQuery('');
                  setSelectedCity('');
                  setCitySearchQuery('');
                  setSearchQuery('');
                  setShowVerifiedOnly(false);
                  setShow24Only(false);
                }}
                aria-label="Resetează toate filtrele"
                className="px-5 py-3 rounded-xl border border-rose/50 text-rose hover:bg-rose/5 btn-press"
              >
                ✕ Resetează filtrele
              </button>
            )}
          </div>
            </div>
          </div>
        </div>
      </section>

      {/* Main content area - Results outside gradient */}
      <main id="main-content" role="main" aria-label="Rezultate căutare">
        <div className="max-w-6xl mx-auto px-4 py-8">
          {/* Mobile Filter Button + Quick Filter Chips */}
          <div className="md:hidden mb-4">
            {/* Mobile Filter Button */}
            <div className="flex items-center gap-3 mb-4">
              <button
                onClick={() => setShowMobileFilters(true)}
                className="flex items-center gap-2 px-4 py-2.5 rounded-full text-sm font-medium bg-navy text-white shadow-md"
                style={{ backgroundColor: '#001D3D' }}
              >
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
                </svg>
                Filtre
                {(selectedCounty || selectedCity || searchQuery || showVerifiedOnly || show24Only) && (
                  <span className="ml-1 px-1.5 py-0.5 bg-white/20 rounded-full text-xs">
                    {[selectedCounty, selectedCity, searchQuery, showVerifiedOnly, show24Only].filter(Boolean).length}
                  </span>
                )}
              </button>
              <span className="text-sm text-slate">
                {filteredCompanies.length} rezultate
              </span>
            </div>

            {/* Horizontal Quick Filter Chips */}
            <div className="flex gap-2 overflow-x-auto pb-2 -mx-4 px-4 scrollbar-hide">
              <button
                onClick={() => setShowVerifiedOnly(!showVerifiedOnly)}
                className={`flex-shrink-0 flex items-center gap-1.5 px-3 py-2 rounded-full text-sm font-medium transition-all whitespace-nowrap ${
                  showVerifiedOnly 
                    ? 'text-white shadow-sm' 
                    : 'bg-white text-slate-600 border border-slate-200'
                }`}
                style={showVerifiedOnly ? { backgroundColor: '#C1A050' } : {}}
              >
                <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Verificat DSP
              </button>
              <button
                onClick={() => setShow24Only(!show24Only)}
                className={`flex-shrink-0 flex items-center gap-1.5 px-3 py-2 rounded-full text-sm font-medium transition-all whitespace-nowrap ${
                  show24Only 
                    ? 'text-white shadow-sm' 
                    : 'bg-white text-slate-600 border border-slate-200'
                }`}
                style={show24Only ? { backgroundColor: '#C1A050' } : {}}
              >
                <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                24/7
              </button>
              {selectedCounty && (
                <button
                  onClick={() => { setSelectedCounty(''); setCountySearchQuery(''); }}
                  className="flex-shrink-0 flex items-center gap-1.5 px-3 py-2 rounded-full text-sm font-medium bg-slate-100 text-slate-700 whitespace-nowrap"
                >
                  {selectedCounty}
                  <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              )}
              {selectedCity && (
                <button
                  onClick={() => { setSelectedCity(''); setCitySearchQuery(''); }}
                  className="flex-shrink-0 flex items-center gap-1.5 px-3 py-2 rounded-full text-sm font-medium bg-slate-100 text-slate-700 whitespace-nowrap"
                >
                  {selectedCity}
                  <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              )}
            </div>
          </div>

          {/* Results count and location indicator - Desktop */}
          <div className="mb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 hidden md:flex">
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
            {/* Split View - Desktop Only */}
            <button
              onClick={() => setViewMode('split')}
              className={`hidden lg:flex px-4 py-2.5 rounded-xl border btn-press items-center gap-2 ${
                viewMode === 'split'
                  ? 'bg-navy/10 border-navy text-navy'
                  : 'bg-white border-warm-grey text-slate hover:bg-cream'
              }`}
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 10V7m0 10a2 2 0 002 2h2a2 2 0 002-2V7a2 2 0 00-2-2h-2a2 2 0 00-2 2" />
              </svg>
              Split
            </button>
          </div>
        </div>

        {/* Split View - Desktop Only (60% list / 40% map) */}
        {viewMode === 'split' && (
          <div className="hidden lg:flex gap-6 h-[calc(100vh-200px)] min-h-[600px]">
            {/* Left Side - Scrollable List (60%) */}
            <div className="w-[60%] overflow-y-auto pr-4 scrollbar-hide">
              {/* Horizontal Filter Bar */}
              <div className="sticky top-0 z-10 bg-cream/95 backdrop-blur-sm pb-4 mb-4 border-b border-warm-grey/30">
                <div className="flex flex-wrap items-center gap-3">
                  {/* County Dropdown */}
                  <div className="relative">
                    <select
                      value={selectedCounty}
                      onChange={(e) => {
                        setSelectedCounty(e.target.value);
                        setCountySearchQuery(e.target.value);
                        setSelectedCity('');
                        setCitySearchQuery('');
                      }}
                      className="appearance-none pl-3 pr-8 py-2 text-sm border border-warm-grey rounded-lg bg-white cursor-pointer hover:border-navy/50 transition-colors"
                    >
                      <option value="">Toate județele</option>
                      {counties.map((county) => (
                        <option key={county.id} value={county.name}>{county.name}</option>
                      ))}
                    </select>
                    <svg className="w-4 h-4 absolute right-2 top-1/2 -translate-y-1/2 text-slate/50 pointer-events-none" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
                    </svg>
                  </div>

                  {/* City Dropdown */}
                  <div className="relative">
                    <select
                      value={selectedCity}
                      onChange={(e) => {
                        setSelectedCity(e.target.value);
                        setCitySearchQuery(e.target.value);
                      }}
                      disabled={availableCities.length === 0}
                      className="appearance-none pl-3 pr-8 py-2 text-sm border border-warm-grey rounded-lg bg-white cursor-pointer hover:border-navy/50 transition-colors disabled:bg-slate-100 disabled:cursor-not-allowed"
                    >
                      <option value="">Toate orașele</option>
                      {availableCities.map((city) => (
                        <option key={city} value={city || ''}>{city}</option>
                      ))}
                    </select>
                    <svg className="w-4 h-4 absolute right-2 top-1/2 -translate-y-1/2 text-slate/50 pointer-events-none" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
                    </svg>
                  </div>

                  {/* Quick Filters */}
                  <button
                    onClick={() => setShowVerifiedOnly(!showVerifiedOnly)}
                    className={`px-3 py-2 text-sm rounded-lg transition-all ${
                      showVerifiedOnly 
                        ? 'text-white' 
                        : 'bg-white border border-warm-grey text-slate hover:border-navy/50'
                    }`}
                    style={showVerifiedOnly ? { backgroundColor: '#C1A050' } : {}}
                  >
                    ✓ DSP
                  </button>
                  <button
                    onClick={() => setShow24Only(!show24Only)}
                    className={`px-3 py-2 text-sm rounded-lg transition-all ${
                      show24Only 
                        ? 'text-white' 
                        : 'bg-white border border-warm-grey text-slate hover:border-navy/50'
                    }`}
                    style={show24Only ? { backgroundColor: '#C1A050' } : {}}
                  >
                    24/7
                  </button>

                  {/* More Filters Button */}
                  <button
                    onClick={() => setShowMobileFilters(true)}
                    className="px-3 py-2 text-sm rounded-lg bg-white border border-warm-grey text-slate hover:border-navy/50 transition-all"
                  >
                    Mai multe filtre
                  </button>

                  {/* Results count */}
                  <span className="text-sm text-slate ml-auto">
                    {splitViewCompanies.length} rezultate
                  </span>
                </div>
              </div>

              {/* Cards Grid */}
              <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
                {loading ? (
                  <>
                    <CompanyCardSkeleton />
                    <CompanyCardSkeleton />
                    <CompanyCardSkeleton />
                    <CompanyCardSkeleton />
                  </>
                ) : splitViewCompanies.length > 0 ? (
                  splitViewCompanies.map((company) => (
                    <div 
                      key={company.id}
                      onMouseEnter={() => setSelectedMapCompany(company)}
                      onMouseLeave={() => setSelectedMapCompany(null)}
                    >
                      <CompanyCard company={company} />
                    </div>
                  ))
                ) : (
                  <div className="col-span-full text-center py-16">
                    <p className="text-slate inline-flex items-center justify-center"><svg className="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2"><path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>Nicio firmă nu corespunde criteriilor.</p>
                    <p className="text-slate/60 text-sm mt-2">Încercați să modificați filtrele sau căutarea.</p>
                  </div>
                )}
              </div>
            </div>

            {/* Right Side - Fixed Map (40%) */}
            <div className="w-[40%] sticky top-0 h-full rounded-2xl overflow-hidden shadow-tactile">
              <Map 
                companies={filteredCompanies}
                selectedCompany={selectedMapCompany}
                onCompanySelect={(company) => setSelectedMapCompany(company)}
                height="100%"
                showAllMarkers={true}
                onBoundsChange={handleBoundsChange}
                disableAutoFit={userInteractedWithMap}
              />
            </div>
          </div>
        )}

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
                        <span className="inline-flex items-center"><svg className="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2"><path strokeLinecap="round" strokeLinejoin="round" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path strokeLinecap="round" strokeLinejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>{selectedMapCompany.locations[0].address}, {selectedMapCompany.locations[0].city}</span>
                      </p>
                    )}
                    {selectedMapCompany.contacts?.[0] && (
                      <a 
                        href={`tel:${selectedMapCompany.contacts[0].value}`}
                        className="text-navy hover:text-navy-dark text-sm inline-block mt-1"
                      >
                        <span className="inline-flex items-center"><svg className="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2"><path strokeLinecap="round" strokeLinejoin="round" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>{selectedMapCompany.contacts[0].value}</span>
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
          <>
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
              ) : displayedCompanies.length > 0 ? (
                displayedCompanies.map((company) => (
                  <CompanyCard key={company.id} company={company} />
                ))
              ) : (
              <div className="col-span-full text-center py-16 animate-fade-in">
                <p className="text-slate text-lg">
                  {companies.length === 0
                    ? <span className="inline-flex items-center"><svg className="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2"><path strokeLinecap="round" strokeLinejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>Nu există încă firme în baza de date.</span>
                    : <span className="inline-flex items-center"><svg className="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2"><path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>Nicio firmă nu corespunde criteriilor de căutare.</span>}
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
            
            {/* Show More Button */}
            {hasMoreCompanies && !loading && (
              <div className="flex justify-center mt-8">
                <button
                  onClick={() => setDisplayLimit(prev => prev + 6)}
                  className="px-8 py-3 bg-white border-2 border-navy text-navy rounded-xl hover:bg-navy hover:text-white transition-all duration-300 font-medium shadow-soft hover:shadow-tactile"
                >
                  Arată mai multe companii ({filteredCompanies.length - displayLimit} rămase)
                </button>
              </div>
            )}
          </>
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
            <a href="/contact" className="text-slate link-animated">
              Raportează o Problemă
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

      {/* Mobile Filter Bottom Sheet */}
      <BottomSheet
        isOpen={showMobileFilters}
        onClose={() => setShowMobileFilters(false)}
        title="Filtre"
        footer={
          <button
            onClick={() => setShowMobileFilters(false)}
            className="w-full py-3.5 rounded-xl text-white font-medium transition-all"
            style={{ backgroundColor: '#C1A050' }}
          >
            Arată {filteredCompanies.length} {filteredCompanies.length === 1 ? 'Rezultat' : 'Rezultate'}
          </button>
        }
      >
        <div className="space-y-6">
          {/* County Filter */}
          <div>
            <label className="block text-sm font-medium text-navy mb-2">Județ</label>
            <div className="relative">
              <div className="absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none">
                <svg className="w-5 h-5 text-slate/40" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                </svg>
              </div>
              <select
                value={selectedCounty}
                onChange={(e) => {
                  setSelectedCounty(e.target.value);
                  setCountySearchQuery(e.target.value);
                  setSelectedCity('');
                  setCitySearchQuery('');
                }}
                className="w-full pl-10 pr-4 py-3 border border-warm-grey rounded-xl bg-white appearance-none"
              >
                <option value="">Toate județele</option>
                {counties.map((county) => (
                  <option key={county.id} value={county.name}>{county.name}</option>
                ))}
              </select>
              <div className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none">
                <svg className="w-5 h-5 text-slate/40" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
                </svg>
              </div>
            </div>
          </div>

          {/* City Filter */}
          <div>
            <label className="block text-sm font-medium text-navy mb-2">Oraș</label>
            <div className="relative">
              <div className="absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none">
                <svg className="w-5 h-5 text-slate/40" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M15 11V5l-3-3-3 3v2H3v14h18V11h-6zm-8 8H5v-2h2v2zm0-4H5v-2h2v2zm0-4H5V9h2v2zm6 8h-2v-2h2v2zm0-4h-2v-2h2v2zm0-4h-2V9h2v2zm0-4h-2V5h2v2zm6 12h-2v-2h2v2zm0-4h-2v-2h2v2z"/>
                </svg>
              </div>
              <select
                value={selectedCity}
                onChange={(e) => {
                  setSelectedCity(e.target.value);
                  setCitySearchQuery(e.target.value);
                }}
                disabled={availableCities.length === 0}
                className="w-full pl-10 pr-4 py-3 border border-warm-grey rounded-xl bg-white appearance-none disabled:bg-slate-100 disabled:text-slate-400"
              >
                <option value="">Toate orașele</option>
                {availableCities.map((city) => (
                  <option key={city} value={city || ''}>{city}</option>
                ))}
              </select>
              <div className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none">
                <svg className="w-5 h-5 text-slate/40" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
                </svg>
              </div>
            </div>
          </div>

          {/* Name Search */}
          <div>
            <label className="block text-sm font-medium text-navy mb-2">Caută după nume</label>
            <div className="relative">
              <div className="absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none">
                <svg className="w-5 h-5 text-slate/40" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Nume firmă..."
                className="w-full pl-10 pr-4 py-3 border border-warm-grey rounded-xl bg-white"
              />
            </div>
          </div>

          {/* Toggle Filters */}
          <div className="space-y-3">
            <label className="block text-sm font-medium text-navy mb-2">Filtre rapide</label>
            
            <button
              onClick={() => setShowVerifiedOnly(!showVerifiedOnly)}
              className={`w-full flex items-center justify-between px-4 py-3 rounded-xl border transition-all ${
                showVerifiedOnly 
                  ? 'border-transparent text-white' 
                  : 'border-warm-grey bg-white text-slate-700'
              }`}
              style={showVerifiedOnly ? { backgroundColor: '#C1A050' } : {}}
            >
              <span className="flex items-center gap-2">
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Verificat DSP
              </span>
              {showVerifiedOnly && (
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                </svg>
              )}
            </button>

            <button
              onClick={() => setShow24Only(!show24Only)}
              className={`w-full flex items-center justify-between px-4 py-3 rounded-xl border transition-all ${
                show24Only 
                  ? 'border-transparent text-white' 
                  : 'border-warm-grey bg-white text-slate-700'
              }`}
              style={show24Only ? { backgroundColor: '#C1A050' } : {}}
            >
              <span className="flex items-center gap-2">
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Disponibil 24/7
              </span>
              {show24Only && (
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                </svg>
              )}
            </button>
          </div>

          {/* Reset Filters */}
          {(selectedCounty || selectedCity || searchQuery || showVerifiedOnly || show24Only) && (
            <button
              onClick={() => {
                setSelectedCounty('');
                setCountySearchQuery('');
                setSelectedCity('');
                setCitySearchQuery('');
                setSearchQuery('');
                setShowVerifiedOnly(false);
                setShow24Only(false);
              }}
              className="w-full py-3 rounded-xl border border-rose/50 text-rose hover:bg-rose/5 transition-colors"
            >
              Resetează toate filtrele
            </button>
          )}
        </div>
      </BottomSheet>
    </div>
  );
}
