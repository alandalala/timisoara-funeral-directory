import { Metadata } from 'next';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'Despre Noi',
  description: 'Despre directorul de servicii funerare din România. Misiunea noastră este să ajutăm familiile să găsească servicii funerare de încredere în momentele dificile.',
};

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b">
        <div className="container mx-auto px-4 py-4">
          <Link
            href="/"
            className="inline-flex items-center text-gray-600 hover:text-gray-900 transition-colors"
          >
            <svg
              className="w-5 h-5 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M15 19l-7-7 7-7"
              />
            </svg>
            Înapoi la căutare
          </Link>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-12">
        <div className="max-w-3xl mx-auto">
          <h1 className="text-4xl font-bold text-gray-900 mb-8">
            Despre Servicii Funerare România
          </h1>

          <div className="prose prose-lg max-w-none">
            <section className="mb-10">
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">
                Misiunea Noastră
              </h2>
              <p className="text-gray-600 leading-relaxed mb-4">
                Servicii Funerare România este un director online dedicat ajutorării familiilor 
                în momentele dificile. Înțelegem că pierderea unei persoane dragi este una dintre 
                cele mai grele experiențe, iar găsirea rapidă a serviciilor funerare potrivite 
                nu ar trebui să fie o povară suplimentară.
              </p>
              <p className="text-gray-600 leading-relaxed">
                Misiunea noastră este să oferim acces facil la informații verificate despre 
                firmele de servicii funerare din toată România, astfel încât să puteți lua 
                decizii informate în momente când timpul și claritatea sunt esențiale.
              </p>
            </section>

            <section className="mb-10">
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">
                Ce Oferim
              </h2>
              <ul className="space-y-3 text-gray-600">
                <li className="flex items-start">
                  <span className="text-green-500 mr-3 mt-1">✓</span>
                  <span><strong>Director Complet:</strong> Acoperire în toate cele 41 de județe ale României plus București</span>
                </li>
                <li className="flex items-start">
                  <span className="text-green-500 mr-3 mt-1">✓</span>
                  <span><strong>Informații Verificate:</strong> Date de contact actualizate și verificate</span>
                </li>
                <li className="flex items-start">
                  <span className="text-green-500 mr-3 mt-1">✓</span>
                  <span><strong>Căutare Rapidă:</strong> Filtrare după județ, oraș și tipuri de servicii</span>
                </li>
                <li className="flex items-start">
                  <span className="text-green-500 mr-3 mt-1">✓</span>
                  <span><strong>Servicii Non-Stop:</strong> Identificare rapidă a firmelor disponibile 24/7</span>
                </li>
                <li className="flex items-start">
                  <span className="text-green-500 mr-3 mt-1">✓</span>
                  <span><strong>Hartă Interactivă:</strong> Vizualizare pe hartă pentru a găsi servicii în apropiere</span>
                </li>
                <li className="flex items-start">
                  <span className="text-green-500 mr-3 mt-1">✓</span>
                  <span><strong>Acces Gratuit:</strong> Toate informațiile sunt disponibile gratuit</span>
                </li>
              </ul>
            </section>

            <section className="mb-10">
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">
                Tipuri de Servicii
              </h2>
              <p className="text-gray-600 leading-relaxed mb-4">
                În directorul nostru puteți găsi firme care oferă o gamă completă de servicii funerare:
              </p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-gray-600">
                <div className="bg-white p-3 rounded-lg border">🕯️ Transport funerar</div>
                <div className="bg-white p-3 rounded-lg border">⚰️ Sicrie și urne</div>
                <div className="bg-white p-3 rounded-lg border">💐 Aranjamente florale</div>
                <div className="bg-white p-3 rounded-lg border">🏛️ Capele și săli de priveghi</div>
                <div className="bg-white p-3 rounded-lg border">⛪ Servicii religioase</div>
                <div className="bg-white p-3 rounded-lg border">🔥 Crematoriu</div>
                <div className="bg-white p-3 rounded-lg border">📋 Acte și formalități</div>
                <div className="bg-white p-3 rounded-lg border">🌍 Repatriere internațională</div>
              </div>
            </section>

            <section className="mb-10">
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">
                Confidențialitate și GDPR
              </h2>
              <p className="text-gray-600 leading-relaxed mb-4">
                Respectăm confidențialitatea tuturor utilizatorilor și ne conformăm 
                Regulamentului General privind Protecția Datelor (GDPR). Nu colectăm 
                date personale fără consimțământ și nu partajăm informații cu terțe părți.
              </p>
              <p className="text-gray-600 leading-relaxed">
                Dacă sunteți proprietarul unei firme listate și doriți actualizarea sau 
                eliminarea informațiilor, vă rugăm să ne contactați prin{' '}
                <Link href="/eliminare" className="text-blue-600 hover:text-blue-800">
                  formularul de solicitare
                </Link>.
              </p>
            </section>

            <section className="bg-blue-50 p-6 rounded-lg">
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">
                Contact
              </h2>
              <p className="text-gray-600 mb-4">
                Pentru întrebări, sugestii sau solicitări, ne puteți contacta:
              </p>
              <div className="space-y-2">
                <p className="text-gray-600">
                  📧 Email: <a href="mailto:contact@serviciifunerare.ro" className="text-blue-600 hover:text-blue-800">contact@serviciifunerare.ro</a>
                </p>
                <p className="text-gray-600">
                  📝 <Link href="/contact" className="text-blue-600 hover:text-blue-800">Formular de contact</Link>
                </p>
              </div>
            </section>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-8 mt-12">
        <div className="container mx-auto px-4 text-center">
          <p className="text-gray-400">
            © 2024 Servicii Funerare România. Toate drepturile rezervate.
          </p>
        </div>
      </footer>
    </div>
  );
}
