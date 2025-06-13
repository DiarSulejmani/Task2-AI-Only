import pathlib, textwrap, json, os, sys

base_dir = pathlib.Path('frontend')
base_dir.mkdir(exist_ok=True)

files = {}

# Basic config files
files['package.json'] = textwrap.dedent('''
{
  "name": "duoquanto-frontend",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "axios": "^1.5.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.14.2"
  },
  "devDependencies": {
    "@types/react": "^18.2.12",
    "@types/react-dom": "^18.2.5",
    "@vitejs/plugin-react": "^4.0.0",
    "typescript": "^5.2.2",
    "vite": "^4.4.9"
  }
}
''')

files['vite.config.ts'] = textwrap.dedent('''
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
  },
});
''')

files['tsconfig.json'] = textwrap.dedent('''
{
  "compilerOptions": {
    "target": "ESNext",
    "useDefineForClassFields": true,
    "lib": ["DOM", "DOM.Iterable", "ESNext"],
    "allowJs": false,
    "skipLibCheck": true,
    "esModuleInterop": false,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "module": "ESNext",
    "moduleResolution": "Node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx"
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
''')

files['tsconfig.node.json'] = textwrap.dedent('''
{
  "compilerOptions": {
    "composite": true,
    "module": "ESNext",
    "moduleResolution": "Node",
    "allowSyntheticDefaultImports": true
  },
  "include": ["vite.config.ts"]
}
''')

files['index.html'] = textwrap.dedent('''
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>DuoQuanto</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
''')

# src/main.tsx
files['src/main.tsx'] = textwrap.dedent('''
import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>
);
''')

# src/App.tsx
files['src/App.tsx'] = textwrap.dedent('''
import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import AboutPage from './pages/AboutPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import TeacherDashboard from './pages/TeacherDashboard';
import StudentDashboard from './pages/StudentDashboard';
import CreateQuestions from './pages/CreateQuestions';
import AnalyzeProgress from './pages/AnalyzeProgress';
import MyTopics from './pages/MyTopics';
import Quiz from './pages/Quiz';
import MyProgress from './pages/MyProgress';

import Header from './components/layout/Header';
import Footer from './components/layout/Footer';
import ProtectedRoute from './utils/ProtectedRoute';
import { AuthProvider } from './context/AuthContext';

const App: React.FC = () => {
  return (
    <AuthProvider>
      <Header />
      <Routes>
        {/* Public */}
        <Route path="/" element={<LandingPage />} />
        <Route path="/about" element={<AboutPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />

        {/* Teacher */}
        <Route
          path="/teacher"
          element={
            <ProtectedRoute requiredRoles={['teacher']}>
              <TeacherDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/teacher/create-questions"
          element={
            <ProtectedRoute requiredRoles={['teacher']}>
              <CreateQuestions />
            </ProtectedRoute>
          }
        />
        <Route
          path="/teacher/analyze-progress"
          element={
            <ProtectedRoute requiredRoles={['teacher']}>
              <AnalyzeProgress />
            </ProtectedRoute>
          }
        />

        {/* Student */}
        <Route
          path="/student"
          element={
            <ProtectedRoute requiredRoles={['student']}>
              <StudentDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/student/topics"
          element={
            <ProtectedRoute requiredRoles={['student']}>
              <MyTopics />
            </ProtectedRoute>
          }
        />
        <Route
          path="/student/quiz"
          element={
            <ProtectedRoute requiredRoles={['student']}>
              <Quiz />
            </ProtectedRoute>
          }
        />
        <Route
          path="/student/progress"
          element={
            <ProtectedRoute requiredRoles={['student']}>
              <MyProgress />
            </ProtectedRoute>
          }
        />

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
      <Footer />
    </AuthProvider>
  );
};

export default App;
''')

# AuthContext
files['src/context/AuthContext.tsx'] = textwrap.dedent('''
import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from '../api/duoquanto';

export type Role = 'teacher' | 'student' | null;

interface AuthContextType {
  role: Role;
  isAuthenticated: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [role, setRole] = useState<Role>(() => {
    const stored = localStorage.getItem('role');
    return stored ? (stored as Role) : null;
  });
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(() => {
    return localStorage.getItem('isAuthenticated') === 'true';
  });

  useEffect(() => {
    if (role) localStorage.setItem('role', role);
    localStorage.setItem('isAuthenticated', String(isAuthenticated));
  }, [role, isAuthenticated]);

  const login = async (username: string, password: string) => {
    // TODO: replace with backend endpoint
    const res = await axios.post('/auth/login', { username, password });
    if (res.status === 200) {
      setRole(res.data.role as Role);
      setIsAuthenticated(true);
    }
  };

  const logout = () => {
    setRole(null);
    setIsAuthenticated(false);
    localStorage.removeItem('role');
    localStorage.removeItem('isAuthenticated');
  };

  return (
    <AuthContext.Provider value={{ role, isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
};
''')

# ProtectedRoute util
files['src/utils/ProtectedRoute.tsx'] = textwrap.dedent('''
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
''')

# API instance
files['src/api/duoquanto.ts'] = textwrap.dedent('''
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: true,
});

export default api;
''')

# Header component
files['src/components/layout/Header.tsx'] = textwrap.dedent('''
import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const Header: React.FC = () => {
  const { role, isAuthenticated, logout } = useAuth();

  return (
    <header style={{ padding: '1rem', backgroundColor: '#f5f5f5' }}>
      <nav style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
        <Link to="/">Home</Link>
        <Link to="/about">About</Link>
        {!isAuthenticated && <Link to="/login">Login</Link>}
        {!isAuthenticated && <Link to="/register">Register</Link>}

        {role === 'teacher' && (
          <>
            <Link to="/teacher">Dashboard</Link>
            <Link to="/teacher/create-questions">Create Questions</Link>
            <Link to="/teacher/analyze-progress">Analyze Progress</Link>
          </>
        )}
        {role === 'student' && (
          <>
            <Link to="/student">Dashboard</Link>
            <Link to="/student/topics">My Topics</Link>
            <Link to="/student/quiz">Quiz</Link>
            <Link to="/student/progress">My Progress</Link>
          </>
        )}

        {isAuthenticated && (
          <button style={{ marginLeft: 'auto' }} onClick={logout}>
            Logout
          </button>
        )}
      </nav>
    </header>
  );
};

export default Header;
''')

# Footer component
files['src/components/layout/Footer.tsx'] = textwrap.dedent('''
import React from 'react';

const Footer: React.FC = () => {
  return (
    <footer style={{ padding: '1rem', backgroundColor: '#f5f5f5', textAlign: 'center' }}>
      DuoQuanto © {new Date().getFullYear()}
    </footer>
  );
};

export default Footer;
''')

# Pages
page_names = [
    'LandingPage',
    'AboutPage',
    'LoginPage',
    'RegisterPage',
    'TeacherDashboard',
    'StudentDashboard',
    'CreateQuestions',
    'AnalyzeProgress',
    'MyTopics',
    'Quiz',
    'MyProgress',
]

for page in page_names:
    display_name = page.replace('Page', '').replace('Dashboard', ' Dashboard')
    files[f'src/pages/{page}.tsx'] = textwrap.dedent(f'''
import React from 'react';

const {page}: React.FC = () => (
  <div style={{{{ padding: '2rem' }}}}>
    <h1>{display_name}</h1>
    <p>This is the {display_name}.</p>
  </div>
);

export default {page};
''')

# Write files
created = []
for rel_path, content in files.items():
    path = base_dir / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.lstrip())
    created.append(str(path))

print(json.dumps({'created': created, 'count': len(created)}, indent=2))