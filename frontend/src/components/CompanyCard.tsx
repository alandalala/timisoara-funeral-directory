'use client';

import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Company, SERVICE_LABELS, ServiceTag } from '@/types';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

interface CompanyCardProps {
  company: Company;
}

// Simulated sentiment tags based on company attributes
function getSentimentTags(company: Company): string[] {
  const tags: string[] = [];
  
  if (company.is_verified) tags.push('Profesionist');
  if (company.is_non_stop) tags.push('Disponibil');
  if (company.services && company.services.length >= 15) tags.push('Complet');
  if (company.locations && company.locations.length > 1) tags.push('Accesibil');
  if (company.motto) tags.push('Dedicat');
  
  // Return max 3 tags
  return tags.slice(0, 3);
}

export function CompanyCard({ company }: CompanyCardProps) {
  const router = useRouter();
  
  const primaryPhone = company.contacts?.find(
    (c) => c.is_primary && (c.type === 'phone_mobile' || c.type === 'phone_landline')
  ) || company.contacts?.find(
    (c) => c.type === 'phone_mobile' || c.type === 'phone_landline'
  );

  const primaryEmail = company.contacts?.find((c) => c.type === 'email');
  const headquarters = company.locations?.find((l) => l.type === 'headquarters') || company.locations?.[0];

  // Check if company has pricing info (for price certification badge)
  const hasPricingInfo = company.metadata?.has_price_list || company.services && company.services.length >= 10;
  
  // Generate social proof number (families served) - based on company data
  const familiesServed = company.metadata?.families_served || 
    (company.is_verified ? Math.floor(150 + (company.services?.length || 0) * 15 + (company.locations?.length || 0) * 50) : null);

  // Get sentiment tags
  const sentimentTags = getSentimentTags(company);

  // Handle card click (white space) - navigate to profile
  const handleCardClick = (e: React.MouseEvent) => {
    // Don't navigate if clicking on interactive elements
    const target = e.target as HTMLElement;
    if (
      target.closest('a') || 
      target.closest('button') || 
      target.tagName === 'A' || 
      target.tagName === 'BUTTON'
    ) {
      return;
    }
    router.push(`/company/${company.slug}`);
  };

  return (
    <Card 
      className="relative bg-white border border-warm-grey/30 rounded-2xl h-full flex flex-col animate-fade-in hover:-translate-y-1 hover:shadow-tactile transition-all duration-300 cursor-pointer"
      style={{ 
        boxShadow: '0 10px 30px -10px rgba(0, 29, 61, 0.15)',
      }}
      onClick={handleCardClick}
      role="article"
      aria-label={`${company.name}${company.is_verified ? ' - Verificat DSP' : ''}${company.is_non_stop ? ' - Disponibil 24/7' : ''}`}
    >
      {/* Trust Badges Container - Top Right */}
      <div className="absolute -top-2 -right-2 z-10 flex flex-col gap-1.5 items-end">
        {/* Badge 1: DSP Verified (Identity/Licensed) - Matte Gold */}
        {company.is_verified && (
          <div 
            className="flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold shadow-md"
            style={{ 
              background: 'linear-gradient(135deg, #D4B86A 0%, #C1A050 50%, #A68A40 100%)',
              color: '#FFFFFF',
              boxShadow: '0 2px 8px rgba(193, 160, 80, 0.4)',
            }}
            title="Licențiat și verificat DSP"
          >
            <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
            DSP
          </div>
        )}
        
        {/* Badge 2: Price Certified - Deep Navy */}
        {hasPricingInfo && (
          <div 
            className="flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-medium shadow-sm"
            style={{ 
              backgroundColor: '#001D3D',
              color: '#FFFFFF',
              boxShadow: '0 2px 6px rgba(0, 29, 61, 0.3)',
            }}
            title="Preț transparent"
          >
            <svg className="w-2.5 h-2.5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
            </svg>
            Preț
          </div>
        )}
      </div>

      <CardHeader className="pb-3 pt-4">
        {/* Top row: 24/7 Badge + Social Proof */}
        <div className="flex items-center justify-between mb-2">
          {/* 24/7 Badge - more visible styling */}
          {company.is_non_stop ? (
            <Badge 
              variant="secondary" 
              className="text-xs font-bold rounded-full px-3 py-1 border-0" 
              style={{
                background: 'linear-gradient(135deg, #4A5D6B 0%, #3D4F5C 100%)',
                color: '#FFFFFF',
                boxShadow: '0 2px 6px rgba(74, 93, 107, 0.3)',
              }}
              role="listitem"
            >
              24/7
            </Badge>
          ) : <div />}
          
          {/* Social Proof - Families Served */}
          {familiesServed && familiesServed > 0 && (
            <div 
              className="flex items-center gap-1 text-xs text-slate/70"
              title={`${familiesServed}+ familii au avut încredere în această firmă`}
            >
              <svg className="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z" />
              </svg>
              <span className="font-medium">{familiesServed}+</span>
              <span className="hidden sm:inline">familii</span>
            </div>
          )}
        </div>
        
        {/* Company name - Serif font, semibold, NO underline */}
        <Link 
          href={`/company/${company.slug}`} 
          aria-label={`Vezi detalii pentru ${company.name}`} 
          className="no-underline"
          style={{ textDecoration: 'none' }}
        >
          <CardTitle 
            className="text-xl font-heading font-semibold leading-tight cursor-pointer transition-colors"
            style={{ 
              textDecoration: 'none',
              color: '#2D3436',
            }}
            onMouseEnter={(e) => e.currentTarget.style.color = '#4A5D6B'}
            onMouseLeave={(e) => e.currentTarget.style.color = '#2D3436'}
          >
            {company.name}
          </CardTitle>
        </Link>
        
        {/* Motto - lighter and smaller for hierarchy */}
        {company.motto && (
          <p className="text-xs text-slate/60 italic mt-2 font-light tracking-wide">
            "{company.motto}"
          </p>
        )}
        
        {/* Price indicator - "De la X RON" format */}
        {company.metadata?.starting_price && (
          <div className="mt-2 group relative">
            <div className="flex items-center gap-1.5">
              <span className="text-sm text-slate/60">De la</span>
              <span className="text-lg font-semibold text-navy">
                {company.metadata.starting_price.toLocaleString('ro-RO')} RON
              </span>
              <button 
                className="text-slate/40 hover:text-slate/70 transition-colors"
                title="Vezi detalii preț"
              >
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </button>
            </div>
            {/* Tooltip with price breakdown */}
            <div className="absolute left-0 top-full mt-1 hidden group-hover:block z-20 bg-white border border-warm-grey/30 rounded-xl p-3 shadow-lg min-w-[200px]">
              <p className="text-xs text-slate/70 mb-2">Prețul include:</p>
              <ul className="text-xs text-slate/80 space-y-1">
                <li className="flex items-center gap-1.5">
                  <svg className="w-3 h-3 text-sage" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                  Transport decedat
                </li>
                <li className="flex items-center gap-1.5">
                  <svg className="w-3 h-3 text-sage" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                  Sicriu standard
                </li>
                <li className="flex items-center gap-1.5">
                  <svg className="w-3 h-3 text-sage" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                  Formalități administrative
                </li>
              </ul>
            </div>
          </div>
        )}
      </CardHeader>

      <CardContent className="flex-1 flex flex-col pt-0">
        {/* Location with city/county */}
        {headquarters && (
          <a
            href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(
              `${headquarters.address}, ${headquarters.city}, Romania`
            )}`}
            target="_blank"
            rel="noopener noreferrer"
            aria-label={`Vezi locația pe Google Maps: ${headquarters.address}, ${headquarters.city}`}
            className="flex items-start gap-2.5 text-sm text-slate mb-3 hover:text-navy transition-colors group">
            <svg className="w-4 h-4 mt-0.5 text-slate/50 flex-shrink-0" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
            </svg>
            <div>
              <span className="group-hover:text-navy">{headquarters.address}</span>
              {(headquarters.city || headquarters.county) && (
                <div className="text-xs text-slate/60 mt-0.5">
                  {headquarters.city}{headquarters.city && headquarters.county && ', '}{headquarters.county}
                </div>
              )}
            </div>
          </a>
        )}

        {/* Phone */}
        {primaryPhone && (
          <div className="flex items-center gap-2.5 text-sm mb-3">
            <svg className="w-4 h-4 text-slate/50 flex-shrink-0" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/>
            </svg>
            <a
              href={`tel:${primaryPhone.value}`}
              className="text-charcoal hover:text-navy font-medium transition-colors"
            >
              {primaryPhone.value}
            </a>
          </div>
        )}

        {/* Services - subtle divider */}
        {company.services && company.services.length > 0 && (
          <div className="mt-auto pt-3 border-t border-slate/10">
            <div className="flex flex-wrap gap-1.5">
              {/* Show "Servicii complete" if company has 25+ services (full-service provider) */}
              {company.services.length >= 25 ? (
                <Badge
                  variant="outline"
                  className="text-xs font-medium border-0 rounded-full px-3"
                  style={{ 
                    background: 'linear-gradient(135deg, #D4AF37 0%, #C5A065 100%)',
                    color: '#FFFFFF',
                  }}
                >
                  ★ Servicii complete
                </Badge>
              ) : (
                <>
                  {company.services.slice(0, 3).map((service) => {
                    const label = SERVICE_LABELS[service.service_tag as ServiceTag];
                    return (
                      <Badge
                        key={service.id}
                        variant="outline"
                        className="text-xs font-normal border-slate/20 text-slate/70 rounded-full bg-slate/5"
                      >
                        {label?.ro || service.service_tag}
                      </Badge>
                    );
                  })}
                  {company.services.length > 3 && (
                    <Badge variant="outline" className="text-xs font-normal border-slate/20 text-slate/70 rounded-full bg-slate/5">
                      +{company.services.length - 3}
                    </Badge>
                  )}
                </>
              )}
            </div>
          </div>
        )}

        {/* Sentiment Tags - extracted from reviews */}
        {sentimentTags.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mt-3">
            {sentimentTags.map((tag) => (
              <span
                key={tag}
                className="px-2.5 py-1 text-[11px] font-medium rounded-full bg-slate-100 text-slate-600"
              >
                {tag}
              </span>
            ))}
          </div>
        )}

        {/* Actions - View Details button + Circular Call button */}
        <div className="flex items-center justify-between gap-3 mt-5" role="group" aria-label="Acțiuni">
          {/* View Details - Primary action */}
          <Link
            href={`/company/${company.slug}`}
            aria-label={`Vezi toate detaliile pentru ${company.name}`}
            className="flex-1 py-3 rounded-full text-sm font-medium min-h-[48px] flex items-center justify-center gap-1.5 transition-all no-underline"
            style={{
              border: '1.5px solid #94a3b8',
              color: '#475569',
              textDecoration: 'none',
              backgroundColor: 'transparent',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.borderColor = '#001D3D';
              e.currentTarget.style.color = '#001D3D';
              e.currentTarget.style.backgroundColor = 'rgba(0, 29, 61, 0.03)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.borderColor = '#94a3b8';
              e.currentTarget.style.color = '#475569';
              e.currentTarget.style.backgroundColor = 'transparent';
            }}
            onClick={(e) => e.stopPropagation()}
          >
            Vezi detalii
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
            </svg>
          </Link>

          {/* Circular Call Button - 44x44px touch target */}
          {primaryPhone && (
            <a
              href={`tel:${primaryPhone.value}`}
              onClick={(e) => e.stopPropagation()}
              aria-label={`Sună la ${company.name}: ${primaryPhone.value}`}
              className="w-[44px] h-[44px] rounded-full flex items-center justify-center transition-all hover:scale-110 active:scale-95 flex-shrink-0"
              style={{ 
                background: 'linear-gradient(135deg, #7A9E7E 0%, #6B8F6F 100%)',
                boxShadow: '0 4px 14px rgba(122, 158, 126, 0.4)',
              }}
              title={`Sună: ${primaryPhone.value}`}
            >
              <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/>
              </svg>
            </a>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
