/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.htm", "./src/**/*.{vue,html,js}"],
  prefix: "tw-",
  theme: {
    extend: {
      colors: {
        primary: "#8c2d19",
        secondary: {
          DEFAULT: "#2a3c24",
          light: "#566551"
        },
        background: "#fff1de"
      },
      textColors: {
        primary: "#8c2d19",
        secondary: {
          DEFAULT: "#2a3c24",
          light: "#566551"
        },
      },
    },
  },
  plugins: [],
  safelist: [
    {
      pattern:
        /(bg|text|border)-(background|transparent|current|white|purple|midnight|metal|tahiti|silver|bermuda)/,
    },
  ],
};
