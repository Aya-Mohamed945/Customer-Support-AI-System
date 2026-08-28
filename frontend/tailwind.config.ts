import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['var(--font-jakarta)', 'sans-serif'],
        display: ['var(--font-space)', 'sans-serif'],
      },
      fontSize: {
        'xs': ['0.75rem', { lineHeight: '1rem' }],       // Label / Subtitle
        'sm': ['0.875rem', { lineHeight: '1.25rem' }],   // Body text / Inputs
        'base': ['1rem', { lineHeight: '1.5rem' }],      // Main Content
        'lg': ['1.125rem', { lineHeight: '1.75rem' }],   // Card Title
        'xl': ['1.25rem', { lineHeight: '1.75rem' }],    // Section Header
        '2xl': ['1.5rem', { lineHeight: '2rem' }],       // Modal Header
        '3xl': ['1.875rem', { lineHeight: '2.25rem' }], // Main Title
        '4xl': ['2.25rem', { lineHeight: '2.5rem' }],    // Hero Title
        '5xl': ['3rem', { lineHeight: '1.16' }],         // Large Hero Title
      },
      boxShadow: {
        'glass': '0 8px 32px 0 rgba(31, 38, 135, 0.37)',
        'glow-indigo': '0 0 30px rgba(79, 70, 229, 0.3)',
      }
    },
  },
  plugins: [],
};

export default config;