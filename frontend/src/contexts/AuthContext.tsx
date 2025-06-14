import React, { createContext, useContext, useEffect, useState } from 'react';

type Role = 'teacher' | 'student';
interface User {
  id: string;
  role: Role;
  token: string;
}

interface AuthContextProps {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, role: Role) => Promise<void>;
  logout: () => void;
}

export const AuthContext = createContext<AuthContextProps | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const stored = localStorage.getItem('auth');
    if (stored) {
      setUser(JSON.parse(stored));
    }
  }, []);

  const login = async (email: string, password: string) => {
    const res = await fetch('/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    if (!res.ok) throw new Error('Login failed');
    const data = await res.json();
    const userObj = { id: data.id, role: data.role as Role, token: data.token } as User;
    localStorage.setItem('auth', JSON.stringify(userObj));
    setUser(userObj);
  };

  const register = async (email: string, password: string, role: Role) => {
    const res = await fetch('/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, role }),
    });
    if (!res.ok) throw new Error('Register failed');
    const data = await res.json();
    const userObj = { id: data.id, role: data.role as Role, token: data.token } as User;
    localStorage.setItem('auth', JSON.stringify(userObj));
    setUser(userObj);
  };

  const logout = () => {
    localStorage.removeItem('auth');
    setUser(null);
  };

  const value: AuthContextProps = { user, login, register, logout };
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
};
