'use client';

import Link from 'next/link';
import { Company, SERVICE_LABELS, ServiceTag } from '@/types';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

interface CompanyCardProps {
  company: Company;
}

export function CompanyCard({ company }: CompanyCardProps) {
  const primaryPhone = company.contacts?.find(
    (c) => c.is_primary && (c.type === 'phone_mobile' || c.type === 'phone_landline')
  ) || company.contacts?.find(
    (c) => c.type === 'phone_mobile' || c.type === 'phone_landline'
  );

  const primaryEmail = company.contacts?.find((c) => c.type === 'email');
  const headquarters = company.locations?.find((l) => l.type === 'headquarters') || company.locations?.[0];

  return (
    <Card 
      className="bg-white border-warm-grey rounded-2xl h-full flex flex-col animate-fade-in"
      role="article"
      aria-label={`${company.name}${company.is_verified ? ' - Verificat DSP' : ''}${company.is_non_stop ? ' - Disponibil 24/7' : ''}`}
    >
      <CardHeader className="pb-3">
        {/* Badges row - moved above title */}
        <div className="flex gap-1.5 mb-2" role="list" aria-label="Statusuri">
          {company.is_non_stop && (
            <Badge variant="secondary" className="text-xs bg-sand/20 text-sand border-sand/30 rounded-lg badge-interactive" role="listitem">
              24/7
            </Badge>
          )}
          {company.is_verified && (
            <Badge variant="default" className="bg-sage hover:bg-sage/90 text-white text-xs rounded-lg badge-interactive" role="listitem">
              <span aria-hidden="true">✓</span> DSP
            </Badge>
          )}
        </div>
        
        {/* Company name - full width */}
        <Link href={`/company/${company.slug}`} aria-label={`Vezi detalii pentru ${company.name}`}>
          <CardTitle className="text-lg font-heading text-charcoal leading-tight link-animated cursor-pointer">
            {company.name}
          </CardTitle>
        </Link>
        
        {company.motto && (
          <p className="text-sm text-slate italic mt-2">
            "{company.motto}"
          </p>
        )}
      </CardHeader>

      <CardContent className="flex-1 flex flex-col">
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
            <svg className="w-4 h-4 mt-0.5 text-rose flex-shrink-0" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
            </svg>
            <div>
              <span className="group-hover:underline">{headquarters.address}</span>
              {(headquarters.city || headquarters.county) && (
                <div className="text-xs text-slate/70 mt-0.5 group-hover:text-navy">
                  {headquarters.city}{headquarters.city && headquarters.county && ', '}{headquarters.county}
                </div>
              )}
            </div>
          </a>
        )}

        {/* Phone */}
        {primaryPhone && (
          <div className="flex items-center gap-2.5 text-sm mb-3">
            <svg className="w-4 h-4 text-sage flex-shrink-0" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/>
            </svg>
            <a
              href={`tel:${primaryPhone.value}`}
              className="text-navy hover:text-navy-dark font-medium transition-colors"
            >
              {primaryPhone.value}
            </a>
          </div>
        )}

        {/* Services */}
        {company.services && company.services.length > 0 && (
          <div className="mt-auto pt-3 border-t border-warm-grey">
            <div className="flex flex-wrap gap-1.5">
              {/* Show "Servicii complete" if company has 25+ services (full-service provider) */}
              {company.services.length >= 25 ? (
                <Badge
                  variant="outline"
                  className="text-xs font-medium border-sage text-sage bg-sage/10 rounded-lg"
                >
                  ✨ Servicii complete
                </Badge>
              ) : (
                <>
                  {company.services.slice(0, 4).map((service) => {
                    const label = SERVICE_LABELS[service.service_tag as ServiceTag];
                    return (
                      <Badge
                        key={service.id}
                        variant="outline"
                        className="text-xs font-normal border-warm-grey text-slate rounded-lg"
                      >
                        {label?.ro || service.service_tag}
                      </Badge>
                    );
                  })}
                  {company.services.length > 4 && (
                    <Badge variant="outline" className="text-xs font-normal border-warm-grey text-slate rounded-lg">
                      +{company.services.length - 4}
                    </Badge>
                  )}
                </>
              )}
            </div>
          </div>
        )}

        {/* Actions - Softened buttons with micro-interactions */}
        <div className="flex gap-2 mt-4" role="group" aria-label="Acțiuni">
          {primaryPhone && (
            <a
              href={`tel:${primaryPhone.value}`}
              onClick={(e) => e.stopPropagation()}
              aria-label={`Sună la ${company.name}: ${primaryPhone.value}`}
              className="flex-1 bg-sage text-center py-2.5 rounded-xl text-sm font-medium btn-press hover:bg-sage/90 min-h-[44px] flex items-center justify-center gap-2"
              style={{ color: '#FFFFFF' }}
            >
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/>
              </svg>
              Sună acum
            </a>
          )}
          <Link
            href={`/company/${company.slug}`}
            aria-label={`Vezi toate detaliile pentru ${company.name}`}
            className="px-4 py-2.5 border border-warm-grey rounded-xl text-sm font-medium btn-press hover:bg-cream text-charcoal min-h-[44px] flex items-center justify-center"
          >
            Detalii <span aria-hidden="true">→</span>
          </Link>
        </div>
      </CardContent>
    </Card>
  );
}
