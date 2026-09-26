/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        teal: {
          light: '#e0f2f1',
          DEFAULT: '#008080',
          dark: '#005E5E',
        },
        slate: {
          DEFAULT: '#2F4F4F',
        }
      },
    },
  },
  plugins: [],
};  
