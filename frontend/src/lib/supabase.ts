import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;

if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error(
    'Missing Supabase environment variables. Please check your .env.local file.'
  );
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey);

// Helper type for database queries
export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[];

export interface Database {
  public: {
    Tables: {
      companies: {
        Row: {
          id: string;
          name: string;
          slug: string;
          motto: string | null;
          description: string | null;
          fiscal_code: string | null;
          website: string | null;
          is_verified: boolean;
          is_non_stop: boolean;
          metadata: Json;
          created_at: string;
          updated_at: string;
        };
        Insert: {
          id?: string;
          name: string;
          slug: string;
          motto?: string | null;
          description?: string | null;
          fiscal_code?: string | null;
          website?: string | null;
          is_verified?: boolean;
          is_non_stop?: boolean;
          metadata?: Json;
          created_at?: string;
          updated_at?: string;
        };
        Update: {
          id?: string;
          name?: string;
          slug?: string;
          motto?: string | null;
          description?: string | null;
          fiscal_code?: string | null;
          website?: string | null;
          is_verified?: boolean;
          is_non_stop?: boolean;
          metadata?: Json;
          created_at?: string;
          updated_at?: string;
        };
      };
      // Add other tables as needed
    };
  };
}
