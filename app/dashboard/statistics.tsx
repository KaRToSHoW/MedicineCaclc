/**
 * Dashboard Statistics Screen
 * Placeholder for future statistics functionality
 */

import React, { useEffect } from 'react';
import { View, Text, ScrollView, Pressable } from 'react-native';
import { router } from 'expo-router';
import { useAuth } from '@/hooks/useAuth';

export default function DashboardStatisticsScreen() {
  const { isAuthenticated, isLoading } = useAuth();

  // Redirect if not authenticated
  useEffect(() => {
    if (!isAuthenticated && !isLoading) {
      router.replace('/(auth)/sign-in');
    }
  }, [isAuthenticated, isLoading]);

  if (isLoading || !isAuthenticated) {
    return null;
  }

  return (
    <View className="flex-1 bg-surface">
      {/* Header */}
      <View className="bg-primary px-6 pt-16 pb-8">
        <Text className="text-2xl font-bold text-text-inverse mb-2">
          Статистика
        </Text>
        <Text className="text-sm text-text-inverse opacity-90">
          Обзор активности
        </Text>
      </View>

      <ScrollView className="flex-1 px-6 py-6">
        <View className="bg-surface-elevated rounded-2xl p-6 border border-border">
          <Text className="text-center text-text-secondary mb-2">
            Пока нет статистики
          </Text>
          <Pressable onPress={() => router.push('/')} className="mt-4 active:opacity-70">
            <Text className="text-center text-primary font-medium">
              Вернуться на главную
            </Text>
          </Pressable>
        </View>
      </ScrollView>
    </View>
  );
}
