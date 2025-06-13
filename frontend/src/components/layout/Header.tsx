import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import styles from '../../styles/layout.module.css';

const Header: React.FC = () => {
  const { user, logout } = useAuth();
  return (
    <header className={styles.header}>
      <h1>DuoQuanto</h1>
      <nav>
        <ul>
          <li><Link to="/">Home</Link></li>
          {!user && (
            <>
              <li><Link to="/login">Login</Link></li>
              <li><Link to="/register">Register</Link></li>
            </>
          )}
          {user?.role === 'teacher' && (
            <>
              <li><Link to="/teacher">Dashboard</Link></li>
              <li><Link to="/teacher/create-questions">Create Questions</Link></li>
              <li><Link to="/teacher/analyze-progress">Analyze Progress</Link></li>
              <li><Link to="/teacher/my-topics">My Topics</Link></li>
            </>
          )}
          {user?.role === 'student' && (
            <>
              <li><Link to="/student">Dashboard</Link></li>
              <li><Link to="/student/quiz">Quiz</Link></li>
              <li><Link to="/student/my-progress">My Progress</Link></li>
            </>
          )}
          {user && (
            <li>
              <button onClick={logout}>Logout</button>
            </li>
          )}
        </ul>
      </nav>
    </header>
  );
};

export default Header;
