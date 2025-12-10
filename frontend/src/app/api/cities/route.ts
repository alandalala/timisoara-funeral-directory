import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const county = searchParams.get('county');

    if (!county) {
      return NextResponse.json(
        { error: 'County parameter is required' },
        { status: 400 }
      );
    }

    // Get distinct cities from locations table for the specified county
    const { data: locations, error } = await supabase
      .from('locations')
      .select('city')
      .ilike('county', county)
      .not('city', 'is', null);

    if (error) {
      console.error('Error fetching cities:', error);
      return NextResponse.json(
        { error: 'Failed to fetch cities' },
        { status: 500 }
      );
    }

    // Get unique cities and sort them
    const uniqueCities = [...new Set(locations?.map((l) => l.city).filter(Boolean))]
      .sort((a, b) => a.localeCompare(b, 'ro'));

    return NextResponse.json({ 
      data: uniqueCities.map((city) => ({ name: city })),
      county,
    });
  } catch (error) {
    console.error('API Error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
