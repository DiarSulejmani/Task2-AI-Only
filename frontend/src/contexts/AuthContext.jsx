import React, { createContext, useEffect, useState } from 'react';
import axios from '../api/api';
import { useNavigate } from 'react-router-dom';

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const stored = localStorage.getItem('dq_user');
    if (stored) {
      setUser(JSON.parse(stored));
    }
  }, []);

  const login = async (email, password) => {
    const res = await axios.post('/login', { email, password });
    setUser(res.data);
    localStorage.setItem('dq_user', JSON.stringify(res.data));
    navigate('/');
  };

  const register = async (name, email, password) => {
    const res = await axios.post('/register', { name, email, password });
    setUser(res.data);
    localStorage.setItem('dq_user', JSON.stringify(res.data));
    navigate('/');
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('dq_user');
    navigate('/');
  };

  return (
    <AuthContext.Provider value={{ user, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
