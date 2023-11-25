/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.htm", "./src/**/*.{vue,html,js}"],
  prefix: "tw-",
  theme: {
    extend: {
      colors: {
        primary: "#8c2d19",
        secondary: "#3b5249",
      },
      textColors: {
        primary: "#8c2d19",
        secondary: "#3b5249",
      },
    },
  },
  plugins: [],
  safelist: [
    {
      pattern:
        /(bg|text|border)-(transparent|current|white|purple|midnight|metal|tahiti|silver|bermuda)/,
    },
  ],
};
