import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    
    // Parse query parameters
    const page = parseInt(searchParams.get('page') || '1');
    const limit = parseInt(searchParams.get('limit') || '20');
    const search = searchParams.get('search') || '';
    const county = searchParams.get('county') || '';
    const city = searchParams.get('city') || '';
    const isNonStop = searchParams.get('is_non_stop') === 'true';
    const isVerified = searchParams.get('is_verified') === 'true';
    
    // Calculate offset
    const offset = (page - 1) * limit;

    // Build query
    let query = supabase
      .from('companies')
      .select(`
        *,
        contacts (*),
        services (*),
        locations (*)
      `, { count: 'exact' })
      .eq('status', 'active')
      .order('is_verified', { ascending: false })
      .order('name', { ascending: true });

    // Apply filters
    if (search) {
      query = query.ilike('name', `%${search}%`);
    }

    if (isNonStop) {
      query = query.eq('is_non_stop', true);
    }

    if (isVerified) {
      query = query.eq('is_verified', true);
    }

    // Apply pagination
    query = query.range(offset, offset + limit - 1);

    const { data: companies, error, count } = await query;

    if (error) {
      console.error('Error fetching companies:', error);
      return NextResponse.json(
        { error: 'Failed to fetch companies' },
        { status: 500 }
      );
    }

    // Filter by county/city (post-query filter since it's in related table)
    let filteredCompanies = companies || [];
    
    if (county) {
      filteredCompanies = filteredCompanies.filter((company) =>
        company.locations?.some((loc: { county?: string }) => 
          loc.county?.toLowerCase() === county.toLowerCase()
        )
      );
    }

    if (city) {
      filteredCompanies = filteredCompanies.filter((company) =>
        company.locations?.some((loc: { city?: string }) => 
          loc.city?.toLowerCase() === city.toLowerCase()
        )
      );
    }

    // Calculate pagination info
    const totalCount = county || city ? filteredCompanies.length : (count || 0);
    const totalPages = Math.ceil(totalCount / limit);

    return NextResponse.json({
      data: filteredCompanies,
      pagination: {
        page,
        limit,
        totalCount,
        totalPages,
        hasMore: page < totalPages,
      },
    });
  } catch (error) {
    console.error('API Error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
