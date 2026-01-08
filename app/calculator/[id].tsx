import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, Pressable, TextInput, ActivityIndicator } from 'react-native';
import { router, useLocalSearchParams } from 'expo-router';
import { useCalculatorsStore } from '@/stores/calculatorsStore';
import { useCalculationResultsStore } from '@/stores/calculationResultsStore';
import { Calculator, InputField } from '@/types/calculators';
import evaluateFormula from '@/utils/formulaEvaluator';
import { useAuth } from '@/hooks/useAuth';
import getInterpretation from '@/utils/interpreter';

/**
 * Calculator Input Screen
 * Displays input fields for a specific calculator and performs calculations
 */

export default function CalculatorScreen() {
  const params = useLocalSearchParams();
  const calculatorId = params.id as string;
  
  const { items: calculators, loading: loadingCalc } = useCalculatorsStore();
  const { addItem: createResult, loading: calculating } = useCalculationResultsStore();
  const { isAuthenticated } = useAuth();
  
  const [calculator, setCalculator] = useState<Calculator | null>(null);
  const [inputValues, setInputValues] = useState<Record<string, string>>({});
  const [errors, setErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    const calc = calculators.find((c) => String(c.id) === String(calculatorId));
    if (calc) {
      setCalculator(calc);
      // Initialize input values
      const initialValues: Record<string, string> = {};
      calc.inputFields.forEach((field) => {
        initialValues[field.name] = '';
      });
      setInputValues(initialValues);
    }
  }, [calculatorId, calculators]);

  const validateInputs = (): boolean => {
    const newErrors: Record<string, string> = {};
    
    calculator?.inputFields.forEach((field) => {
      const value = inputValues[field.name];
      if (!value || value.trim() === '') {
        newErrors[field.name] = 'Это поле обязательно';
      } else if (field.type === 'number') {
        const numValue = parseFloat(value);
        if (isNaN(numValue)) {
          newErrors[field.name] = 'Введите корректное число';
        } else if (field.min !== undefined && numValue < field.min) {
          newErrors[field.name] = `Значение должно быть не менее ${field.min}`;
        } else if (field.max !== undefined && numValue > field.max) {
          newErrors[field.name] = `Значение не должно превышать ${field.max}`;
        }
      }
    });
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleCalculate = async () => {
    if (!validateInputs() || !calculator) return;

    // No authentication required — calculations and results are stored locally

    try {
      // Convert string values to numbers for numeric fields
      const processedData: Record<string, any> = {};
      calculator.inputFields.forEach((field) => {
        const value = inputValues[field.name];
        processedData[field.name] = field.type === 'number' ? parseFloat(value) : value;
      });

      // Evaluate formula if provided
      let computedValue: number | null = null;
      let interpretation = '';
      if (calculator.formula && calculator.formula.indexOf('{') !== -1) {
        try {
          const val = evaluateFormula(calculator.formula, processedData);
          if (typeof val === 'number' && !isNaN(val) && isFinite(val)) {
            computedValue = val;
          }
        } catch (err) {
          console.warn('Formula evaluation failed:', err);
        }
      }

      // Use centralized interpreter for clinical interpretation
      interpretation = getInterpretation(calculator, computedValue, processedData);

      const payload: any = {
        calculatorId: calculator.id,
        calculator: { id: calculator.id, name: calculator.name, category: calculator.category },
        inputData: processedData,
        resultValue: computedValue,
        interpretation,
      };

      // Require authentication to persist directly to Firebase
      if (!isAuthenticated) {
        // Avoid navigating (web navigator state can cause errors); show message instead
        setErrors({ general: 'Пожалуйста, войдите в систему, чтобы сохранить результат в облаке.' });
        return;
      }

      const result = await createResult(payload);

      // Navigate to result screen
      if (result) {
        router.push(`/result/${result.id}`);
      }
    } catch (error: any) {
      console.error('Calculation error:', error);
      setErrors({ general: error.message || 'Ошибка расчета. Попробуйте еще раз.' });
    }
  };

  const handleReset = () => {
    const resetValues: Record<string, string> = {};
    calculator?.inputFields.forEach((field) => {
      resetValues[field.name] = '';
    });
    setInputValues(resetValues);
    setErrors({});
  };

  if (loadingCalc || !calculator) {
    return (
      <View className="flex-1 bg-surface items-center justify-center">
        <ActivityIndicator size="large" color="#0080FF" />
        <Text className="text-text-secondary mt-4">Загрузка калькулятора...</Text>
      </View>
    );
  }

  // If calculator exists but has no input fields, show a helpful message
  if (calculator && (!calculator.inputFields || calculator.inputFields.length === 0)) {
    return (
      <View className="flex-1 bg-surface items-center justify-center px-6">
        <Text className="text-lg font-semibold mb-2">{calculator.name}</Text>
        <Text className="text-sm text-text-secondary mb-4">Для этого калькулятора не заданы входные параметры.</Text>
        <Pressable onPress={() => router.canGoBack() ? router.back() : router.push('/')} className="bg-primary rounded-xl px-6 py-3">
          <Text className="text-text-inverse">Назад</Text>
        </Pressable>
      </View>
    );
  }

  return (
    <ScrollView className="flex-1 bg-surface">
      {/* Header - Mobile Optimized */}
      <View className="bg-primary px-4 pt-12 pb-6">
        <Pressable onPress={() => router.canGoBack() ? router.back() : router.push('/')} className="mb-3 active:opacity-70">
          <Text className="text-text-inverse text-base">← Назад</Text>
        </Pressable>
        <Text className="text-xl font-bold text-text-inverse mb-1">
          {calculator.nameRu || calculator.name}
        </Text>
        <Text className="text-xs text-text-inverse opacity-90 capitalize">
          {calculator.categoryRu || calculator.category}
        </Text>
      </View>

      <View className="px-4 py-4">
        {/* Description - Mobile Optimized */}
        <View className="bg-info-bg border border-info rounded-xl p-3 mb-4">
          <Text className="text-xs text-text-secondary">
            {calculator.descriptionRu || calculator.description}
          </Text>
        </View>

        {/* Input Fields - Mobile Optimized */}
        <View className="bg-surface-elevated rounded-2xl p-4 mb-4 border border-border">
          <Text className="text-base font-bold text-text-primary mb-3">
            Введите значения
          </Text>

          {calculator.inputFields.map((field: InputField, index: number) => (
            <View key={field.name} className={index > 0 ? 'mt-3' : ''}>
              <Text className="text-xs font-medium text-text-primary mb-1.5">
                {field.labelRu || field.label}
                {field.unit ? ` (${field.unit})` : ''}
              </Text>
              
              {field.type === 'select' && field.options ? (
                <View className="gap-2">
                  {field.options.map((option: any) => {
                    const optionValue = typeof option === 'object' ? option.value : option;
                    const optionLabel = typeof option === 'object' ? (option.labelRu || option.label) : option;
                    return (
                      <Pressable
                        key={optionValue}
                        onPress={() => setInputValues({ ...inputValues, [field.name]: String(optionValue) })}
                        className={`rounded-xl px-3 py-2.5 border ${
                          inputValues[field.name] === String(optionValue)
                            ? 'bg-primary border-primary'
                            : 'bg-surface border-border'
                        } active:opacity-70`}
                      >
                        <Text
                          className={`text-sm ${
                            inputValues[field.name] === String(optionValue)
                              ? 'text-text-inverse font-medium'
                              : 'text-text-secondary'
                          }`}
                        >
                          {optionLabel}
                        </Text>
                      </Pressable>
                    );
                  })}
                </View>
              ) : (
                <TextInput
                  value={inputValues[field.name] || ''}
                  onChangeText={(value) => setInputValues({ ...inputValues, [field.name]: value })}
                  keyboardType={field.type === 'number' ? 'numeric' : 'default'}
                  placeholder={`Введите ${(field.labelRu || field.label).toLowerCase()}`}
                  placeholderTextColor="#A0A0A0"
                  className={`bg-surface border rounded-xl px-3 py-2.5 text-sm text-text-primary ${
                    errors[field.name] ? 'border-danger' : 'border-border'
                  }`}
                />
              )}
              
              {errors[field.name] ? (
                <Text className="text-danger text-xs mt-1">
                  {errors[field.name]}
                </Text>
              ) : null}
            </View>
          ))}

          {errors.general ? (
            <View className="bg-danger-bg border border-danger rounded-xl p-2.5 mt-3">
              <Text className="text-danger-text text-xs">
                {errors.general}
              </Text>
            </View>
          ) : null}
        </View>

        {/* Action Buttons - Mobile Optimized */}
        <View className="flex-row gap-2 mb-6">
          <Pressable
            onPress={handleCalculate}
            disabled={calculating}
            className={`flex-1 bg-primary rounded-xl py-3 items-center ${
              calculating ? 'opacity-50' : 'active:opacity-80'
            }`}
          >
            {calculating ? (
              <ActivityIndicator color="#FFFFFF" />
            ) : (
              <Text className="text-sm font-semibold text-text-inverse">
                Рассчитать
              </Text>
            )}
          </Pressable>
          <Pressable
            onPress={handleReset}
            disabled={calculating}
            className="bg-surface-secondary border border-border rounded-xl px-5 py-3 items-center active:opacity-70"
          >
            <Text className="text-sm font-semibold text-text-secondary">
              Сбросить
            </Text>
          </Pressable>
        </View>
      </View>
    </ScrollView>
  );
}
