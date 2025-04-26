// /src/lib/api/activity.ts
import apiClient from './client';
import { Activity } from './types';

// Fetch all activities
export const fetchActivities = async (): Promise<Activity[]> => {
    const response = await apiClient.get('/activity/all');
    const data = response?.data?.data;
  
    // Ensure it returns an array even if the API returns something unexpected
    if (!Array.isArray(data)) {
      return [];
    }
  
    return data;
  };
 
  export const fetchRewards = async (): Promise<Activity[]> => {
    const response = await apiClient.get('/activity/all_reward');
    const data = response?.data?.data;
  
    // Ensure it returns an array even if the API returns something unexpected
    if (!Array.isArray(data)) {
      return [];
    }
  
    return data;
  };
  