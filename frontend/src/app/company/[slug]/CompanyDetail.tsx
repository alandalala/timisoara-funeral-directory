'use client';

import { useRouter } from 'next/navigation';
import Link from 'next/link';
import dynamic from 'next/dynamic';
import { Company, SERVICE_LABELS, ServiceTag } from '@/types';
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
  const allPhones = company.contacts?.filter(
    (c) => c.type === 'phone_mobile' || c.type === 'phone_landline'
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

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* Company Header */}
        <div className="mb-8">
          <div className="flex flex-wrap items-center gap-3 mb-3">
            <h1 className="text-3xl font-heading text-charcoal">{company.name}</h1>
            {company.is_verified && (
              <Badge className="bg-sage/10 text-sage border-sage/30 rounded-lg">
                ✓ Verificat
              </Badge>
            )}
            {company.is_non_stop && (
              <Badge className="bg-sand/20 text-sand border-sand/30 rounded-lg">
                🕐 Non-Stop
              </Badge>
            )}
          </div>
          {company.motto && (
            <p className="text-lg text-slate italic">&ldquo;{company.motto}&rdquo;</p>
          )}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Main Info */}
          <div className="lg:col-span-2 space-y-6">
            {/* Contact Card */}
            <Card className="bg-white border-warm-grey rounded-2xl shadow-soft">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 font-heading text-charcoal">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                  </svg>
                  Contact
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Phone Numbers */}
                {allPhones && allPhones.length > 0 && (
                  <div>
                    <h4 className="font-medium text-charcoal mb-2">Telefon</h4>
                    <div className="space-y-2">
                      {allPhones.map((phone) => (
                        <a
                          key={phone.id}
                          href={`tel:${phone.value.replace(/\s/g, '')}`}
                          className="flex items-center gap-2 text-lg text-navy hover:text-navy-dark transition-colors"
                        >
                          <span className="text-2xl">📞</span>
                          <span className="font-medium">{phone.value}</span>
                          {phone.is_primary && (
                            <Badge variant="outline" className="text-xs border-warm-grey rounded-lg">Principal</Badge>
                          )}
                        </a>
                      ))}
                    </div>
                  </div>
                )}

                {/* Email */}
                {emails && emails.length > 0 && (
                  <div>
                    <h4 className="font-medium text-charcoal mb-2">Email</h4>
                    <div className="space-y-2">
                      {emails.map((email) => (
                        <a
                          key={email.id}
                          href={`mailto:${email.value}`}
                          className="flex items-center gap-2 text-navy hover:text-navy-dark transition-colors"
                        >
                          <span className="text-xl">✉️</span>
                          <span>{email.value}</span>
                        </a>
                      ))}
                    </div>
                  </div>
                )}

                {/* Website */}
                {company.website && (
                  <div>
                    <h4 className="font-medium text-charcoal mb-2">Website</h4>
                    <a
                      href={company.website.startsWith('http') ? company.website : `https://${company.website}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center gap-2 text-navy hover:text-navy-dark transition-colors"
                    >
                      <span className="text-xl">🌐</span>
                      <span>{company.website}</span>
                    </a>
                  </div>
                )}

                {/* CTA Button */}
                {primaryPhone && (
                  <div className="pt-4 space-y-3">
                    <a
                      href={`tel:${primaryPhone.value.replace(/\s/g, '')}`}
                      className="block w-full"
                    >
                      <Button variant="success" className="w-full text-lg py-6">
                        📞 Sună Acum: {primaryPhone.value}
                      </Button>
                    </a>
                    {headquarters && (
                      <a
                        href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(
                          `${headquarters.address}, ${headquarters.city}, ${headquarters.county}, Romania`
                        )}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="block w-full"
                      >
                        <Button variant="outline" className="w-full text-lg py-6">
                          📍 Deschide în Google Maps
                        </Button>
                      </a>
                    )}
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Services Card */}
            {company.services && company.services.length > 0 && (
              <Card className="bg-white border-warm-grey rounded-2xl shadow-soft">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 font-heading text-charcoal">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                    </svg>
                    Servicii Oferite
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    {company.services.map((service) => {
                      const label = SERVICE_LABELS[service.service_tag as ServiceTag];
                      return (
                        <div
                          key={service.id}
                          className="flex items-center gap-2 p-3 bg-cream rounded-xl"
                        >
                          <span className="text-sage">✓</span>
                          <span className="text-charcoal">{label?.ro || service.service_tag}</span>
                        </div>
                      );
                    })}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Description Card */}
            {company.description && !company.description.includes('[SAMPLE]') && (
              <Card className="bg-white border-warm-grey rounded-2xl shadow-soft">
                <CardHeader>
                  <CardTitle className="font-heading text-charcoal">Despre Firmă</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-slate whitespace-pre-wrap">{company.description}</p>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Right Column - Location & Info */}
          <div className="space-y-6">
            {/* Location Card */}
            <Card className="bg-white border-warm-grey rounded-2xl shadow-soft">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 font-heading text-charcoal">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
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
                    height="200px"
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
                    
                    {/* Google Maps Link */}
                    <a
                      href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(
                        `${headquarters.address}, ${headquarters.city}, ${headquarters.county}, Romania`
                      )}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 mt-2 text-navy hover:text-navy-dark text-sm transition-colors"
                    >
                      <span>📍</span> Vezi pe Google Maps
                    </a>
                  </div>
                )}

                {otherLocations && otherLocations.length > 0 && (
                  <div className="border-t border-warm-grey pt-4">
                    <h4 className="font-medium text-charcoal mb-2">Alte Locații</h4>
                    <div className="space-y-3">
                      {otherLocations.map((loc) => (
                        <div key={loc.id} className="text-sm">
                          <Badge variant="outline" className="mb-1 border-warm-grey rounded-lg">
                            {loc.type === 'wake_house' ? 'Capelă' : 'Showroom'}
                          </Badge>
                          <p className="text-slate">{loc.address}</p>
                          <p className="text-slate">{loc.city}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Info Card */}
            <Card className="bg-white border-warm-grey rounded-2xl shadow-soft">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 font-heading text-charcoal">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
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
                  <span className={`font-medium ${company.is_verified ? 'text-sage' : 'text-slate'}`}>
                    {company.is_verified ? '✓ Verificat' : 'Neverificat'}
                  </span>
                </div>
              </CardContent>
            </Card>

            {/* Report Card */}
            <Card className="bg-cream border-warm-grey rounded-2xl">
              <CardContent className="pt-6">
                <p className="text-sm text-slate mb-3">
                  Informațiile nu sunt corecte sau doriți să raportați o problemă?
                </p>
                <a href={`/contact?subject=report_error&company=${encodeURIComponent(company.name)}`}>
                  <Button variant="outline" className="w-full" size="sm">
                    🚩 Raportează o problemă
                  </Button>
                </a>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-warm-grey py-10 mt-16">
        <div className="container mx-auto px-4 text-center">
          <p className="text-slate">
            © 2025 Servicii Funerare România. Toate drepturile rezervate.
          </p>
        </div>
      </footer>
    </div>
  );
}
