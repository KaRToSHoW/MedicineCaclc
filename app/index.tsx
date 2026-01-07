import React, { useEffect } from 'react';
import { View, Text, ScrollView, Pressable } from 'react-native';
import { Link, router } from 'expo-router';
import { useCalculatorsStore } from '@/stores/calculatorsStore';
import { useAuth } from '@/hooks/useAuth';

/**
 * Home Screen - Main Entry Point
 * Displays calculator categories and popular calculators
 */

const categories = [
  { id: 'general', name: 'Общие', icon: '⚕️', color: 'bg-primary' },
  { id: 'cardiology', name: 'Кардиология', icon: '❤️', color: 'bg-danger' },
  { id: 'endocrinology', name: 'Эндокринология', icon: '🔬', color: 'bg-secondary' },
  { id: 'neurology', name: 'Неврология', icon: '🧠', color: 'bg-accent' },
  { id: 'pediatrics', name: 'Педиатрия', icon: '👶', color: 'bg-info' },
];

export default function HomeScreen() {
  const { user, isAuthenticated } = useAuth();
  const { items: calculators, loading, error, fetchAll } = useCalculatorsStore();

  useEffect(() => {
    fetchAll();
  }, []);

  const handleCategoryPress = (category: string) => {
    router.push(`/calculators?category=${category}`);
  };

  const handleCalculatorPress = (id: number) => {
    router.push(`/calculator/${id}`);
  };

  return (
    <ScrollView className="flex-1 bg-surface">
      {/* Header */}
      <View className="bg-primary px-6 pt-16 pb-8">
        <View className="flex-row items-start justify-between mb-4">
          <View className="flex-1">
            <Text className="text-3xl font-bold text-text-inverse mb-2">
              🏥 Медицинский калькулятор
            </Text>
            <Text className="text-base text-text-inverse opacity-90">
              Профессиональные клинические расчеты
            </Text>
          </View>
          {isAuthenticated ? (
            <Pressable
              onPress={() => router.push('/settings')}
              className="bg-primary-light rounded-xl px-4 py-2 active:opacity-80"
            >
              <Text className="text-xs text-text-inverse font-medium">
                {user?.name || user?.email || 'Профиль'}
              </Text>
            </Pressable>
          ) : (
            <Pressable
              onPress={() => router.push('/(auth)/sign-in')}
              className="bg-surface-elevated rounded-xl px-4 py-2 active:opacity-80"
            >
              <Text className="text-xs text-primary font-semibold">
                Войти
              </Text>
            </Pressable>
          )}
        </View>
      </View>

      {/* Quick Actions */}
      <View className="px-6 pt-6 pb-4">
        <View className="flex-row gap-3">
          <Pressable
            onPress={() => router.push('/history')}
            className="flex-1 bg-surface-elevated border border-border rounded-xl p-4 active:opacity-70"
          >
            <Text className="text-2xl mb-2">📊</Text>
            <Text className="text-sm font-semibold text-text-primary">История</Text>
          </Pressable>
          <Pressable
            onPress={() => router.push('/statistics')}
            className="flex-1 bg-surface-elevated border border-border rounded-xl p-4 active:opacity-70"
          >
            <Text className="text-2xl mb-2">📈</Text>
            <Text className="text-sm font-semibold text-text-primary">Статистика</Text>
          </Pressable>
          <Pressable
            onPress={() => router.push('/calculators')}
            className="flex-1 bg-surface-elevated border border-border rounded-xl p-4 active:opacity-70"
          >
            <Text className="text-2xl mb-2">🔍</Text>
            <Text className="text-sm font-semibold text-text-primary">Все</Text>
          </Pressable>
        </View>
      </View>

      {/* Categories */}
      <View className="px-6 pb-6">
        <Text className="text-lg font-bold text-text-primary mb-4">
          Категории
        </Text>
        <View className="flex-row flex-wrap gap-3">
          {categories.map((category) => (
            <Pressable
              key={category.id}
              onPress={() => handleCategoryPress(category.id)}
              className={`${category.color} rounded-2xl px-5 py-4 flex-row items-center active:opacity-80 min-w-[45%]`}
            >
              <Text className="text-3xl mr-3">{category.icon}</Text>
              <Text className="text-base font-semibold text-text-inverse">
                {category.name}
              </Text>
            </Pressable>
          ))}
        </View>
      </View>

      {/* Popular Calculators */}
      <View className="px-6 pb-8">
        <View className="flex-row items-center justify-between mb-4">
          <Text className="text-lg font-bold text-text-primary">
            Популярные калькуляторы
          </Text>
          <Link href="/calculators" asChild>
            <Pressable className="active:opacity-70">
              <Text className="text-sm font-medium text-primary">
                Все
              </Text>
            </Pressable>
          </Link>
        </View>

        {loading ? (
          <View className="bg-surface-elevated rounded-2xl p-6 border border-border">
            <Text className="text-center text-text-secondary">Загрузка калькуляторов...</Text>
          </View>
        ) : error ? (
          <View className="bg-danger-bg border border-danger rounded-xl p-4">
            <Text className="text-danger-text text-sm">{error}</Text>
          </View>
        ) : (
          <View className="gap-3">
            {calculators.slice(0, 5).map((calculator) => (
              <Pressable
                key={calculator.id}
                onPress={() => handleCalculatorPress(calculator.id)}
                className="bg-surface-elevated rounded-2xl p-4 border border-border active:opacity-70"
              >
                <View className="flex-row items-start">
                  <View className="w-12 h-12 rounded-full bg-primary-light items-center justify-center mr-4">
                    <Text className="text-2xl">
                      {calculator.category === 'cardiology' ? '❤️' :
                        calculator.category === 'endocrinology' ? '🔬' :
                          calculator.category === 'neurology' ? '🧠' :
                            calculator.category === 'pediatrics' ? '👶' : '⚕️'}
                    </Text>
                  </View>
                  <View className="flex-1">
                    <Text className="text-base font-semibold text-text-primary mb-1">
                      {calculator.name}
                    </Text>
                    <Text className="text-xs text-text-secondary capitalize">
                      {calculator.category}
                    </Text>
                  </View>
                  <Text className="text-text-muted text-lg">→</Text>
                </View>
              </Pressable>
            ))}
          </View>
        )}
      </View>

      {/* Info Note */}
      <View className="px-6 pb-8">
        <View className="bg-info-bg border border-info rounded-xl p-4">
          <View className="flex-row items-start">
            <Text className="text-xl mr-3">ℹ️</Text>
            <View className="flex-1">
              <Text className="text-sm font-medium text-info-text mb-1">
                Медицинский дисклеймер
              </Text>
              <Text className="text-xs text-text-secondary">
                Эти калькуляторы предоставляют оценки на основе стандартных медицинских формул.
                {' '}Всегда консультируйтесь с квалифицированным медицинским специалистом.
              </Text>
            </View>
          </View>
        </View>
      </View>
    </ScrollView>
  );
}
