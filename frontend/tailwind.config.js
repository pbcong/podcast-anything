/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      typography: {
        DEFAULT: {
          css: {
            maxWidth: "none",
            color: "inherit",
            p: {
              color: "inherit",
            },
            strong: {
              color: "inherit",
            },
            a: {
              color: "#3b82f6",
              "&:hover": {
                color: "#2563eb",
              },
            },
            code: {
              color: "inherit",
              backgroundColor: "#f3f4f6",
              padding: "2px 4px",
              borderRadius: "3px",
            },
            "code::before": {
              content: '""',
            },
            "code::after": {
              content: '""',
            },
          },
        },
      },
    },
  },
  plugins: [require("@tailwindcss/typography")],
};
