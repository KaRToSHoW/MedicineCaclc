/**
 * Dashboard Layout
 * Tab-based navigation for user dashboard
 */

import { Slot } from 'expo-router';
import { View, Text } from 'react-native';

export default function DashboardLayout() {
  return (
    <Slot
      screenOptions={{
        headerShown: false,
        tabBarStyle: {
          backgroundColor: '#ffffff',
          borderTopWidth: 1,
          borderTopColor: '#E5E7EB',
          paddingBottom: 8,
          paddingTop: 8,
          height: 65,
        },
        tabBarActiveTintColor: '#6366f1',
        tabBarInactiveTintColor: '#9CA3AF',
        tabBarLabelStyle: {
          fontSize: 12,
          fontWeight: '600',
        },
      }}
    >
      <Slot.Screen
        name="index"
        options={{
          title: 'Обзор',
          tabBarIcon: ({ color, size }) => (
            <View>
              <Text style={{ fontSize: 24 }}>📊</Text>
            </View>
          ),
        }}
      />
      <Slot.Screen
        name="history"
        options={{
          title: 'История',
          tabBarIcon: ({ color, size }) => (
            <View>
              <Text style={{ fontSize: 24 }}>📋</Text>
            </View>
          ),
        }}
      />
      <Slot.Screen
        name="statistics"
        options={{
          title: 'Статистика',
          tabBarIcon: ({ color, size }) => (
            <View>
              <Text style={{ fontSize: 24 }}>📈</Text>
            </View>
          ),
        }}
      />
      <Slot.Screen
        name="profile"
        options={{
          title: 'Профиль',
          tabBarIcon: ({ color, size }) => (
            <View>
              <Text style={{ fontSize: 24 }}>👤</Text>
            </View>
          ),
        }}
      />
    </Slot>
  );
}
