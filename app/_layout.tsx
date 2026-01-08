import { Slot, usePathname } from 'expo-router';
import { AuthProvider } from '@/contexts/AuthContext';
import { useEffect, useState } from 'react';
import { View, Text, Pressable, LogBox } from 'react-native';
import {
  errorHandler,
  ErrorBoundary,
  ErrorStatusBar,
} from '@/utils/errorHandler';
import { reloadApp } from '@/utils/reload';
import BottomNavigation from '@/components/BottomNavigation';
import '../global.css';

/**
 * Root Layout with Demo Detection & Error Handling
 *
 * Features:
 * 1. Demo Preview Mode: Dynamically loads components/Demo.tsx if it exists
 * 2. Error Handling: ErrorBoundary + ErrorStatusBar for development
 * 3. Disable LogBox: Use our custom ErrorStatusBar instead
 *
 * Usage:
 * - Early stage: Keep Demo.tsx to show clients a quick preview
 * - Production: Delete Demo.tsx file to use real homepage (auto-detects at runtime)
 *
 * Implementation:
 * - Uses runtime require() in useEffect to gracefully handle missing Demo.tsx
 * - No manual code changes needed when adding/removing demo file
 * - Safe for hot reload - deleting Demo.tsx won't cause crashes
 */

// Disable Expo's LogBox (yellow warnings) - use our ErrorStatusBar instead
if (__DEV__ && LogBox) {
  LogBox.ignoreAllLogs();
}

// Initialize error handler (this will also suppress RedBox)
errorHandler.init();

export default function RootLayout() {
  const pathname = usePathname();
  const [shouldShowDemo, setShouldShowDemo] = useState(false);
  const [showBanner, setShowBanner] = useState(true);
  const [DemoComponent, setDemoComponent] = useState<any>(null);

  // Hide bottom navigation on auth screens, calculator detail, and result screens
  const hideBottomNav = pathname.includes('/sign-in') || 
                        pathname.includes('/sign-up') || 
                        pathname.includes('/forgot-password') ||
                        pathname.startsWith('/calculator/') ||
                        pathname.startsWith('/result/');

  useEffect(() => {
    // Try to load Demo component at runtime
    try {
      // eslint-disable-next-line @typescript-eslint/no-var-requires
      const module = require('../components/Demo');
      if (module?.default) {
        setDemoComponent(() => module.default);
        setShouldShowDemo(true);
      }
    } catch (e) {
      // Demo component doesn't exist, will render normal app
      setShouldShowDemo(false);
    }
  }, []);

  const handleRefresh = () => {
    reloadApp();
  };

  // Render Demo or Normal App
  const content = shouldShowDemo && DemoComponent ? (
    <>
      {/* Demo Preview Banner */}
      {showBanner ? <View className="bg-info-bg border-b border-info-light">
        <View className="px-4 py-3 flex-row items-center justify-between">
          <View className="flex-1 flex-row items-center gap-2">
            <Text className="text-lg">💡</Text>
            <View className="flex-1">
              <Text className="text-sm font-medium text-text-primary">
                  Quick Preview Version
              </Text>
              <Text className="text-xs text-text-secondary">
                  This is a demo with fake data. Real features are under development.
              </Text>
            </View>
          </View>
          <View className="flex-row items-center gap-2">
            <Pressable
              onPress={handleRefresh}
              className="px-3 py-1.5 rounded-lg bg-info/10 active:opacity-70"
            >
              <Text className="text-xs font-medium text-info">
                  Refresh
              </Text>
            </Pressable>
            <Pressable
              onPress={() => setShowBanner(false)}
              className="px-2 py-1 active:opacity-70"
            >
              <Text className="text-lg text-text-secondary">×</Text>
            </Pressable>
          </View>
        </View>
      </View> : null}
      <DemoComponent />
    </>
  ) : (
    <Slot />
  );

  return (
    <ErrorBoundary>
      <AuthProvider>
        <View className="flex-1">
          <View className="flex-1">
            {content}
          </View>
          {!shouldShowDemo && !hideBottomNav && <BottomNavigation />}
          <ErrorStatusBar />
        </View>
      </AuthProvider>
    </ErrorBoundary>
  );
}
