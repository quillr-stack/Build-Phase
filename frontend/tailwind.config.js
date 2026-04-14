/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        sattva: {
          cream: '#F2EDE3',
          navy: '#0D2240',
          'navy-mid': '#1B3A6B',
          'navy-light': '#4A7AB5',
          green: '#2D7A4F',
          amber: '#C8961A',
          grid: '#C8BFB0',
          white: '#FFFFFF',
          muted: '#8A8070',
        },
      },
      fontFamily: {
        display: ['Space Grotesk', 'sans-serif'],
        body: ['Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
    },
  },
  plugins: [],
}
