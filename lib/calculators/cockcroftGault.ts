/**
 * Cockcroft-Gault Creatinine Clearance Calculator
 * Formula: ((140 - age) * weight * sex_factor) / (72 * creatinine)
 */

export interface InputField {
  name: string;
  nameRu?: string;
  type: 'number' | 'select' | 'text';
  label: string;
  labelRu?: string;
  required?: boolean;
  min?: number;
  max?: number;
  step?: number;
  unit?: string;
  unitRu?: string;
  options?: {
    value: string;
    label: string;
    labelRu?: string;
    sexFactor?: number;
  }[];
}

export interface InterpretationRule {
  condition: string;
  interpretation: string;
  interpretationRu?: string;
  severity?: 'normal' | 'warning' | 'danger';
}

export interface Calculator {
  name: string;
  nameRu?: string;
  description?: string;
  descriptionRu?: string;
  category: string;
  categoryRu?: string;
  inputFields: InputField[];
  interpretationRules?: InterpretationRule[];
  calculate: (inputData: Record<string, any>) => number;
  interpret?: (resultValue: number) => { text: string; textRu?: string; severity?: string };
}

export const cockcroftGaultCalculator: Calculator = {
  name: 'Cockcroft-Gault Creatinine Clearance',
  nameRu: 'Клиренс креатинина (Cockcroft-Gault)',
  description: 'Kidney function assessment for medication dose adjustment',
  descriptionRu: 'Оценка функции почек для коррекции доз лекарств',
  category: 'nephrology',
  categoryRu: 'нефрология',
  
  inputFields: [
    {
      name: 'age',
      nameRu: 'возраст',
      type: 'number',
      label: 'Age',
      labelRu: 'Возраст',
      required: true,
      min: 18,
      max: 120,
      step: 1,
      unit: 'years',
      unitRu: 'лет'
    },
    {
      name: 'weight',
      nameRu: 'вес',
      type: 'number',
      label: 'Weight',
      labelRu: 'Вес',
      required: true,
      min: 30,
      max: 300,
      step: 0.1,
      unit: 'kg',
      unitRu: 'кг'
    },
    {
      name: 'creatinine',
      nameRu: 'креатинин',
      type: 'number',
      label: 'Serum Creatinine',
      labelRu: 'Креатинин сыворотки',
      required: true,
      min: 0.1,
      max: 20,
      step: 0.1,
      unit: 'mg/dL',
      unitRu: 'мг/дл'
    },
    {
      name: 'sex',
      nameRu: 'пол',
      type: 'select',
      label: 'Sex',
      labelRu: 'Пол',
      required: true,
      options: [
        {
          value: 'male',
          label: 'Male',
          labelRu: 'Мужской',
          sexFactor: 1.0
        },
        {
          value: 'female',
          label: 'Female',
          labelRu: 'Женский',
          sexFactor: 0.85
        }
      ]
    }
  ],
  
  interpretationRules: [
    {
      condition: 'result >= 90',
      interpretation: 'Normal kidney function (CKD Stage 1)',
      interpretationRu: 'Нормальная функция почек (ХБП стадия 1)',
      severity: 'normal'
    },
    {
      condition: 'result >= 60 and result < 90',
      interpretation: 'Mild reduction in kidney function (CKD Stage 2)',
      interpretationRu: 'Легкое снижение функции почек (ХБП стадия 2)',
      severity: 'normal'
    },
    {
      condition: 'result >= 30 and result < 60',
      interpretation: 'Moderate reduction in kidney function (CKD Stage 3)',
      interpretationRu: 'Умеренное снижение функции почек (ХБП стадия 3)',
      severity: 'warning'
    },
    {
      condition: 'result >= 15 and result < 30',
      interpretation: 'Severe reduction in kidney function (CKD Stage 4)',
      interpretationRu: 'Выраженное снижение функции почек (ХБП стадия 4)',
      severity: 'danger'
    },
    {
      condition: 'result < 15',
      interpretation: 'Kidney failure (CKD Stage 5)',
      interpretationRu: 'Почечная недостаточность (ХБП стадия 5)',
      severity: 'danger'
    }
  ],
  
  calculate: (inputData: Record<string, any>): number => {
    const age = parseFloat(inputData.age);
    const weight = parseFloat(inputData.weight);
    const creatinine = parseFloat(inputData.creatinine);
    const sexFactor = parseFloat(inputData.sex_factor || inputData.sexFactor || '1.0');
    
    // Cockcroft-Gault formula: ((140 - age) * weight * sex_factor) / (72 * creatinine)
    const result = ((140 - age) * weight * sexFactor) / (72 * creatinine);
    
    return Math.round(result * 100) / 100; // Round to 2 decimal places
  },
  
  interpret: (resultValue: number) => {
    const rules = cockcroftGaultCalculator.interpretationRules || [];
    
    for (const rule of rules) {
      const condition = rule.condition;
      
      try {
        // Parse condition and check if result matches
        if (condition.includes('>=') && condition.includes('and') && condition.includes('<')) {
          // Range: result >= X and result < Y
          const parts = condition.split('and');
          const minMatch = parts[0].match(/>=\s*(\d+\.?\d*)/);
          const maxMatch = parts[1].match(/<\s*(\d+\.?\d*)/);
          
          if (minMatch && maxMatch) {
            const minVal = parseFloat(minMatch[1]);
            const maxVal = parseFloat(maxMatch[1]);
            
            if (resultValue >= minVal && resultValue < maxVal) {
              return {
                text: rule.interpretation,
                textRu: rule.interpretationRu,
                severity: rule.severity
              };
            }
          }
        } else if (condition.includes('>=')) {
          // Greater than or equal: result >= X
          const match = condition.match(/>=\s*(\d+\.?\d*)/);
          if (match) {
            const minVal = parseFloat(match[1]);
            if (resultValue >= minVal) {
              return {
                text: rule.interpretation,
                textRu: rule.interpretationRu,
                severity: rule.severity
              };
            }
          }
        } else if (condition.includes('<')) {
          // Less than: result < X
          const match = condition.match(/<\s*(\d+\.?\d*)/);
          if (match) {
            const maxVal = parseFloat(match[1]);
            if (resultValue < maxVal) {
              return {
                text: rule.interpretation,
                textRu: rule.interpretationRu,
                severity: rule.severity
              };
            }
          }
        }
      } catch (error) {
        continue;
      }
    }
    
    return {
      text: 'Result calculated',
      textRu: 'Результат рассчитан',
      severity: 'normal'
    };
  }
};
