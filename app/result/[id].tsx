import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, Pressable, ActivityIndicator } from 'react-native';
import { router, useLocalSearchParams } from 'expo-router';
import { useCalculationResultsStore } from '@/stores/calculationResultsStore';
import { CalculationResult } from '@/types/calculation_results';

/**
 * Calculation Result Screen
 * Displays calculation result with clinical interpretation
 */

const getSeverityStyles = (interpretation: string) => {
  const lower = interpretation.toLowerCase();
  
  if (lower.includes('critical') || lower.includes('severe') || lower.includes('emergency')) {
    return {
      bg: 'bg-danger-bg',
      text: 'text-danger-text',
      border: 'border-danger',
      badge: 'bg-danger',
      icon: '🚨'
    };
  } else if (lower.includes('danger') || lower.includes('class ii') || lower.includes('hypertensive')) {
    return {
      bg: 'bg-danger-bg',
      text: 'text-danger-text',
      border: 'border-danger',
      badge: 'bg-danger',
      icon: '⚠️'
    };
  } else if (lower.includes('warning') || lower.includes('caution') || lower.includes('consult')) {
    return {
      bg: 'bg-warning-bg',
      text: 'text-warning-text',
      border: 'border-warning',
      badge: 'bg-warning',
      icon: '⚡'
    };
  } else if (lower.includes('normal') || lower.includes('healthy') || lower.includes('optimal')) {
    return {
      bg: 'bg-success-bg',
      text: 'text-success-text',
      border: 'border-success',
      badge: 'bg-success',
      icon: '✅'
    };
  } else {
    return {
      bg: 'bg-info-bg',
      text: 'text-info-text',
      border: 'border-info',
      badge: 'bg-info',
      icon: 'ℹ️'
    };
  }
};

export default function ResultScreen() {
  const params = useLocalSearchParams();
  const resultId = parseInt(params.id as string);
  
  const { items: results, loading } = useCalculationResultsStore();
  const [result, setResult] = useState<CalculationResult | null>(null);

  useEffect(() => {
    const foundResult = results.find((r) => r.id === resultId);
    if (foundResult) {
      setResult(foundResult);
    }
  }, [resultId, results]);

  if (loading || !result) {
    return (
      <View className="flex-1 bg-surface items-center justify-center">
        <ActivityIndicator size="large" color="#0080FF" />
        <Text className="text-text-secondary mt-4">Loading result...</Text>
      </View>
    );
  }

  const styles = getSeverityStyles(result.interpretation);

  return (
    <ScrollView className="flex-1 bg-surface">
      {/* Header */}
      <View className={`${styles.bg} px-6 pt-16 pb-8 border-b-4 ${styles.border}`}>
        <Pressable onPress={() => router.back()} className="mb-4 active:opacity-70">
          <Text className={`${styles.text} text-lg font-medium`}>← Back</Text>
        </Pressable>
        <View className="flex-row items-center mb-2">
          <Text className="text-3xl mr-3">{styles.icon}</Text>
          <Text className={`text-2xl font-bold ${styles.text}`}>
            Calculation Result
          </Text>
        </View>
        <Text className="text-sm text-text-secondary">
          {result.calculator?.name || 'Medical Calculator'}
        </Text>
      </View>

      <View className="px-6 py-6">
        {/* Result Value Card */}
        <View className={`rounded-2xl p-6 mb-6 border-2 ${styles.border} ${styles.bg}`}>
          <Text className="text-sm font-medium text-text-secondary mb-3">
            Calculated Value
          </Text>
          <View className="flex-row items-baseline mb-4">
            <Text className="text-6xl font-bold text-text-primary">
              {result.resultValue.toFixed(2)}
            </Text>
            <Text className="text-lg text-text-secondary ml-2">
              {result.calculator?.category === 'general' && result.calculator?.name?.includes('BMI') ? 'kg/m²' : ''}
            </Text>
          </View>
        </View>

        {/* Interpretation Card */}
        <View className="bg-surface-elevated rounded-2xl p-6 mb-6 border border-border">
          <Text className="text-lg font-bold text-text-primary mb-4">
            Clinical Interpretation
          </Text>
          <View className={`rounded-xl p-4 ${styles.bg} border ${styles.border}`}>
            <Text className={`text-base ${styles.text} font-medium`}>
              {result.interpretation}
            </Text>
          </View>
        </View>

        {/* Input Data Card */}
        <View className="bg-surface-elevated rounded-2xl p-6 mb-6 border border-border">
          <Text className="text-lg font-bold text-text-primary mb-4">
            Input Parameters
          </Text>
          <View className="gap-3">
            {Object.entries(result.inputData).map(([key, value]) => (
              <View key={key} className="flex-row justify-between items-center py-2 border-b border-border last:border-b-0">
                <Text className="text-sm font-medium text-text-secondary capitalize">
                  {key.replace(/_/g, ' ')}
                </Text>
                <Text className="text-base font-semibold text-text-primary">
                  {typeof value === 'number' ? value.toFixed(1) : value}
                </Text>
              </View>
            ))}
          </View>
        </View>

        {/* Metadata */}
        <View className="bg-surface-elevated rounded-2xl p-5 mb-6 border border-border">
          <View className="flex-row items-center mb-3">
            <Text className="text-base mr-2">📅</Text>
            <Text className="text-sm text-text-secondary">
              Date: {new Date(result.performedAt).toLocaleDateString('ru-RU')}
            </Text>
          </View>
          <View className="flex-row items-center">
            <Text className="text-base mr-2">⏱️</Text>
            <Text className="text-sm text-text-secondary">
              Time: {new Date(result.performedAt).toLocaleTimeString('ru-RU')}
            </Text>
          </View>
        </View>

        {/* Medical Disclaimer */}
        <View className="bg-info-bg border border-info rounded-xl p-4 mb-6">
          <View className="flex-row items-start">
            <Text className="text-xl mr-3">ℹ️</Text>
            <View className="flex-1">
              <Text className="text-sm font-medium text-info-text mb-1">
                Medical Disclaimer
              </Text>
              <Text className="text-xs text-text-secondary">
                This result is for informational purposes only and should not replace professional
                medical advice. Always consult with a qualified healthcare provider for diagnosis
                and treatment.
              </Text>
            </View>
          </View>
        </View>

        {/* Action Buttons */}
        <View className="gap-3">
          <Pressable
            onPress={() => router.push('/')}
            className="bg-primary rounded-xl py-4 items-center active:opacity-80"
          >
            <Text className="text-base font-semibold text-text-inverse">
              Calculate Another
            </Text>
          </Pressable>
          <Pressable
            onPress={() => router.push('/history')}
            className="bg-surface-secondary border border-border rounded-xl py-4 items-center active:opacity-70"
          >
            <Text className="text-base font-semibold text-text-secondary">
              View History
            </Text>
          </Pressable>
        </View>
      </View>
    </ScrollView>
  );
}
