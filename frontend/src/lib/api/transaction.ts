// /src/lib/api/activity.ts
import apiClient from './client';
import { Transaction } from './types';

// Fetch all activities
export const fetchTransactions = async (): Promise<Transaction[]> => {
    const response = await apiClient.get('/transaction/all');
    const data = response?.data?.data;
  
    // Ensure it returns an array even if the API returns something unexpected
    if (!Array.isArray(data)) {
      return [];
    }
  
    return data;
  };