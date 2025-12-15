/** @type {import('tailwindcss').Config} */

// Medical Calculator Design System - Professional Medical Color Palette
// Color scheme optimized for healthcare applications with trust and professionalism
const colors = {
  // Medical Brand Colors - Trustworthy blues and healing greens
  primary: {
    DEFAULT: 'hsl(210, 100%, 50%)',    // Medical Blue - professional and trustworthy
    light: 'hsl(210, 100%, 92%)',      // Light blue backgrounds
    dark: 'hsl(210, 100%, 40%)',       // Dark blue for emphasis
  },
  secondary: {
    DEFAULT: 'hsl(145, 63%, 42%)',     // Medical Green - healing and health
    light: 'hsl(145, 63%, 90%)',       // Light green backgrounds
    dark: 'hsl(145, 63%, 32%)',        // Dark green for emphasis
  },
  accent: {
    DEFAULT: 'hsl(200, 80%, 55%)',     // Calming teal - modern medical feel
    light: 'hsl(200, 80%, 95%)',       // Very light teal
    dark: 'hsl(200, 80%, 40%)',        // Deep teal
  },

  // Text colors - optimized for medical readability
  text: {
    primary: 'hsl(210, 20%, 20%)',     // Dark blue-gray for main text
    secondary: 'hsl(210, 15%, 45%)',   // Medium blue-gray for descriptions
    muted: 'hsl(210, 10%, 65%)',       // Light gray for helper text
    inverse: 'hsl(0, 0%, 100%)',       // White text for colored backgrounds
  },

  // Surface colors - clean clinical whites and soft grays
  surface: {
    DEFAULT: 'hsl(0, 0%, 100%)',       // Pure white - clean clinical feel
    elevated: 'hsl(210, 40%, 98%)',    // Very subtle blue-tinted white for cards
    secondary: 'hsl(210, 30%, 96%)',   // Light blue-gray background
  },
  border: 'hsl(210, 20%, 88%)',        // Soft blue-gray borders

  // Neutral colors
  neutral: {
    DEFAULT: 'hsl(210, 10%, 65%)',
    light: 'hsl(210, 10%, 85%)',
    dark: 'hsl(210, 10%, 45%)',
  },

  // Clinical Status Colors - Medical interpretation standards
  success: {
    DEFAULT: 'hsl(145, 63%, 42%)',     // Healthy/Normal green
    bg: 'hsl(145, 63%, 95%)',          // Light green background
    text: 'hsl(145, 63%, 32%)',        // Dark green text
  },
  warning: {
    DEFAULT: 'hsl(38, 92%, 50%)',      // Caution/Borderline orange
    bg: 'hsl(38, 92%, 95%)',           // Light orange background
    text: 'hsl(38, 92%, 35%)',         // Dark orange text
  },
  danger: {
    DEFAULT: 'hsl(0, 84%, 55%)',       // Critical/Abnormal red
    bg: 'hsl(0, 84%, 96%)',            // Light red background
    text: 'hsl(0, 84%, 40%)',          // Dark red text
  },
  info: {
    DEFAULT: 'hsl(210, 100%, 50%)',    // Information blue
    bg: 'hsl(210, 100%, 95%)',         // Light blue background
    text: 'hsl(210, 100%, 35%)',       // Dark blue text
  },
};

module.exports = {
  content: [
    "./App.{js,jsx,ts,tsx}",
    "./app/**/*.{js,jsx,ts,tsx}",
    "./components/**/*.{js,jsx,ts,tsx}",
    "./config/**/*.{js,jsx,ts,tsx}",
    "./utils/**/*.{js,jsx,ts,tsx}",
  ],
  darkMode: 'class',
  presets: [require("nativewind/preset")],
  theme: {
    extend: {
      /*
       * Design System - Semantic Color Tokens
       *
       * Usage:
       * - Text: text-text-primary, text-text-secondary, text-text-muted
       * - Surface: bg-surface, bg-surface-elevated
       * - Brand: bg-primary, bg-secondary, bg-primary-light, bg-primary-dark
       * - Status: bg-success, bg-warning, bg-danger, bg-info
       * - Borders: border-border
       *
       * ⚠️ NEVER use direct colors: text-white, bg-white, text-black, bg-black
       * ⚠️ Use semantic tokens only for maintainability and theme consistency
       */
      colors: colors,

      // Aliases for AI's common mistake: bg-bg-primary -> bg-primary
      backgroundColor: {
        'bg-primary': colors.primary.DEFAULT,
        'bg-primary-light': colors.primary.light,
        'bg-primary-dark': colors.primary.dark,
        'bg-secondary': colors.secondary.DEFAULT,
        'bg-secondary-light': colors.secondary.light,
        'bg-secondary-dark': colors.secondary.dark,
        'bg-surface': colors.surface.DEFAULT,
        'bg-surface-elevated': colors.surface.elevated,
        'bg-danger': colors.danger.DEFAULT,
        'bg-warning': colors.warning.DEFAULT,
        'bg-success': colors.success.DEFAULT,
        'bg-info': colors.info.DEFAULT,
      },

      // Aliases for AI's common mistake: text-text-primary -> text-text-primary
      textColor: {
        'text-primary': colors.text.primary,
        'text-secondary': colors.text.secondary,
        'text-muted': colors.text.muted,
        'text-inverse': colors.text.inverse,
      },

      // Border aliases
      borderColor: {
        'border-border': colors.border,
      },
    },
  },
  plugins: [],
}
