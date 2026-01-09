module.exports = {
  expo: {
    name: 'Клиренс креатинина',
    slug: 'creatinine-clearance',
    version: '1.0.0',
    orientation: 'portrait',
    icon: './assets/icon.png',
    userInterfaceStyle: 'light',
    newArchEnabled: true,
    splash: {
      image: './assets/splash-icon.png',
      resizeMode: 'contain',
      backgroundColor: '#ffffff',
    },
    ios: {
      supportsTablet: true,
    },
    android: {
      adaptiveIcon: {
        foregroundImage: './assets/adaptive-icon.png',
        backgroundColor: '#ffffff',
      },
      edgeToEdgeEnabled: true,
      predictiveBackGestureEnabled: false,
    },
    web: {
      favicon: './assets/favicon.png',
    },
    extra: {
      // Use EXPO_PUBLIC_ prefixed variables (Expo convention)
      APP_PORT: process.env.EXPO_PUBLIC_APP_PORT || '8000',
      PUBLIC_HOST: process.env.EXPO_PUBLIC_PUBLIC_HOST || process.env.PUBLIC_HOST || '',
      CLACKY_PREVIEW_DOMAIN_BASE: process.env.EXPO_PUBLIC_CLACKY_PREVIEW_DOMAIN_BASE || process.env.CLACKY_PREVIEW_DOMAIN_BASE || '',
    },
  },
};
