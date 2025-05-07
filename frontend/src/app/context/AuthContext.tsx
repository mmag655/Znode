'use client';

import { createContext, useContext, useState, ReactNode, useEffect } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { login, logout, signup, getCurrentUser, clearAuthTokens, User, getAccessToken, updateUserStatus, resetPassword as resetPasswordAPI, forgotPassword as forgotPasswordAPI } from '@/lib/api';

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  signup: (email: string, password: string, name: string) => Promise<void>;
  logout: () => Promise<void>;
  forgotPassword: (email: string) => Promise<string>;
  resetPassword: (token: string, newPassword: string) => Promise<string>;
  completeFirstTimeLogin: () => Promise<void>;
  isAuthenticated: boolean;
  loading: boolean;
  error: string | null;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    const loadUser = async () => {
      const token = getAccessToken();
      console.log("Token from localStorage on loadUser():", token);

      if (!token) {
        setLoading(false);
        return;
      }

      try {
        const userData = await getCurrentUser();
        console.log("User loaded from token:", userData);
        setUser(userData.data);
      } catch (err) {
        console.log("Error fetching user. Clearing tokens.", err);
        clearAuthTokens();
      } finally {
        setLoading(false);
      }
    };

    loadUser();
  }, [pathname, router]);

  const resetPassword = async (token: string, newPassword: string) => {
    const response = await resetPasswordAPI(token, newPassword);
    return response;
  };

  const forgotPassword = async (email: string) => {
    const response = await forgotPasswordAPI(email);
    return response.data.reset_token;
  };

  const completeFirstTimeLogin = async () => {
    try {
      if (!user) throw new Error('No user logged in');
      
      await updateUserStatus({
        is_first_time_login: false,
        import_status: 'completed'
      });

      setUser({
        ...user,
        is_first_time_login: false,
        import_status: 'completed'
      });
      
      router.push('/');
    } catch (err) {
      console.error('Failed to complete first time login', err);
      throw err;
    }
  };
  
  const handleLogin = async (email: string, password: string) => {
    setLoading(true);
    setError(null);
    try {
      await login({ email, password });
      const userData = await getCurrentUser();
      setUser(userData.data);
      router.push('/');
    } catch (err) {
      setError('Login failed');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const handleSignup = async (email: string, password: string, username: string) => {
    setLoading(true);
    setError(null);
    try {
      await signup({ email, password, username });
      await handleLogin(email, password);
    } catch (err) {
      setError('Signup failed');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    try {
      await logout();
      setUser(null);
      router.push('/auth/login');
    } catch (err) {
      console.error('Logout failed', err);
    }
  };

  const value = {
    user,
    login: handleLogin,
    signup: handleSignup,
    logout: handleLogout,
    forgotPassword,
    resetPassword,
    completeFirstTimeLogin,
    isAuthenticated: !!user,
    loading,
    error,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

export function AuthInitializer({ children }: { children: ReactNode }) {
  const { loading, isAuthenticated, user } = useAuth();
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    if (loading) return;

    // Redirect unauthenticated users
    if (!isAuthenticated && !pathname.startsWith('/auth')) {
      router.push('/auth/login');
      return;
    }

    // Handle first-time login
    if (user?.is_first_time_login && 
        user?.import_status === 'pending' && 
        !pathname.includes('/auth/reset-password')) {
      router.push('/auth/reset-password');
    }
  }, [loading, isAuthenticated, user, pathname, router]);

  return (
    <>
      {loading && (
        <div className="fixed inset-0 bg-white/80 z-50 flex items-center justify-center">
          Loading...
        </div>
      )}
      {children}
    </>
  );
}