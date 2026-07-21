import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Platform branding colors
        brand: {
          dark: '#0B0F19',
          light: '#F8FAFC',
          cardDark: '#1E293B',
          cardLight: '#FFFFFF',
        },
        // Five core developmental sector colors
        sector: {
          academic: '#2563EB',      // Sapphire Blue
          professional: '#059669',  // Emerald Green
          entrepreneurial: '#D97706',// Gold/Orange
          socialImpact: '#7C3AED',   // Amethyst Purple
          personal: '#E11D48',       // Crimson Rose
        }
      },
      fontFamily: {
        sans: ['var(--font-inter)', 'sans-serif'],
      },
    },
  },
  plugins: [],
}

export default config
