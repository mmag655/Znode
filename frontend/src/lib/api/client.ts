import axios, { AxiosError, AxiosHeaders, AxiosInstance, AxiosRequestConfig } from 'axios';
import { getAccessToken, setAuthTokens, clearAuthTokens } from './auth';
import { toast } from 'react-toastify';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

interface ApiErrorResponse {
  status: 'error';
  message: string;
  error: {
    code: number;
    detail: string;
  };
}

const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

let isRefreshing = false;
let refreshSubscribers: ((token: string) => void)[] = [];

function onRefreshed(token: string) {
  refreshSubscribers.forEach((cb) => cb(token));
  refreshSubscribers = [];
}

function addSubscriber(cb: (token: string) => void) {
  refreshSubscribers.push(cb);
}

// Modify this function to properly handle `AxiosHeaders` with the `.set()` method
function setAuthHeader(headers: AxiosHeaders, token: string) {
  if (headers) {
    headers.set('Authorization', `Bearer ${token}`);  // Correct way to set headers in Axios
  }
}

apiClient.interceptors.request.use((config) => {
  const token = getAccessToken();
  if (token && config.headers) {
    setAuthHeader(config.headers as AxiosHeaders, token);
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean };
    const status = error.response?.status;
    const errorData = error.response?.data as ApiErrorResponse;
    const errorMessage = errorData?.message || 'Something went wrong';

    // Token expired - Try refresh
    if (status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      if (isRefreshing) {
        return new Promise((resolve) => {
          addSubscriber((token: string) => {
            setAuthHeader(originalRequest.headers as AxiosHeaders, token);
            resolve(apiClient(originalRequest));
          });
        });
      }

      isRefreshing = true;
      try {
        const response = await axios.post(`${API_BASE_URL}/auth/token/refresh`, {}, {
          withCredentials: true,
        });

        const access_token = response.data.data.access_token;
        setAuthTokens(access_token);
        onRefreshed(access_token);
        setAuthHeader(originalRequest.headers as AxiosHeaders, access_token);

        return apiClient(originalRequest);
      } catch (refreshError) {
        clearAuthTokens();
        toast.error('Session expired. Please log in again.');

        // 🔁 Redirect to login
        if (typeof window !== 'undefined') {
          window.location.href = '/auth/login';
        }

        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    // Handle other errors
    switch (status) {
      case 401:
        toast.info(errorMessage || 'Session expired. Please log in again.');
        clearAuthTokens();
        if (typeof window !== 'undefined') {
          window.location.href = '/auth/login';
        }
        break;
      case 400:
        toast.error(errorMessage || 'Bad request. Please check your input.');
        break;
      case 403:
        toast.error(errorMessage || 'Access denied. You do not have permission.');
        break;
      case 404:
        toast.error(errorMessage || 'Resource not found.');
        break;
      case 500:
        toast.error(errorMessage || 'Internal server error.');
        break;
      default:
        toast.error(errorMessage || 'Something went wrong.');
        break;
    }

    return Promise.reject(error);
  }
);

export default apiClient;
