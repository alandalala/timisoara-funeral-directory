import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

const baseUrl = process.env.NEXT_PUBLIC_BASE_URL || 'https://serviciifunerare.ro';

export const metadata: Metadata = {
  metadataBase: new URL(baseUrl),
  title: {
    default: "Servicii Funerare România | Director Național Firme Funerare",
    template: "%s | Servicii Funerare România",
  },
  description: "Găsește servicii funerare verificate în toată România. Director complet cu firme funerare, case mortuare, transport funerar și servicii complete de înmormântare în toate județele.",
  keywords: [
    "servicii funerare",
    "firme funerare",
    "pompe funebre",
    "casa mortuara",
    "transport funerar",
    "inmormantare",
    "servicii inmormantare",
    "Romania",
    "funerare non-stop",
    "sicrie",
    "servicii religioase",
  ],
  authors: [{ name: "Servicii Funerare România" }],
  creator: "Servicii Funerare România",
  publisher: "Servicii Funerare România",
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
  openGraph: {
    type: "website",
    locale: "ro_RO",
    url: "https://servicii-funerare.ro",
    siteName: "Servicii Funerare România",
    title: "Servicii Funerare România | Director Național Firme Funerare",
    description: "Găsește servicii funerare verificate în toată România. Director complet cu firme funerare în toate județele.",
    images: [
      {
        url: "/og-image.jpg",
        width: 1200,
        height: 630,
        alt: "Servicii Funerare România",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Servicii Funerare România | Director Național",
    description: "Găsește servicii funerare verificate în toată România.",
    images: ["/og-image.jpg"],
  },
  verification: {
    // Add your Google Search Console verification code here
    // google: "your-verification-code",
  },
  alternates: {
    canonical: "https://servicii-funerare.ro",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ro">
      <head>
        <link rel="icon" href="/favicon.ico" sizes="any" />
        <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
        <meta name="theme-color" content="#1e40af" />
      </head>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
