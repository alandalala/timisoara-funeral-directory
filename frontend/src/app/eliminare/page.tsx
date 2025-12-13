'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export default function RemovalRequestPage() {
  const [formData, setFormData] = useState({
    company_name: '',
    requester_name: '',
    requester_email: '',
    requester_phone: '',
    relationship: '',
    reason: '',
    additional_info: '',
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError('');

    try {
      const response = await fetch('/api/removal-request', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'A apărut o eroare');
      }

      setSubmitted(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'A apărut o eroare. Vă rugăm încercați din nou.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  if (submitted) {
    return (
      <div className="min-h-screen bg-cream flex items-center justify-center">
        <Card className="max-w-md mx-4 bg-white border-warm-grey rounded-2xl shadow-soft animate-fade-in">
          <CardContent className="pt-8 text-center">
            <div className="mb-4" aria-hidden="true"><svg className="w-16 h-16 mx-auto text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="1.5"><path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg></div>
            <h2 className="text-2xl font-heading text-charcoal mb-2">
              Cerere Înregistrată
            </h2>
            <p className="text-slate mb-4">
              Cererea dvs. de eliminare a fost înregistrată cu succes.
            </p>
            <p className="text-sm text-slate/80 mb-6">
              În conformitate cu GDPR, cererea va fi procesată în maximum 30 de zile. 
              Veți primi o confirmare pe email când procesarea este completă.
            </p>
            <Link href="/">
              <Button>← Înapoi la pagina principală</Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-cream">
      {/* Header */}
      <header className="bg-white border-b border-warm-grey" role="banner">
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
              aria-hidden="true"
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
      <main id="main-content" className="container mx-auto px-4 py-12" role="main">
        <div className="max-w-2xl mx-auto animate-fade-in">
          <h1 className="text-4xl font-heading text-charcoal mb-4">
            Solicitare Eliminare Date
          </h1>
          
          {/* GDPR Info Box */}
          <div className="bg-navy/5 border border-navy/10 rounded-2xl p-5 mb-8">
            <h2 className="font-heading text-charcoal mb-2">
              🔒 Drepturile dvs. conform GDPR
            </h2>
            <p className="text-slate text-sm">
              În conformitate cu Regulamentul General privind Protecția Datelor (GDPR), 
              aveți dreptul de a solicita ștergerea datelor dvs. personale sau ale firmei dvs. 
              din directorul nostru. Vom procesa cererea în maximum 30 de zile.
            </p>
          </div>

          <Card className="bg-white border-warm-grey rounded-2xl shadow-soft">
            <CardHeader>
              <CardTitle className="font-heading text-charcoal">Formular de Solicitare</CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-6">
                {/* Company Info */}
                <div className="border-b border-warm-grey pb-4 mb-4">
                  <h3 className="font-medium text-charcoal mb-4">Informații Firmă</h3>
                  <div>
                    <label htmlFor="company_name" className="block text-sm font-medium text-charcoal mb-2">
                      Denumirea Firmei *
                    </label>
                    <Input
                      id="company_name"
                      name="company_name"
                      type="text"
                      required
                      value={formData.company_name}
                      onChange={handleChange}
                      placeholder="Ex: Servicii Funerare Example SRL"
                    />
                    <p className="text-xs text-slate/70 mt-1">
                      Introduceți numele exact al firmei așa cum apare în director
                    </p>
                  </div>
                </div>

                {/* Requester Info */}
                <div className="border-b border-warm-grey pb-4 mb-4">
                  <h3 className="font-medium text-charcoal mb-4">Datele Solicitantului</h3>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                    <div>
                      <label htmlFor="requester_name" className="block text-sm font-medium text-charcoal mb-2">
                        Nume și Prenume *
                      </label>
                      <Input
                        id="requester_name"
                        name="requester_name"
                        type="text"
                        required
                        value={formData.requester_name}
                        onChange={handleChange}
                        placeholder="Ion Popescu"
                      />
                    </div>
                    <div>
                      <label htmlFor="requester_email" className="block text-sm font-medium text-charcoal mb-2">
                        Email *
                      </label>
                      <Input
                        id="requester_email"
                        name="requester_email"
                        type="email"
                        required
                        value={formData.requester_email}
                        onChange={handleChange}
                        placeholder="ion@example.com"
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label htmlFor="requester_phone" className="block text-sm font-medium text-charcoal mb-2">
                        Telefon (opțional)
                      </label>
                      <Input
                        id="requester_phone"
                        name="requester_phone"
                        type="tel"
                        value={formData.requester_phone}
                        onChange={handleChange}
                        placeholder="07XX XXX XXX"
                      />
                    </div>
                    <div>
                      <label htmlFor="relationship" className="block text-sm font-medium text-charcoal mb-2">
                        Relația cu firma *
                      </label>
                      <select
                        id="relationship"
                        name="relationship"
                        required
                        value={formData.relationship}
                        onChange={handleChange}
                        className="w-full h-11 px-4 rounded-xl border border-[var(--warm-grey)] bg-white text-charcoal input-glow"
                      >
                        <option value="">Selectează</option>
                        <option value="owner">Proprietar / Administrator</option>
                        <option value="employee">Angajat</option>
                        <option value="legal_representative">Reprezentant Legal</option>
                        <option value="other">Altul</option>
                      </select>
                    </div>
                  </div>
                </div>

                {/* Reason */}
                <div>
                  <label htmlFor="reason" className="block text-sm font-medium text-charcoal mb-2">
                    Motivul solicitării *
                  </label>
                  <select
                    id="reason"
                    name="reason"
                    required
                    value={formData.reason}
                    onChange={handleChange}
                    className="w-full h-11 px-4 rounded-xl border border-[var(--warm-grey)] bg-white text-charcoal input-glow mb-4"
                  >
                    <option value="">Selectează motivul</option>
                    <option value="business_closed">Firma nu mai există / S-a închis</option>
                    <option value="privacy">Nu doresc să fiu listat</option>
                    <option value="incorrect_data">Datele sunt incorecte și prefer eliminarea</option>
                    <option value="gdpr">Exercitare drept GDPR la ștergere</option>
                    <option value="other">Alt motiv</option>
                  </select>

                  <label htmlFor="additional_info" className="block text-sm font-medium text-charcoal mb-2">
                    Informații suplimentare (opțional)
                  </label>
                  <textarea
                    id="additional_info"
                    name="additional_info"
                    rows={4}
                    value={formData.additional_info}
                    onChange={handleChange}
                    placeholder="Adăugați orice informații relevante pentru procesarea cererii..."
                    className="w-full px-4 py-3 rounded-xl border border-[var(--warm-grey)] bg-white text-charcoal resize-none input-glow"
                  />
                </div>

                {/* Agreement */}
                <div className="bg-cream p-5 rounded-xl">
                  <label className="flex items-start gap-3">
                    <input
                      type="checkbox"
                      required
                      className="mt-1 w-4 h-4 rounded border-warm-grey text-navy focus:ring-navy/20"
                    />
                    <span className="text-sm text-slate">
                      Confirm că sunt autorizat să solicit eliminarea acestor date și că informațiile 
                      furnizate sunt corecte. Înțeleg că identitatea mea poate fi verificată înainte 
                      de procesarea cererii.
                    </span>
                  </label>
                </div>

                {error && (
                  <div className="p-4 bg-rose/10 border border-rose/30 rounded-xl text-rose text-sm">
                    {error}
                  </div>
                )}

                <Button
                  type="submit"
                  className="w-full"
                  disabled={isSubmitting}
                >
                  {isSubmitting ? (
                    <>
                      <span className="spinner mr-2" />
                      Se procesează...
                    </>
                  ) : (
                    <><svg className="w-4 h-4 mr-2 inline" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2"><path strokeLinecap="round" strokeLinejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10"/></svg>Trimite Solicitarea</>
                  )}
                </Button>
              </form>
            </CardContent>
          </Card>

          {/* Additional Info */}
          <div className="mt-8 text-center text-sm text-slate">
            <p>
              Pentru alte întrebări, ne puteți contacta la{' '}
              <a href="mailto:contact@cautarefunerare.ro" className="text-navy link-animated">
                contact@cautarefunerare.ro
              </a>
            </p>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-warm-grey py-10 mt-16" role="contentinfo">
        <div className="container mx-auto px-4 text-center">
          <p className="text-slate">
            © 2025 CautareFunerare.ro. Toate drepturile rezervate.
          </p>
        </div>
      </footer>
    </div>
  );
}
