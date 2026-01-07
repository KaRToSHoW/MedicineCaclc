/** @type {import('tailwindcss').Config} */

// Professional Medical Design System
// Clean, trustworthy, and calming color palette optimized for healthcare professionals
const colors = {
  // Primary - Medical Blue (trust, professionalism, calm)
  primary: {
    DEFAULT: 'hsl(210, 75%, 45%)',      // Deep medical blue
    light: 'hsl(210, 75%, 96%)',        // Very light blue for backgrounds
    dark: 'hsl(210, 75%, 32%)',         // Dark blue for emphasis
    50: 'hsl(210, 75%, 98%)',
    100: 'hsl(210, 75%, 96%)',
    200: 'hsl(210, 75%, 88%)',
    300: 'hsl(210, 75%, 72%)',
    400: 'hsl(210, 75%, 58%)',
    500: 'hsl(210, 75%, 45%)',
    600: 'hsl(210, 75%, 38%)',
    700: 'hsl(210, 75%, 32%)',
    800: 'hsl(210, 75%, 24%)',
    900: 'hsl(210, 75%, 18%)',
  },
  
  // Secondary - Teal (healthcare, healing, balance)
  secondary: {
    DEFAULT: 'hsl(175, 60%, 40%)',      // Professional teal
    light: 'hsl(175, 60%, 95%)',        // Light teal backgrounds
    dark: 'hsl(175, 60%, 28%)',         // Dark teal
  },

  // Accent - Soft Purple (premium, care)
  accent: {
    DEFAULT: 'hsl(250, 45%, 50%)',      // Muted professional purple
    light: 'hsl(250, 45%, 96%)',        // Very light purple
    dark: 'hsl(250, 45%, 35%)',         // Deep purple
  },

  // Text colors - Professional and readable
  text: {
    primary: 'hsl(210, 30%, 18%)',      // Dark blue-gray (main text)
    secondary: 'hsl(210, 20%, 45%)',    // Medium gray-blue (secondary text)
    muted: 'hsl(210, 15%, 65%)',        // Light gray (labels, hints)
    inverse: 'hsl(0, 0%, 100%)',        // Pure white (on dark backgrounds)
  },

  // Surface colors - Clean and professional
  surface: {
    DEFAULT: 'hsl(0, 0%, 100%)',        // Pure white
    elevated: 'hsl(210, 40%, 98%)',     // Subtle blue-white for cards
    secondary: 'hsl(210, 35%, 96%)',    // Light gray-blue background
    hover: 'hsl(210, 35%, 94%)',        // Hover state
  },
  
  border: 'hsl(210, 25%, 88%)',         // Soft gray-blue borders

  // Neutral grays - Professional palette
  neutral: {
    DEFAULT: 'hsl(210, 15%, 60%)',
    light: 'hsl(210, 15%, 85%)',
    dark: 'hsl(210, 15%, 40%)',
  },

  // Status colors - Clinical standards (calm and clear)
  success: {
    DEFAULT: 'hsl(145, 55%, 42%)',      // Professional green
    bg: 'hsl(145, 55%, 96%)',           // Light green background
    text: 'hsl(145, 55%, 28%)',         // Dark green text
    border: 'hsl(145, 55%, 85%)',       // Green border
  },
  
  warning: {
    DEFAULT: 'hsl(35, 85%, 50%)',       // Professional amber
    bg: 'hsl(35, 85%, 96%)',            // Light amber background
    text: 'hsl(35, 85%, 32%)',          // Dark amber text
    border: 'hsl(35, 85%, 85%)',        // Amber border
  },
  
  danger: {
    DEFAULT: 'hsl(355, 70%, 52%)',      // Professional red
    bg: 'hsl(355, 70%, 97%)',           // Light red background
    text: 'hsl(355, 70%, 35%)',         // Dark red text
    border: 'hsl(355, 70%, 88%)',       // Red border
  },
  
  info: {
    DEFAULT: 'hsl(205, 85%, 48%)',      // Professional blue
    bg: 'hsl(205, 85%, 96%)',           // Light blue background
    text: 'hsl(205, 85%, 30%)',         // Dark blue text
    border: 'hsl(205, 85%, 85%)',       // Blue border
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
       * Professional Medical Design System - Semantic Color Tokens
       *
       * Usage Examples:
       * - Text: text-text-primary, text-text-secondary, text-text-muted, text-text-inverse
       * - Surfaces: bg-surface, bg-surface-elevated, bg-surface-secondary, bg-surface-hover
       * - Brand: bg-primary, bg-secondary, bg-accent, bg-primary-light, bg-primary-dark
       * - Status: bg-success, bg-warning, bg-danger, bg-info (also bg-success-bg, text-success-text, border-success-border)
       * - Borders: border-border, border-success-border, border-warning-border, border-danger-border
       *
       * ⚠️ CRITICAL RULE: NEVER use direct colors like text-white, bg-white, text-black, bg-black
       * ⚠️ ALWAYS use semantic tokens for consistency and maintainability
       */
      colors: colors,
      
      // Professional gradients (subtle and elegant)
      backgroundImage: {
        'gradient-primary': 'linear-gradient(135deg, hsl(210, 75%, 45%) 0%, hsl(210, 75%, 32%) 100%)',
        'gradient-secondary': 'linear-gradient(135deg, hsl(175, 60%, 40%) 0%, hsl(175, 60%, 28%) 100%)',
        'gradient-accent': 'linear-gradient(135deg, hsl(250, 45%, 50%) 0%, hsl(250, 45%, 35%) 100%)',
        'gradient-success': 'linear-gradient(135deg, hsl(145, 55%, 42%) 0%, hsl(145, 55%, 32%) 100%)',
        'gradient-warning': 'linear-gradient(135deg, hsl(35, 85%, 50%) 0%, hsl(35, 85%, 40%) 100%)',
        'gradient-danger': 'linear-gradient(135deg, hsl(355, 70%, 52%) 0%, hsl(355, 70%, 40%) 100%)',
        'gradient-info': 'linear-gradient(135deg, hsl(205, 85%, 48%) 0%, hsl(205, 85%, 35%) 100%)',
        'gradient-soft': 'linear-gradient(135deg, hsl(210, 40%, 98%) 0%, hsl(210, 35%, 96%) 100%)',
      },
      
      // Professional shadows (subtle elevation)
      boxShadow: {
        'soft': '0 2px 8px 0 rgba(30, 58, 95, 0.04)',
        'card': '0 1px 3px 0 rgba(30, 58, 95, 0.08), 0 1px 2px 0 rgba(30, 58, 95, 0.06)',
        'card-hover': '0 8px 16px -4px rgba(30, 58, 95, 0.10), 0 4px 8px -2px rgba(30, 58, 95, 0.08)',
        'lg': '0 10px 15px -3px rgba(30, 58, 95, 0.08), 0 4px 6px -2px rgba(30, 58, 95, 0.05)',
        'xl': '0 20px 25px -5px rgba(30, 58, 95, 0.08), 0 10px 10px -5px rgba(30, 58, 95, 0.04)',
        'inner': 'inset 0 2px 4px 0 rgba(30, 58, 95, 0.06)',
        'glow-primary': '0 0 20px rgba(45, 108, 170, 0.25)',
        'glow-success': '0 0 20px rgba(52, 145, 105, 0.25)',
        'glow-danger': '0 0 20px rgba(207, 72, 80, 0.25)',
      },

      // Professional border radius (consistent and clean)
      borderRadius: {
        'card': '12px',
        'button': '8px',
        'input': '8px',
        'pill': '9999px',
      },

      // Typography scale (professional and readable)
      fontSize: {
        'display': ['32px', { lineHeight: '40px', fontWeight: '700' }],
        'title': ['24px', { lineHeight: '32px', fontWeight: '600' }],
        'heading': ['20px', { lineHeight: '28px', fontWeight: '600' }],
        'subheading': ['18px', { lineHeight: '26px', fontWeight: '600' }],
        'body': ['16px', { lineHeight: '24px', fontWeight: '400' }],
        'caption': ['14px', { lineHeight: '20px', fontWeight: '400' }],
        'small': ['12px', { lineHeight: '16px', fontWeight: '400' }],
      },

      // Smooth animations
      animation: {
        'fade-in': 'fadeIn 0.3s ease-in-out',
        'fade-in-up': 'fadeInUp 0.4s ease-out',
        'fade-in-down': 'fadeInDown 0.4s ease-out',
        'scale-in': 'scaleIn 0.2s ease-out',
        'slide-in-right': 'slideInRight 0.3s ease-out',
        'pulse-soft': 'pulseSoft 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        fadeInUp: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        fadeInDown: {
          '0%': { opacity: '0', transform: 'translateY(-10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        scaleIn: {
          '0%': { opacity: '0', transform: 'scale(0.95)' },
          '100%': { opacity: '1', transform: 'scale(1)' },
        },
        slideInRight: {
          '0%': { opacity: '0', transform: 'translateX(-20px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
        pulseSoft: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.85' },
        },
      },

      // Spacing scale
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem',
      },
    },
  },
  plugins: [],
}
