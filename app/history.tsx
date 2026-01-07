import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, Pressable, TextInput } from 'react-native';
import { router } from 'expo-router';
import { useCalculationResultsStore } from '@/stores/calculationResultsStore';
import { CalculationResult } from '@/types/calculation_results';
import { useAuth } from '@/hooks/useAuth';

/**
 * History Screen
 * Displays user's calculation history with filtering and search
 */

export default function HistoryScreen() {
  const { user, isAuthenticated } = useAuth();
  const { items: results, loading, error, fetchAll } = useCalculationResultsStore();
  const [searchQuery, setSearchQuery] = useState('');
  const [filterCategory, setFilterCategory] = useState('all');

  useEffect(() => {
    if (isAuthenticated) {
      fetchAll();
    }
  }, [isAuthenticated]);

  const categories = ['all', ...new Set(results.map((r) => r.calculator?.category).filter(Boolean))];

  const filteredResults = results.filter((result) => {
    const matchesSearch = 
      result.calculator?.name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      result.interpretation.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = 
      filterCategory === 'all' || result.calculator?.category === filterCategory;
    return matchesSearch && matchesCategory;
  });

  const handleResultPress = (id: number) => {
    router.push(`/result/${id}`);
  };

  const getResultIcon = (interpretation: string) => {
    const lower = interpretation.toLowerCase();
    if (lower.includes('critical') || lower.includes('severe')) return '🚨';
    if (lower.includes('danger') || lower.includes('class ii')) return '⚠️';
    if (lower.includes('warning') || lower.includes('caution')) return '⚡';
    if (lower.includes('normal') || lower.includes('healthy')) return '✅';
    return 'ℹ️';
  };

  const getResultColor = (interpretation: string) => {
    const lower = interpretation.toLowerCase();
    if (lower.includes('critical') || lower.includes('severe') || lower.includes('danger')) {
      return 'bg-danger-bg border-danger';
    }
    if (lower.includes('warning') || lower.includes('caution')) {
      return 'bg-warning-bg border-warning';
    }
    if (lower.includes('normal') || lower.includes('healthy')) {
      return 'bg-success-bg border-success';
    }
    return 'bg-info-bg border-info';
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
            История расчетов
          </Text>
        </View>
        <View className="flex-1 px-6 py-8 justify-center">
          <View className="bg-info-bg border border-info rounded-xl p-6">
            <Text className="text-xl mb-4 text-center">🔒</Text>
            <Text className="text-lg font-semibold text-text-primary text-center mb-2">
              Требуется вход
            </Text>
            <Text className="text-sm text-text-secondary text-center mb-6">
              Пожалуйста, войдите, чтобы просмотреть историю расчетов
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
      <View className="bg-primary px-6 pt-16 pb-6">
        <Pressable onPress={() => router.back()} className="mb-4 active:opacity-70">
          <Text className="text-text-inverse text-lg">← Назад</Text>
        </Pressable>
        <Text className="text-2xl font-bold text-text-inverse mb-2">
          История расчетов
        </Text>
        <Text className="text-sm text-text-inverse opacity-90">
          Найдено {filteredResults.length} расчетов
        </Text>
      </View>

      {/* Search Bar */}
      <View className="px-6 pt-4 pb-3">
        <TextInput
          value={searchQuery}
          onChangeText={setSearchQuery}
          placeholder="Поиск по истории..."
          placeholderTextColor="#A0A0A0"
          className="bg-surface-elevated border border-border rounded-xl px-4 py-3 text-base text-text-primary"
        />
      </View>

      {/* Category Filter */}
      <View className="px-6 pb-4">
        <ScrollView horizontal showsHorizontalScrollIndicator={false}>
          <View className="flex-row gap-2">
            {categories.map((category) => (
              <Pressable
                key={category}
                onPress={() => setFilterCategory(category as string)}
                className={`rounded-full px-5 py-2 border ${
                  filterCategory === category
                    ? 'bg-primary border-primary'
                    : 'bg-surface-elevated border-border'
                } active:opacity-70`}
              >
                <Text
                  className={`text-sm font-medium capitalize ${
                    filterCategory === category
                      ? 'text-text-inverse'
                      : 'text-text-secondary'
                  }`}
                >
                  {category}
                </Text>
              </Pressable>
            ))}
          </View>
        </ScrollView>
      </View>

      {/* Results List */}
      <ScrollView className="flex-1 px-6">
        {loading ? (
          <View className="bg-surface-elevated rounded-2xl p-6 border border-border">
            <Text className="text-center text-text-secondary">Загрузка истории...</Text>
          </View>
        ) : error ? (
          <View className="bg-danger-bg border border-danger rounded-xl p-4">
            <Text className="text-danger-text text-sm">{error}</Text>
          </View>
        ) : filteredResults.length === 0 ? (
          <View className="bg-surface-elevated rounded-2xl p-6 border border-border">
            <Text className="text-center text-text-secondary mb-2">
              {searchQuery || filterCategory !== 'all' 
                ? 'Нет расчетов, соответствующих запросу'
                : 'Пока нет расчетов'}
            </Text>
            {!searchQuery && filterCategory === 'all' ? (
              <Pressable onPress={() => router.push('/')} className="mt-4 active:opacity-70">
                <Text className="text-center text-primary font-medium">
                  Начать расчеты
                </Text>
              </Pressable>
            ) : null}
          </View>
        ) : (
          <View className="gap-3 pb-6">
            {filteredResults.map((result) => (
              <Pressable
                key={result.id}
                onPress={() => handleResultPress(result.id)}
                className={`rounded-2xl p-5 border ${getResultColor(result.interpretation)} active:opacity-70`}
              >
                <View className="flex-row items-start mb-3">
                  <View className="flex-1">
                    <View className="flex-row items-center mb-2">
                      <Text className="text-xl mr-2">
                        {getResultIcon(result.interpretation)}
                      </Text>
                      <Text className="text-base font-semibold text-text-primary">
                        {result.calculator?.name || 'Calculator'}
                      </Text>
                    </View>
                    <Text className="text-xs text-text-secondary capitalize mb-1">
                      {result.calculator?.category}
                    </Text>
                    <Text className="text-xs text-text-muted">
                      {new Date(result.performedAt).toLocaleString('ru-RU')}
                    </Text>
                  </View>
                  <View className="items-end ml-3">
                      <Text className="text-2xl font-bold text-text-primary">
                        {(() => {
                          const v = (result as any).resultValue;
                          if (typeof v === 'number' && isFinite(v)) return v.toFixed(1);
                          if (typeof v === 'string' && v.trim() !== '' && !isNaN(Number(v))) return Number(v).toFixed(1);
                          return '-';
                        })()}
                      </Text>
                    <Text className="text-xs text-text-muted mt-1">→</Text>
                  </View>
                </View>
                
                <View className="bg-surface rounded-xl p-3 mt-2">
                  <Text className="text-sm text-text-secondary" numberOfLines={2}>
                    {result.interpretation}
                  </Text>
                </View>
              </Pressable>
            ))}
          </View>
        )}
      </ScrollView>
    </View>
  );
}
