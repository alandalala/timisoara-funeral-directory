'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export default function ContactPage() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: '',
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError('');

    // Simulate form submission (you can connect to an API later)
    try {
      await new Promise((resolve) => setTimeout(resolve, 1000));
      setSubmitted(true);
    } catch {
      setError('A apărut o eroare. Vă rugăm încercați din nou.');
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
            <div className="text-6xl mb-4">✅</div>
            <h2 className="text-2xl font-heading text-charcoal mb-2">
              Mesaj Trimis!
            </h2>
            <p className="text-slate mb-6">
              Vă mulțumim pentru mesaj. Vom răspunde în cel mai scurt timp posibil.
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
        <div className="max-w-2xl mx-auto animate-fade-in">
          <h1 className="text-4xl font-heading text-charcoal mb-4">
            Contact
          </h1>
          <p className="text-slate mb-8">
            Aveți întrebări sau sugestii? Completați formularul de mai jos și vă vom răspunde cât mai curând.
          </p>

          <Card className="bg-white border-warm-grey rounded-2xl shadow-soft">
            <CardHeader>
              <CardTitle className="font-heading text-charcoal">Trimite un mesaj</CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label htmlFor="name" className="block text-sm font-medium text-charcoal mb-2">
                      Nume complet *
                    </label>
                    <Input
                      id="name"
                      name="name"
                      type="text"
                      required
                      value={formData.name}
                      onChange={handleChange}
                      placeholder="Ion Popescu"
                    />
                  </div>
                  <div>
                    <label htmlFor="email" className="block text-sm font-medium text-charcoal mb-2">
                      Email *
                    </label>
                    <Input
                      id="email"
                      name="email"
                      type="email"
                      required
                      value={formData.email}
                      onChange={handleChange}
                      placeholder="ion@example.com"
                    />
                  </div>
                </div>

                <div>
                  <label htmlFor="subject" className="block text-sm font-medium text-charcoal mb-2">
                    Subiect *
                  </label>
                  <select
                    id="subject"
                    name="subject"
                    required
                    value={formData.subject}
                    onChange={handleChange}
                    className="w-full h-11 px-4 rounded-xl border border-[var(--warm-grey)] bg-white text-charcoal input-glow"
                  >
                    <option value="">Selectează subiectul</option>
                    <option value="general">Întrebare generală</option>
                    <option value="add_company">Adăugare firmă nouă</option>
                    <option value="update_info">Actualizare informații</option>
                    <option value="report_error">Raportare eroare</option>
                    <option value="partnership">Parteneriat</option>
                    <option value="other">Altele</option>
                  </select>
                </div>

                <div>
                  <label htmlFor="message" className="block text-sm font-medium text-charcoal mb-2">
                    Mesaj *
                  </label>
                  <textarea
                    id="message"
                    name="message"
                    required
                    rows={5}
                    value={formData.message}
                    onChange={handleChange}
                    placeholder="Scrieți mesajul dvs. aici..."
                    className="w-full px-4 py-3 rounded-xl border border-[var(--warm-grey)] bg-white text-charcoal resize-none input-glow"
                  />
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
                      Se trimite...
                    </>
                  ) : (
                    '📧 Trimite Mesajul'
                  )}
                </Button>
              </form>
            </CardContent>
          </Card>

          {/* Alternative Contact */}
          <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card className="bg-white border-warm-grey rounded-2xl shadow-soft">
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="text-3xl mb-2">📧</div>
                  <h3 className="font-heading text-charcoal mb-1">Email</h3>
                  <a
                    href="mailto:contact@serviciifunerare.ro"
                    className="text-navy link-animated"
                  >
                    contact@serviciifunerare.ro
                  </a>
                </div>
              </CardContent>
            </Card>
            <Card className="bg-white border-warm-grey rounded-2xl shadow-soft">
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="text-3xl mb-2">🕐</div>
                  <h3 className="font-heading text-charcoal mb-1">Timp de răspuns</h3>
                  <p className="text-slate">24-48 ore lucrătoare</p>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-warm-grey py-10 mt-16">
        <div className="container mx-auto px-4 text-center">
          <p className="text-slate">
            © 2025 Servicii Funerare România. Toate drepturile rezervate.
          </p>
        </div>
      </footer>
    </div>
  );
}
