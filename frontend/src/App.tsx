import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import TeacherDashboard from './pages/TeacherDashboard';
import StudentDashboard from './pages/StudentDashboard';
import CreateQuestions from './pages/CreateQuestions';
import AnalyzeProgress from './pages/AnalyzeProgress';
import MyTopics from './pages/MyTopics';
import QuizScreen from './pages/QuizScreen';
import MyProgress from './pages/MyProgress';
import PrivateRoute from './components/PrivateRoute';

const App: React.FC = () => {
  return (
    <div className="app-wrapper">
      <Header />
      <main style={{ padding: '1rem', minHeight: '80vh' }}>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          <Route path="/student" element={<PrivateRoute allowedRoles={["student"]} />}>
            <Route index element={<StudentDashboard />} />
            <Route path="topics" element={<MyTopics />} />
            <Route path="quiz" element={<QuizScreen />} />
            <Route path="progress" element={<MyProgress />} />
          </Route>

          <Route path="/teacher" element={<PrivateRoute allowedRoles={["teacher"]} />}>
            <Route index element={<TeacherDashboard />} />
            <Route path="create-questions" element={<CreateQuestions />} />
            <Route path="analyze" element={<AnalyzeProgress />} />
          </Route>

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
      <Footer />
    </div>
  );
};

export default App;
