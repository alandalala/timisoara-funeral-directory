import { MetadataRoute } from 'next';
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = process.env.NEXT_PUBLIC_BASE_URL || 'https://cautarefunerare.ro';

  // Static pages
  const staticPages: MetadataRoute.Sitemap = [
    {
      url: baseUrl,
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 1.0,
    },
  ];

  // Fetch all company slugs for dynamic pages
  const { data: companies, error } = await supabase
    .from('companies')
    .select('slug, updated_at')
    .eq('status', 'active');

  if (error) {
    console.error('Error fetching companies for sitemap:', error);
    return staticPages;
  }

  // Generate company pages
  const companyPages: MetadataRoute.Sitemap = (companies || []).map((company) => ({
    url: `${baseUrl}/company/${company.slug}`,
    lastModified: company.updated_at ? new Date(company.updated_at) : new Date(),
    changeFrequency: 'weekly' as const,
    priority: 0.8,
  }));

  return [...staticPages, ...companyPages];
}
