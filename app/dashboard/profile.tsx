/**
 * Dashboard Profile Screen
 * User profile and settings
 */

import React, { useState, useEffect } from 'react';
import { View, Text, ScrollView, Pressable, TextInput, ActivityIndicator } from 'react-native';
import { router } from 'expo-router';
import { useAuth } from '@/hooks/useAuth';
import { Alert } from '@/utils/alert';

export default function DashboardProfileScreen() {
  const { user, isAuthenticated, isLoading, logout } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(false);
  
  // Form state
  const [name, setName] = useState(user?.name || '');
  const [email, setEmail] = useState(user?.email || '');
  const [errors, setErrors] = useState<Record<string, string>>({});

  // Redirect if not authenticated
  useEffect(() => {
    if (!isAuthenticated && !isLoading) {
      router.replace('/(auth)/sign-in');
    }
  }, [isAuthenticated, isLoading]);

  if (isLoading || !isAuthenticated) {
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
      <View className="px-6 py-8">
        {/* Profile Header with Avatar */}
        <View className="items-center mb-8">
          <View className="w-28 h-28 bg-primary rounded-full items-center justify-center mb-4 shadow-card">
            <Text className="text-6xl">👤</Text>
          </View>
          <Text className="text-2xl font-bold text-text-primary mb-1">
            {user?.name || 'Пользователь'}
          </Text>
          <Text className="text-base text-text-secondary">
            {user?.email || 'email@example.com'}
          </Text>
        </View>

        {/* Profile Section */}
        <View className="bg-surface-elevated rounded-2xl p-6 mb-6 border border-border">
          <View className="flex-row items-center justify-between mb-4">
            <Text className="text-lg font-bold text-text-primary">
              Личная информация
            </Text>
            {!isEditing ? (
              <Pressable
                onPress={() => setIsEditing(true)}
                className="bg-primary px-4 py-2 rounded-lg active:opacity-80"
              >
                <Text className="text-sm font-medium text-text-inverse">
                  Изменить
                </Text>
              </Pressable>
            ) : null}
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

        {/* Statistics Section */}
        <View className="bg-surface-elevated rounded-2xl p-6 mb-6 border border-border">
          <Text className="text-lg font-bold text-text-primary mb-4">
            Статистика
          </Text>
          <View className="flex-row gap-3">
            <View className="flex-1 bg-surface border border-border rounded-xl p-4 items-center">
              <Text className="text-3xl font-bold text-primary mb-1">0</Text>
              <Text className="text-sm text-text-secondary text-center">Расчётов</Text>
            </View>
            <View className="flex-1 bg-surface border border-border rounded-xl p-4 items-center">
              <Text className="text-3xl font-bold text-primary mb-1">0</Text>
              <Text className="text-sm text-text-secondary text-center">Сохранено</Text>
            </View>
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
            Клиренс креатинина
          </Text>
          <Text className="text-xs text-text-muted">
            Версия 1.0.0
          </Text>
        </View>
      </View>
    </ScrollView>
  );
}
