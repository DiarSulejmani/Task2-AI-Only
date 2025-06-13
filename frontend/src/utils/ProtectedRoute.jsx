import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const ProtectedRoute = ({ role }) => {
  const { user, role: userRole } = useAuth();
  if (!user) return <Navigate to="/login" replace />;
  if (role && role !== userRole) return <Navigate to="/" replace />;
  return <Outlet />;
};

export default ProtectedRoute;
