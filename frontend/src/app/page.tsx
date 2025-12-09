'use client';

import { useEffect, useState } from 'react';
import { supabase } from '@/lib/supabase';
import { Company, County } from '@/types';
import { CompanyCard } from '@/components/CompanyCard';
import { CompanyCardSkeleton } from '@/components/CompanyCardSkeleton';
import { Input } from '@/components/ui/input';

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
        <div className="mb-4 text-slate-600">
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

        {/* Company Grid */}
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
      </div>

      {/* Footer */}
      <footer className="bg-white border-t mt-12 py-8">
        <div className="max-w-6xl mx-auto px-4 text-center text-slate-500">
          <p>© 2025 Director Servicii Funerare România</p>
          <p className="text-sm mt-2">
            Datele sunt verificate cu listele DSP din fiecare județ.
            <a href="/request-removal" className="text-blue-600 hover:underline ml-1">
              Solicită ștergerea datelor
            </a>
          </p>
        </div>
      </footer>
    </div>
  );
}
