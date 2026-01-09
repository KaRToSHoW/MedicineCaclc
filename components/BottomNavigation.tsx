import { View, Text, Pressable, Platform, Animated, Dimensions } from 'react-native';
import { useRouter, usePathname } from 'expo-router';
import { useEffect, useRef } from 'react';
import { TabIcon } from './TabIcon';

const { width: SCREEN_WIDTH } = Dimensions.get('window');

export default function BottomNavigation() {
  const router = useRouter();
  const pathname = usePathname();

  // Анимации
  const dropPosition = useRef(new Animated.Value(0)).current;
  const bubbleScale = useRef(new Animated.Value(1)).current;
  const bubbleStretch = useRef(new Animated.Value(1)).current;

  const tabs = [
    { name: 'Главная', iconType: 'home' as const, route: '/', activeRoutes: ['/'] },
    {
      name: 'История',
      iconType: 'history' as const,
      route: '/dashboard/history',
      activeRoutes: ['/dashboard/history'],
    },
    {
      name: 'Профиль',
      iconType: 'profile' as const,
      route: '/dashboard/profile',
      activeRoutes: ['/dashboard/profile', '/profile', '/settings', '/dashboard'],
    },
  ];

  const isActive = (tab: typeof tabs[0]) =>
    tab.activeRoutes.some(route =>
      route === '/' ? pathname === '/' : pathname.startsWith(route),
    );

  const activeIndex = tabs.findIndex(tab => isActive(tab));
  const tabWidth = SCREEN_WIDTH / tabs.length;

  useEffect(() => {
    Animated.sequence([
      Animated.parallel([
        Animated.timing(bubbleStretch, {
          toValue: 1.25,
          duration: 140,
          useNativeDriver: true,
        }),
        Animated.timing(bubbleScale, {
          toValue: 0.92,
          duration: 140,
          useNativeDriver: true,
        }),
      ]),
      Animated.spring(dropPosition, {
        toValue: activeIndex,
        tension: 80,
        friction: 10,
        useNativeDriver: true,
      }),
      Animated.parallel([
        Animated.spring(bubbleStretch, {
          toValue: 1,
          tension: 100,
          friction: 8,
          useNativeDriver: true,
        }),
        Animated.spring(bubbleScale, {
          toValue: 1,
          tension: 100,
          friction: 8,
          useNativeDriver: true,
        }),
      ]),
    ]).start();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeIndex]);

  return (
    <View
      style={{
        paddingBottom: Platform.OS === 'ios' ? 22 : 10,
      }}
    >
      {/* УГЛУБЛЕНИЕ (НИША) */}
      <View
        style={{
          position: 'absolute',
          top: 6,
          left: 6,
          right: 6,
          height: 64,
          borderRadius: 32,
          backgroundColor: 'rgba(0,0,0,0.06)',
          shadowColor: '#000',
          shadowOffset: { width: 0, height: 3 },
          shadowOpacity: 0.25,
          shadowRadius: 8,
          elevation: 6,
        }}
      />

      {/* ПРОЗРАЧНЫЙ ПУЗЫРЁК */}
      <Animated.View
        pointerEvents="none"
        style={{
          position: 'absolute',
          top: 8,
          width: 56,
          height: 56,
          borderRadius: 28,
          backgroundColor: 'rgba(255,255,255,0.25)',
          borderWidth: 1,
          borderColor: 'rgba(255,255,255,0.35)',
          transform: [
            {
              translateX: Animated.add(
                Animated.multiply(dropPosition, tabWidth),
                new Animated.Value(tabWidth / 2 - 28),
              ),
            },
            { scaleX: bubbleStretch },
            { scaleY: bubbleScale },
          ],
          shadowColor: '#000',
          shadowOffset: { width: 0, height: 6 },
          shadowOpacity: 0.4,
          shadowRadius: 10,
          elevation: 10,
          zIndex: 2,
        }}
      />

      {/* КНОПКИ */}
      <View className="flex-row justify-around items-center px-2 py-3">
        {tabs.map((tab, index) => {
          const active = index === activeIndex;

          return (
            <Pressable
              key={tab.route}
              onPress={() => router.push(tab.route as any)}
              className="flex-1 items-center"
            >
              <View
                className="items-center justify-center mb-1"
                style={{ height: 40, zIndex: 5 }}
              >
                <TabIcon
                  type={tab.iconType}
                  active={active}
                  size={active ? 28 : 24}
                />
              </View>

              <Text
                className={`text-[11px] font-semibold ${
                  active ? 'text-white' : 'text-text-muted'
                }`}
                style={{ opacity: active ? 1 : 0.7, zIndex: 5 }}
                numberOfLines={1}
              >
                {tab.name}
              </Text>
            </Pressable>
          );
        })}
      </View>
    </View>
  );
}
