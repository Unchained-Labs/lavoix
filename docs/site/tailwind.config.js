/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        rust: {
          bg: '#1b1411',
          panel: '#2a1f1a',
          panelSoft: '#352821',
          border: '#654737',
          text: '#f7ece3',
          muted: '#d2b8a5',
          accent: '#d97736',
          accentSoft: '#f3b98c',
        },
      },
      boxShadow: {
        glow: '0 0 0 1px rgba(217,119,54,0.22), 0 14px 34px rgba(0,0,0,0.35)',
      },
    },
  },
  plugins: [],
}

