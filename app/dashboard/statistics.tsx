/**
 * Dashboard Statistics Screen
 * User calculations statistics and history
 */

import React, { useState, useEffect } from 'react';
import { View, Text, ScrollView, ActivityIndicator, Pressable } from 'react-native';
import { router } from 'expo-router';
import { useAuth } from '@/hooks/useAuth';
import { useCalculationResultsStore } from '@/stores/calculationResultsStore';

export default function DashboardStatisticsScreen() {
  const { isAuthenticated, isLoading } = useAuth();
  const { items: results, loading, fetchAll } = useCalculationResultsStore();
  const [totalCalculations, setTotalCalculations] = useState(0);
  const [recentCalculations, setRecentCalculations] = useState(0);
  const [calculatorStats, setCalculatorStats] = useState<Record<string, number>>({});

  // Redirect if not authenticated
  useEffect(() => {
    if (!isAuthenticated && !isLoading) {
      router.replace('/(auth)/sign-in');
    }
  }, [isAuthenticated, isLoading]);

  // Load calculation results
  useEffect(() => {
    if (isAuthenticated) {
      fetchAll();
    }
  }, [isAuthenticated, fetchAll]);

  // Calculate statistics
  useEffect(() => {
    if (results.length > 0) {
      setTotalCalculations(results.length);

      // Count recent calculations (last 7 days)
      const sevenDaysAgo = new Date();
      sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);
      const recent = results.filter((result: any) => {
        const performedAt = new Date(result.performedAt);
        return performedAt >= sevenDaysAgo;
      });
      setRecentCalculations(recent.length);

      // Count by calculator type
      const stats: Record<string, number> = {};
      results.forEach((result: any) => {
        const name = result.calculatorNameRu || result.calculatorName || 'Неизвестный';
        stats[name] = (stats[name] || 0) + 1;
      });
      setCalculatorStats(stats);
    }
  }, [results]);

  if (isLoading || !isAuthenticated) {
    return null;
  }

  return (
    <ScrollView className="flex-1 bg-surface">
      <View className="px-6 py-8">
        {/* Header */}
        <View className="mb-6">
          <Text className="text-3xl font-bold text-text-primary mb-2">
            Статистика
          </Text>
          <Text className="text-base text-text-secondary">
            Ваша активность и история расчётов
          </Text>
        </View>

        {loading ? (
          <View className="items-center justify-center py-12">
            <ActivityIndicator size="large" color="#6366f1" />
            <Text className="text-text-secondary mt-4">Загрузка статистики...</Text>
          </View>
        ) : (
          <>
            {/* Overview Cards */}
            <View className="mb-6">
              <Text className="text-lg font-bold text-text-primary mb-4">
                Общая статистика
              </Text>
              <View className="flex-row gap-3 mb-3">
                <View className="flex-1 bg-surface-elevated border border-border rounded-xl p-4">
                  <Text className="text-4xl font-bold text-primary mb-1">
                    {totalCalculations}
                  </Text>
                  <Text className="text-sm text-text-secondary">
                    Всего расчётов
                  </Text>
                </View>
                <View className="flex-1 bg-surface-elevated border border-border rounded-xl p-4">
                  <Text className="text-4xl font-bold text-success mb-1">
                    {recentCalculations}
                  </Text>
                  <Text className="text-sm text-text-secondary">
                    За 7 дней
                  </Text>
                </View>
              </View>
            </View>

            {/* Calculator Type Breakdown */}
            {Object.keys(calculatorStats).length > 0 ? (
              <View className="mb-6">
                <Text className="text-lg font-bold text-text-primary mb-4">
                  По типам калькуляторов
                </Text>
                <View className="bg-surface-elevated border border-border rounded-xl p-4">
                  {Object.entries(calculatorStats)
                    .sort(([, a], [, b]) => b - a)
                    .map(([name, count], index) => (
                      <View
                        key={name}
                        className={`flex-row items-center justify-between py-3 ${
                          index !== Object.keys(calculatorStats).length - 1
                            ? 'border-b border-border'
                            : ''
                        }`}
                      >
                        <Text className="text-base text-text-primary flex-1">
                          {name}
                        </Text>
                        <View className="flex-row items-center gap-2">
                          <View className="bg-primary-light rounded-lg px-3 py-1">
                            <Text className="text-sm font-semibold text-primary">
                              {count}
                            </Text>
                          </View>
                          <Text className="text-sm text-text-muted w-12 text-right">
                            {Math.round((count / totalCalculations) * 100)}%
                          </Text>
                        </View>
                      </View>
                    ))}
                </View>
              </View>
            ) : null}

            {/* Recent History */}
            {results.length > 0 ? (
              <View className="mb-6">
                <View className="flex-row items-center justify-between mb-4">
                  <Text className="text-lg font-bold text-text-primary">
                    Последние расчёты
                  </Text>
                  <Pressable
                    onPress={() => router.push('/dashboard/history')}
                    className="active:opacity-70"
                  >
                    <Text className="text-sm font-medium text-primary">
                      Показать все →
                    </Text>
                  </Pressable>
                </View>
                <View className="bg-surface-elevated border border-border rounded-xl overflow-hidden">
                  {results.slice(0, 5).map((result: any, index: number) => {
                    const date = new Date(result.performedAt);
                    const formattedDate = date.toLocaleDateString('ru-RU', {
                      day: 'numeric',
                      month: 'short',
                      year: 'numeric',
                    });
                    const formattedTime = date.toLocaleTimeString('ru-RU', {
                      hour: '2-digit',
                      minute: '2-digit',
                    });

                    return (
                      <View
                        key={result.id}
                        className={`p-4 ${
                          index !== results.slice(0, 5).length - 1
                            ? 'border-b border-border'
                            : ''
                        }`}
                      >
                        <View className="flex-row items-start justify-between mb-2">
                          <Text className="text-base font-semibold text-text-primary flex-1">
                            {result.calculatorNameRu || result.calculatorName || 'Расчёт'}
                          </Text>
                          <View className="bg-primary-light rounded-lg px-3 py-1">
                            <Text className="text-sm font-bold text-primary">
                              {result.resultValue?.toFixed(2)}
                            </Text>
                          </View>
                        </View>
                        <Text className="text-xs text-text-muted">
                          {formattedDate} в {formattedTime}
                        </Text>
                      </View>
                    );
                  })}
                </View>
              </View>
            ) : (
              <View className="bg-surface-elevated border border-border rounded-xl p-8 items-center">
                <Text className="text-6xl mb-4">📊</Text>
                <Text className="text-lg font-semibold text-text-primary mb-2">
                  Нет расчётов
                </Text>
                <Text className="text-sm text-text-secondary text-center mb-6">
                  Начните использовать калькуляторы, чтобы увидеть статистику
                </Text>
                <Pressable
                  onPress={() => router.push('/')}
                  className="bg-primary px-6 py-3 rounded-xl active:opacity-80"
                >
                  <Text className="text-base font-semibold text-text-inverse">
                    Перейти к калькуляторам
                  </Text>
                </Pressable>
              </View>
            )}
          </>
        )}
      </View>
    </ScrollView>
  );
}
