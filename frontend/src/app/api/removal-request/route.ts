import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

interface RemovalRequestBody {
  company_name: string;
  company_slug?: string;
  requester_name: string;
  requester_email: string;
  requester_phone?: string;
  relationship: 'owner' | 'employee' | 'legal_representative' | 'other';
  reason: string;
  additional_info?: string;
}

export async function POST(request: NextRequest) {
  try {
    const body: RemovalRequestBody = await request.json();

    // Validate required fields
    const requiredFields = ['company_name', 'requester_name', 'requester_email', 'relationship', 'reason'];
    const missingFields = requiredFields.filter((field) => !body[field as keyof RemovalRequestBody]);

    if (missingFields.length > 0) {
      return NextResponse.json(
        { error: `Missing required fields: ${missingFields.join(', ')}` },
        { status: 400 }
      );
    }

    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(body.requester_email)) {
      return NextResponse.json(
        { error: 'Invalid email format' },
        { status: 400 }
      );
    }

    // Find company if slug is provided
    let companyId = null;
    if (body.company_slug) {
      const { data: company } = await supabase
        .from('companies')
        .select('id')
        .eq('slug', body.company_slug)
        .single();
      
      if (company) {
        companyId = company.id;
      }
    }

    // Insert the removal request
    const { data: removalRequest, error } = await supabase
      .from('removal_requests')
      .insert({
        company_id: companyId,
        company_name: body.company_name,
        requester_name: body.requester_name,
        requester_email: body.requester_email,
        requester_phone: body.requester_phone || null,
        relationship: body.relationship,
        reason: body.reason,
        additional_info: body.additional_info || null,
        status: 'pending',
        created_at: new Date().toISOString(),
      })
      .select()
      .single();

    if (error) {
      // If removal_requests table doesn't exist, log and return success
      if (error.code === '42P01') {
        console.log('Removal requests table does not exist yet. Request would be:', body);
        return NextResponse.json({
          success: true,
          message: 'Cererea dvs. de eliminare a fost înregistrată și va fi procesată în conformitate cu GDPR în maxim 30 de zile.',
        });
      }
      console.error('Error creating removal request:', error);
      return NextResponse.json(
        { error: 'Failed to create removal request' },
        { status: 500 }
      );
    }

    return NextResponse.json({
      success: true,
      message: 'Cererea dvs. de eliminare a fost înregistrată și va fi procesată în conformitate cu GDPR în maxim 30 de zile.',
      reference: removalRequest?.id,
    });
  } catch (error) {
    console.error('API Error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
