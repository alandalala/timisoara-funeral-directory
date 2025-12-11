-- Migration: Add reviews tables
-- Run this in Supabase SQL Editor

-- Reviews table: Scraped reviews from Google/Facebook
CREATE TABLE IF NOT EXISTS reviews (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
  source TEXT CHECK (source IN ('google', 'facebook', 'manual')),
  author_name TEXT,
  author_location TEXT,
  rating INTEGER CHECK (rating >= 1 AND rating <= 5),
  content TEXT,
  sentiment_tags TEXT[], -- Array of sentiment tags like 'profesionalism', 'empatie', etc.
  review_date TIMESTAMPTZ,
  source_url TEXT,
  is_featured BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Review summary table: Aggregated review stats per company
CREATE TABLE IF NOT EXISTS review_summaries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  company_id UUID UNIQUE REFERENCES companies(id) ON DELETE CASCADE,
  total_reviews INTEGER DEFAULT 0,
  average_rating DECIMAL(2,1),
  google_rating DECIMAL(2,1),
  facebook_rating DECIMAL(2,1),
  top_sentiment_tags TEXT[], -- Most common sentiment tags
  last_scraped_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_reviews_company_id ON reviews(company_id);
CREATE INDEX IF NOT EXISTS idx_reviews_is_featured ON reviews(is_featured);
CREATE INDEX IF NOT EXISTS idx_review_summaries_company_id ON review_summaries(company_id);

-- Enable RLS
ALTER TABLE reviews ENABLE ROW LEVEL SECURITY;
ALTER TABLE review_summaries ENABLE ROW LEVEL SECURITY;

-- Public read access
CREATE POLICY "Allow public read access on reviews" ON reviews FOR SELECT USING (true);
CREATE POLICY "Allow public read access on review_summaries" ON review_summaries FOR SELECT USING (true);

-- Service role full access (for backend scraper)
CREATE POLICY "Allow service role full access on reviews" ON reviews FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');
CREATE POLICY "Allow service role full access on review_summaries" ON review_summaries FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');
