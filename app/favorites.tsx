import { View, Text, Pressable, ScrollView } from 'react-native';
import { useRouter } from 'expo-router';
import { useState, useEffect } from 'react';

// Mock data - в будущем заменить на реальные данные из store
const mockFavorites = [
  {
    id: 'bmi',
    name: 'Индекс массы тела (ИМТ)',
    category: 'общая медицина',
    icon: '⚖️',
    description: 'Расчет индекса массы тела и оценка веса',
  },
  {
    id: 'gfr',
    name: 'СКФ (CKD-EPI)',
    category: 'нефрология',
    icon: '🩺',
    description: 'Скорость клубочковой фильтрации',
  },
  {
    id: 'cardiac-index',
    name: 'Сердечный индекс',
    category: 'кардиология',
    icon: '❤️',
    description: 'Оценка насосной функции сердца',
  },
];

export default function FavoritesScreen() {
  const router = useRouter();
  const [favorites, setFavorites] = useState(mockFavorites);

  const handleRemoveFavorite = (id: string) => {
    setFavorites(favorites.filter(item => item.id !== id));
  };

  const handleOpenCalculator = (id: string) => {
    router.push(`/calculator/${id}`);
  };

  return (
    <View className="flex-1 bg-surface-secondary">
      {/* Header */}
      <View className="bg-gradient-primary px-4 pt-12 pb-6">
        <Text className="text-xl font-bold text-text-inverse mb-1">
          Избранное
        </Text>
        <Text className="text-xs text-text-inverse opacity-90">
          {favorites.length} {favorites.length === 1 ? 'калькулятор' : 'калькуляторов'}
        </Text>
      </View>

      {favorites.length === 0 ? (
        // Empty State
        <View className="flex-1 items-center justify-center px-8" style={{ paddingBottom: 80 }}>
          <View className="w-24 h-24 rounded-full bg-primary-light items-center justify-center mb-4">
            <Text className="text-5xl">⭐</Text>
          </View>
          <Text className="text-base font-bold text-text-primary mb-2 text-center">
            Нет избранных калькуляторов
          </Text>
          <Text className="text-sm text-text-secondary text-center mb-6">
            Добавьте калькуляторы в избранное, чтобы быстро находить их здесь
          </Text>
          <Pressable
            onPress={() => router.push('/calculators')}
            className="bg-primary rounded-xl px-6 py-3 active:opacity-80"
          >
            <Text className="text-sm font-semibold text-text-inverse">
              🧮 Перейти к калькуляторам
            </Text>
          </Pressable>
        </View>
      ) : (
        // Favorites List
        <ScrollView className="flex-1 px-4 pt-4" contentContainerStyle={{ paddingBottom: 80 }} showsVerticalScrollIndicator={false}>
          <View className="pb-6">
            {favorites.map((item, index) => (
              <Pressable
                key={item.id}
                onPress={() => handleOpenCalculator(item.id)}
                className="bg-surface rounded-2xl p-3 border border-border mb-3 active:opacity-70"
              >
                <View className="flex-row items-start">
                  {/* Icon */}
                  <View className="w-12 h-12 rounded-full bg-gradient-soft items-center justify-center mr-3">
                    <Text className="text-2xl">{item.icon}</Text>
                  </View>

                  {/* Content */}
                  <View className="flex-1 mr-2">
                    <Text className="text-sm font-bold text-text-primary mb-1">
                      {item.name}
                    </Text>
                    <Text className="text-xs text-text-secondary mb-2" numberOfLines={2}>
                      {item.description}
                    </Text>
                    <View className="flex-row items-center">
                      <View className="bg-primary-light px-2 py-0.5 rounded-full">
                        <Text className="text-xs font-medium text-primary capitalize">
                          {item.category}
                        </Text>
                      </View>
                    </View>
                  </View>

                  {/* Remove Button */}
                  <Pressable
                    onPress={(e) => {
                      e.stopPropagation();
                      handleRemoveFavorite(item.id);
                    }}
                    className="w-8 h-8 items-center justify-center active:opacity-50"
                  >
                    <Text className="text-xl">⭐</Text>
                  </Pressable>
                </View>
              </Pressable>
            ))}
          </View>

          {/* Info Card */}
          <View className="bg-info-bg border border-info-border rounded-xl p-3 mb-6">
            <View className="flex-row items-start">
              <Text className="text-lg mr-2">💡</Text>
              <View className="flex-1">
                <Text className="text-xs font-medium text-info-text mb-1">
                  Совет
                </Text>
                <Text className="text-xs text-text-secondary">
                  Нажмите на звездочку в карточке калькулятора, чтобы добавить его в избранное
                </Text>
              </View>
            </View>
          </View>
        </ScrollView>
      )}
    </View>
  );
}
