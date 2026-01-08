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
  { id: 'General Health', name: 'Общее здоровье' },
  { id: 'Cardiology', name: 'Кардиология' },
  { id: 'Nephrology', name: 'Нефрология' },
  { id: 'Neurology', name: 'Неврология' },
  { id: 'Pediatrics', name: 'Педиатрия' },
  { id: 'Obstetrics', name: 'Акушерство' },
  { id: 'Hematology', name: 'Гематология' },
  { id: 'Laboratory', name: 'Лабораторная' },
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

  // Normalize search and category filtering using `category` field
  const filteredCalculators = calculators.filter((calc) => {
    const matchesSearch = (calc.nameRu || calc.name).toLowerCase().includes(searchQuery.toLowerCase()) ||
      (calc.descriptionRu || calc.description).toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || calc.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const handleCalculatorPress = (id: string | number) => {
    router.push(`/calculator/${id}`);
  };

  return (
    <View className="flex-1 bg-surface">
      {/* Header - Mobile Optimized */}
      <View className="bg-primary px-4 pt-12 pb-4">
        <Text className="text-xl font-bold text-text-inverse mb-1">
          Все калькуляторы
        </Text>
        <Text className="text-xs text-text-inverse opacity-90">
          Доступно {filteredCalculators.length} калькуляторов
        </Text>
      </View>

      {/* Search Bar - Mobile Optimized */}
      <View className="px-4 pt-3 pb-2">
        <TextInput
          value={searchQuery}
          onChangeText={setSearchQuery}
          placeholder="Поиск калькуляторов..."
          placeholderTextColor="#A0A0A0"
          className="bg-surface-elevated border border-border rounded-xl px-3 py-2.5 text-sm text-text-primary"
        />
      </View>

      {/* Category Filter - Mobile Optimized */}
      <View className="px-4 pb-3">
        <ScrollView horizontal showsHorizontalScrollIndicator={false}>
          <View className="flex-row gap-2">
            {categories.map((category) => (
              <Pressable
                key={category.id}
                onPress={() => setSelectedCategory(category.id)}
                className={`rounded-full px-4 py-1.5 border ${
                  selectedCategory === category.id
                    ? 'bg-primary border-primary'
                    : 'bg-surface-elevated border-border'
                } active:opacity-70`}
              >
                <Text
                  className={`text-xs font-medium ${
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

      {/* Calculators List - Mobile Optimized */}
      <ScrollView className="flex-1 px-4" contentContainerStyle={{ paddingBottom: 80 }}>
        {loading ? (
          <View className="bg-surface-elevated rounded-2xl p-4 border border-border">
            <Text className="text-center text-text-secondary text-sm">Загрузка калькуляторов...</Text>
          </View>
        ) : error ? (
          <View className="bg-danger-bg border border-danger rounded-xl p-3">
            <Text className="text-danger-text text-xs">{error}</Text>
          </View>
        ) : filteredCalculators.length === 0 ? (
          <View className="bg-surface-elevated rounded-2xl p-4 border border-border">
            <Text className="text-center text-text-secondary text-sm">
              Нет калькуляторов, соответствующих вашему запросу.
            </Text>
          </View>
        ) : (
          <View className="gap-2 pb-4">
            {/* Group calculators by category */}
            {Object.entries(
              filteredCalculators.reduce((acc: Record<string, any[]>, calc) => {
                const key = calc.category || 'other';
                acc[key] = acc[key] || [];
                acc[key].push(calc);
                return acc;
              }, {})
            ).map(([categoryId, items]) => (
              <View key={categoryId} className="mb-3">
                <Text className="text-xs font-semibold text-text-primary mb-2 uppercase tracking-wide">
                  {categoryId === 'General Health' ? '⚕️ Общее здоровье'
                    : categoryId === 'Cardiology' ? '❤️ Кардиология' 
                      : categoryId === 'Nephrology' ? '🫘 Нефрология'
                        : categoryId === 'Neurology' ? '🧠 Неврология' 
                          : categoryId === 'Pediatrics' ? '👶 Педиатрия'
                            : categoryId === 'Obstetrics' ? '🤰 Акушерство'
                              : categoryId === 'Hematology' ? '💉 Гематология'
                                : categoryId === 'Laboratory' ? '🔬 Лабораторная'
                                  : 'Прочее'}
                </Text>
                {items.map((calculator: any) => (
                  <Pressable
                    key={calculator.id}
                    onPress={() => handleCalculatorPress(calculator.id)}
                    className="bg-surface-elevated rounded-2xl p-3 border border-border active:opacity-70 mb-2"
                  >
                    <View className="flex-row items-start mb-2">
                      <View className="w-10 h-10 rounded-full bg-primary-50 items-center justify-center mr-3">
                        <Text className="text-xl">
                          {(() => {
                            if (categoryId === 'General Health') return '⚕️';
                            if (categoryId === 'Cardiology') return '❤️';
                            if (categoryId === 'Nephrology') return '🫘';
                            if (categoryId === 'Neurology') return '🧠';
                            if (categoryId === 'Pediatrics') return '👶';
                            if (categoryId === 'Obstetrics') return '🤰';
                            if (categoryId === 'Hematology') return '💉';
                            if (categoryId === 'Laboratory') return '🔬';
                            return '⚕️';
                          })()}
                        </Text>
                      </View>
                      <View className="flex-1">
                        <Text className="text-sm font-semibold text-text-primary mb-0.5">
                          {calculator.nameRu || calculator.name}
                        </Text>
                        <Text className="text-xs text-text-secondary capitalize mb-1">
                          {calculator.categoryRu || calculator.category}
                        </Text>
                        <Text className="text-xs text-text-secondary" numberOfLines={2}>
                          {calculator.descriptionRu || calculator.description}
                        </Text>
                      </View>
                      <Text className="text-text-muted text-base ml-2">→</Text>
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
