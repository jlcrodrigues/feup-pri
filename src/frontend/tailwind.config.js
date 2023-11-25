/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.htm", "./src/**/*.{vue,html,js}"],
    theme: {
    fontFamily: {
      sans: ['Graphik', 'sans-serif'],
      serif: ['Merriweather', 'serif'],
    },
    extend: {
      colors: {
        'primary': '#f00',
      },
      textColors: {
        'primary': '#f00',
      },
    }
  },
  plugins: [],
}

