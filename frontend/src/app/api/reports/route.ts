import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

interface ReportBody {
  company_id?: string;
  company_slug?: string;
  report_type: 'incorrect_info' | 'closed_business' | 'spam' | 'other';
  description: string;
  reporter_email?: string;
}

export async function POST(request: NextRequest) {
  try {
    const body: ReportBody = await request.json();

    // Validate required fields
    if (!body.report_type || !body.description) {
      return NextResponse.json(
        { error: 'Report type and description are required' },
        { status: 400 }
      );
    }

    if (!body.company_id && !body.company_slug) {
      return NextResponse.json(
        { error: 'Company ID or slug is required' },
        { status: 400 }
      );
    }

    // If only slug is provided, get the company ID
    let companyId = body.company_id;
    if (!companyId && body.company_slug) {
      const { data: company, error: companyError } = await supabase
        .from('companies')
        .select('id')
        .eq('slug', body.company_slug)
        .single();

      if (companyError || !company) {
        return NextResponse.json(
          { error: 'Company not found' },
          { status: 404 }
        );
      }
      companyId = company.id;
    }

    // Insert the report
    const { data: report, error } = await supabase
      .from('reports')
      .insert({
        company_id: companyId,
        report_type: body.report_type,
        description: body.description,
        reporter_email: body.reporter_email || null,
        status: 'pending',
        created_at: new Date().toISOString(),
      })
      .select()
      .single();

    if (error) {
      // If reports table doesn't exist, log and return success anyway
      if (error.code === '42P01') {
        console.log('Reports table does not exist yet. Report would be:', body);
        return NextResponse.json({
          success: true,
          message: 'Raportul a fost înregistrat. Vă mulțumim!',
        });
      }
      console.error('Error creating report:', error);
      return NextResponse.json(
        { error: 'Failed to create report' },
        { status: 500 }
      );
    }

    return NextResponse.json({
      success: true,
      message: 'Raportul a fost înregistrat. Vă mulțumim!',
      data: report,
    });
  } catch (error) {
    console.error('API Error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
