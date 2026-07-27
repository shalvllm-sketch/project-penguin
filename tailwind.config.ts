import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: {
          DEFAULT: "#2e1a24",
          soft: "#6a4d58",
          mute: "#a08890",
        },
        rose: {
          DEFAULT: "#a85f76",
          deep: "#7a3f56",
          soft: "#d6a8b4",
          wash: "#f2dee2",
        },
        terracotta: "#b57559",
        gold: "#a88a52",
        ivory: "#f6efe6",
        cream: "#f0e6d8",
        paper: "#fbf6ee",
      },
      fontFamily: {
        serif: ["Fraunces", "Cormorant Garamond", "Georgia", "serif"],
        sans: ["Inter", "system-ui", "sans-serif"],
      },
      letterSpacing: {
        wider2: "0.24em",
        widest2: "0.32em",
      },
      boxShadow: {
        soft: "0 1px 2px rgba(46,26,36,0.04), 0 8px 24px -12px rgba(46,26,36,0.12)",
        lift: "0 2px 8px rgba(46,26,36,0.06), 0 20px 48px -18px rgba(46,26,36,0.18)",
      },
    },
  },
  plugins: [],
};
export default config;
