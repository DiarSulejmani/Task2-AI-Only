import pathlib, textwrap

files = {}

# package.json
files['frontend/package.json'] = textwrap.dedent('''
{
  "name": "duoquanto-frontend",
  "version": "0.0.1",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.23.0",
    "axios": "^1.6.2"
  },
  "devDependencies": {
    "@types/react": "^18.2.14",
    "@types/react-dom": "^18.2.7",
    "@types/react-router-dom": "^5.3.3",
    "typescript": "^5.2.2",
    "vite": "^5.0.1",
    "@vitejs/plugin-react": "^4.0.3"
  }
}
''')

# tsconfig
files['frontend/tsconfig.json'] = textwrap.dedent('''
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

files['frontend/tsconfig.node.json'] = textwrap.dedent('''
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

# vite.config
files['frontend/vite.config.ts'] = textwrap.dedent('''
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
  },
});
''')

# main.tsx
files['frontend/src/main.tsx'] = textwrap.dedent('''
import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import { AuthProvider } from './context/AuthContext';
import './index.css';

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <App />
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>
);
''')

# index.css
files['frontend/src/index.css'] = textwrap.dedent('''
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: Arial, Helvetica, sans-serif; }
header, footer { background: #282c34; color: #fff; padding: 1rem; }
nav a { color: #61dafb; margin-right: 1rem; text-decoration: none; }
button { cursor: pointer; }
''')

# App.tsx
files['frontend/src/App.tsx'] = textwrap.dedent('''
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
''')

# Header component
files['frontend/src/components/Header.tsx'] = textwrap.dedent('''
import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Header: React.FC = () => {
  const { user, logout } = useAuth();

  return (
    <header>
      <nav>
        <Link to="/">Home</Link>
        {user ? (
          <>
            {user.role === 'student' && <Link to="/student">Dashboard</Link>}
            {user.role === 'teacher' && <Link to="/teacher">Dashboard</Link>}
            <button style={{ marginLeft: '1rem' }} onClick={logout}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </>
        )}
      </nav>
    </header>
  );
};

export default Header;
''')

# Footer
files['frontend/src/components/Footer.tsx'] = textwrap.dedent('''
import React from 'react';

const Footer: React.FC = () => {
  return (
    <footer>
      <p>© {new Date().getFullYear()} DuoQuanto. All rights reserved.</p>
    </footer>
  );
};

export default Footer;
''')

# PrivateRoute
files['frontend/src/components/PrivateRoute.tsx'] = textwrap.dedent('''
import React from 'react';
import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

interface PrivateRouteProps {
  allowedRoles: string[];
}

const PrivateRoute: React.FC<PrivateRouteProps> = ({ allowedRoles }) => {
  const { user, loading } = useAuth();
  const location = useLocation();

  if (loading) return <p>Loading...</p>;
  if (!user) return <Navigate to="/login" state={{ from: location }} replace />;
  if (!allowedRoles.includes(user.role)) return <Navigate to="/" replace />;

  return <Outlet />;
};

export default PrivateRoute;
''')

# Pages generic
pages = [
    'LandingPage',
    'LoginPage',
    'RegisterPage',
    'TeacherDashboard',
    'StudentDashboard',
    'AnalyzeProgress',
    'MyTopics',
    'QuizScreen',
    'MyProgress'
]

for page in pages:
    display = page.replace('Page', '').replace('Dashboard', ' Dashboard')
    code = (
        "import React from 'react';\n\n"
        f"const {page}: React.FC = () => {{\n"
        "  return (\n"
        "    <div>\n"
        f"      <h1>{display}</h1>\n"
        f"      {{/* TODO: Implement {page} */}}\n"
        "    </div>\n"
        "  );\n"
        "};\n\n"
        f"export default {page};\n"
    )
    files[f'frontend/src/pages/{page}.tsx'] = code

# CreateQuestions page
files['frontend/src/pages/CreateQuestions.tsx'] = textwrap.dedent('''
import React, { useState } from 'react';

const TABS = ['Multiple Choice', 'True/False', 'Fill in the Blank'];

const CreateQuestions: React.FC = () => {
  const [activeTab, setActiveTab] = useState<string>(TABS[0]);

  return (
    <div>
      <h1>Create Questions</h1>
      <div style={{ display: 'flex', gap: '1rem', marginBottom: '1rem' }}>
        {TABS.map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            style={{
              padding: '.5rem 1rem',
              background: activeTab === tab ? '#61dafb' : '#eee',
            }}
          >
            {tab}
          </button>
        ))}
      </div>
      <p>Selected Tab: {activeTab}</p>
      {/* TODO: Implement question forms for each tab */}
    </div>
  );
};

export default CreateQuestions;
''')

# AuthContext
files['frontend/src/context/AuthContext.tsx'] = textwrap.dedent('''
import React, { createContext, useContext, useEffect, useState } from 'react';
import api from '../utils/api';

interface User {
  id: string;
  email: string;
  role: 'student' | 'teacher';
}

interface AuthContextValue {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  register: (email: string, password: string, role: 'student' | 'teacher') => Promise<void>;
}

const AuthContext = createContext<AuthContextValue>({
  user: null,
  loading: true,
  login: async () => {},
  logout: async () => {},
  register: async () => {},
});

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    (async () => {
      try {
        const res = await api.get('/auth/session');
        setUser(res.user);
      } catch (_) {
        setUser(null);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const login = async (email: string, password: string) => {
    setLoading(true);
    const res = await api.post('/auth/login', { email, password });
    setUser(res.user);
    setLoading(false);
  };

  const logout = async () => {
    setLoading(true);
    await api.post('/auth/logout');
    setUser(null);
    setLoading(false);
  };

  const register = async (email: string, password: string, role: 'student' | 'teacher') => {
    setLoading(true);
    await api.post('/auth/register', { email, password, role });
    await login(email, password);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, register }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
''')

# utils api
files['frontend/src/utils/api.ts'] = textwrap.dedent('''
const API_BASE = import.meta.env.VITE_API_URL || '';

async function handleResponse(res: Response) {
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || 'API Error');
  }
  return res.json();
}

const api = {
  get: (path: string) => fetch(`${API_BASE}${path}`, { credentials: 'include' }).then(handleResponse),
  post: (path: string, body?: unknown) => fetch(`${API_BASE}${path}`, {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body ?? {}),
  }).then(handleResponse),
  put: (path: string, body?: unknown) => fetch(`${API_BASE}${path}`, {
    method: 'PUT',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body ?? {}),
  }).then(handleResponse),
  delete: (path: string) => fetch(`${API_BASE}${path}`, {
    method: 'DELETE',
    credentials: 'include',
  }).then(handleResponse),
};

export default api;
''')

# write files
for path, content in files.items():
    full = pathlib.Path(path)
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(content.strip() + '\n')

print('Created', len(files), 'frontend files.')