import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, Pressable, ActivityIndicator } from 'react-native';
import { router, useLocalSearchParams } from 'expo-router';
import { useCalculationResultsStore } from '@/stores/calculationResultsStore';
import { useCalculatorsStore } from '@/stores/calculatorsStore';
import { CalculationResult } from '@/types/calculation_results';
import { Calculator } from '@/types/calculators';

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
  const resultId = params.id as string;
  
  const { items: results, loading } = useCalculationResultsStore();
  const { items: calculators } = useCalculatorsStore();
  const [result, setResult] = useState<CalculationResult | null>(null);
  const [calculator, setCalculator] = useState<Calculator | null>(null);
  const [conclusion, setConclusion] = useState<string>('');
  const [recommendations, setRecommendations] = useState<string>('');

  useEffect(() => {
    const foundResult = results.find((r) => String(r.id) === String(resultId));
    if (foundResult) {
      setResult(foundResult);
      
      // Find calculator and extract conclusion/recommendations
      const calc = calculators.find((c) => String(c.id) === String(foundResult.calculatorId));
      if (calc) {
        setCalculator(calc);
        
        // Find matching interpretation rule
        if (calc.interpretationRules && calc.interpretationRules.length > 0) {
          const rule = calc.interpretationRules.find((r) => {
            const interp = r.interpretationRu || r.interpretation || '';
            return interp.toLowerCase() === foundResult.interpretation.toLowerCase();
          });
          
          if (rule) {
            setConclusion(rule.conclusion || '');
            setRecommendations(rule.recommendations || '');
          }
        }
      }
    }
  }, [resultId, results, calculators]);

  if (loading || !result) {
    return (
      <View className="flex-1 bg-surface items-center justify-center">
        <ActivityIndicator size="large" color="#0080FF" />
        <Text className="text-text-secondary mt-4">Загрузка результата...</Text>
      </View>
    );
  }

  const styles = getSeverityStyles(result.interpretation);

  return (
    <ScrollView className="flex-1 bg-surface-secondary">
      {/* Header with Gradient */}
      <View className="bg-gradient-primary px-6 pt-16 pb-8 shadow-lg">
        <Pressable onPress={() => router.canGoBack() ? router.back() : router.push('/')} className="mb-4 active:opacity-70">
          <Text className="text-text-inverse text-lg font-medium">← Назад</Text>
        </Pressable>
        <View className="flex-row items-center mb-2">
          <Text className="text-4xl mr-3">{styles.icon}</Text>
          <Text className="text-3xl font-bold text-text-inverse">
            Результат расчета
          </Text>
        </View>
        <Text className="text-base text-text-inverse opacity-90">
          {calculator?.nameRu || calculator?.name || result.calculator?.name || 'Medical Calculator'}
        </Text>
      </View>

      <View className="px-6 py-6">
        {/* Result Value Card with Animation */}
        <View className={`rounded-card p-6 mb-6 shadow-card-hover ${styles.bg}`}>
          <Text className="text-sm font-semibold text-text-secondary mb-3 uppercase tracking-wide">
            Рассчитанное значение
          </Text>
          <View className="flex-row items-baseline mb-2">
            <Text className="text-6xl font-bold text-text-primary">
              {(() => {
                const val = result.resultValue as any;
                // If formula likely returns a date (e.g., Naegele's rule) the value may be a timestamp
                const isDateLike = typeof val === 'number' && val > 1e11;
                if (isDateLike) {
                  return new Date(val).toLocaleDateString('ru-RU');
                }
                if (typeof val === 'number') return val.toFixed(2);
                return String(val ?? '');
              })()}
            </Text>
            <Text className="text-xl text-text-secondary ml-3">
              {calculator?.category === 'Anthropometry' && calculator?.name?.includes('BMI') ? 'kg/m²' : ''}
              {calculator?.name?.includes('BMR') ? 'kcal/day' : ''}
            </Text>
          </View>
        </View>

        {/* Interpretation Card */}
        <View className="bg-surface rounded-card p-6 mb-6 shadow-card">
          <View className="flex-row items-center mb-4">
            <Text className="text-2xl mr-2">{styles.icon}</Text>
            <Text className="text-xl font-bold text-text-primary">
              Клиническая интерпретация
            </Text>
          </View>
          <View className={`rounded-xl p-5 ${styles.bg}`}>
            <Text className={`text-lg ${styles.text} font-semibold`}>
              {result.interpretation}
            </Text>
          </View>
        </View>

        {/* Conclusion Card */}
        {conclusion ? (
          <View className="bg-surface rounded-card p-6 mb-6 shadow-card">
            <View className="flex-row items-center mb-4">
              <Text className="text-2xl mr-2">📋</Text>
              <Text className="text-xl font-bold text-text-primary">
                Заключение
              </Text>
            </View>
            <Text className="text-base text-text-primary leading-6">
              {conclusion}
            </Text>
          </View>
        ) : null}

        {/* Recommendations Card */}
        {recommendations ? (
          <View className="bg-gradient-soft rounded-card p-6 mb-6 shadow-card border border-primary-light">
            <View className="flex-row items-center mb-4">
              <Text className="text-2xl mr-2">💡</Text>
              <Text className="text-xl font-bold text-primary">
                Рекомендации
              </Text>
            </View>
            <Text className="text-base text-text-primary leading-6">
              {recommendations}
            </Text>
          </View>
        ) : null}

        {/* Input Data Card */}
        <View className="bg-surface rounded-card p-6 mb-6 shadow-card">
          <View className="flex-row items-center mb-4">
            <Text className="text-2xl mr-2">📝</Text>
            <Text className="text-xl font-bold text-text-primary">
              Входные параметры
            </Text>
          </View>
          <View className="gap-3">
            {Object.entries(result.inputData).map(([key, value], index) => (
              <View key={key} className={`flex-row justify-between items-center py-3 ${index < Object.keys(result.inputData).length - 1 ? 'border-b border-border' : ''}`}>
                <Text className="text-base font-medium text-text-secondary capitalize">
                  {key.replace(/_/g, ' ')}
                </Text>
                <Text className="text-lg font-bold text-text-primary">
                  {typeof value === 'number' ? value.toFixed(1) : value}
                </Text>
              </View>
            ))}
          </View>
        </View>

        {/* Metadata */}
        <View className="bg-surface rounded-card p-5 mb-6 shadow-soft">
          <View className="flex-row items-center mb-3">
            <Text className="text-xl mr-3">📅</Text>
            <Text className="text-base text-text-secondary">
              {new Date(result.performedAt).toLocaleDateString('ru-RU')}
            </Text>
          </View>
          <View className="flex-row items-center">
            <Text className="text-xl mr-3">⏱️</Text>
            <Text className="text-base text-text-secondary">
              {new Date(result.performedAt).toLocaleTimeString('ru-RU')}
            </Text>
          </View>
        </View>

        {/* Medical Disclaimer */}
        <View className="bg-info-bg border-2 border-info rounded-card p-5 mb-6 shadow-soft">
          <View className="flex-row items-start">
            <Text className="text-2xl mr-3">ℹ️</Text>
            <View className="flex-1">
              <Text className="text-base font-bold text-info-text mb-2">
                Медицинское предупреждение
              </Text>
              <Text className="text-sm text-text-secondary leading-5">
                Этот результат носит исключительно информационный характер и не должен заменять профессиональный
                медицинский совет. Всегда консультируйтесь с квалифицированным врачом для диагностики
                и лечения.
              </Text>
            </View>
          </View>
        </View>

        {/* Action Buttons */}
        <View className="gap-4">
          <Pressable
            onPress={() => router.push('/')}
            className="bg-gradient-primary rounded-button py-4 items-center shadow-lg active:opacity-90"
          >
            <Text className="text-lg font-bold text-text-inverse">
              🔄 Рассчитать еще
            </Text>
          </Pressable>
          <Pressable
            onPress={() => router.push('/history')}
            className="bg-surface border-2 border-primary rounded-button py-4 items-center shadow-card active:opacity-80"
          >
            <Text className="text-lg font-bold text-primary">
              📊 Смотреть историю
            </Text>
          </Pressable>
        </View>
      </View>
    </ScrollView>
  );
}
