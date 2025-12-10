import { NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

export async function GET() {
  try {
    const { data: counties, error } = await supabase
      .from('counties')
      .select('*')
      .order('name', { ascending: true });

    if (error) {
      console.error('Error fetching counties:', error);
      return NextResponse.json(
        { error: 'Failed to fetch counties' },
        { status: 500 }
      );
    }

    return NextResponse.json({ data: counties });
  } catch (error) {
    console.error('API Error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
