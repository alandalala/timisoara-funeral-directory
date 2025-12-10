import { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { createClient } from '@supabase/supabase-js';
import CompanyDetail from './CompanyDetail';
import { Company } from '@/types';

// Create server-side Supabase client
const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

interface Props {
  params: Promise<{ slug: string }>;
}

// Fetch company data for both metadata and page
async function getCompany(slug: string): Promise<Company | null> {
  const { data, error } = await supabase
    .from('companies')
    .select(`
      *,
      contacts (*),
      services (*),
      locations (*)
    `)
    .eq('slug', slug)
    .single();

  if (error) {
    console.error('Error fetching company:', error);
    return null;
  }

  return data as Company;
}

// Generate dynamic metadata for SEO
export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const company = await getCompany(slug);

  if (!company) {
    return {
      title: 'Firmă Negăsită',
      description: 'Firma căutată nu a fost găsită în directorul nostru.',
    };
  }

  // Get headquarters location
  const headquarters = company.locations?.find((l) => l.type === 'headquarters');
  const city = headquarters?.city || '';
  const county = headquarters?.county || '';

  // Build location string
  const locationString = city && county 
    ? `${city}, jud. ${county}` 
    : city || county || 'România';

  // Build title
  const title = `${company.name} - Servicii Funerare ${locationString}`;

  // Build description
  const serviceCount = company.services?.length || 0;
  const servicesText = serviceCount > 0 
    ? `Oferă ${serviceCount} tipuri de servicii.` 
    : '';
  const programText = company.is_non_stop ? 'Program Non-Stop (24/7).' : '';
  const verifiedText = company.is_verified ? 'Firmă verificată.' : '';
  
  const description = `${company.name} - servicii funerare complete în ${locationString}. ${servicesText} ${programText} ${verifiedText} Contact și detalii pe Servicii Funerare România.`.trim();

  // Build keywords
  const keywords = [
    'servicii funerare',
    company.name.toLowerCase(),
    city.toLowerCase(),
    county.toLowerCase(),
    'pompe funebre',
    'înmormântare',
    ...(company.is_non_stop ? ['servicii funerare non-stop', 'pompe funebre 24/7'] : []),
  ].filter(Boolean);

  // Build canonical URL
  const baseUrl = process.env.NEXT_PUBLIC_BASE_URL || 'https://cautarefunerare.ro';
  const canonicalUrl = `${baseUrl}/company/${slug}`;

  return {
    title,
    description,
    keywords,
    alternates: {
      canonical: canonicalUrl,
    },
    openGraph: {
      title,
      description,
      url: canonicalUrl,
      siteName: 'Servicii Funerare România',
      locale: 'ro_RO',
      type: 'website',
    },
    twitter: {
      card: 'summary',
      title,
      description,
    },
    robots: {
      index: true,
      follow: true,
    },
  };
}

// Generate JSON-LD structured data for LocalBusiness
function generateStructuredData(company: Company) {
  const headquarters = company.locations?.find((l) => l.type === 'headquarters');
  const primaryPhone = company.contacts?.find(
    (c) => c.type === 'phone_mobile' && c.is_primary
  );
  const email = company.contacts?.find((c) => c.type === 'email');

  const structuredData = {
    '@context': 'https://schema.org',
    '@type': 'FuneralHome',
    name: company.name,
    description: company.motto || `Servicii funerare în ${headquarters?.city || 'România'}`,
    ...(headquarters && {
      address: {
        '@type': 'PostalAddress',
        streetAddress: headquarters.address,
        addressLocality: headquarters.city,
        addressRegion: headquarters.county,
        addressCountry: 'RO',
      },
    }),
    ...(primaryPhone && { telephone: primaryPhone.value }),
    ...(email && { email: email.value }),
    ...(company.website && { url: company.website }),
    ...(company.is_non_stop && {
      openingHoursSpecification: {
        '@type': 'OpeningHoursSpecification',
        dayOfWeek: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        opens: '00:00',
        closes: '23:59',
      },
    }),
    priceRange: '$$',
  };

  return structuredData;
}

// Page Component
export default async function CompanyPage({ params }: Props) {
  const { slug } = await params;
  const company = await getCompany(slug);

  if (!company) {
    notFound();
  }

  const structuredData = generateStructuredData(company);

  return (
    <>
      {/* JSON-LD Structured Data */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify(structuredData),
        }}
      />
      
      {/* Main Content */}
      <CompanyDetail company={company} />
    </>
  );
}