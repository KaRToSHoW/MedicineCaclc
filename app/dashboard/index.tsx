/**
 * Dashboard Overview Screen
 * Main dashboard with user info and quick actions
 */

import React, { useEffect } from 'react';
import { View, Text, ScrollView, Pressable } from 'react-native';
import { router } from 'expo-router';
import { useAuth } from '@/hooks/useAuth';

export default function DashboardOverviewScreen() {
  const { user, isAuthenticated, isLoading } = useAuth();

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
              <Text className="text-3xl mb-2 text-center">🏠</Text>
              <Text className="text-sm font-semibold text-text-primary text-center">
                Главная
              </Text>
            </Pressable>
            <Pressable
              onPress={() => router.push('/settings')}
              className="flex-1 bg-surface-elevated rounded-xl p-4 border border-border active:opacity-80"
            >
              <Text className="text-3xl mb-2 text-center">⚙️</Text>
              <Text className="text-sm font-semibold text-text-primary text-center">
                Настройки
              </Text>
            </Pressable>
          </View>
        </View>

        {/* Welcome Message */}
        <View className="bg-surface-elevated rounded-2xl p-6 mb-6 border border-border">
          <Text className="text-lg font-bold text-text-primary mb-4">
            Профиль
          </Text>
          <Text className="text-sm text-text-secondary mb-4">
            Здесь будет отображаться информация о вашем профиле и активности.
          </Text>
          <View className="bg-info-bg border border-info rounded-xl p-4">
            <Text className="text-sm text-info-text">
              💡 Система готова к работе
            </Text>
          </View>
        </View>
      </View>
    </ScrollView>
  );
}
