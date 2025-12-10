import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Solicitare Eliminare Date (GDPR)',
  description: 'Solicitați eliminarea datelor firmei dvs. din directorul de servicii funerare. Conform GDPR, procesăm cererile în maximum 30 de zile.',
};

export default function EliminareLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return children;
}
