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
  { id: 'General Health', name: 'Общее здоровье', icon: '⚕️' },
  { id: 'Cardiology', name: 'Кардиология', icon: '❤️' },
  { id: 'Nephrology', name: 'Нефрология', icon: '🫘' },
  { id: 'Neurology', name: 'Неврология', icon: '🧠' },
  { id: 'Pediatrics', name: 'Педиатрия', icon: '👶' },
  { id: 'Obstetrics', name: 'Акушерство', icon: '🤰' },
  { id: 'Hematology', name: 'Гематология', icon: '💉' },
  { id: 'Laboratory', name: 'Лабораторная', icon: '🔬' },
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

  const handleCalculatorPress = (id: string | number) => {
    router.push(`/calculator/${id}`);
  };

  return (
    <ScrollView className="flex-1 bg-surface-secondary">
      {/* Header with Gradient */}
      <View className="bg-gradient-primary px-6 pt-16 pb-10 shadow-xl">
        <View className="flex-row items-start justify-between mb-6">
          <View className="flex-1">
            <Text className="text-4xl font-bold text-text-inverse mb-3">
              🏥 Медицинский калькулятор
            </Text>
            <Text className="text-lg text-text-inverse opacity-95">
              Профессиональные клинические расчеты
            </Text>
          </View>
          {isAuthenticated ? (
            <Pressable
              onPress={() => router.push('/settings')}
              className="bg-surface rounded-button px-4 py-3 shadow-card active:opacity-80"
            >
              <Text className="text-sm text-primary font-bold">
                {user?.name || user?.email || 'Профиль'}
              </Text>
            </Pressable>
          ) : (
            <Pressable
              onPress={() => router.push('/(auth)/sign-in')}
              className="bg-surface rounded-button px-5 py-3 shadow-card active:opacity-80"
            >
              <Text className="text-sm text-primary font-bold">
                Войти
              </Text>
            </Pressable>
          )}
        </View>
      </View>

      {/* Quick Actions */}
      <View className="px-6 pt-6 pb-6">
        <View className="flex-row gap-4">
          <Pressable
            onPress={() => router.push('/history')}
            className="flex-1 bg-surface rounded-card p-5 shadow-card-hover active:opacity-80"
          >
            <Text className="text-3xl mb-3">📊</Text>
            <Text className="text-base font-bold text-text-primary">История</Text>
          </Pressable>
          <Pressable
            onPress={() => router.push('/statistics')}
            className="flex-1 bg-surface rounded-card p-5 shadow-card-hover active:opacity-80"
          >
            <Text className="text-3xl mb-3">📈</Text>
            <Text className="text-base font-bold text-text-primary">Статистика</Text>
          </Pressable>
          <Pressable
            onPress={() => router.push('/calculators')}
            className="flex-1 bg-surface rounded-card p-5 shadow-card-hover active:opacity-80"
          >
            <Text className="text-3xl mb-3">🔍</Text>
            <Text className="text-base font-bold text-text-primary">Все</Text>
          </Pressable>
        </View>
      </View>

      {/* Categories */}
      <View className="px-6 pb-6">
        <Text className="text-xl font-bold text-text-primary mb-5">
          Категории
        </Text>
        <View className="flex-row flex-wrap gap-4">
          {categories.map((category) => (
            <Pressable
              key={category.id}
              onPress={() => handleCategoryPress(category.id)}
              className={`${
                category.id === 'General Health' ? 'bg-gradient-primary' :
                  category.id === 'Cardiology' ? 'bg-gradient-danger' :
                    category.id === 'Nephrology' ? 'bg-gradient-secondary' :
                      category.id === 'Neurology' ? 'bg-gradient-accent' :
                        category.id === 'Pediatrics' ? 'bg-gradient-info' :
                          category.id === 'Obstetrics' ? 'bg-gradient-success' :
                            category.id === 'Hematology' ? 'bg-gradient-danger' :
                              'bg-gradient-accent'
              } rounded-card px-6 py-5 flex-row items-center shadow-card-hover active:opacity-90 min-w-[45%]`}
            >
              <Text className="text-4xl mr-4">{category.icon}</Text>
              <Text className="text-lg font-bold text-text-inverse flex-shrink">
                {category.name}
              </Text>
            </Pressable>
          ))}
        </View>
      </View>

      {/* Popular Calculators */}
      <View className="px-6 pb-8">
        <View className="flex-row items-center justify-between mb-5">
          <Text className="text-xl font-bold text-text-primary">
            Популярные калькуляторы
          </Text>
          <Link href="/calculators" asChild>
            <Pressable className="active:opacity-70">
              <Text className="text-base font-bold text-primary">
                Все →
              </Text>
            </Pressable>
          </Link>
        </View>

        {loading ? (
          <View className="bg-surface rounded-card p-6 shadow-card">
            <Text className="text-center text-text-secondary">Загрузка калькуляторов...</Text>
          </View>
        ) : error ? (
          <View className="bg-danger-bg border-2 border-danger rounded-card p-5 shadow-soft">
            <Text className="text-danger-text text-base font-medium">{error}</Text>
          </View>
        ) : (
          <View className="gap-4">
            {calculators.slice(0, 5).map((calculator) => (
              <Pressable
                key={calculator.id}
                onPress={() => handleCalculatorPress(calculator.id)}
                className="bg-surface rounded-card p-5 shadow-card-hover active:opacity-90"
              >
                <View className="flex-row items-start">
                  <View className="w-14 h-14 rounded-pill bg-gradient-soft items-center justify-center mr-4 shadow-soft">
                    <Text className="text-3xl">
                      {calculator.category === 'Cardiology' ? '❤️' :
                        calculator.category === 'Neurology' ? '🧠' :
                          calculator.category === 'Pediatrics' ? '👶' :
                            calculator.category === 'General Health' ? '⚕️' :
                              calculator.category === 'Nephrology' ? '🫘' :
                                calculator.category === 'Obstetrics' ? '🤰' :
                                  calculator.category === 'Hematology' ? '💉' :
                                    calculator.category === 'Laboratory' ? '🔬' : '⚕️'}
                    </Text>
                  </View>
                  <View className="flex-1">
                    <Text className="text-lg font-bold text-text-primary mb-1">
                      {calculator.nameRu || calculator.name}
                    </Text>
                    <Text className="text-sm text-text-secondary capitalize">
                      {calculator.categoryRu || calculator.category}
                    </Text>
                  </View>
                  <Text className="text-text-muted text-2xl">→</Text>
                </View>
              </Pressable>
            ))}
          </View>
        )}
      </View>

      {/* Info Note */}
      <View className="px-6 pb-8">
        <View className="bg-info-bg border-2 border-info rounded-card p-5 shadow-soft">
          <View className="flex-row items-start">
            <Text className="text-2xl mr-3">ℹ️</Text>
            <View className="flex-1">
              <Text className="text-base font-bold text-info-text mb-2">
                Медицинский дисклеймер
              </Text>
              <Text className="text-sm text-text-secondary leading-5">
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
