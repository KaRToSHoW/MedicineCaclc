/**
 * CalculationResults Store
 * Zustand store for managing calculation_results state
 * Firebase Firestore only
 */

import { create } from 'zustand';
import { calculationResultsService } from '@/services/calculation_results';
import type { CalculationResult, CreateCalculationResultInput } from '@/types/calculation_results';

interface CalculationResultsStore {
  // State
  items: CalculationResult[];
  loading: boolean;
  error: string | null;

  // Actions
  fetchAll: () => Promise<void>;
  addItem: (data: CreateCalculationResultInput) => Promise<CalculationResult | null>;
  reset: () => void;
}

export const useCalculationResultsStore = create<CalculationResultsStore>((set) => ({
  items: [],
  loading: false,
  error: null,

  fetchAll: async () => {
    set({ loading: true, error: null });
    try {
      const items = await calculationResultsService.getAll();
      set({ items, loading: false });
    } catch (error: any) {
      console.error('Failed to fetch calculation_results:', error);
      
      // Check if it's an authentication error
      if (error.message?.includes('authenticated')) {
        set({ 
          items: [], 
          error: 'Войдите в систему для просмотра истории расчётов', 
          loading: false 
        });
      } else {
        set({ 
          error: error.message || 'Не удалось загрузить результаты расчётов', 
          loading: false 
        });
      }
    }
  },

  addItem: async (data: CreateCalculationResultInput) => {
    try {
      const newItem = await calculationResultsService.create(data);
      set((state) => ({
        items: [newItem, ...state.items]
      }));
      return newItem;
    } catch (error: any) {
      console.error('Failed to create calculation_result:', error);
      
      // Check if it's an authentication error
      if (error.message?.includes('authenticated')) {
        set({ error: 'Войдите в систему для сохранения результатов' });
      } else {
        set({ error: error.message || 'Не удалось сохранить результат расчёта' });
      }
      return null;
    }
  },

  reset: () => set({ items: [], loading: false, error: null }),
}));
