import Link from 'next/link';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Firmă Negăsită',
  description: 'Firma căutată nu a fost găsită în directorul nostru de servicii funerare.',
  robots: {
    index: false,
    follow: true,
  },
};

export default function NotFound() {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="max-w-md text-center px-4">
        <div className="text-8xl mb-6">😔</div>
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Firmă Negăsită
        </h1>
        <p className="text-gray-600 mb-8">
          Ne pare rău, firma pe care o căutați nu există sau a fost eliminată din directorul nostru.
        </p>
        <Link
          href="/"
          className="inline-flex items-center justify-center px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
        >
          ← Înapoi la căutare
        </Link>
      </div>
    </div>
  );
}
