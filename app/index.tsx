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
    <ScrollView className="flex-1 bg-surface-secondary" contentContainerStyle={{ paddingBottom: 80 }}>
      {/* Header with Gradient - Mobile Optimized */}
      <View className="bg-gradient-primary px-4 pt-12 pb-6 shadow-xl">
        <View className="flex-row items-start justify-between mb-4">
          <View className="flex-1">
            <Text className="text-2xl font-bold text-text-inverse mb-2">
              🏥 Медицинский калькулятор
            </Text>
            <Text className="text-sm text-text-inverse opacity-95">
              Профессиональные клинические расчеты
            </Text>
          </View>
          {isAuthenticated ? (
            <Pressable
              onPress={() => router.push('/dashboard')}
              className="bg-surface rounded-button px-3 py-2 shadow-card active:opacity-80"
            >
              <Text className="text-xs text-primary font-bold">
                👤 Кабинет
              </Text>
            </Pressable>
          ) : (
            <Pressable
              onPress={() => router.push('/(auth)/sign-in')}
              className="bg-surface rounded-button px-3 py-2 shadow-card active:opacity-80"
            >
              <Text className="text-xs text-primary font-bold">
                Войти
              </Text>
            </Pressable>
          )}
        </View>
      </View>

      {/* Quick Actions - Mobile Optimized */}
      <View className="px-4 pt-4 pb-4">
        <View className="flex-row gap-3">
          {isAuthenticated ? (
            <Pressable
              onPress={() => router.push('/dashboard')}
              className="flex-1 bg-surface rounded-card p-4 shadow-card-hover active:opacity-80"
            >
              <Text className="text-2xl mb-2">👤</Text>
              <Text className="text-sm font-bold text-text-primary">Личный кабинет</Text>
            </Pressable>
          ) : null}
          <Pressable
            onPress={() => router.push('/calculators')}
            className="flex-1 bg-surface rounded-card p-4 shadow-card-hover active:opacity-80"
          >
            <Text className="text-2xl mb-2">🔍</Text>
            <Text className="text-sm font-bold text-text-primary">Калькуляторы</Text>
          </Pressable>
        </View>
      </View>

      {/* Categories - Mobile Optimized */}
      <View className="px-4 pb-4">
        <Text className="text-lg font-bold text-text-primary mb-3">
          Категории
        </Text>
        <View className="flex-row flex-wrap gap-2">
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
              } rounded-card px-3 py-3 flex-row items-center shadow-card-hover active:opacity-90 min-w-[47%]`}
            >
              <Text className="text-2xl mr-2">{category.icon}</Text>
              <Text className="text-sm font-bold text-text-inverse flex-shrink">
                {category.name}
              </Text>
            </Pressable>
          ))}
        </View>
      </View>

      {/* Popular Calculators - Mobile Optimized */}
      <View className="px-4 pb-6">
        <View className="flex-row items-center justify-between mb-3">
          <Text className="text-lg font-bold text-text-primary">
            Популярные калькуляторы
          </Text>
          <Link href="/calculators" asChild>
            <Pressable className="active:opacity-70">
              <Text className="text-sm font-bold text-primary">
                Все →
              </Text>
            </Pressable>
          </Link>
        </View>

        {loading ? (
          <View className="bg-surface rounded-card p-4 shadow-card">
            <Text className="text-center text-text-secondary text-sm">Загрузка калькуляторов...</Text>
          </View>
        ) : error ? (
          <View className="bg-danger-bg border-2 border-danger rounded-card p-3 shadow-soft">
            <Text className="text-danger-text text-sm font-medium">{error}</Text>
          </View>
        ) : (
          <View className="gap-2">
            {calculators.slice(0, 5).map((calculator) => (
              <Pressable
                key={calculator.id}
                onPress={() => handleCalculatorPress(calculator.id)}
                className="bg-surface rounded-card p-3 shadow-card-hover active:opacity-90"
              >
                <View className="flex-row items-start">
                  <View className="w-10 h-10 rounded-pill bg-gradient-soft items-center justify-center mr-3 shadow-soft">
                    <Text className="text-xl">
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
                    <Text className="text-sm font-bold text-text-primary mb-0.5">
                      {calculator.nameRu || calculator.name}
                    </Text>
                    <Text className="text-xs text-text-secondary capitalize">
                      {calculator.categoryRu || calculator.category}
                    </Text>
                  </View>
                  <Text className="text-text-muted text-xl">→</Text>
                </View>
              </Pressable>
            ))}
          </View>
        )}
      </View>

      {/* Info Note - Mobile Optimized */}
      <View className="px-4 pb-6">
        <View className="bg-info-bg border-2 border-info rounded-card p-3 shadow-soft">
          <View className="flex-row items-start">
            <Text className="text-xl mr-2">ℹ️</Text>
            <View className="flex-1">
              <Text className="text-sm font-bold text-info-text mb-1">
                Медицинский дисклеймер
              </Text>
              <Text className="text-xs text-text-secondary leading-4">
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
