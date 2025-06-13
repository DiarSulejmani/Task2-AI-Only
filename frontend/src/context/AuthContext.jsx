import React, { createContext, useContext, useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => JSON.parse(localStorage.getItem('user')) || null);
  const [role, setRole] = useState(() => localStorage.getItem('role') || null);
  const navigate = useNavigate();

  useEffect(() => {
    if (user) {
      localStorage.setItem('user', JSON.stringify(user));
      localStorage.setItem('role', role);
    } else {
      localStorage.removeItem('user');
      localStorage.removeItem('role');
    }
  }, [user, role]);

  const login = async (email, password) => {
    const { data } = await axios.post('/login', { email, password });
    setUser(data.user);
    setRole(data.role);
    navigate(data.role === 'teacher' ? '/teacher' : '/student');
  };

  const register = async (form) => {
    const { data } = await axios.post('/register', form);
    setUser(data.user);
    setRole(data.role);
    navigate(data.role === 'teacher' ? '/teacher' : '/student');
  };

  const logout = async () => {
    await axios.post('/logout');
    setUser(null);
    setRole(null);
    navigate('/');
  };

  return (
    <AuthContext.Provider value={{ user, role, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
