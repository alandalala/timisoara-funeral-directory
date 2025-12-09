'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { supabase } from '@/lib/supabase';
import { Company, SERVICE_LABELS, ServiceTag } from '@/types';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';

export default function CompanyDetailPage() {
  const params = useParams();
  const router = useRouter();
  const slug = params.slug as string;

  const [company, setCompany] = useState<Company | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchCompany() {
      if (!slug) return;

      setLoading(true);
      setError(null);

      try {
        // Fetch company with all relations
        const { data, error: fetchError } = await supabase
          .from('companies')
          .select(`
            *,
            contacts (*),
            services (*),
            locations (*)
          `)
          .eq('slug', slug)
          .single();

        if (fetchError) {
          if (fetchError.code === 'PGRST116') {
            setError('Firma nu a fost găsită.');
          } else {
            throw fetchError;
          }
          return;
        }

        setCompany(data as Company);
      } catch (err) {
        console.error('Error fetching company:', err);
        setError('A apărut o eroare la încărcarea datelor.');
      } finally {
        setLoading(false);
      }
    }

    fetchCompany();
  }, [slug]);

  // Loading state
  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="container mx-auto px-4 py-8">
          <Skeleton className="h-8 w-32 mb-6" />
          <Skeleton className="h-12 w-96 mb-4" />
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 space-y-6">
              <Skeleton className="h-48 w-full" />
              <Skeleton className="h-32 w-full" />
            </div>
            <div className="space-y-6">
              <Skeleton className="h-48 w-full" />
              <Skeleton className="h-32 w-full" />
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Error state
  if (error || !company) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Card className="max-w-md">
          <CardContent className="pt-6 text-center">
            <div className="text-6xl mb-4">😔</div>
            <h2 className="text-xl font-semibold mb-2">
              {error || 'Firma nu a fost găsită'}
            </h2>
            <p className="text-gray-600 mb-4">
              Ne pare rău, nu am putut găsi firma pe care o căutați.
            </p>
            <Button onClick={() => router.push('/')}>
              ← Înapoi la listă
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

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
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b">
        <div className="container mx-auto px-4 py-4">
          <Link
            href="/"
            className="inline-flex items-center text-gray-600 hover:text-gray-900 transition-colors"
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
          <div className="flex flex-wrap items-center gap-3 mb-2">
            <h1 className="text-3xl font-bold text-gray-900">{company.name}</h1>
            {company.is_verified && (
              <Badge className="bg-green-100 text-green-800 border-green-200">
                ✓ Verificat
              </Badge>
            )}
            {company.is_non_stop && (
              <Badge className="bg-blue-100 text-blue-800 border-blue-200">
                🕐 Non-Stop
              </Badge>
            )}
          </div>
          {company.motto && (
            <p className="text-lg text-gray-600 italic">&ldquo;{company.motto}&rdquo;</p>
          )}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Main Info */}
          <div className="lg:col-span-2 space-y-6">
            {/* Contact Card */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
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
                    <h4 className="font-medium text-gray-700 mb-2">Telefon</h4>
                    <div className="space-y-2">
                      {allPhones.map((phone) => (
                        <a
                          key={phone.id}
                          href={`tel:${phone.value.replace(/\s/g, '')}`}
                          className="flex items-center gap-2 text-lg text-blue-600 hover:text-blue-800"
                        >
                          <span className="text-2xl">📞</span>
                          <span className="font-medium">{phone.value}</span>
                          {phone.is_primary && (
                            <Badge variant="outline" className="text-xs">Principal</Badge>
                          )}
                        </a>
                      ))}
                    </div>
                  </div>
                )}

                {/* Email */}
                {emails && emails.length > 0 && (
                  <div>
                    <h4 className="font-medium text-gray-700 mb-2">Email</h4>
                    <div className="space-y-2">
                      {emails.map((email) => (
                        <a
                          key={email.id}
                          href={`mailto:${email.value}`}
                          className="flex items-center gap-2 text-blue-600 hover:text-blue-800"
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
                    <h4 className="font-medium text-gray-700 mb-2">Website</h4>
                    <a
                      href={company.website.startsWith('http') ? company.website : `https://${company.website}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center gap-2 text-blue-600 hover:text-blue-800"
                    >
                      <span className="text-xl">🌐</span>
                      <span>{company.website}</span>
                    </a>
                  </div>
                )}

                {/* CTA Button */}
                {primaryPhone && (
                  <div className="pt-4">
                    <a
                      href={`tel:${primaryPhone.value.replace(/\s/g, '')}`}
                      className="block w-full"
                    >
                      <Button className="w-full bg-green-600 hover:bg-green-700 text-lg py-6">
                        📞 Sună Acum: {primaryPhone.value}
                      </Button>
                    </a>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Services Card */}
            {company.services && company.services.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
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
                          className="flex items-center gap-2 p-3 bg-gray-50 rounded-lg"
                        >
                          <span className="text-green-500">✓</span>
                          <span>{label?.ro || service.service_tag}</span>
                        </div>
                      );
                    })}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Description Card */}
            {company.description && !company.description.includes('[SAMPLE]') && (
              <Card>
                <CardHeader>
                  <CardTitle>Despre Firmă</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-700 whitespace-pre-wrap">{company.description}</p>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Right Column - Location & Info */}
          <div className="space-y-6">
            {/* Location Card */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  Locație
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {headquarters && (
                  <div>
                    <h4 className="font-medium text-gray-700 mb-1">Sediu Principal</h4>
                    <p className="text-gray-600">{headquarters.address}</p>
                    <p className="text-gray-600">
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
                      className="inline-flex items-center gap-1 mt-2 text-blue-600 hover:text-blue-800 text-sm"
                    >
                      <span>📍</span> Vezi pe Google Maps
                    </a>
                  </div>
                )}

                {otherLocations && otherLocations.length > 0 && (
                  <div className="border-t pt-4">
                    <h4 className="font-medium text-gray-700 mb-2">Alte Locații</h4>
                    <div className="space-y-3">
                      {otherLocations.map((loc) => (
                        <div key={loc.id} className="text-sm">
                          <Badge variant="outline" className="mb-1">
                            {loc.type === 'wake_house' ? 'Capelă' : 'Showroom'}
                          </Badge>
                          <p className="text-gray-600">{loc.address}</p>
                          <p className="text-gray-600">{loc.city}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Info Card */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Informații
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                {company.fiscal_code && (
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-500">CUI / CIF:</span>
                    <span className="font-medium">{company.fiscal_code}</span>
                  </div>
                )}
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">Program:</span>
                  <span className="font-medium">
                    {company.is_non_stop ? 'Non-Stop (24/7)' : 'Program normal'}
                  </span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">Status:</span>
                  <span className={`font-medium ${company.is_verified ? 'text-green-600' : 'text-gray-600'}`}>
                    {company.is_verified ? '✓ Verificat' : 'Neverificat'}
                  </span>
                </div>
              </CardContent>
            </Card>

            {/* Report Card */}
            <Card className="bg-gray-50">
              <CardContent className="pt-6">
                <p className="text-sm text-gray-600 mb-3">
                  Informațiile nu sunt corecte sau doriți să raportați o problemă?
                </p>
                <Button variant="outline" className="w-full" size="sm">
                  🚩 Raportează o problemă
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-8 mt-12">
        <div className="container mx-auto px-4 text-center">
          <p className="text-gray-400">
            © 2024 Servicii Funerare România. Toate drepturile rezervate.
          </p>
        </div>
      </footer>
    </div>
  );
}
