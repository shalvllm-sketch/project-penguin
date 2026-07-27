import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        peach: {
          50: "#fff7f3",
          100: "#ffe9df",
          200: "#ffd0bd",
          300: "#ffb198",
          400: "#ff8a6c",
        },
        blush: {
          50: "#fff5f8",
          100: "#ffe4ed",
          200: "#ffc4d6",
          300: "#ff9dbc",
          400: "#f970a2",
        },
        cream: "#fffaf5",
      },
      fontFamily: {
        serif: ["'Cormorant Garamond'", "Georgia", "serif"],
        sans: ["'Nunito'", "system-ui", "sans-serif"],
      },
      animation: {
        float: "float 8s ease-in-out infinite",
        "float-slow": "float 14s ease-in-out infinite",
        "fade-in": "fadeIn 0.6s ease-out both",
        "pop-in": "popIn 0.35s cubic-bezier(0.22, 1.4, 0.36, 1) both",
      },
      keyframes: {
        float: {
          "0%": { transform: "translateY(100vh) scale(0.6)", opacity: "0" },
          "10%": { opacity: "0.9" },
          "100%": { transform: "translateY(-10vh) scale(1.1)", opacity: "0" },
        },
        fadeIn: {
          from: { opacity: "0", transform: "translateY(10px)" },
          to: { opacity: "1", transform: "translateY(0)" },
        },
        popIn: {
          from: { opacity: "0", transform: "scale(0.85)" },
          to: { opacity: "1", transform: "scale(1)" },
        },
      },
    },
  },
  plugins: [],
};
export default config;
