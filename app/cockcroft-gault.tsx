import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, ScrollView, TouchableOpacity, ActivityIndicator } from 'react-native';
import { router } from 'expo-router';
import { useAuth } from '@/hooks/useAuth';
import { useCalculationResultsStore } from '@/stores/calculationResultsStore';
import { cockcroftGaultCalculator } from '@/lib/calculators/cockcroftGault';
import type { InputField } from '@/lib/calculators/cockcroftGault';

export default function CockcroftGaultScreen() {
  const { isAuthenticated, isLoading } = useAuth();
  const { addItem: createResult, loading: calculating } = useCalculationResultsStore();
  
  const calculator = cockcroftGaultCalculator;
  const [formData, setFormData] = useState<Record<string, any>>({});
  const [result, setResult] = useState<{ value: number; interpretation: string; severity?: string } | null>(null);
  const [errors, setErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    if (!isAuthenticated && !isLoading) {
      router.replace('/(auth)/sign-in');
      return;
    }
    
    if (isAuthenticated) {
      // Initialize form
      initializeForm();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isAuthenticated, isLoading]);

  if (isLoading || !isAuthenticated) {
    return null;
  }

  const initializeForm = () => {
    const initialData: Record<string, any> = {};
    calculator.inputFields.forEach((field: InputField) => {
      if (field.type === 'select' && field.name === 'sex') {
        initialData[field.name] = '';
        initialData['sex_factor'] = 1.0; // Default to male
      } else {
        initialData[field.name] = '';
      }
    });
    setFormData(initialData);
  };

  const handleInputChange = (fieldName: string, value: string, field: InputField) => {
    setFormData(prev => {
      const updated = { ...prev, [fieldName]: value };
      
      // Handle sex selection - extract sex_factor
      if (fieldName === 'sex' && field.type === 'select' && field.options) {
        const selectedOption = field.options.find((opt: any) => opt.value === value);
        if (selectedOption && selectedOption.sexFactor !== undefined) {
          updated['sex_factor'] = selectedOption.sexFactor;
        }
      }
      
      return updated;
    });
    
    // Clear error for this field
    if (errors[fieldName]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[fieldName];
        return newErrors;
      });
    }
  };

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};
    
    calculator.inputFields.forEach((field: InputField) => {
      if (field.required && !formData[field.name]) {
        newErrors[field.name] = `${field.nameRu || field.name} обязательно`;
      }
      
      if (field.type === 'number' && formData[field.name]) {
        const numValue = parseFloat(formData[field.name]);
        if (isNaN(numValue)) {
          newErrors[field.name] = 'Введите корректное число';
        } else {
          if (field.min !== undefined && numValue < field.min) {
            newErrors[field.name] = `Минимальное значение: ${field.min}`;
          }
          if (field.max !== undefined && numValue > field.max) {
            newErrors[field.name] = `Максимальное значение: ${field.max}`;
          }
        }
      }
    });
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleCalculate = async () => {
    if (!validateForm()) return;
    
    try {
      // Prepare input data with proper types
      const inputData: Record<string, any> = {};
      calculator.inputFields.forEach((field: InputField) => {
        if (field.type === 'number') {
          inputData[field.name] = parseFloat(formData[field.name]);
        } else {
          inputData[field.name] = formData[field.name];
        }
      });
      
      // Add sex_factor
      inputData['sex_factor'] = formData['sex_factor'];
      
      // Calculate on frontend
      const resultValue = calculator.calculate(inputData);
      
      // Interpret result
      const interpretationResult = calculator.interpret 
        ? calculator.interpret(resultValue) 
        : { text: 'Result calculated', textRu: 'Результат рассчитан', severity: 'normal' };
      
      // Save to backend history
      await createResult({
        calculatorName: calculator.name,
        calculatorNameRu: calculator.nameRu,
        inputData,
        resultValue,
        interpretation: interpretationResult.textRu || interpretationResult.text
      });
      
      setResult({
        value: resultValue,
        interpretation: interpretationResult.textRu || interpretationResult.text,
        severity: interpretationResult.severity
      });
    } catch (error: any) {
      console.error('Calculation error:', error);
      alert('Ошибка при расчете. Попробуйте снова.');
    }
  };

  const handleReset = () => {
    initializeForm();
    setResult(null);
    setErrors({});
  };

  const getSeverityColor = () => {
    if (!result) return 'bg-primary';
    
    switch (result.severity) {
      case 'normal':
        return 'bg-success';
      case 'warning':
        return 'bg-warning';
      case 'danger':
        return 'bg-danger';
      default:
        return 'bg-info';
    }
  };

  return (
    <ScrollView className="flex-1 bg-surface">
      {/* Header */}
      <View className="bg-primary px-6 pt-16 pb-8">
        <TouchableOpacity onPress={() => router.back()} className="mb-4">
          <Text className="text-text-inverse text-base">← Назад</Text>
        </TouchableOpacity>
        <Text className="text-3xl font-bold text-text-inverse mb-2">
          {calculator.nameRu || calculator.name}
        </Text>
        <Text className="text-text-inverse opacity-90">
          {calculator.descriptionRu || calculator.description}
        </Text>
      </View>

      {/* Form */}
      <View className="px-6 py-6">
        <View className="bg-surface-elevated rounded-2xl p-6 border border-border mb-6">
          <Text className="text-xl font-bold text-text-primary mb-4">
            Введите данные
          </Text>
          
          {calculator.inputFields.map((field: InputField, index: number) => (
            <View key={field.name} className={index > 0 ? 'mt-4' : ''}>
              <Text className="text-text-primary font-medium mb-2">
                {field.labelRu || field.label}
                {field.required ? ' *' : ''}
                {field.unit ? ` (${field.unitRu || field.unit})` : ''}
              </Text>
              
              {field.type === 'number' ? (
                <TextInput
                  className={`bg-surface border ${errors[field.name] ? 'border-danger' : 'border-border'} rounded-xl px-4 py-3 text-text-primary`}
                  placeholder={`Введите ${(field.nameRu || field.name).toLowerCase()}`}
                  placeholderTextColor="#9ca3af"
                  value={formData[field.name]?.toString() || ''}
                  onChangeText={(text) => handleInputChange(field.name, text, field)}
                  keyboardType="decimal-pad"
                />
              ) : field.type === 'select' ? (
                <View className={`bg-surface border ${errors[field.name] ? 'border-danger' : 'border-border'} rounded-xl overflow-hidden`}>
                  {field.options?.map((option: any) => (
                    <TouchableOpacity
                      key={option.value}
                      onPress={() => handleInputChange(field.name, option.value, field)}
                      className={`px-4 py-3 ${formData[field.name] === option.value ? 'bg-primary-light' : 'bg-surface'} border-b border-border`}
                    >
                      <Text className={`${formData[field.name] === option.value ? 'text-primary font-semibold' : 'text-text-primary'}`}>
                        {option.labelRu || option.label}
                      </Text>
                    </TouchableOpacity>
                  ))}
                </View>
              ) : null}
              
              {errors[field.name] ? (
                <Text className="text-danger text-sm mt-1">{errors[field.name]}</Text>
              ) : null}
            </View>
          ))}
          
          <View className="flex-row gap-3 mt-6">
            <TouchableOpacity
              onPress={handleCalculate}
              disabled={calculating}
              className={`flex-1 py-4 rounded-xl ${calculating ? 'bg-primary opacity-60' : 'bg-primary'}`}
            >
              {calculating ? (
                <ActivityIndicator size="small" color="#fff" />
              ) : (
                <Text className="text-text-inverse text-center font-bold text-base">
                  Рассчитать
                </Text>
              )}
            </TouchableOpacity>
            
            <TouchableOpacity
              onPress={handleReset}
              className="px-6 py-4 rounded-xl border border-border bg-surface"
            >
              <Text className="text-text-primary text-center font-semibold">
                Сбросить
              </Text>
            </TouchableOpacity>
          </View>
        </View>

        {/* Result */}
        {result ? (
          <View className={`${getSeverityColor()} rounded-2xl p-6 mb-6`}>
            <Text className="text-text-inverse text-lg font-semibold mb-2">
              Результат
            </Text>
            <Text className="text-text-inverse text-4xl font-bold mb-4">
              {result.value.toFixed(1)} мл/мин
            </Text>
            <View className="bg-white bg-opacity-20 rounded-xl p-4">
              <Text className="text-text-inverse font-medium">
                {result.interpretation}
              </Text>
            </View>
          </View>
        ) : null}
      </View>
    </ScrollView>
  );
}
