/**
 * CalculationResults API Service
 * Firebase Firestore only - no local storage
 */

import { db, authReady, getCurrentFirebaseUser } from './firebase';
import { 
  collection, 
  getDocs, 
  getDoc,
  doc,
  addDoc, 
  query, 
  where, 
  orderBy 
} from 'firebase/firestore';
import type {
  CalculationResult,
  CalculationResultResponse,
  CalculationResultsResponse,
  CreateCalculationResultInput,
} from '../types/calculation_results';

class CalculationResultsService {
  /**
   * Get all calculation results for current user from Firestore
   */
  async getAll(): Promise<CalculationResultsResponse> {
    await authReady;
    const currentUser = await getCurrentFirebaseUser();
    
    if (!currentUser) {
      throw new Error('User must be authenticated to access calculation results');
    }

    const uid = currentUser.uid;

    try {
      const col = collection(db, 'calculation_results');
      const q = query(
        col, 
        where('userId', '==', uid), 
        orderBy('performedAt', 'desc')
      );
      const snap = await getDocs(q);
      const items: CalculationResult[] = snap.docs.map(d => ({ 
        id: d.id, 
        ...(d.data() as any) 
      }));
      return items as CalculationResultsResponse;
    } catch (err) {
      console.error('Failed to fetch calculation results from Firestore:', err);
      throw new Error('Failed to load calculation results');
    }
  }

  /**
   * Get a single calculation result by ID
   */
  async getById(id: string): Promise<CalculationResultResponse> {
    await authReady;
    const currentUser = await getCurrentFirebaseUser();
    
    if (!currentUser) {
      throw new Error('User must be authenticated');
    }

    try {
      const docRef = doc(db, 'calculation_results', id);
      const docSnap = await getDoc(docRef);
      
      if (!docSnap.exists()) {
        throw new Error('Calculation result not found');
      }

      const data = docSnap.data();
      
      // Verify ownership
      if (data.userId !== currentUser.uid) {
        throw new Error('Access denied');
      }

      return { id: docSnap.id, ...data } as CalculationResultResponse;
    } catch (err) {
      console.error('Failed to fetch calculation result:', err);
      throw err;
    }
  }

  /**
   * Create a new calculation result in Firestore
   */
  async create(data: CreateCalculationResultInput): Promise<CalculationResultResponse> {
    await authReady;
    const currentUser = await getCurrentFirebaseUser();
    
    if (!currentUser) {
      throw new Error('User must be authenticated to save calculation results');
    }

    const uid = currentUser.uid;

    const payload: any = {
      ...data,
      userId: uid,
      performedAt: new Date().toISOString(),
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };

    try {
      const ref = await addDoc(collection(db, 'calculation_results'), payload);
      const saved = { id: ref.id, ...payload } as CalculationResultResponse;
      return saved;
    } catch (err) {
      console.error('Failed to save calculation result to Firestore:', err);
      throw new Error('Failed to save calculation result');
    }
  }
}

export const calculationResultsService = new CalculationResultsService();
