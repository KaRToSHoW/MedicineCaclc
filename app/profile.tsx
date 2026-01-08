import { View, Text, Pressable, ScrollView } from 'react-native';
import { useRouter } from 'expo-router';
import { useAuth } from '@/hooks/useAuth';

export default function ProfileScreen() {
  const router = useRouter();
  const { user, logout } = useAuth();

  const menuSections = [
    {
      title: 'Аккаунт',
      items: [
        { icon: '👤', label: 'Личные данные', route: '/settings', badge: null },
        { icon: '📊', label: 'Статистика', route: '/statistics', badge: null },
        { icon: '📜', label: 'История расчетов', route: '/history', badge: null },
      ],
    },
    {
      title: 'Настройки',
      items: [
        { icon: '🔔', label: 'Уведомления', route: '/settings', badge: null },
        { icon: '🌙', label: 'Тема оформления', route: '/settings', badge: 'Скоро' },
        { icon: '🌐', label: 'Язык', route: '/settings', badge: 'RU' },
      ],
    },
    {
      title: 'Информация',
      items: [
        { icon: '📖', label: 'О приложении', route: '/settings', badge: null },
        { icon: '❓', label: 'Помощь и FAQ', route: '/settings', badge: null },
        { icon: '📧', label: 'Обратная связь', route: '/settings', badge: null },
      ],
    },
  ];

  const handleLogout = async () => {
    try {
      await logout();
      router.replace('/sign-in');
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  return (
    <View className="flex-1 bg-surface-secondary">
      {/* Header */}
      <View className="bg-gradient-primary px-4 pt-12 pb-6">
        <Text className="text-xl font-bold text-text-inverse mb-1">
          Профиль
        </Text>
        <Text className="text-xs text-text-inverse opacity-90">
          Управление аккаунтом и настройками
        </Text>
      </View>

      <ScrollView className="flex-1" contentContainerStyle={{ paddingBottom: 80 }} showsVerticalScrollIndicator={false}>
        {/* User Card */}
        <View className="px-4 pt-4 pb-3">
          <View className="bg-surface rounded-2xl p-4 border border-border shadow-card">
            <View className="flex-row items-center">
              {/* Avatar */}
              <View className="w-16 h-16 rounded-full bg-gradient-primary items-center justify-center mr-4">
                <Text className="text-3xl">👨‍⚕️</Text>
              </View>
              
              {/* User Info */}
              <View className="flex-1">
                <Text className="text-base font-bold text-text-primary mb-0.5">
                  {user?.email || 'Гость'}
                </Text>
                <Text className="text-xs text-text-secondary mb-2">
                  Медицинский специалист
                </Text>
                <View className="flex-row items-center gap-2">
                  <View className="bg-primary-light px-2 py-1 rounded-full">
                    <Text className="text-xs font-medium text-primary">
                      ⭐ Премиум
                    </Text>
                  </View>
                  <View className="bg-success-bg px-2 py-1 rounded-full">
                    <Text className="text-xs font-medium text-success-text">
                      ✓ Активен
                    </Text>
                  </View>
                </View>
              </View>
            </View>

            {/* Quick Stats */}
            <View className="flex-row mt-4 pt-4 border-t border-border">
              <View className="flex-1 items-center">
                <Text className="text-lg font-bold text-primary mb-0.5">47</Text>
                <Text className="text-xs text-text-secondary">Расчетов</Text>
              </View>
              <View className="w-px bg-border" />
              <View className="flex-1 items-center">
                <Text className="text-lg font-bold text-secondary mb-0.5">12</Text>
                <Text className="text-xs text-text-secondary">Избранных</Text>
              </View>
              <View className="w-px bg-border" />
              <View className="flex-1 items-center">
                <Text className="text-lg font-bold text-accent mb-0.5">8</Text>
                <Text className="text-xs text-text-secondary">Дней</Text>
              </View>
            </View>
          </View>
        </View>

        {/* Menu Sections */}
        {menuSections.map((section, sectionIndex) => (
          <View key={section.title} className="px-4 pb-3">
            <Text className="text-xs font-semibold text-text-muted uppercase mb-2 px-2">
              {section.title}
            </Text>
            <View className="bg-surface rounded-2xl border border-border overflow-hidden">
              {section.items.map((item, itemIndex) => (
                <View key={item.label}>
                  <Pressable
                    onPress={() => router.push(item.route as any)}
                    className="flex-row items-center px-4 py-3.5 active:bg-surface-hover"
                  >
                    <View className="w-9 h-9 rounded-full bg-surface-secondary items-center justify-center mr-3">
                      <Text className="text-lg">{item.icon}</Text>
                    </View>
                    <Text className="flex-1 text-sm font-medium text-text-primary">
                      {item.label}
                    </Text>
                    {item.badge && (
                      <View className="bg-primary-light px-2 py-0.5 rounded-full mr-2">
                        <Text className="text-xs font-medium text-primary">
                          {item.badge}
                        </Text>
                      </View>
                    )}
                    <Text className="text-lg text-text-muted">›</Text>
                  </Pressable>
                  {itemIndex < section.items.length - 1 && (
                    <View className="h-px bg-border ml-16" />
                  )}
                </View>
              ))}
            </View>
          </View>
        ))}

        {/* Logout Button */}
        <View className="px-4 pb-6">
          <Pressable
            onPress={handleLogout}
            className="bg-danger-bg border border-danger-border rounded-xl py-3.5 items-center active:opacity-70"
          >
            <Text className="text-sm font-semibold text-danger-text">
              🚪 Выйти из аккаунта
            </Text>
          </Pressable>
        </View>

        {/* App Version */}
        <View className="px-4 pb-8 items-center">
          <Text className="text-xs text-text-muted">
            Медицинский Калькулятор v1.0.0
          </Text>
          <Text className="text-xs text-text-muted mt-1">
            © 2024 Все права защищены
          </Text>
        </View>
      </ScrollView>
    </View>
  );
}
