import { Metadata } from 'next';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'Despre Noi',
  description: 'Despre directorul de servicii funerare din România. Misiunea noastră este să ajutăm familiile să găsească servicii funerare de încredere în momentele dificile.',
};

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-cream">
      {/* Header */}
      <header className="bg-white border-b border-warm-grey">
        <div className="container mx-auto px-4 py-4">
          <Link
            href="/"
            className="inline-flex items-center text-slate link-animated"
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
        <div className="max-w-3xl mx-auto animate-fade-in">
          <h1 className="text-4xl font-heading text-charcoal mb-8">
            Despre Servicii Funerare România
          </h1>

          <div className="prose prose-lg max-w-none">
            <section className="mb-10">
              <h2 className="text-2xl font-heading text-charcoal mb-4">
                Misiunea Noastră
              </h2>
              <p className="text-slate leading-relaxed mb-4">
                Servicii Funerare România este un director online dedicat ajutorării familiilor 
                în momentele dificile. Înțelegem că pierderea unei persoane dragi este una dintre 
                cele mai grele experiențe, iar găsirea rapidă a serviciilor funerare potrivite 
                nu ar trebui să fie o povară suplimentară.
              </p>
              <p className="text-slate leading-relaxed">
                Misiunea noastră este să oferim acces facil la informații verificate despre 
                firmele de servicii funerare din toată România, astfel încât să puteți lua 
                decizii informate în momente când timpul și claritatea sunt esențiale.
              </p>
            </section>

            <section className="mb-10">
              <h2 className="text-2xl font-heading text-charcoal mb-4">
                Ce Oferim
              </h2>
              <ul className="space-y-3 text-slate">
                <li className="flex items-start">
                  <span className="text-sage mr-3 mt-1">✓</span>
                  <span><strong className="text-charcoal">Director Complet:</strong> Acoperire în toate cele 41 de județe ale României plus București</span>
                </li>
                <li className="flex items-start">
                  <span className="text-sage mr-3 mt-1">✓</span>
                  <span><strong className="text-charcoal">Informații Verificate:</strong> Date de contact actualizate și verificate</span>
                </li>
                <li className="flex items-start">
                  <span className="text-sage mr-3 mt-1">✓</span>
                  <span><strong className="text-charcoal">Căutare Rapidă:</strong> Filtrare după județ, oraș și tipuri de servicii</span>
                </li>
                <li className="flex items-start">
                  <span className="text-sage mr-3 mt-1">✓</span>
                  <span><strong className="text-charcoal">Servicii Non-Stop:</strong> Identificare rapidă a firmelor disponibile 24/7</span>
                </li>
                <li className="flex items-start">
                  <span className="text-sage mr-3 mt-1">✓</span>
                  <span><strong className="text-charcoal">Hartă Interactivă:</strong> Vizualizare pe hartă pentru a găsi servicii în apropiere</span>
                </li>
                <li className="flex items-start">
                  <span className="text-sage mr-3 mt-1">✓</span>
                  <span><strong className="text-charcoal">Acces Gratuit:</strong> Toate informațiile sunt disponibile gratuit</span>
                </li>
              </ul>
            </section>

            <section className="mb-10">
              <h2 className="text-2xl font-heading text-charcoal mb-4">
                Tipuri de Servicii
              </h2>
              <p className="text-slate leading-relaxed mb-4">
                În directorul nostru puteți găsi firme care oferă o gamă completă de servicii funerare:
              </p>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 text-slate">
                <div className="bg-white p-4 rounded-xl border border-warm-grey shadow-soft">Acte și Formalități</div>
                <div className="bg-white p-4 rounded-xl border border-warm-grey shadow-soft">Transport Funerar</div>
                <div className="bg-white p-4 rounded-xl border border-warm-grey shadow-soft">Sicrie și Urne</div>
                <div className="bg-white p-4 rounded-xl border border-warm-grey shadow-soft">Capelă / Cameră Mortuară</div>
                <div className="bg-white p-4 rounded-xl border border-warm-grey shadow-soft">Coroane și Aranjamente Florale</div>
                <div className="bg-white p-4 rounded-xl border border-warm-grey shadow-soft">Servicii Religioase</div>
                <div className="bg-white p-4 rounded-xl border border-warm-grey shadow-soft">Incinerare</div>
                <div className="bg-white p-4 rounded-xl border border-warm-grey shadow-soft">Monumente Funerare</div>
                <div className="bg-white p-4 rounded-xl border border-warm-grey shadow-soft">Repatriere Internațională</div>
              </div>
            </section>

            <section className="mb-10">
              <h2 className="text-2xl font-heading text-charcoal mb-4">
                Confidențialitate și GDPR
              </h2>
              <p className="text-slate leading-relaxed mb-4">
                Respectăm confidențialitatea tuturor utilizatorilor și ne conformăm 
                Regulamentului General privind Protecția Datelor (GDPR). Nu colectăm 
                date personale fără consimțământ și nu partajăm informații cu terțe părți.
              </p>
              <p className="text-slate leading-relaxed">
                Dacă sunteți proprietarul unei firme listate și doriți actualizarea sau 
                eliminarea informațiilor, vă rugăm să ne contactați prin{' '}
                <Link href="/eliminare" className="text-navy link-animated">
                  formularul de solicitare
                </Link>.
              </p>
            </section>

            <section className="bg-navy/5 p-6 rounded-2xl border border-navy/10">
              <h2 className="text-2xl font-heading text-charcoal mb-4">
                Contact
              </h2>
              <p className="text-slate mb-4">
                Pentru întrebări, sugestii sau solicitări, ne puteți contacta:
              </p>
              <div className="space-y-2">
                <p className="text-slate">
                  <span className="inline-flex items-center"><svg className="w-4 h-4 mr-2 text-navy" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="1.5"><path strokeLinecap="round" strokeLinejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75"/></svg>Email:</span> <a href="mailto:contact@cautarefunerare.ro" className="text-navy link-animated">contact@cautarefunerare.ro</a>
                </p>
                <p className="text-slate inline-flex items-center">
                  <svg className="w-4 h-4 mr-2 text-navy" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="1.5"><path strokeLinecap="round" strokeLinejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10"/></svg>
                  <Link href="/contact" className="text-navy link-animated">Formular de contact</Link>
                </p>
              </div>
            </section>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-warm-grey py-10 mt-16">
        <div className="container mx-auto px-4 text-center">
          <p className="text-slate">
            © 2025 CautareFunerare.ro. Toate drepturile rezervate.
          </p>
        </div>
      </footer>
    </div>
  );
}
