// /src/lib/api/activity.ts
import apiClient from './client';
import { AdminTransactionLog, Transaction } from './types';

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

  export const fetchAllTransactions = async (): Promise<AdminTransactionLog[]> => {
    const response = await apiClient.get('/transaction/admin/all');
    console.log("transaction response data : ", response.data.data)
    const data = response?.data?.data;
  
    // Ensure it returns an array even if the API returns something unexpected
    if (!Array.isArray(data)) {
      return [];
    }
  
    return data;
  }

  export const approveTransaction = async (transaction_ids: number[]): Promise<void> => {
    const response = await apiClient.patch('/transaction/admin/approve', { transaction_ids: transaction_ids });
    return response.data.data;
  }