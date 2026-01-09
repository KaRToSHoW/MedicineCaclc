/**
 * API Configuration
 *
 * Matches backend/lib/env_checker.rb logic:
 * 1. Production: PUBLIC_HOST -> https://PUBLIC_HOST
 * 2. Cloud dev: APP_PORT + CLACKY_PREVIEW_DOMAIN_BASE -> https://8000.dev.clacky.com
 * 3. Local dev: http://localhost:8000
 *
 * Environment variables are mapped through app.config.js to support
 * both system-injected vars (APP_PORT) and Expo format (EXPO_PUBLIC_APP_PORT)
 */

import Constants from 'expo-constants';

const getApiBaseUrl = (): string => {
  const extra = Constants.expoConfig?.extra || {};

  console.log('[API Config] Environment variables:', {
    APP_PORT: extra.APP_PORT,
    PUBLIC_HOST: extra.PUBLIC_HOST,
    CLACKY_PREVIEW_DOMAIN_BASE: extra.CLACKY_PREVIEW_DOMAIN_BASE
  });

  // 1. Production: Use PUBLIC_HOST if set
  if (extra.PUBLIC_HOST) {
    const url = `https://${extra.PUBLIC_HOST}`;
    console.log('[API Config] Using PUBLIC_HOST:', url);
    return url;
  }

  // 2. Cloud dev: Use APP_PORT + CLACKY_PREVIEW_DOMAIN_BASE
  if (extra.CLACKY_PREVIEW_DOMAIN_BASE) {
    const port = extra.APP_PORT || '8000';
    const domainBase = extra.CLACKY_PREVIEW_DOMAIN_BASE;
    const url = `https://${port}${domainBase}`;
    console.log('[API Config] Using Cloud dev:', url, { port, domainBase });
    return url;
  }

  // 3. Local dev: fallback to localhost
  const defaultPort = extra.APP_PORT || '8000';
  const url = `http://localhost:${defaultPort}`;
  console.log('[API Config] Using localhost:', url);
  return url;
};

export const API_BASE_URL = getApiBaseUrl();
export const API_URL = API_BASE_URL; // Alias for compatibility

export const API_ENDPOINTS = {
  health: `${API_BASE_URL}/api/v1/health`,
};
