/**
 * Dashboard History Screen
 * Shows user's calculation history with real data
 */

import React, { useEffect } from 'react';
import { View, Text, ScrollView, Pressable, ActivityIndicator } from 'react-native';
import { router } from 'expo-router';
import { useAuth } from '@/hooks/useAuth';
import { useCalculationResultsStore } from '@/stores/calculationResultsStore';

export default function DashboardHistoryScreen() {
  const { isAuthenticated, isLoading: authLoading } = useAuth();
  const { items, loading, fetchAll } = useCalculationResultsStore();

  // Load calculation history only when authenticated
  useEffect(() => {
    if (!authLoading && isAuthenticated) {
      fetchAll();
    } else if (!authLoading && !isAuthenticated) {
      router.replace('/(auth)/sign-in');
    }
  }, [isAuthenticated, authLoading, fetchAll]);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInMs = now.getTime() - date.getTime();
    const diffInHours = Math.floor(diffInMs / (1000 * 60 * 60));
    const diffInDays = Math.floor(diffInHours / 24);

    if (diffInHours < 1) {
      return 'Менее часа назад';
    } else if (diffInHours < 24) {
      return `${diffInHours} ч. назад`;
    } else if (diffInDays < 7) {
      return `${diffInDays} д. назад`;
    } else {
      return date.toLocaleDateString('ru-RU', {
        day: 'numeric',
        month: 'short',
        year: date.getFullYear() !== now.getFullYear() ? 'numeric' : undefined,
      });
    }
  };

  return (
    <View className="flex-1 bg-surface">
      <ScrollView className="flex-1 px-6 py-8">
        {/* Page Title */}
        <Text className="text-3xl font-bold text-text-primary mb-2">
          История
        </Text>
        <Text className="text-base text-text-secondary mb-6">
          Все ваши расчёты
        </Text>

        {/* Loading State */}
        {loading && items.length === 0 ? (
          <View className="items-center justify-center py-12">
            <ActivityIndicator size="large" color="hsl(210, 75%, 45%)" />
            <Text className="text-text-secondary mt-4">Загрузка...</Text>
          </View>
        ) : items.length === 0 ? (
          /* Empty State */
          <View className="bg-surface-elevated rounded-2xl p-8 border border-border items-center">
            <Text className="text-5xl mb-4">📅</Text>
            <Text className="text-lg font-semibold text-text-primary mb-2 text-center">
              Пока нет истории
            </Text>
            <Text className="text-sm text-text-secondary mb-6 text-center">
              Выполните первый расчёт
            </Text>
            <Pressable
              onPress={() => router.push('/')}
              className="bg-primary px-6 py-3 rounded-xl active:opacity-80"
            >
              <Text className="text-base font-semibold text-text-inverse">
                К калькуляторам
              </Text>
            </Pressable>
          </View>
        ) : (
          /* Calculation History List */
          <View className="gap-4">
            {items.map((result) => (
              <View
                key={result.id}
                className="bg-surface-elevated rounded-2xl p-5 border border-border"
              >
                <View className="flex-row items-start justify-between mb-3">
                  <View className="flex-1">
                    <Text className="text-lg font-bold text-text-primary mb-1">
                      {result.calculatorName || 'Калькулятор'}
                    </Text>
                    <Text className="text-sm text-text-secondary">
                      {formatDate(result.createdAt)}
                    </Text>
                  </View>
                  <View className="bg-primary-light px-3 py-1 rounded-lg">
                    <Text className="text-sm font-semibold text-primary">
                      {result.resultValue}
                    </Text>
                  </View>
                </View>

                {/* Input Parameters */}
                {result.inputData && Object.keys(result.inputData).length > 0 ? (
                  <View className="bg-surface rounded-xl p-3 mb-3">
                    <Text className="text-xs font-semibold text-text-secondary mb-2">
                      ПАРАМЕТРЫ
                    </Text>
                    <View className="gap-1">
                      {Object.entries(result.inputData).map(([key, value]) => (
                        <View key={key} className="flex-row justify-between">
                          <Text className="text-sm text-text-secondary">{key}:</Text>
                          <Text className="text-sm font-medium text-text-primary">
                            {String(value)}
                          </Text>
                        </View>
                      ))}
                    </View>
                  </View>
                ) : null}

                {/* Interpretation */}
                {result.interpretation ? (
                  <View className="bg-info-light border border-info rounded-xl p-3">
                    <Text className="text-xs font-semibold text-info mb-1">
                      ИНТЕРПРЕТАЦИЯ
                    </Text>
                    <Text className="text-sm text-text-primary">
                      {result.interpretation}
                    </Text>
                  </View>
                ) : null}
              </View>
            ))}
          </View>
        )}

        {/* Bottom spacing for navigation */}
        <View style={{ height: 100 }} />
      </ScrollView>
    </View>
  );
}
