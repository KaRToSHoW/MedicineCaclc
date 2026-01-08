/**
 * Dashboard Overview Screen
 * Main dashboard with stats overview and quick actions
 */

import React, { useEffect } from 'react';
import { View, Text, ScrollView, Pressable } from 'react-native';
import { router } from 'expo-router';
import { useAuth } from '@/hooks/useAuth';
import { useCalculationResultsStore } from '@/stores/calculationResultsStore';
import { useCalculatorsStore } from '@/stores/calculatorsStore';

export default function DashboardOverviewScreen() {
  const { user, isAuthenticated } = useAuth();
  const { items: results, loading, fetchAll } = useCalculationResultsStore();
  const { items: calculators, fetchAll: fetchCalculators } = useCalculatorsStore();

  useEffect(() => {
    if (isAuthenticated) {
      fetchAll();
      fetchCalculators();
    }
  }, [isAuthenticated]);

  // Redirect if not authenticated
  if (!isAuthenticated) {
    router.replace('/(auth)/sign-in');
    return null;
  }

  // Calculate statistics
  const totalCalculations = results.length;
  
  const last7Days = results.filter((result) => {
    const resultDate = new Date(result.performedAt);
    const today = new Date();
    const diffTime = Math.abs(today.getTime() - resultDate.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays <= 7;
  }).length;

  const calculatorUsage = results.reduce((acc, result) => {
    const name = result.calculator?.name || 'Unknown';
    acc[name] = (acc[name] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  const categoryUsage = results.reduce((acc, result) => {
    const category = result.calculator?.category || 'unknown';
    acc[category] = (acc[category] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  const topCalculators = Object.entries(calculatorUsage)
    .sort(([, a], [, b]) => b - a)
    .slice(0, 3);

  const recentResults = results
    .sort((a, b) => new Date(b.performedAt).getTime() - new Date(a.performedAt).getTime())
    .slice(0, 5);

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'Cardiology': return '❤️';
      case 'Neurology': return '🧠';
      case 'Pediatrics': return '👶';
      case 'Nephrology': return '🫘';
      case 'Obstetrics': return '🤰';
      case 'Hematology': return '💉';
      case 'Laboratory': return '🔬';
      case 'General Health': return '⚕️';
      default: return '📊';
    }
  };

  return (
    <ScrollView className="flex-1 bg-surface">
      {/* Header */}
      <View className="bg-primary px-6 pt-16 pb-8">
        <Text className="text-3xl font-bold text-text-inverse mb-2">
          Добро пожаловать, {user?.name || 'Доктор'}! 👋
        </Text>
        <Text className="text-base text-text-inverse opacity-90">
          Обзор вашей активности
        </Text>
      </View>

      <View className="px-6 py-6">
        {/* Quick Stats */}
        <View className="flex-row gap-3 mb-6">
          <View className="flex-1 bg-gradient-to-br from-primary to-primary-dark rounded-2xl p-5 shadow-card">
            <Text className="text-4xl font-bold text-text-inverse mb-1">
              {totalCalculations}
            </Text>
            <Text className="text-sm text-text-inverse opacity-80">
              Всего расчетов
            </Text>
          </View>
          <View className="flex-1 bg-gradient-to-br from-success to-success-dark rounded-2xl p-5 shadow-card">
            <Text className="text-4xl font-bold text-text-inverse mb-1">
              {last7Days}
            </Text>
            <Text className="text-sm text-text-inverse opacity-80">
              За неделю
            </Text>
          </View>
        </View>

        {/* Quick Actions */}
        <View className="mb-6">
          <Text className="text-lg font-bold text-text-primary mb-4">
            Быстрые действия
          </Text>
          <View className="flex-row gap-3">
            <Pressable
              onPress={() => router.push('/')}
              className="flex-1 bg-surface-elevated rounded-xl p-4 border border-border active:opacity-80"
            >
              <Text className="text-3xl mb-2 text-center">🧮</Text>
              <Text className="text-sm font-semibold text-text-primary text-center">
                Новый расчет
              </Text>
            </Pressable>
            <Pressable
              onPress={() => router.push('/calculators')}
              className="flex-1 bg-surface-elevated rounded-xl p-4 border border-border active:opacity-80"
            >
              <Text className="text-3xl mb-2 text-center">🔍</Text>
              <Text className="text-sm font-semibold text-text-primary text-center">
                Калькуляторы
              </Text>
            </Pressable>
          </View>
        </View>

        {/* Top Calculators */}
        {topCalculators.length > 0 ? (
          <View className="bg-surface-elevated rounded-2xl p-5 mb-6 border border-border">
            <Text className="text-lg font-bold text-text-primary mb-4">
              Чаще всего используете
            </Text>
            <View className="gap-3">
              {topCalculators.map(([name, count], index) => (
                <View key={name} className="flex-row items-center justify-between">
                  <View className="flex-row items-center flex-1">
                    <View className="w-8 h-8 bg-primary rounded-full items-center justify-center mr-3">
                      <Text className="text-sm font-bold text-text-inverse">
                        {index + 1}
                      </Text>
                    </View>
                    <Text className="text-sm font-medium text-text-primary flex-1" numberOfLines={1}>
                      {name}
                    </Text>
                  </View>
                  <View className="bg-primary-light px-3 py-1 rounded-full">
                    <Text className="text-xs font-bold text-primary">
                      {count}
                    </Text>
                  </View>
                </View>
              ))}
            </View>
          </View>
        ) : null}

        {/* Categories Distribution */}
        {Object.keys(categoryUsage).length > 0 ? (
          <View className="bg-surface-elevated rounded-2xl p-5 mb-6 border border-border">
            <Text className="text-lg font-bold text-text-primary mb-4">
              По категориям
            </Text>
            <View className="gap-3">
              {Object.entries(categoryUsage)
                .sort(([, a], [, b]) => b - a)
                .slice(0, 4)
                .map(([category, count]) => (
                  <View key={category} className="flex-row items-center justify-between">
                    <View className="flex-row items-center flex-1">
                      <Text className="text-2xl mr-3">
                        {getCategoryIcon(category)}
                      </Text>
                      <Text className="text-sm font-medium text-text-primary capitalize">
                        {category}
                      </Text>
                    </View>
                    <Text className="text-base font-semibold text-text-primary">
                      {count}
                    </Text>
                  </View>
                ))}
            </View>
          </View>
        ) : null}

        {/* Recent Activity */}
        <View className="bg-surface-elevated rounded-2xl p-5 mb-6 border border-border">
          <View className="flex-row items-center justify-between mb-4">
            <Text className="text-lg font-bold text-text-primary">
              Недавние расчеты
            </Text>
            <Pressable
              onPress={() => router.push('/dashboard/history')}
              className="active:opacity-70"
            >
              <Text className="text-sm font-semibold text-primary">
                Все →
              </Text>
            </Pressable>
          </View>
          {recentResults.length > 0 ? (
            <View className="gap-3">
              {recentResults.map((result) => (
                <Pressable
                  key={result.id}
                  onPress={() => router.push(`/result/${result.id}`)}
                  className="bg-surface rounded-xl p-4 border border-border active:opacity-70"
                >
                  <View className="flex-row items-center justify-between">
                    <View className="flex-1">
                      <Text className="text-sm font-semibold text-text-primary mb-1" numberOfLines={1}>
                        {result.calculator?.name || 'Calculator'}
                      </Text>
                      <Text className="text-xs text-text-secondary">
                        {new Date(result.performedAt).toLocaleDateString('ru-RU')}
                      </Text>
                    </View>
                    <Text className="text-xl ml-2">→</Text>
                  </View>
                </Pressable>
              ))}
            </View>
          ) : (
            <View className="py-8">
              <Text className="text-center text-text-secondary mb-4">
                Пока нет расчетов
              </Text>
              <Pressable
                onPress={() => router.push('/')}
                className="bg-primary rounded-xl py-3 active:opacity-80"
              >
                <Text className="text-base font-semibold text-text-inverse text-center">
                  Начать расчеты
                </Text>
              </Pressable>
            </View>
          )}
        </View>
      </View>
    </ScrollView>
  );
}
