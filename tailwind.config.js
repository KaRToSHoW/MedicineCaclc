/** @type {import('tailwindcss').Config} */

// Modern Medical Calculator Design System with Gradients & Animations
// Fresh, clean, and professional color palette optimized for healthcare
const colors = {
  // Primary Brand - Modern Medical Blue
  primary: {
    DEFAULT: 'hsl(211, 100%, 50%)',     // Vibrant medical blue
    light: 'hsl(211, 100%, 95%)',       // Very light blue for backgrounds
    dark: 'hsl(211, 100%, 35%)',        // Deep blue for emphasis
    50: 'hsl(211, 100%, 98%)',
    100: 'hsl(211, 100%, 95%)',
    200: 'hsl(211, 100%, 85%)',
    300: 'hsl(211, 100%, 70%)',
    400: 'hsl(211, 100%, 60%)',
    500: 'hsl(211, 100%, 50%)',
    600: 'hsl(211, 100%, 45%)',
    700: 'hsl(211, 100%, 35%)',
    800: 'hsl(211, 100%, 25%)',
    900: 'hsl(211, 100%, 15%)',
  },
  
  // Secondary - Fresh Teal/Cyan accent
  secondary: {
    DEFAULT: 'hsl(186, 100%, 42%)',     // Fresh teal
    light: 'hsl(186, 100%, 94%)',       // Light teal backgrounds
    dark: 'hsl(186, 100%, 30%)',        // Dark teal
  },

  // Accent - Modern Purple for highlights
  accent: {
    DEFAULT: 'hsl(262, 83%, 58%)',      // Modern purple
    light: 'hsl(262, 83%, 95%)',        // Very light purple
    dark: 'hsl(262, 83%, 40%)',         // Deep purple
  },

  // Text colors - High contrast and readable
  text: {
    primary: 'hsl(220, 26%, 14%)',      // Almost black with blue tint
    secondary: 'hsl(220, 16%, 40%)',    // Medium gray-blue
    muted: 'hsl(220, 10%, 60%)',        // Light gray
    inverse: 'hsl(0, 0%, 100%)',        // Pure white
  },

  // Surface colors - Clean and modern
  surface: {
    DEFAULT: 'hsl(0, 0%, 100%)',        // Pure white
    elevated: 'hsl(220, 40%, 99%)',     // Subtle blue-white for cards
    secondary: 'hsl(220, 30%, 97%)',    // Light gray-blue background
    hover: 'hsl(220, 30%, 95%)',        // Hover state
  },
  
  border: 'hsl(220, 20%, 90%)',         // Soft gray-blue borders

  // Neutral grays
  neutral: {
    DEFAULT: 'hsl(220, 10%, 60%)',
    light: 'hsl(220, 10%, 85%)',
    dark: 'hsl(220, 10%, 40%)',
  },

  // Status colors - Clinical standards with modern twist
  success: {
    DEFAULT: 'hsl(142, 71%, 45%)',      // Fresh green
    bg: 'hsl(142, 71%, 96%)',           // Light green background
    text: 'hsl(142, 71%, 30%)',         // Dark green text
    border: 'hsl(142, 71%, 85%)',       // Green border
  },
  
  warning: {
    DEFAULT: 'hsl(38, 92%, 55%)',       // Bright amber
    bg: 'hsl(38, 92%, 96%)',            // Light amber background
    text: 'hsl(38, 92%, 30%)',          // Dark amber text
    border: 'hsl(38, 92%, 85%)',        // Amber border
  },
  
  danger: {
    DEFAULT: 'hsl(0, 84%, 60%)',        // Modern red
    bg: 'hsl(0, 84%, 97%)',             // Light red background
    text: 'hsl(0, 84%, 35%)',           // Dark red text
    border: 'hsl(0, 84%, 88%)',         // Red border
  },
  
  info: {
    DEFAULT: 'hsl(199, 89%, 48%)',      // Bright blue
    bg: 'hsl(199, 89%, 96%)',           // Light blue background
    text: 'hsl(199, 89%, 30%)',         // Dark blue text
    border: 'hsl(199, 89%, 85%)',       // Blue border
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
       * Modern Medical Design System - Semantic Color Tokens
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
      
      // Modern gradients for beautiful UI
      backgroundImage: {
        'gradient-primary': 'linear-gradient(135deg, hsl(211, 100%, 50%) 0%, hsl(211, 100%, 35%) 100%)',
        'gradient-secondary': 'linear-gradient(135deg, hsl(186, 100%, 42%) 0%, hsl(186, 100%, 30%) 100%)',
        'gradient-accent': 'linear-gradient(135deg, hsl(262, 83%, 58%) 0%, hsl(262, 83%, 40%) 100%)',
        'gradient-success': 'linear-gradient(135deg, hsl(142, 71%, 45%) 0%, hsl(142, 71%, 35%) 100%)',
        'gradient-warning': 'linear-gradient(135deg, hsl(38, 92%, 55%) 0%, hsl(38, 92%, 45%) 100%)',
        'gradient-danger': 'linear-gradient(135deg, hsl(0, 84%, 60%) 0%, hsl(0, 84%, 45%) 100%)',
        'gradient-info': 'linear-gradient(135deg, hsl(199, 89%, 48%) 0%, hsl(199, 89%, 35%) 100%)',
        'gradient-soft': 'linear-gradient(135deg, hsl(220, 40%, 99%) 0%, hsl(220, 30%, 97%) 100%)',
      },
      
      // Modern shadows for depth and elevation
      boxShadow: {
        'soft': '0 2px 8px 0 rgba(0, 0, 0, 0.05)',
        'card': '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
        'card-hover': '0 8px 16px -4px rgba(0, 0, 0, 0.12), 0 4px 8px -2px rgba(0, 0, 0, 0.08)',
        'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
        'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
        'inner': 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)',
        'glow-primary': '0 0 20px rgba(0, 128, 255, 0.3)',
        'glow-success': '0 0 20px rgba(16, 185, 129, 0.3)',
        'glow-danger': '0 0 20px rgba(239, 68, 68, 0.3)',
      },

      // Modern border radius
      borderRadius: {
        'card': '16px',
        'button': '12px',
        'input': '12px',
        'pill': '9999px',
      },

      // Typography scale
      fontSize: {
        'display': ['36px', { lineHeight: '44px', fontWeight: '700' }],
        'title': ['28px', { lineHeight: '36px', fontWeight: '600' }],
        'heading': ['22px', { lineHeight: '30px', fontWeight: '600' }],
        'subheading': ['18px', { lineHeight: '26px', fontWeight: '600' }],
        'body': ['16px', { lineHeight: '24px', fontWeight: '400' }],
        'caption': ['14px', { lineHeight: '20px', fontWeight: '400' }],
        'small': ['12px', { lineHeight: '16px', fontWeight: '400' }],
      },

      // Animations & Transitions
      animation: {
        'fade-in': 'fadeIn 0.3s ease-in-out',
        'fade-in-up': 'fadeInUp 0.4s ease-out',
        'fade-in-down': 'fadeInDown 0.4s ease-out',
        'scale-in': 'scaleIn 0.2s ease-out',
        'slide-in-right': 'slideInRight 0.3s ease-out',
        'pulse-soft': 'pulseSoft 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'shimmer': 'shimmer 2s linear infinite',
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
          '50%': { opacity: '0.8' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-1000px 0' },
          '100%': { backgroundPosition: '1000px 0' },
        },
      },

      // Spacing scale (extended)
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem',
      },
    },
  },
  plugins: [],
}
