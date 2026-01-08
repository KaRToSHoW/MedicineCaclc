/**
 * Dashboard Profile Screen
 * User profile and settings
 */

import React, { useState } from 'react';
import { View, Text, ScrollView, Pressable, TextInput, ActivityIndicator } from 'react-native';
import { router } from 'expo-router';
import { useAuth } from '@/hooks/useAuth';
import { Alert } from '@/utils/alert';

export default function DashboardProfileScreen() {
  const { user, isAuthenticated, logout } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(false);
  
  // Form state
  const [name, setName] = useState(user?.name || '');
  const [email, setEmail] = useState(user?.email || '');
  const [errors, setErrors] = useState<Record<string, string>>({});

  // Redirect if not authenticated
  if (!isAuthenticated) {
    router.replace('/(auth)/sign-in');
    return null;
  }

  const handleSave = async () => {
    // Validate inputs
    const newErrors: Record<string, string> = {};
    
    if (!name.trim()) {
      newErrors.name = 'Имя обязательно';
    }
    
    if (!email.trim()) {
      newErrors.email = 'Email обязателен';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      newErrors.email = 'Введите корректный email';
    }
    
    setErrors(newErrors);
    
    if (Object.keys(newErrors).length > 0) {
      return;
    }

    try {
      setLoading(true);
      // TODO: Implement API call to update user profile
      // await updateProfile({ name, email });
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      Alert.alert('Успех', 'Профиль успешно обновлен');
      setIsEditing(false);
    } catch (error: any) {
      Alert.alert('Ошибка', error.message || 'Не удалось обновить профиль');
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    setName(user?.name || '');
    setEmail(user?.email || '');
    setErrors({});
    setIsEditing(false);
  };

  const handleLogout = async () => {
    Alert.alert(
      'Выход',
      'Вы уверены, что хотите выйти?',
      [
        {
          text: 'Отмена',
          style: 'cancel',
        },
        {
          text: 'Выйти',
          onPress: async () => {
            try {
              await logout();
              router.replace('/');
            } catch (error: any) {
              Alert.alert('Ошибка', error.message || 'Не удалось выйти');
            }
          },
          style: 'destructive',
        },
      ]
    );
  };

  return (
    <ScrollView className="flex-1 bg-surface">
      {/* Header */}
      <View className="bg-primary px-6 pt-16 pb-8">
        <Text className="text-2xl font-bold text-text-inverse mb-2">
          Профиль
        </Text>
        <Text className="text-sm text-text-inverse opacity-90">
          Управление профилем и настройками
        </Text>
      </View>

      <View className="px-6 py-6">
        {/* Profile Section */}
        <View className="bg-surface-elevated rounded-2xl p-6 mb-6 border border-border">
          <View className="flex-row items-center justify-between mb-4">
            <Text className="text-lg font-bold text-text-primary">
              Информация профиля
            </Text>
            {!isEditing ? (
              <Pressable
                onPress={() => setIsEditing(true)}
                className="bg-primary px-4 py-2 rounded-lg active:opacity-80"
              >
                <Text className="text-sm font-medium text-text-inverse">
                  Редактировать
                </Text>
              </Pressable>
            ) : null}
          </View>

          {/* Profile Icon */}
          <View className="items-center mb-6">
            <View className="w-24 h-24 bg-primary rounded-full items-center justify-center mb-3 shadow-card">
              <Text className="text-5xl">👤</Text>
            </View>
            <Text className="text-base font-semibold text-text-primary">
              {user?.name || 'Пользователь'}
            </Text>
            <Text className="text-sm text-text-secondary">
              {user?.email}
            </Text>
          </View>

          {/* Profile Form */}
          <View className="gap-4">
            <View>
              <Text className="text-sm font-medium text-text-primary mb-2">
                Имя
              </Text>
              <TextInput
                value={name}
                onChangeText={setName}
                editable={isEditing}
                placeholder="Введите ваше имя"
                placeholderTextColor="#A0A0A0"
                className={`bg-surface border rounded-xl px-4 py-3 text-base text-text-primary ${
                  errors.name ? 'border-danger' : 'border-border'
                } ${!isEditing ? 'opacity-50' : ''}`}
              />
              {errors.name ? (
                <Text className="text-danger text-xs mt-1">{errors.name}</Text>
              ) : null}
            </View>

            <View>
              <Text className="text-sm font-medium text-text-primary mb-2">
                Email
              </Text>
              <TextInput
                value={email}
                onChangeText={setEmail}
                editable={isEditing}
                keyboardType="email-address"
                autoCapitalize="none"
                placeholder="Введите ваш email"
                placeholderTextColor="#A0A0A0"
                className={`bg-surface border rounded-xl px-4 py-3 text-base text-text-primary ${
                  errors.email ? 'border-danger' : 'border-border'
                } ${!isEditing ? 'opacity-50' : ''}`}
              />
              {errors.email ? (
                <Text className="text-danger text-xs mt-1">{errors.email}</Text>
              ) : null}
            </View>
          </View>

          {/* Edit Actions */}
          {isEditing ? (
            <View className="flex-row gap-3 mt-6">
              <Pressable
                onPress={handleSave}
                disabled={loading}
                className={`flex-1 bg-primary rounded-xl py-3 items-center ${
                  loading ? 'opacity-50' : 'active:opacity-80'
                }`}
              >
                {loading ? (
                  <ActivityIndicator color="#FFFFFF" />
                ) : (
                  <Text className="text-base font-semibold text-text-inverse">
                    Сохранить
                  </Text>
                )}
              </Pressable>
              <Pressable
                onPress={handleCancel}
                disabled={loading}
                className="bg-surface-secondary border border-border rounded-xl px-6 py-3 items-center active:opacity-70"
              >
                <Text className="text-base font-semibold text-text-secondary">
                  Отмена
                </Text>
              </Pressable>
            </View>
          ) : null}
        </View>

        {/* Quick Links */}
        <View className="bg-surface-elevated rounded-2xl p-6 mb-6 border border-border">
          <Text className="text-lg font-bold text-text-primary mb-4">
            Быстрые действия
          </Text>
          <View className="gap-3">
            <Pressable
              onPress={() => router.push('/')}
              className="bg-surface border border-border rounded-xl p-4 flex-row items-center active:opacity-70"
            >
              <Text className="text-2xl mr-3">🏠</Text>
              <Text className="text-base font-medium text-text-primary flex-1">
                Главная страница
              </Text>
              <Text className="text-text-muted">→</Text>
            </Pressable>
            <Pressable
              onPress={() => router.push('/calculators')}
              className="bg-surface border border-border rounded-xl p-4 flex-row items-center active:opacity-70"
            >
              <Text className="text-2xl mr-3">🧮</Text>
              <Text className="text-base font-medium text-text-primary flex-1">
                Все калькуляторы
              </Text>
              <Text className="text-text-muted">→</Text>
            </Pressable>
          </View>
        </View>

        {/* Account Actions */}
        <View className="bg-surface-elevated rounded-2xl p-6 mb-6 border border-border">
          <Text className="text-lg font-bold text-text-primary mb-4">
            Аккаунт
          </Text>
          <Pressable
            onPress={handleLogout}
            className="bg-danger rounded-xl py-3 active:opacity-80"
          >
            <Text className="text-base font-semibold text-text-inverse text-center">
              Выйти из аккаунта
            </Text>
          </Pressable>
        </View>

        {/* App Info */}
        <View className="items-center py-4">
          <Text className="text-xs text-text-muted mb-1">
            Медицинский Калькулятор
          </Text>
          <Text className="text-xs text-text-muted">
            Версия 1.0.0
          </Text>
        </View>
      </View>
    </ScrollView>
  );
}
