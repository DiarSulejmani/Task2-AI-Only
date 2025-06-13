import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout/Layout';
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import TeacherDashboard from './pages/dashboards/TeacherDashboard';
import StudentDashboard from './pages/dashboards/StudentDashboard';
import CreateQuestions from './pages/teacher/CreateQuestions';
import AnalyzeProgress from './pages/teacher/AnalyzeProgress';
import MyTopics from './pages/teacher/MyTopics';
import Quiz from './pages/student/Quiz';
import MyProgress from './pages/student/MyProgress';
import ProtectedRoute from './components/ProtectedRoute';

const AppRouter: React.FC = () => {
  return (
    <Routes>
      <Route element={<Layout />}>            
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />

        {/* Teacher */}
        <Route element={<ProtectedRoute roles={['teacher']} />}>  
          <Route path="/teacher" element={<TeacherDashboard />} />
          <Route path="/teacher/create-questions" element={<CreateQuestions />} />
          <Route path="/teacher/analyze-progress" element={<AnalyzeProgress />} />
          <Route path="/teacher/my-topics" element={<MyTopics />} />
        </Route>

        {/* Student */}
        <Route element={<ProtectedRoute roles={['student']} />}> 
          <Route path="/student" element={<StudentDashboard />} />
          <Route path="/student/quiz" element={<Quiz />} />
          <Route path="/student/my-progress" element={<MyProgress />} />
        </Route>

        {/* Fallback */}
        <Route path="*" element={<LandingPage />} />
      </Route>
    </Routes>
  );
};

export default AppRouter;
