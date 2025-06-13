import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

interface Props {
  roles?: Array<'teacher' | 'student'>;
}

const ProtectedRoute: React.FC<Props> = ({ roles }) => {
  const { user } = useAuth();

  if (!user) return <Navigate to="/login" replace />;
  if (roles && !roles.includes(user.role)) {
    return user.role === 'teacher' ? (
      <Navigate to="/teacher" replace />
    ) : (
      <Navigate to="/student" replace />
    );
  }
  return <Outlet />;
};

export default ProtectedRoute;
