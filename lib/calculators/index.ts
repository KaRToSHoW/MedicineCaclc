/**
 * Calculator registry
 * All calculators are defined here on the frontend
 */

import { cockcroftGaultCalculator, Calculator } from './cockcroftGault';

// Export all calculators
export const calculators: Calculator[] = [
  cockcroftGaultCalculator
];

// Helper function to get calculator by name
export const getCalculatorByName = (name: string): Calculator | undefined => {
  return calculators.find(calc => calc.name === name);
};

// Export types
export type { Calculator, InputField, InterpretationRule } from './cockcroftGault';
