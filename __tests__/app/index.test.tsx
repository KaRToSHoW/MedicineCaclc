import React from 'react';
import { render } from '@testing-library/react-native';
import * as fs from 'fs';
import * as path from 'path';

// Mock expo-router
jest.mock('expo-router', () => ({
  Slot: ({ children }: { children?: React.ReactNode }) => <>{children}</>,
  usePathname: () => '/',
}));

// Mock AuthContext
jest.mock('@/contexts/AuthContext', () => ({
  AuthProvider: ({ children }: { children: React.ReactNode }) => <>{children}</>,
}));

// Mock utils
jest.mock('@/utils/errorHandler', () => ({
  errorHandler: { init: jest.fn() },
  ErrorBoundary: ({ children }: { children: React.ReactNode }) => <>{children}</>,
  ErrorStatusBar: () => null,
}));

jest.mock('@/utils/reload', () => ({
  reloadApp: jest.fn(),
}));

// Mock BottomNavigation
jest.mock('@/components/BottomNavigation', () => ({
  __esModule: true,
  default: () => null,
}));

describe('App Root', () => {
  it('should not have Demo.tsx when real index.tsx exists', () => {
    const indexPath = path.join(__dirname, '../../app/index.tsx');
    const demoPath = path.join(__dirname, '../../components/Demo.tsx');

    if (fs.existsSync(indexPath)) {
      expect(fs.existsSync(demoPath)).toBe(false);
    }
  });

  it('app directory structure exists', () => {
    const appPath = path.join(__dirname, '../../app');
    expect(fs.existsSync(appPath)).toBe(true);
  });
});
