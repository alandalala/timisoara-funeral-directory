'use client';

import { useRouter } from 'next/navigation';
import { useState, useEffect } from 'react';
import Link from 'next/link';
import dynamic from 'next/dynamic';
import { Company, SERVICE_LABELS, ServiceTag, Review, ReviewSummary, SENTIMENT_LABELS } from '@/types';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';

// Dynamic import for Map to avoid SSR issues
const Map = dynamic(() => import('@/components/Map').then(mod => ({ default: mod.Map })), {
  ssr: false,
  loading: () => (
    <div className="h-[250px] bg-cream rounded-xl flex items-center justify-center">
      <div className="text-slate">Se încarcă harta...</div>
    </div>
  ),
});

interface CompanyDetailProps {
  company: Company;
}

export default function CompanyDetail({ company }: CompanyDetailProps) {
  const router = useRouter();

  const primaryPhone = company.contacts?.find(
    (c) => c.type === 'phone_mobile' && c.is_primary
  );
  // Deduplicate phones by value
  const allPhones = company.contacts?.filter(
    (c) => c.type === 'phone_mobile' || c.type === 'phone_landline'
  ).filter((phone, index, self) => 
    index === self.findIndex(p => p.value === phone.value)
  );
  const emails = company.contacts?.filter((c) => c.type === 'email');
  const headquarters = company.locations?.find((l) => l.type === 'headquarters');
  const otherLocations = company.locations?.filter((l) => l.type !== 'headquarters');

  return (
    <div className="min-h-screen bg-cream">
      {/* Header */}
      <header className="bg-white border-b border-warm-grey">
        <div className="container mx-auto px-4 py-4">
          <Link
            href="/"
            className="inline-flex items-center text-slate hover:text-navy transition-colors"
          >
            <svg
              className="w-5 h-5 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M15 19l-7-7 7-7"
              />
            </svg>
            Înapoi la căutare
          </Link>
        </div>
      </header>

      {/* Hero Image */}
      <HeroImage company={company} />

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* Trust Cluster - Key trust indicators */}
        <div className="flex flex-wrap items-center gap-4 mb-8 pb-6 border-b border-warm-grey">
          {company.is_verified && (
            <div className="flex items-center gap-2 text-navy">
              <div className="w-10 h-10 rounded-full bg-gold/10 flex items-center justify-center">
                <svg className="w-5 h-5 text-gold" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
              </div>
              <div>
                <span className="text-sm font-semibold">Licență Verificată</span>
                <span className="block text-xs text-slate">Autorizat DSP</span>
              </div>
            </div>
          )}
          
          {company.founded_year && (
            <div className="flex items-center gap-2 text-navy">
              <div className="w-10 h-10 rounded-full bg-navy/5 flex items-center justify-center">
                <svg className="w-5 h-5 text-navy" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
                </svg>
              </div>
              <div>
                <span className="text-sm font-semibold">Experiență</span>
                <span className="block text-xs text-slate">Activă din {company.founded_year}</span>
              </div>
            </div>
          )}
          
          {company.is_non_stop && (
            <div className="flex items-center gap-2 text-navy">
              <div className="w-10 h-10 rounded-full bg-sage/10 flex items-center justify-center">
                <svg className="w-5 h-5 text-sage" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
              </div>
              <div>
                <span className="text-sm font-semibold">24/7 Disponibil</span>
                <span className="block text-xs text-slate">Non-stop</span>
              </div>
            </div>
          )}
          
          {headquarters && (
            <div className="flex items-center gap-2 text-navy ml-auto">
              <svg className="w-4 h-4 text-slate" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
              </svg>
              <span className="text-sm text-slate">{headquarters.city}, {headquarters.county}</span>
            </div>
          )}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Content (Services, Description, Location, Info) */}
          <div className="lg:col-span-2 space-y-6">
            {/* Services Card - Expandable Accordion Style */}
            {company.services && company.services.length > 0 && (
              <ServicesAccordion services={company.services} />
            )}

            {/* Review Sentiment Section - Ce Spun Familiile */}
            <ReviewSection 
              reviews={company.reviews} 
              reviewSummary={company.review_summary}
              companyCity={headquarters?.city}
            />

            {/* Description Card */}
            {company.description && !company.description.includes('[SAMPLE]') && (
              <Card className="bg-white border-0 rounded-2xl shadow-tactile-deep">
                <CardHeader className="pb-4">
                  <CardTitle className="font-heading text-navy">Despre Firmă</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-slate whitespace-pre-wrap">{company.description}</p>
                </CardContent>
              </Card>
            )}

            {/* Location Card */}
            <Card className="bg-white border-0 rounded-2xl shadow-tactile-deep">
              <CardHeader className="pb-4">
                <CardTitle className="flex items-center gap-2 font-heading text-navy">
                  <svg className="w-5 h-5 text-gold" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                  </svg>
                  Locație
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Mini Map */}
                <div className="mb-4 rounded-xl overflow-hidden">
                  <Map 
                    companies={[company]}
                    selectedCompany={company}
                    height="250px"
                    showAllMarkers={false}
                  />
                </div>

                {headquarters && (
                  <div>
                    <h4 className="font-medium text-charcoal mb-1">Sediu Principal</h4>
                    <p className="text-slate">{headquarters.address}</p>
                    <p className="text-slate">
                      {headquarters.city}
                      {headquarters.county && `, jud. ${headquarters.county}`}
                    </p>
                  </div>
                )}

                {otherLocations && otherLocations.length > 0 && (
                  <div className="border-t border-warm-grey pt-4">
                    <h4 className="font-medium text-charcoal mb-2">Alte Locații</h4>
                    <div className="space-y-3">
                      {otherLocations.map((loc) => (
                        <div key={loc.id} className="text-sm">
                          <Badge variant="outline" className="mb-1 border-warm-grey rounded-lg">
                            {loc.type === 'wake_house' ? 'Casă Funerară' : loc.type === 'showroom' ? 'Punct de Lucru' : 'Sediu'}
                          </Badge>
                          <p className="text-slate">{loc.address}</p>
                          <p className="text-slate">{loc.city}{loc.county && `, jud. ${loc.county}`}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Info Card */}
            <Card className="bg-white border-0 rounded-2xl shadow-tactile-deep">
              <CardHeader className="pb-4">
                <CardTitle className="flex items-center gap-2 font-heading text-navy">
                  <svg className="w-5 h-5 text-gold" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/>
                  </svg>
                  Informații
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                {company.fiscal_code && (
                  <div className="flex justify-between text-sm">
                    <span className="text-slate">CUI / CIF:</span>
                    <span className="font-medium text-charcoal">{company.fiscal_code}</span>
                  </div>
                )}
                <div className="flex justify-between text-sm">
                  <span className="text-slate">Program:</span>
                  <span className="font-medium text-charcoal">
                    {company.is_non_stop ? 'Non-Stop (24/7)' : 'Program normal'}
                  </span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-slate">Status:</span>
                  <span className={`font-bold ${company.is_verified ? 'text-sage' : 'text-slate'}`}>
                    {company.is_verified ? '✓ Verificat DSP' : 'Neverificat'}
                  </span>
                </div>
              </CardContent>
            </Card>

            {/* Report Card */}
            <Card className="bg-white border-0 rounded-2xl shadow-tactile-deep">
              <CardContent className="pt-6">
                <p className="text-sm text-slate mb-3">
                  Informațiile nu sunt corecte sau doriți să raportați o problemă?
                </p>
                <a href={`/contact?subject=report_error&company=${encodeURIComponent(company.name)}`} className="no-underline">
                  <Button variant="outline" className="w-full flex items-center justify-center gap-2 no-underline" size="sm">
                    <svg className="w-4 h-4 text-rose" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                      <path d="M14.4 6L14 4H5v17h2v-7h5.6l.4 2h7V6z"/>
                    </svg>
                    Raportează o problemă
                  </Button>
                </a>
              </CardContent>
            </Card>
          </div>

          {/* Right Column - Sticky Contact Sidebar */}
          <div className="lg:sticky lg:top-6 lg:self-start space-y-6">
            {/* Contact Card */}
            <Card className="bg-white border-0 rounded-2xl shadow-tactile-deep">
              <CardHeader className="pb-4">
                <CardTitle className="font-heading text-navy">
                  Contact
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Phone Numbers */}
                {allPhones && allPhones.length > 0 && (
                  <div className="space-y-2">
                    {allPhones.map((phone) => (
                      <a
                        key={phone.id}
                        href={`tel:${phone.value.replace(/\s/g, '')}`}
                        className="flex items-center gap-2 text-navy hover:text-navy-dark transition-colors no-underline"
                      >
                        <svg className="w-5 h-5 text-gold flex-shrink-0" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                          <path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/>
                        </svg>
                        <span className="font-medium">{phone.value}</span>
                        {phone.is_primary && (
                          <span className="text-xs bg-gold/10 text-gold rounded-full px-2 py-0.5">Principal</span>
                        )}
                      </a>
                    ))}
                  </div>
                )}

                {/* Email */}
                <div className="space-y-2">
                  <div className="flex items-center gap-2 text-slate/60">
                    <svg className="w-5 h-5 text-gold flex-shrink-0" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                      <path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
                    </svg>
                    <span className="text-sm font-medium text-charcoal">Email</span>
                  </div>
                  {emails && emails.length > 0 ? (
                    <div className="pl-7 space-y-1">
                      {emails.map((email) => (
                        <a
                          key={email.id}
                          href={`mailto:${email.value}`}
                          className="block text-navy hover:text-navy-dark transition-colors no-underline text-sm"
                        >
                          {email.value}
                        </a>
                      ))}
                    </div>
                  ) : (
                    <p className="pl-7 text-sm text-slate/50 italic">Indisponibil</p>
                  )}
                </div>

                {/* Website */}
                <div className="space-y-2">
                  <div className="flex items-center gap-2 text-slate/60">
                    <svg className="w-5 h-5 text-gold flex-shrink-0" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
                    </svg>
                    <span className="text-sm font-medium text-charcoal">Website</span>
                  </div>
                  {company.website ? (
                    <a
                      href={company.website.startsWith('http') ? company.website : `https://${company.website}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="pl-7 block text-navy hover:text-navy-dark transition-colors no-underline text-sm truncate"
                    >
                      {company.website}
                    </a>
                  ) : (
                    <p className="pl-7 text-sm text-slate/50 italic">Indisponibil</p>
                  )}
                </div>

                {/* CTA Buttons */}
                {primaryPhone && (
                  <div className="pt-4 space-y-3 border-t border-warm-grey">
                    {/* Primary CTA - Matte Gold */}
                    <a
                      href={`tel:${primaryPhone.value.replace(/\s/g, '')}`}
                      className="block w-full no-underline"
                    >
                      <button 
                        className="w-full py-4 px-6 rounded-xl font-semibold text-white flex items-center justify-center gap-2 transition-all hover:opacity-90 active:scale-[0.98]"
                        style={{ 
                          backgroundColor: '#C1A050',
                          boxShadow: '0 4px 15px rgba(193, 160, 80, 0.3)'
                        }}
                      >
                        <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                          <path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/>
                        </svg>
                        Sună Acum
                      </button>
                    </a>
                    
                    {/* Secondary CTA - Ghost Button */}
                    {headquarters && (
                      <a
                        href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(
                          `${headquarters.address}, ${headquarters.city}, ${headquarters.county}, Romania`
                        )}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="block w-full no-underline"
                      >
                        <button 
                          className="w-full py-3 px-6 rounded-xl font-medium flex items-center justify-center gap-2 transition-all hover:bg-navy/5 border-2"
                          style={{ 
                            color: '#001D3D',
                            borderColor: '#001D3D',
                            backgroundColor: 'transparent'
                          }}
                        >
                          <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                            <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                          </svg>
                          Deschide în Google Maps
                        </button>
                      </a>
                    )}

                    {/* Tertiary - Download Price List */}
                    <a
                      href="#"
                      className="flex items-center justify-center gap-2 text-sm text-slate hover:text-navy transition-colors pt-2 no-underline"
                    >
                      <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clipRule="evenodd" />
                      </svg>
                      Descarcă Lista de Prețuri (PDF)
                    </a>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </main>

      {/* Mobile Bottom Sheet - Fixed Contact Bar */}
      <div className="lg:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-warm-grey shadow-lg z-40 px-4 py-3 safe-area-pb">
        <div className="flex gap-3 max-w-lg mx-auto">
          {/* Primary CTA - Call */}
          {primaryPhone && (
            <a
              href={`tel:${primaryPhone.value.replace(/\s/g, '')}`}
              className="flex-1 no-underline"
            >
              <button 
                className="w-full py-3 px-4 rounded-xl font-semibold text-white flex items-center justify-center gap-2 transition-all active:scale-[0.98]"
                style={{ 
                  backgroundColor: '#C1A050',
                  boxShadow: '0 4px 12px rgba(193, 160, 80, 0.3)'
                }}
              >
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/>
                </svg>
                Sună
              </button>
            </a>
          )}
          
          {/* Secondary CTA - Directions */}
          {headquarters && (
            <a
              href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(
                `${headquarters.address}, ${headquarters.city}, ${headquarters.county}, Romania`
              )}`}
              target="_blank"
              rel="noopener noreferrer"
              className="flex-1 no-underline"
            >
              <button 
                className="w-full py-3 px-4 rounded-xl font-semibold flex items-center justify-center gap-2 transition-all active:scale-[0.98] border-2"
                style={{ 
                  color: '#001D3D',
                  borderColor: '#001D3D',
                  backgroundColor: 'transparent'
                }}
              >
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                </svg>
                Direcții
              </button>
            </a>
          )}
        </div>
      </div>
      
      {/* Add bottom padding to prevent content from being hidden behind mobile bottom sheet */}
      <div className="lg:hidden h-20" aria-hidden="true" />

      {/* Footer */}
      <footer className="bg-white border-t border-warm-grey py-10 mt-16">
        <div className="container mx-auto px-4 text-center">
          <p className="text-slate">
            © 2025 CautareFunerare.ro. Toate drepturile rezervate.
          </p>
        </div>
      </footer>
    </div>
  );
}

// Hero Image Component - Static hero with Ken Burns effect
function HeroImage({ company }: { company: Company }) {
  // Use the same hero image as the main page
  const heroImage = '/hero-forest.jpg';

  return (
    <section className="relative h-[400px] overflow-hidden">
      {/* Image - static */}
      <div
        className="absolute inset-0 bg-cover bg-center"
        style={{ backgroundImage: `url(${heroImage})` }}
      />
      
      {/* Stronger gradient overlay for text readability */}
      <div 
        className="absolute inset-0" 
        style={{ background: 'linear-gradient(to top, rgba(0,0,0,0.8) 0%, rgba(0,0,0,0.4) 50%, rgba(0,0,0,0.2) 100%)' }}
      />
      
      {/* Company info overlay - bottom left */}
      <div className="absolute bottom-0 left-0 right-0 p-6 md:p-10">
        <div className="container mx-auto">
          <div className="flex items-end gap-4">
            <div>
              <h1 
                className="text-3xl md:text-4xl lg:text-5xl font-heading font-bold drop-shadow-lg"
                style={{ color: '#FFFFFF' }}
              >
                {company.name}
              </h1>
              {company.motto && (
                <p 
                  className="text-lg md:text-xl font-lora italic mt-2 drop-shadow-md"
                  style={{ color: 'rgba(255,255,255,0.9)' }}
                >
                  &ldquo;{company.motto}&rdquo;
                </p>
              )}
            </div>
            {company.is_verified && (
              <div 
                className="flex items-center gap-2 px-4 py-2 rounded-full backdrop-blur-sm"
                style={{
                  background: 'linear-gradient(135deg, rgba(212, 175, 55, 0.9) 0%, rgba(193, 160, 80, 0.9) 100%)',
                  boxShadow: '0 4px 15px rgba(0, 0, 0, 0.3)',
                }}
              >
                <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
                <span className="font-semibold text-white text-sm">Verificat DSP</span>
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}

// Services Accordion Component
function ServicesAccordion({ services }: { services: { id: string; service_tag: string }[] }) {
  const [isExpanded, setIsExpanded] = useState(false);
  const INITIAL_SHOW = 4;
  
  const visibleServices = isExpanded ? services : services.slice(0, INITIAL_SHOW);
  const hasMore = services.length > INITIAL_SHOW;
  
  return (
    <Card className="bg-white border-0 rounded-2xl shadow-tactile-deep overflow-hidden">
      <CardHeader className="pb-4">
        <CardTitle className="flex items-center gap-2 font-heading text-navy">
          <svg className="w-5 h-5 text-gold" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
          </svg>
          Servicii Oferite
          <span className="ml-auto text-sm font-normal text-slate">
            {services.length} servicii
          </span>
        </CardTitle>
      </CardHeader>
      <CardContent className="pt-0">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {visibleServices.map((service) => {
            const label = SERVICE_LABELS[service.service_tag as ServiceTag];
            return (
              <div
                key={service.id}
                className="flex items-center gap-2 p-3 bg-cream rounded-xl transition-all hover:bg-cream/80"
              >
                <span className="text-gold">✓</span>
                <span className="text-charcoal">{label?.ro || service.service_tag}</span>
              </div>
            );
          })}
        </div>
        
        {/* Expand/Collapse Button */}
        {hasMore && (
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="w-full mt-4 py-3 flex items-center justify-center gap-2 text-navy hover:text-navy-dark transition-colors border-t border-warm-grey"
          >
            <span className="text-sm font-medium">
              {isExpanded 
                ? 'Arată mai puțin' 
                : `Arată toate ${services.length} servicii`
              }
            </span>
            <svg 
              className={`w-4 h-4 transition-transform ${isExpanded ? 'rotate-180' : ''}`}
              fill="currentColor" 
              viewBox="0 0 20 20"
            >
              <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
          </button>
        )}
      </CardContent>
    </Card>
  );
}

// Review Section Component
function ReviewSection({ 
  reviews, 
  reviewSummary,
  companyCity 
}: { 
  reviews?: Review[] | null;
  reviewSummary?: ReviewSummary | null;
  companyCity?: string | null;
}) {
  const hasReviews = reviews && reviews.length > 0;
  const hasSummary = reviewSummary && reviewSummary.total_reviews > 0;
  
  // Only show section if there are actual reviews
  if (!hasReviews && !hasSummary) {
    return null;
  }
  
  // Get featured review or first review with content
  const featuredReview = reviews?.find(r => r.is_featured && r.content) || reviews?.find(r => r.content);
  
  // Get sentiment tags from summary or aggregate from reviews
  const sentimentTags = reviewSummary?.top_sentiment_tags || 
    (reviews?.flatMap(r => r.sentiment_tags || []).filter((tag, index, self) => self.indexOf(tag) === index).slice(0, 5)) ||
    [];

  // Only show tags if we have real data
  const displayTags = sentimentTags;
  
  return (
    <Card className="bg-white border-0 rounded-2xl shadow-tactile-deep">
      <CardHeader className="pb-4">
        <CardTitle className="flex items-center gap-2 font-heading text-navy">
          <svg className="w-5 h-5 text-gold" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-7 12h-2v-2h2v2zm0-4h-2V6h2v4z"/>
          </svg>
          Ce Spun Familiile
          {hasSummary && (
            <span className="ml-auto text-sm font-normal text-slate">
              {reviewSummary.total_reviews} recenzii
              {reviewSummary.average_rating && (
                <span className="ml-2 inline-flex items-center">
                  <svg className="w-4 h-4 text-gold mr-0.5" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
                  {reviewSummary.average_rating.toFixed(1)}
                </span>
              )}
            </span>
          )}
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Sentiment Chips */}
        {displayTags.length > 0 && (
          <div className="flex flex-wrap gap-2">
            {displayTags.map((tag) => {
              const label = SENTIMENT_LABELS[tag];
              return (
                <span 
                  key={tag}
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-sage/10 text-sage rounded-full text-sm font-medium"
                >
                  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                  {label?.ro || tag}
                </span>
              );
            })}
          </div>
        )}
        
        {/* Featured Review Quote */}
        {featuredReview?.content && (
          <blockquote className="border-l-4 border-gold pl-4 py-2 mt-4">
            <p className="font-lora italic text-slate/80 text-sm">
              „{featuredReview.content}"
            </p>
            <footer className="mt-2 text-xs text-slate flex items-center gap-2">
              <span>— {featuredReview.author_name || 'Familie'}</span>
              {featuredReview.author_location && (
                <span>din {featuredReview.author_location}</span>
              )}
              {featuredReview.source && (
                <span className="inline-flex items-center gap-1 text-slate/60">
                  • {featuredReview.source === 'google' ? 'Google' : featuredReview.source === 'facebook' ? 'Facebook' : 'Recenzie'}
                </span>
              )}
              {featuredReview.rating && (
                <span className="inline-flex text-gold">
                  {[...Array(featuredReview.rating)].map((_, i) => (
                    <svg key={i} className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
                  ))}
                </span>
              )}
            </footer>
          </blockquote>
        )}
        
        {/* Additional Reviews Preview */}
        {hasReviews && reviews.length > 1 && (
          <div className="pt-2 border-t border-warm-grey mt-4">
            <p className="text-sm text-slate mb-2">Mai multe recenzii:</p>
            <div className="space-y-2">
              {reviews.slice(1, 3).map((review) => (
                review.content && (
                  <div key={review.id} className="text-sm text-slate/70 pl-4 border-l-2 border-warm-grey">
                    <p className="line-clamp-2">„{review.content}"</p>
                    <span className="text-xs">— {review.author_name || 'Anonim'}</span>
                  </div>
                )
              ))}
            </div>
          </div>
        )}
        
        {/* Reviews Source Info */}
        <div className="pt-2">
          <p className="text-xs text-slate">
            {hasReviews 
              ? 'Recenziile sunt colectate din surse publice (Google Reviews, Facebook)'
              : 'Recenziile sunt colectate din surse publice (Google Reviews, Facebook)'
            }
          </p>
        </div>
      </CardContent>
    </Card>
  );
}
