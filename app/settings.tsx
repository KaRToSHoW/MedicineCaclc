import React, { useState } from 'react';
import { View, Text, ScrollView, Pressable, TextInput, ActivityIndicator } from 'react-native';
import { router } from 'expo-router';
import { useAuth } from '@/hooks/useAuth';
import { Alert } from '@/utils/alert';

/**
 * User Settings/Profile Screen
 * Allows users to view and edit their profile information
 */

export default function SettingsScreen() {
  const { user, isAuthenticated, logout } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(false);
  
  // Form state
  const [name, setName] = useState(user?.name || '');
  const [email, setEmail] = useState(user?.email || '');
  const [errors, setErrors] = useState<Record<string, string>>({});

  // Show login prompt if not authenticated
  if (!isAuthenticated) {
    return (
      <View className="flex-1 bg-surface">
        <View className="bg-primary px-6 pt-16 pb-8">
          <Pressable onPress={() => router.back()} className="mb-4 active:opacity-70">
            <Text className="text-text-inverse text-lg">← Назад</Text>
          </Pressable>
          <Text className="text-2xl font-bold text-text-inverse mb-2">
            Настройки
          </Text>
        </View>
        <View className="flex-1 px-6 py-8 justify-center">
          <View className="bg-info-bg border border-info rounded-xl p-6">
            <Text className="text-xl mb-4 text-center">🔒</Text>
            <Text className="text-lg font-semibold text-text-primary text-center mb-2">
              Требуется вход
            </Text>
            <Text className="text-sm text-text-secondary text-center mb-6">
              Пожалуйста, войдите, чтобы просмотреть настройки
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
        <Pressable onPress={() => router.back()} className="mb-4 active:opacity-70">
          <Text className="text-text-inverse text-lg">← Назад</Text>
        </Pressable>
        <Text className="text-2xl font-bold text-text-inverse mb-2">
          Настройки
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
              Профиль пользователя
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
            <View className="w-24 h-24 bg-primary rounded-full items-center justify-center mb-3">
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

        {/* App Settings Section */}
        <View className="bg-surface-elevated rounded-2xl p-6 mb-6 border border-border">
          <Text className="text-lg font-bold text-text-primary mb-4">
            Настройки приложения
          </Text>
          
          <View className="gap-3">
            <Pressable
              onPress={() => Alert.alert('Информация', 'Функция в разработке')}
              className="flex-row items-center justify-between py-3 border-b border-border active:opacity-70"
            >
              <View className="flex-row items-center">
                <Text className="text-2xl mr-3">🌐</Text>
                <Text className="text-base text-text-primary">Язык</Text>
              </View>
              <Text className="text-sm text-text-secondary">Русский</Text>
            </Pressable>

            <Pressable
              onPress={() => Alert.alert('Информация', 'Функция в разработке')}
              className="flex-row items-center justify-between py-3 border-b border-border active:opacity-70"
            >
              <View className="flex-row items-center">
                <Text className="text-2xl mr-3">🎨</Text>
                <Text className="text-base text-text-primary">Тема</Text>
              </View>
              <Text className="text-sm text-text-secondary">Светлая</Text>
            </Pressable>

            <Pressable
              onPress={() => Alert.alert('Информация', 'Функция в разработке')}
              className="flex-row items-center justify-between py-3 active:opacity-70"
            >
              <View className="flex-row items-center">
                <Text className="text-2xl mr-3">🔔</Text>
                <Text className="text-base text-text-primary">Уведомления</Text>
              </View>
              <Text className="text-sm text-text-secondary">Включены</Text>
            </Pressable>
          </View>
        </View>

        {/* About Section */}
        <View className="bg-surface-elevated rounded-2xl p-6 mb-6 border border-border">
          <Text className="text-lg font-bold text-text-primary mb-4">
            О приложении
          </Text>
          
          <View className="gap-3">
            <Pressable
              onPress={() => Alert.alert('Информация', 'Функция в разработке')}
              className="flex-row items-center justify-between py-3 border-b border-border active:opacity-70"
            >
              <Text className="text-base text-text-primary">Версия</Text>
              <Text className="text-sm text-text-secondary">1.0.0</Text>
            </Pressable>

            <Pressable
              onPress={() => Alert.alert('Информация', 'Функция в разработке')}
              className="flex-row items-center justify-between py-3 border-b border-border active:opacity-70"
            >
              <Text className="text-base text-text-primary">Политика конфиденциальности</Text>
              <Text className="text-sm text-text-secondary">→</Text>
            </Pressable>

            <Pressable
              onPress={() => Alert.alert('Информация', 'Функция в разработке')}
              className="flex-row items-center justify-between py-3 active:opacity-70"
            >
              <Text className="text-base text-text-primary">Условия использования</Text>
              <Text className="text-sm text-text-secondary">→</Text>
            </Pressable>
          </View>
        </View>

        {/* Logout Button */}
        <Pressable
          onPress={handleLogout}
          className="bg-danger rounded-xl py-4 items-center mb-8 active:opacity-80"
        >
          <Text className="text-base font-semibold text-text-inverse">
            Выйти из аккаунта
          </Text>
        </Pressable>
      </View>
    </ScrollView>
  );
}
