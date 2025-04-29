import { AxiosError } from 'axios';
import apiClient from './client';
import { BulkUserImport } from './types';

type LoginResponse = {
  access_token: string;
  token_type: string;
};

type UserData = {
  email: string;
  password: string;
  username?: string;
};

// Token management
export const setAuthTokens = (accessToken: string) => {
  if (typeof window !== 'undefined') {
    console.log("saving token to loacl storage", accessToken)
    localStorage.setItem('access_token', accessToken);
    // Refresh token is httpOnly cookie, no need to store in localStorage
  }
};

export const getAccessToken = (): string | null => {
  if (typeof window !== 'undefined') {
    console.log("get access token called")
    return localStorage.getItem('access_token');
  }
  return null;
};

export const clearAuthTokens = () => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('access_token');
  }
};

// API calls
export const login = async (credentials: UserData): Promise<LoginResponse> => {
    console.log("calling login .....................");
    const response = await apiClient.post('/auth/login', credentials);
    console.log("response data : ", response.data)
    const { access_token } = response.data.data;
    
    console.log("access token : ", access_token);
  
    setAuthTokens(access_token); // Must be before any navigation or reload
    return response.data;
};
  
export const signup = async (userData: UserData) => {
  try {
    const response = await apiClient.post('/auth/signup', userData);
    console.log("response data : ", response.data)
    console.log("response.data.status : ", response.data.status)
    if (response.data.status !== 'success') {
      throw new Error(response.data.message || 'Failed to sign up');
    }
    console.log("response.data.data : ", response.data.data)
    return response.data.data;
    
  } catch (error) {
    if (error instanceof AxiosError) {
      console.error('Error response:', error.response);
      throw new Error(error.response?.data?.message || 'Signup error');
    } else if (error instanceof Error) {
      console.error('Error:', error.message);
      throw new Error(error.message || 'Signup error');
    } else {
      console.error('Unknown error:', error);
      throw new Error('Signup error');
    }
  }
};


export const logout = async () => {
  try {
    await apiClient.post('/auth/logout');
  } finally {
    clearAuthTokens();
  }
};

export const getCurrentUser = async () => {
  const response = await apiClient.get('/users/get');
  return response.data;
};

export const getAllUsers = async () => {

  const response = await apiClient.get('/users/all');
  return response.data.data;
}

export const bulkCreate = async (usersData: BulkUserImport[]) => {
  const response = await apiClient.post('/users/bulk/create', usersData);
  return response.data;
};

export const updateUserStatus = async (data: {
    is_first_time_login: boolean;
    import_status: string;
  }) => {
    console.log("data update user : ", data)
    const response = await apiClient.patch('/users/update', data);
    return response.data;
  };

  export const updateUserProfile = async (data: {
    user_id: number;
    email: string;
    nodes: number; 
  }) => {
    console.log("Updating user profile data:", data);
    const response = await apiClient.patch('/users/update', data);
    return response.data;
  };

  export const suspendUser = async (user_id: number) => {
    console.log("Suspending user:", user_id);
    const response = await apiClient.patch(`/users/suspend/${user_id}`);
    return response.data;
  };


  export const resetPassword = async (token: string, new_password: string) => {
    try {
      const response = await apiClient.post('/auth/reset-password', {
        "token": token,
        "new_password": new_password,
      });
      return response.data;
    } catch (error) {
      if (error instanceof AxiosError) {
        console.error('Error response:', error.response);
        throw new Error(error.response?.data?.message || 'Signup error');
      } else if (error instanceof Error) {
        console.error('Error:', error.message);
        throw new Error(error.message || 'Signup error');
      } else {
        console.error('Unknown error:', error);
        throw new Error('Signup error');
      }
    }
  };

  export const forgotPassword = async (email: string) => {
    try {
      const response = await apiClient.post('/auth/forgot-password', {"email": email});
      return response.data;
    } catch (error) {
      if (error instanceof AxiosError) {
        console.error('Error response:', error.response);
        throw new Error(error.response?.data?.message || 'Signup error');
      } else if (error instanceof Error) {
        console.error('Error:', error.message);
        throw new Error(error.message || 'Signup error');
      } else {
        console.error('Unknown error:', error);
        throw new Error('Signup error');
      }
    }
  };