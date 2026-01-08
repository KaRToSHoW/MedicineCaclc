import { View, Text, Pressable, Platform, Animated, Dimensions } from 'react-native';
import { useRouter, usePathname } from 'expo-router';
import { useEffect, useRef } from 'react';
import { TabIcon } from './TabIcon';

const { width: SCREEN_WIDTH } = Dimensions.get('window');

export default function BottomNavigation() {
  const router = useRouter();
  const pathname = usePathname();
  const dropPosition = useRef(new Animated.Value(0)).current;

  const tabs = [
    {
      name: 'Главная',
      iconType: 'home' as const,
      route: '/',
      activeRoutes: ['/'],
    },
    {
      name: 'Калькуляторы',
      iconType: 'calculator' as const,
      route: '/calculators',
      activeRoutes: ['/calculators', '/calculator'],
    },
    {
      name: 'Избранное',
      iconType: 'favorite' as const,
      route: '/favorites',
      activeRoutes: ['/favorites'],
    },
    {
      name: 'Профиль',
      iconType: 'profile' as const,
      route: '/profile',
      activeRoutes: ['/profile', '/settings'],
    },
  ];

  const isActive = (tab: typeof tabs[0]) => {
    return tab.activeRoutes.some(route => {
      if (route === '/') {
        return pathname === '/';
      }
      return pathname.startsWith(route);
    });
  };

  const activeIndex = tabs.findIndex(tab => isActive(tab));
  const tabWidth = SCREEN_WIDTH / tabs.length;

  useEffect(() => {
    Animated.spring(dropPosition, {
      toValue: activeIndex * tabWidth + tabWidth / 2,
      useNativeDriver: true,
      tension: 68,
      friction: 12,
    }).start();
    // dropPosition is a ref and doesn't need to be in dependencies
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeIndex, tabWidth]);

  return (
    <View 
      className="bg-surface relative"
      style={{
        paddingBottom: Platform.OS === 'ios' ? 20 : 8,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: -4 },
        shadowOpacity: 0.12,
        shadowRadius: 12,
        elevation: 12,
      }}
    >
      {/* Animated Liquid Drop Indicator */}
      <Animated.View
        className="absolute top-0 items-center"
        style={{
          transform: [{ translateX: dropPosition }, { translateY: -8 }],
          marginLeft: -18,
        }}
      >
        {/* Main Drop */}
        <View 
          className="bg-primary items-center justify-center"
          style={{
            width: 36,
            height: 36,
            borderRadius: 18,
            shadowColor: 'hsl(210, 75%, 45%)',
            shadowOffset: { width: 0, height: 4 },
            shadowOpacity: 0.3,
            shadowRadius: 8,
            elevation: 6,
          }}
        >
          {/* Inner glow */}
          <View 
            className="bg-primary-light"
            style={{
              width: 20,
              height: 20,
              borderRadius: 10,
              opacity: 0.5,
            }}
          />
        </View>
        
        {/* Drop Tail */}
        <View 
          className="bg-primary"
          style={{
            width: 12,
            height: 8,
            borderBottomLeftRadius: 8,
            borderBottomRightRadius: 8,
            marginTop: -2,
          }}
        />
        
        {/* Small drip */}
        <View 
          className="bg-primary"
          style={{
            width: 4,
            height: 4,
            borderRadius: 2,
            marginTop: 1,
          }}
        />
      </Animated.View>

      {/* Tabs */}
      <View className="flex-row justify-around items-center px-2 pt-8 pb-2">
        {tabs.map((tab, index) => {
          const active = isActive(tab);
          return (
            <Pressable
              key={tab.route}
              onPress={() => router.push(tab.route as any)}
              className="flex-1 items-center py-2 active:scale-95"
              style={{ 
                minWidth: 60,
                transform: active ? [{ scale: 1.05 }] : [{ scale: 1 }],
              }}
            >
              {/* Icon with background when active */}
              {active ? (
                <View 
                  className="items-center justify-center mb-2 bg-primary-light"
                  style={{
                    width: 48,
                    height: 48,
                    borderRadius: 24,
                  }}
                >
                  <TabIcon type={tab.iconType} active={active} size={26} />
                </View>
              ) : (
                <View className="items-center justify-center mb-2">
                  <TabIcon type={tab.iconType} active={active} size={24} />
                </View>
              )}
              
              {/* Label */}
              <Text 
                className={`text-xs font-semibold ${
                  active 
                    ? 'text-primary' 
                    : 'text-text-muted'
                }`}
                numberOfLines={1}
                style={{
                  opacity: active ? 1 : 0.7,
                }}
              >
                {tab.name}
              </Text>
              
              {/* Active indicator dots */}
              {active ? (
                <View className="flex-row gap-1 mt-1">
                  <View 
                    className="bg-primary"
                    style={{
                      width: 3,
                      height: 3,
                      borderRadius: 1.5,
                    }}
                  />
                  <View 
                    className="bg-primary"
                    style={{
                      width: 3,
                      height: 3,
                      borderRadius: 1.5,
                      opacity: 0.6,
                    }}
                  />
                  <View 
                    className="bg-primary"
                    style={{
                      width: 3,
                      height: 3,
                      borderRadius: 1.5,
                      opacity: 0.3,
                    }}
                  />
                </View>
              ) : null}
            </Pressable>
          );
        })}
      </View>
    </View>
  );
}
