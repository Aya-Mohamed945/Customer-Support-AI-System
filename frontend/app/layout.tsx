// frontend/app/layout.tsx
import type { Metadata, Viewport } from 'next';
import { Plus_Jakarta_Sans, Inter } from 'next/font/google';
import './globals.css';

const jakarta = Plus_Jakarta_Sans({
  subsets: ['latin'],
  variable: '--font-jakarta',
  display: 'swap',
});

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
});

export const metadata: Metadata = {
  title: 'Customer Support AI',
  description: 'AI-Powered Ticket Classification & Solution System',
};

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${jakarta.variable} ${inter.variable}`}data-scroll-behavior="smooth">
      <body className="font-sans antialiased text-slate-100 bg-[#0b0f19] min-h-screen relative">
        {/* ✅ Background Layer - Global for all pages */}
        <div className="bg-layer">
          <div className="bg-gradient"></div>
          <div className="bg-overlay"></div>
          <div className="orb orb-1"></div>
          <div className="orb orb-2"></div>
          <div className="orb orb-3"></div>
          <div className="orb orb-4"></div>
          <div className="orb orb-5"></div>
        </div>

        {/* ✅ Content with relative z-index */}
        <div className="relative z-10">
          {children}
        </div>
      </body>
    </html>
  );
}
