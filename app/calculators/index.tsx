import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, Pressable, TextInput } from 'react-native';
import { router, useLocalSearchParams } from 'expo-router';
import { useCalculatorsStore } from '@/stores/calculatorsStore';

/**
 * Calculators List Screen
 * Displays all calculators with filtering and search
 */

const categories = [
  { id: 'all', name: 'Все' },
  { id: 'cardiology', name: 'Кардиология' },
  { id: 'endocrinology', name: 'Эндокринология' },
  { id: 'neurology', name: 'Неврология' },
  { id: 'pediatrics', name: 'Педиатрия' },
];

export default function CalculatorsListScreen() {
  const params = useLocalSearchParams();
  const { items: calculators, loading, error, fetchAll } = useCalculatorsStore();
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState(
    (params.category as string) || 'all'
  );

  useEffect(() => {
    fetchAll();
  }, []);

  // Normalize search and category filtering using `categoryId` created by the store
  const filteredCalculators = calculators.filter((calc) => {
    const matchesSearch = calc.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      calc.description.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || calc.categoryId === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const handleCalculatorPress = (id: string) => {
    router.push(`/calculator/${id}`);
  };

  return (
    <View className="flex-1 bg-surface">
      {/* Header */}
      <View className="bg-primary px-6 pt-16 pb-6">
        <Text className="text-2xl font-bold text-text-inverse mb-2">
          Все калькуляторы
        </Text>
        <Text className="text-sm text-text-inverse opacity-90">
          Доступно {filteredCalculators.length} калькуляторов
        </Text>
      </View>

      {/* Search Bar */}
      <View className="px-6 pt-4 pb-3">
        <TextInput
          value={searchQuery}
          onChangeText={setSearchQuery}
          placeholder="Поиск калькуляторов..."
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
                key={category.id}
                onPress={() => setSelectedCategory(category.id)}
                className={`rounded-full px-5 py-2 border ${
                  selectedCategory === category.id
                    ? 'bg-primary border-primary'
                    : 'bg-surface-elevated border-border'
                } active:opacity-70`}
              >
                <Text
                  className={`text-sm font-medium ${
                    selectedCategory === category.id
                      ? 'text-text-inverse'
                      : 'text-text-secondary'
                  }`}
                >
                  {category.name}
                </Text>
              </Pressable>
            ))}
          </View>
        </ScrollView>
      </View>

      {/* Calculators List */}
      <ScrollView className="flex-1 px-6">
        {loading ? (
          <View className="bg-surface-elevated rounded-2xl p-6 border border-border">
            <Text className="text-center text-text-secondary">Загрузка калькуляторов...</Text>
          </View>
        ) : error ? (
          <View className="bg-danger-bg border border-danger rounded-xl p-4">
            <Text className="text-danger-text text-sm">{error}</Text>
          </View>
        ) : filteredCalculators.length === 0 ? (
          <View className="bg-surface-elevated rounded-2xl p-6 border border-border">
            <Text className="text-center text-text-secondary">
              Нет калькуляторов, соответствующих вашему запросу.
            </Text>
          </View>
        ) : (
          <View className="gap-3 pb-6">
            {/* Group calculators by categoryId */}
            {Object.entries(
              filteredCalculators.reduce((acc: Record<string, any[]>, calc) => {
                const key = calc.categoryId || 'other';
                acc[key] = acc[key] || [];
                acc[key].push(calc);
                return acc;
              }, {})
            ).map(([categoryId, items]) => (
              <View key={categoryId} className="mb-6">
                <Text className="text-sm font-semibold text-text-primary mb-3">{categoryId === 'cardiology' ? 'Кардиология' : categoryId === 'endocrinology' ? 'Эндокринология' : categoryId === 'neurology' ? 'Неврология' : categoryId === 'pediatrics' ? 'Педиатрия' : 'Прочее'}</Text>
                {items.map((calculator: any) => (
                  <Pressable
                    key={calculator.id}
                    onPress={() => handleCalculatorPress(calculator.id)}
                    className="bg-surface-elevated rounded-2xl p-5 border border-border active:opacity-70 mb-3"
                  >
                    <View className="flex-row items-start mb-3">
                      <View className="w-12 h-12 rounded-full bg-primary-light items-center justify-center mr-4">
                        <Text className="text-2xl">
                          {categoryId === 'cardiology' ? '❤️' : categoryId === 'endocrinology' ? '🔬' : categoryId === 'neurology' ? '🧠' : categoryId === 'pediatrics' ? '👶' : '⚕️'}
                        </Text>
                      </View>
                      <View className="flex-1">
                        <Text className="text-base font-semibold text-text-primary mb-1">
                          {calculator.name}
                        </Text>
                        <Text className="text-xs text-text-secondary capitalize mb-2">
                          {calculator.category}
                        </Text>
                        <Text className="text-sm text-text-secondary" numberOfLines={2}>
                          {calculator.description}
                        </Text>
                      </View>
                      <Text className="text-text-muted text-lg ml-2">→</Text>
                    </View>
                  </Pressable>
                ))}
              </View>
            ))}
          </View>
        )}
      </ScrollView>
    </View>
  );
}
