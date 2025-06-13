import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

interface Props {
  children: JSX.Element;
  requiredRoles: string[];
}

const ProtectedRoute: React.FC<Props> = ({ children, requiredRoles }) => {
  const { isAuthenticated, role } = useAuth();

  if (!isAuthenticated) return <Navigate to="/login" replace />;

  if (role && !requiredRoles.includes(role)) return <Navigate to="/" replace />;

  return children;
};

export default ProtectedRoute;
