import React, { createContext, useContext, useEffect, useState } from 'react';
import api from '../utils/api';

interface User {
  id: string;
  email: string;
  role: 'student' | 'teacher';
}

interface AuthContextValue {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  register: (email: string, password: string, role: 'student' | 'teacher') => Promise<void>;
}

const AuthContext = createContext<AuthContextValue>({
  user: null,
  loading: true,
  login: async () => {},
  logout: async () => {},
  register: async () => {},
});

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    (async () => {
      try {
        const res = await api.get('/auth/session');
        setUser(res.user);
      } catch (_) {
        setUser(null);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const login = async (email: string, password: string) => {
    setLoading(true);
    const res = await api.post('/auth/login', { email, password });
    setUser(res.user);
    setLoading(false);
  };

  const logout = async () => {
    setLoading(true);
    await api.post('/auth/logout');
    setUser(null);
    setLoading(false);
  };

  const register = async (email: string, password: string, role: 'student' | 'teacher') => {
    setLoading(true);
    await api.post('/auth/register', { email, password, role });
    await login(email, password);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, register }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
