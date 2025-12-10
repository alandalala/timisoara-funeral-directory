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
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Card className="max-w-md mx-4">
          <CardContent className="pt-6 text-center">
            <div className="text-6xl mb-4">✅</div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              Cerere Înregistrată
            </h2>
            <p className="text-gray-600 mb-4">
              Cererea dvs. de eliminare a fost înregistrată cu succes.
            </p>
            <p className="text-sm text-gray-500 mb-6">
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
        <div className="max-w-2xl mx-auto">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Solicitare Eliminare Date
          </h1>
          
          {/* GDPR Info Box */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-8">
            <h2 className="font-semibold text-blue-900 mb-2">
              🔒 Drepturile dvs. conform GDPR
            </h2>
            <p className="text-blue-800 text-sm">
              În conformitate cu Regulamentul General privind Protecția Datelor (GDPR), 
              aveți dreptul de a solicita ștergerea datelor dvs. personale sau ale firmei dvs. 
              din directorul nostru. Vom procesa cererea în maximum 30 de zile.
            </p>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>Formular de Solicitare</CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-6">
                {/* Company Info */}
                <div className="border-b pb-4 mb-4">
                  <h3 className="font-medium text-gray-900 mb-4">Informații Firmă</h3>
                  <div>
                    <label htmlFor="company_name" className="block text-sm font-medium text-gray-700 mb-1">
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
                    <p className="text-xs text-gray-500 mt-1">
                      Introduceți numele exact al firmei așa cum apare în director
                    </p>
                  </div>
                </div>

                {/* Requester Info */}
                <div className="border-b pb-4 mb-4">
                  <h3 className="font-medium text-gray-900 mb-4">Datele Solicitantului</h3>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                    <div>
                      <label htmlFor="requester_name" className="block text-sm font-medium text-gray-700 mb-1">
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
                      <label htmlFor="requester_email" className="block text-sm font-medium text-gray-700 mb-1">
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
                      <label htmlFor="requester_phone" className="block text-sm font-medium text-gray-700 mb-1">
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
                      <label htmlFor="relationship" className="block text-sm font-medium text-gray-700 mb-1">
                        Relația cu firma *
                      </label>
                      <select
                        id="relationship"
                        name="relationship"
                        required
                        value={formData.relationship}
                        onChange={handleChange}
                        className="w-full h-10 px-3 rounded-md border border-gray-300 bg-white text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
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
                  <label htmlFor="reason" className="block text-sm font-medium text-gray-700 mb-1">
                    Motivul solicitării *
                  </label>
                  <select
                    id="reason"
                    name="reason"
                    required
                    value={formData.reason}
                    onChange={handleChange}
                    className="w-full h-10 px-3 rounded-md border border-gray-300 bg-white text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500 mb-4"
                  >
                    <option value="">Selectează motivul</option>
                    <option value="business_closed">Firma nu mai există / S-a închis</option>
                    <option value="privacy">Nu doresc să fiu listat</option>
                    <option value="incorrect_data">Datele sunt incorecte și prefer eliminarea</option>
                    <option value="gdpr">Exercitare drept GDPR la ștergere</option>
                    <option value="other">Alt motiv</option>
                  </select>

                  <label htmlFor="additional_info" className="block text-sm font-medium text-gray-700 mb-1">
                    Informații suplimentare (opțional)
                  </label>
                  <textarea
                    id="additional_info"
                    name="additional_info"
                    rows={4}
                    value={formData.additional_info}
                    onChange={handleChange}
                    placeholder="Adăugați orice informații relevante pentru procesarea cererii..."
                    className="w-full px-3 py-2 rounded-md border border-gray-300 bg-white text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                  />
                </div>

                {/* Agreement */}
                <div className="bg-gray-50 p-4 rounded-lg">
                  <label className="flex items-start gap-3">
                    <input
                      type="checkbox"
                      required
                      className="mt-1"
                    />
                    <span className="text-sm text-gray-600">
                      Confirm că sunt autorizat să solicit eliminarea acestor date și că informațiile 
                      furnizate sunt corecte. Înțeleg că identitatea mea poate fi verificată înainte 
                      de procesarea cererii.
                    </span>
                  </label>
                </div>

                {error && (
                  <div className="p-3 bg-red-50 border border-red-200 rounded-md text-red-600 text-sm">
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
                      <svg className="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                      </svg>
                      Se procesează...
                    </>
                  ) : (
                    '📝 Trimite Solicitarea'
                  )}
                </Button>
              </form>
            </CardContent>
          </Card>

          {/* Additional Info */}
          <div className="mt-8 text-center text-sm text-gray-500">
            <p>
              Pentru alte întrebări, ne puteți contacta la{' '}
              <a href="mailto:contact@serviciifunerare.ro" className="text-blue-600 hover:text-blue-800">
                contact@serviciifunerare.ro
              </a>
            </p>
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
