import React from 'react';
import { View, Text, ScrollView, Pressable } from 'react-native';
import { router } from 'expo-router';
import { useAuth } from '@/hooks/useAuth';

/**
 * Home Screen - Main Entry Point
 */

export default function HomeScreen() {
  const { user, isAuthenticated } = useAuth();

  return (
    <ScrollView className="flex-1 bg-surface-secondary" contentContainerStyle={{ paddingBottom: 80 }}>
      {/* Header with Gradient - Mobile Optimized */}
      <View className="bg-gradient-primary px-4 pt-12 pb-6 shadow-xl">
        <View className="flex-row items-start justify-between mb-4">
          <View className="flex-1">
            <Text className="text-2xl font-bold text-text-inverse mb-2">
              🏥 Медицинский калькулятор
            </Text>
            <Text className="text-sm text-text-inverse opacity-95">
              Профессиональные клинические расчеты
            </Text>
          </View>
          {isAuthenticated ? (
            <Pressable
              onPress={() => router.push('/dashboard')}
              className="bg-surface rounded-button px-3 py-2 shadow-card active:opacity-80"
            >
              <Text className="text-xs text-primary font-bold">
                👤 Кабинет
              </Text>
            </Pressable>
          ) : (
            <Pressable
              onPress={() => router.push('/(auth)/sign-in')}
              className="bg-surface rounded-button px-3 py-2 shadow-card active:opacity-80"
            >
              <Text className="text-xs text-primary font-bold">
                Войти
              </Text>
            </Pressable>
          )}
        </View>
      </View>

      {/* Welcome Message */}
      <View className="px-4 pt-6 pb-4">
        <View className="bg-surface rounded-card p-6 shadow-card">
          <Text className="text-xl font-bold text-text-primary mb-3 text-center">
            Добро пожаловать! 👋
          </Text>
          <Text className="text-sm text-text-secondary text-center leading-5">
            Система готова к работе. Здесь будут отображаться основные функции приложения.
          </Text>
        </View>
      </View>

      {/* Calculators Section */}
      <View className="px-4 pb-4">
        <Text className="text-lg font-bold text-text-primary mb-3">
          Калькуляторы
        </Text>
        <Pressable
          onPress={() => router.push('/cockcroft-gault')}
          className="bg-surface rounded-card p-4 shadow-card-hover active:opacity-80 mb-3"
        >
          <View className="flex-row items-center">
            <View className="bg-primary-light rounded-xl p-3 mr-3">
              <Text className="text-2xl">🫀</Text>
            </View>
            <View className="flex-1">
              <Text className="text-base font-bold text-text-primary mb-1">
                Клиренс креатинина (Cockcroft-Gault)
              </Text>
              <Text className="text-sm text-text-secondary">
                Оценка функции почек для коррекции доз лекарств
              </Text>
            </View>
            <Text className="text-2xl text-text-secondary">›</Text>
          </View>
        </Pressable>
      </View>

      {/* Quick Actions - Mobile Optimized */}
      <View className="px-4 pb-4">
        <Text className="text-lg font-bold text-text-primary mb-3">
          Быстрые действия
        </Text>
        <View className="flex-row gap-3">
          {isAuthenticated ? (
            <Pressable
              onPress={() => router.push('/dashboard')}
              className="flex-1 bg-surface rounded-card p-4 shadow-card-hover active:opacity-80"
            >
              <Text className="text-2xl mb-2">👤</Text>
              <Text className="text-sm font-bold text-text-primary">Личный кабинет</Text>
            </Pressable>
          ) : (
            <Pressable
              onPress={() => router.push('/(auth)/sign-in')}
              className="flex-1 bg-surface rounded-card p-4 shadow-card-hover active:opacity-80"
            >
              <Text className="text-2xl mb-2">🔑</Text>
              <Text className="text-sm font-bold text-text-primary">Войти</Text>
            </Pressable>
          )}
          <Pressable
            onPress={() => router.push('/settings')}
            className="flex-1 bg-surface rounded-card p-4 shadow-card-hover active:opacity-80"
          >
            <Text className="text-2xl mb-2">⚙️</Text>
            <Text className="text-sm font-bold text-text-primary">Настройки</Text>
          </Pressable>
        </View>
      </View>

      {/* Info Note - Mobile Optimized */}
      <View className="px-4 pb-6">
        <View className="bg-info-bg border-2 border-info rounded-card p-3 shadow-soft">
          <View className="flex-row items-start">
            <Text className="text-xl mr-2">ℹ️</Text>
            <View className="flex-1">
              <Text className="text-sm font-bold text-info-text mb-1">
                Медицинский дисклеймер
              </Text>
              <Text className="text-xs text-text-secondary leading-4">
                Эти калькуляторы предоставляют оценки на основе стандартных медицинских формул.
                {' '}Всегда консультируйтесь с квалифицированным медицинским специалистом.
              </Text>
            </View>
          </View>
        </View>
      </View>
    </ScrollView>
  );
}
