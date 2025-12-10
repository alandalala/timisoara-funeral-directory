-- =============================================
-- Reports & Removal Requests Tables
-- Run this in Supabase SQL Editor
-- =============================================

-- Reports table for user feedback
CREATE TABLE IF NOT EXISTS reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID REFERENCES companies(id) ON DELETE SET NULL,
    report_type VARCHAR(50) NOT NULL CHECK (report_type IN ('incorrect_info', 'closed_business', 'spam', 'other')),
    description TEXT NOT NULL,
    reporter_email VARCHAR(255),
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'reviewed', 'resolved', 'dismissed')),
    admin_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_reports_status ON reports(status);
CREATE INDEX IF NOT EXISTS idx_reports_company ON reports(company_id);
CREATE INDEX IF NOT EXISTS idx_reports_created ON reports(created_at DESC);

-- GDPR Removal Requests table
CREATE TABLE IF NOT EXISTS removal_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID REFERENCES companies(id) ON DELETE SET NULL,
    company_name VARCHAR(255) NOT NULL,
    requester_name VARCHAR(255) NOT NULL,
    requester_email VARCHAR(255) NOT NULL,
    requester_phone VARCHAR(50),
    relationship VARCHAR(50) NOT NULL CHECK (relationship IN ('owner', 'employee', 'legal_representative', 'other')),
    reason TEXT NOT NULL,
    additional_info TEXT,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'completed', 'rejected')),
    admin_notes TEXT,
    processed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for removal requests
CREATE INDEX IF NOT EXISTS idx_removal_requests_status ON removal_requests(status);
CREATE INDEX IF NOT EXISTS idx_removal_requests_email ON removal_requests(requester_email);
CREATE INDEX IF NOT EXISTS idx_removal_requests_created ON removal_requests(created_at DESC);

-- Enable RLS
ALTER TABLE reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE removal_requests ENABLE ROW LEVEL SECURITY;

-- Allow public to insert reports
CREATE POLICY "Allow public to create reports"
    ON reports FOR INSERT
    TO public
    WITH CHECK (true);

-- Allow public to insert removal requests
CREATE POLICY "Allow public to create removal requests"
    ON removal_requests FOR INSERT
    TO public
    WITH CHECK (true);

-- Only allow reading own reports (by email)
CREATE POLICY "Allow reading own reports by email"
    ON reports FOR SELECT
    TO public
    USING (reporter_email IS NOT NULL);

-- Only allow reading own removal requests (by email)
CREATE POLICY "Allow reading own removal requests by email"
    ON removal_requests FOR SELECT
    TO public
    USING (requester_email IS NOT NULL);

-- Update trigger for reports
CREATE OR REPLACE FUNCTION update_reports_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_reports_timestamp
    BEFORE UPDATE ON reports
    FOR EACH ROW
    EXECUTE FUNCTION update_reports_timestamp();

-- Update trigger for removal_requests
CREATE TRIGGER update_removal_requests_timestamp
    BEFORE UPDATE ON removal_requests
    FOR EACH ROW
    EXECUTE FUNCTION update_reports_timestamp();

-- =============================================
-- Success message
-- =============================================
SELECT 'Reports and Removal Requests tables created successfully!' AS message;
