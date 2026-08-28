// frontend/app/layout.tsx

import type { Metadata, Viewport } from 'next';
import { Plus_Jakarta_Sans, Inter } from 'next/font/google';
import './globals.css';

const jakarta = Plus_Jakarta_Sans({
  subsets: ['latin'],
  variable: '--font-jakarta',
  display: 'swap',
  weight: ['400', '500', '600', '700', '800'],
});

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
  weight: ['400', '500', '600'],
});

export const metadata: Metadata = {
  title: 'SupportAI | Intelligent Customer Support',
  description: 'AI-powered ticket classification, sentiment analysis, and smart solutions for modern customer support teams.',
  keywords: 'AI customer support, ticket classification, sentiment analysis, RAG, support automation',
  authors: [{ name: 'SupportAI Team' }],
  openGraph: {
    title: 'SupportAI | Intelligent Customer Support',
    description: 'AI-powered ticket classification and smart solutions',
    type: 'website',
    url: 'https://supportai.dev',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'SupportAI | Intelligent Customer Support',
    description: 'AI-powered ticket classification and smart solutions',
  },
};

export const viewport: Viewport = {
  themeColor: '#0F172A',
  width: 'device-width',
  initialScale: 1,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${jakarta.variable} ${inter.variable}`}>
      <body>
        {/* ============================================
            ANIMATED BACKGROUND
            ============================================ */}
        <div className="bg-layer" aria-hidden="true">
          <div className="bg-gradient" />
          <div className="bg-overlay" />
          <div className="orb orb-1" />
          <div className="orb orb-2" />
          <div className="orb orb-3" />
          <div className="orb orb-4" />
          <div className="orb orb-5" />
        </div>

        {/* ============================================
            MAIN CONTENT
            ============================================ */}
        <main className="relative z-10 min-h-screen">
          {children}
        </main>
      </body>
    </html>
  );
}