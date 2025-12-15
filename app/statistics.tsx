import React, { useEffect } from 'react';
import { View, Text, ScrollView, Pressable } from 'react-native';
import { router } from 'expo-router';
import { useCalculationResultsStore } from '@/stores/calculationResultsStore';
import { useAuth } from '@/hooks/useAuth';

/**
 * Statistics Screen
 * Displays usage metrics and frequency charts
 */

export default function StatisticsScreen() {
  const { user, isAuthenticated } = useAuth();
  const { items: results, loading, error, fetchAll } = useCalculationResultsStore();

  useEffect(() => {
    if (isAuthenticated) {
      fetchAll();
    }
  }, [isAuthenticated]);

  // Calculate statistics
  const totalCalculations = results.length;
  
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

  const last7Days = results.filter((result) => {
    const resultDate = new Date(result.performedAt);
    const today = new Date();
    const diffTime = Math.abs(today.getTime() - resultDate.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays <= 7;
  }).length;

  const last30Days = results.filter((result) => {
    const resultDate = new Date(result.performedAt);
    const today = new Date();
    const diffTime = Math.abs(today.getTime() - resultDate.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays <= 30;
  }).length;

  const topCalculators = Object.entries(calculatorUsage)
    .sort(([, a], [, b]) => b - a)
    .slice(0, 5);

  const getPercentage = (count: number) => {
    return totalCalculations > 0 ? ((count / totalCalculations) * 100).toFixed(1) : '0';
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'cardiology': return '❤️';
      case 'endocrinology': return '🔬';
      case 'neurology': return '🧠';
      case 'pediatrics': return '👶';
      case 'general': return '⚕️';
      default: return '📊';
    }
  };

  // Show login prompt if not authenticated
  if (!isAuthenticated) {
    return (
      <View className="flex-1 bg-surface">
        <View className="bg-primary px-6 pt-16 pb-8">
          <Pressable onPress={() => router.back()} className="mb-4 active:opacity-70">
            <Text className="text-text-inverse text-lg">← Назад</Text>
          </Pressable>
          <Text className="text-2xl font-bold text-text-inverse mb-2">
            Статистика использования
          </Text>
        </View>
        <View className="flex-1 px-6 py-8 justify-center">
          <View className="bg-info-bg border border-info rounded-xl p-6">
            <Text className="text-xl mb-4 text-center">🔒</Text>
            <Text className="text-lg font-semibold text-text-primary text-center mb-2">
              Требуется вход
            </Text>
            <Text className="text-sm text-text-secondary text-center mb-6">
              Пожалуйста, войдите, чтобы просмотреть статистику
            </Text>
            <Pressable
              onPress={() => router.push('/(auth)/sign-in')}
              className="bg-primary rounded-xl py-3 active:opacity-80"
            >
              <Text className="text-base font-semibold text-text-inverse text-center">
                Войти
              </Text>
            </Pressable>
            <Pressable
              onPress={() => router.push('/(auth)/sign-up')}
              className="mt-3 active:opacity-70"
            >
              <Text className="text-sm text-primary text-center">
                Нет аккаунта? Зарегистрироваться
              </Text>
            </Pressable>
          </View>
        </View>
      </View>
    );
  }

  return (
    <View className="flex-1 bg-surface">
      {/* Header */}
      <View className="bg-primary px-6 pt-16 pb-8">
        <Pressable onPress={() => router.back()} className="mb-4 active:opacity-70">
          <Text className="text-text-inverse text-lg">← Back</Text>
        </Pressable>
        <Text className="text-2xl font-bold text-text-inverse mb-2">
          Usage Statistics
        </Text>
        <Text className="text-sm text-text-inverse opacity-90">
          Обзор вашей активности
        </Text>
      </View>

      <ScrollView className="flex-1 px-6 py-6">
        {loading ? (
          <View className="bg-surface-elevated rounded-2xl p-6 border border-border">
            <Text className="text-center text-text-secondary">Загрузка статистики...</Text>
          </View>
        ) : error ? (
          <View className="bg-danger-bg border border-danger rounded-xl p-4">
            <Text className="text-danger-text text-sm">{error}</Text>
          </View>
        ) : (
          <>
            {/* Overview Cards */}
            <View className="flex-row gap-3 mb-6">
              <View className="flex-1 bg-gradient-to-br from-primary to-primary-dark rounded-2xl p-5">
                <Text className="text-4xl font-bold text-text-inverse mb-1">
                  {totalCalculations}
                </Text>
                <Text className="text-sm text-text-inverse opacity-80">
                  Всего расчетов
                </Text>
              </View>
              <View className="flex-1 bg-gradient-to-br from-secondary to-secondary-dark rounded-2xl p-5">
                <Text className="text-4xl font-bold text-text-inverse mb-1">
                  {Object.keys(calculatorUsage).length}
                </Text>
                <Text className="text-sm text-text-inverse opacity-80">
                  Использовано калькуляторов
                </Text>
              </View>
            </View>

            {/* Time-based Stats */}
            <View className="bg-surface-elevated rounded-2xl p-6 mb-6 border border-border">
              <Text className="text-lg font-bold text-text-primary mb-4">
                Последняя активность
              </Text>
              <View className="gap-3">
                <View className="flex-row justify-between items-center py-2">
                  <Text className="text-sm text-text-secondary">Последние 7 дней</Text>
                  <Text className="text-2xl font-bold text-primary">
                    {last7Days}
                  </Text>
                </View>
                <View className="flex-row justify-between items-center py-2">
                  <Text className="text-sm text-text-secondary">Последние 30 дней</Text>
                  <Text className="text-2xl font-bold text-primary">
                    {last30Days}
                  </Text>
                </View>
              </View>
            </View>

            {/* Top Calculators */}
            <View className="bg-surface-elevated rounded-2xl p-6 mb-6 border border-border">
              <Text className="text-lg font-bold text-text-primary mb-4">
                Чаще всего используемые
              </Text>
              {topCalculators.length > 0 ? (
                <View className="gap-3">
                  {topCalculators.map(([name, count], index) => (
                    <View key={name} className="gap-2">
                      <View className="flex-row justify-between items-center">
                        <View className="flex-row items-center flex-1">
                          <Text className="text-lg font-bold text-primary mr-2">
                            {index + 1}.
                          </Text>
                          <Text className="text-sm font-medium text-text-primary flex-1" numberOfLines={1}>
                            {name}
                          </Text>
                        </View>
                        <Text className="text-base font-semibold text-text-primary ml-2">
                          {count}
                        </Text>
                      </View>
                      <View className="bg-surface h-2 rounded-full overflow-hidden">
                        <View
                          className="bg-primary h-full rounded-full"
                          style={{ width: `${getPercentage(count)}%` as any }}
                        />
                      </View>
                    </View>
                  ))}
                </View>
              ) : (
                <Text className="text-center text-text-secondary py-4">
                  Пока нет расчетов
                </Text>
              )}
            </View>

            {/* Category Distribution */}
            <View className="bg-surface-elevated rounded-2xl p-6 mb-6 border border-border">
              <Text className="text-lg font-bold text-text-primary mb-4">
                По категориям
              </Text>
              {Object.keys(categoryUsage).length > 0 ? (
                <View className="gap-3">
                  {Object.entries(categoryUsage)
                    .sort(([, a], [, b]) => b - a)
                    .map(([category, count]) => (
                      <View key={category} className="flex-row items-center justify-between py-2">
                        <View className="flex-row items-center flex-1">
                          <Text className="text-2xl mr-3">
                            {getCategoryIcon(category)}
                          </Text>
                          <Text className="text-sm font-medium text-text-primary capitalize">
                            {category}
                          </Text>
                        </View>
                        <View className="flex-row items-center">
                          <Text className="text-base font-semibold text-text-primary mr-2">
                            {count}
                          </Text>
                          <Text className="text-xs text-text-muted">
                            ({getPercentage(count)}%)
                          </Text>
                        </View>
                      </View>
                    ))}
                </View>
              ) : (
                <Text className="text-center text-text-secondary py-4">
                  No data available
                </Text>
              )}
            </View>

            {/* Info Note */}
            <View className="bg-info-bg border border-info rounded-xl p-4">
              <View className="flex-row items-start">
                <Text className="text-xl mr-3">💡</Text>
                <View className="flex-1">
                  <Text className="text-sm font-medium text-info-text mb-1">
                    Statistics Info
                  </Text>
                  <Text className="text-xs text-text-secondary">
                    These statistics are based on your personal calculation history. Data is stored locally and securely.
                  </Text>
                </View>
              </View>
            </View>
          </>
        )}
      </ScrollView>
    </View>
  );
}
