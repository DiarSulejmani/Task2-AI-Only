import os, json, textwrap, pathlib

project_files = {
    'frontend/package.json': textwrap.dedent('''
        {
          "name": "duoquanto-frontend",
          "version": "0.1.0",
          "private": true,
          "scripts": {
            "dev": "vite",
            "build": "vite build",
            "preview": "vite preview"
          },
          "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-router-dom": "^6.14.2",
            "styled-components": "^6.0.4"
          },
          "devDependencies": {
            "@types/react": "^18.2.6",
            "@types/react-dom": "^18.2.4",
            "@types/styled-components": "^5.1.26",
            "@vitejs/plugin-react": "^4.0.0",
            "typescript": "^5.2.2",
            "vite": "^4.4.9"
          }
        }
    '''),

    'frontend/tsconfig.json': textwrap.dedent('''
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
          "include": ["src"]
        }
    '''),

    'frontend/vite.config.ts': textwrap.dedent('''
        import { defineConfig } from 'vite';
        import react from '@vitejs/plugin-react';

        export default defineConfig({
          plugins: [react()],
          server: {
            port: 5173,
          },
        });
    '''),

    'frontend/README.md': textwrap.dedent('''
        # DuoQuanto Frontend

        This project was bootstrapped with [Vite](https://vitejs.dev/) and uses **React 18 + TypeScript**.

        ## Available Scripts

        Inside the `frontend/` folder you can run:

        ```bash
        npm install   # or yarn
        npm run dev   # Runs the app in the development mode.
        npm run build # Builds the app for production.
        npm run preview # Preview the production build.
        ```

        The app will be available at http://localhost:5173 by default.

        ## Project Structure

        - `src/contexts` – React Context providers (e.g. authentication)
        - `src/components` – Reusable UI components (Layout, ProtectedRoute, etc.)
        - `src/pages` – Page level components rendered by React Router
        - `src/styles` – Global & module CSS (you can switch to styled-components if you prefer)

        ## Authentication

        The `AuthContext` handles login, register and logout actions via
        backend endpoints:

        - `POST /auth/login`
        - `POST /auth/register`

        A successful response is expected to include `{ id, role, token }`.
        These details are persisted in `localStorage` to keep the user signed-in
        after a page refresh.
    '''),

    'frontend/src/main.tsx': textwrap.dedent('''
        import React from 'react';
        import ReactDOM from 'react-dom/client';
        import { BrowserRouter } from 'react-router-dom';
        import AppRouter from './AppRouter';
        import { AuthProvider } from './contexts/AuthContext';
        import './index.css';

        ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
          <React.StrictMode>
            <AuthProvider>
              <BrowserRouter>
                <AppRouter />
              </BrowserRouter>
            </AuthProvider>
          </React.StrictMode>
        );
    '''),

    'frontend/src/AppRouter.tsx': textwrap.dedent('''
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
    '''),

    'frontend/src/contexts/AuthContext.tsx': textwrap.dedent('''
        import React, { createContext, useContext, useEffect, useState } from 'react';

        type Role = 'teacher' | 'student';
        interface User {
          id: string;
          role: Role;
          token: string;
        }

        interface AuthContextProps {
          user: User | null;
          login: (email: string, password: string) => Promise<void>;
          register: (email: string, password: string, role: Role) => Promise<void>;
          logout: () => void;
        }

        const AuthContext = createContext<AuthContextProps | undefined>(undefined);

        export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
          const [user, setUser] = useState<User | null>(null);

          useEffect(() => {
            const stored = localStorage.getItem('auth');
            if (stored) {
              setUser(JSON.parse(stored));
            }
          }, []);

          const login = async (email: string, password: string) => {
            const res = await fetch('/auth/login', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ email, password }),
            });
            if (!res.ok) throw new Error('Login failed');
            const data = await res.json();
            const userObj = { id: data.id, role: data.role as Role, token: data.token } as User;
            localStorage.setItem('auth', JSON.stringify(userObj));
            setUser(userObj);
          };

          const register = async (email: string, password: string, role: Role) => {
            const res = await fetch('/auth/register', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ email, password, role }),
            });
            if (!res.ok) throw new Error('Register failed');
            const data = await res.json();
            const userObj = { id: data.id, role: data.role as Role, token: data.token } as User;
            localStorage.setItem('auth', JSON.stringify(userObj));
            setUser(userObj);
          };

          const logout = () => {
            localStorage.removeItem('auth');
            setUser(null);
          };

          const value: AuthContextProps = { user, login, register, logout };
          return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
        };

        export const useAuth = () => {
          const ctx = useContext(AuthContext);
          if (!ctx) throw new Error('useAuth must be used within AuthProvider');
          return ctx;
        };
    '''),

    'frontend/src/components/ProtectedRoute.tsx': textwrap.dedent('''
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
    '''),

    'frontend/src/components/Layout/Header.tsx': textwrap.dedent('''
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
    '''),

    'frontend/src/components/Layout/Footer.tsx': textwrap.dedent('''
        import React from 'react';
        import styles from '../../styles/layout.module.css';

        const Footer: React.FC = () => (
          <footer className={styles.footer}>
            © {new Date().getFullYear()} DuoQuanto
          </footer>
        );

        export default Footer;
    '''),

    'frontend/src/components/Layout/Layout.tsx': textwrap.dedent('''
        import React from 'react';
        import { Outlet } from 'react-router-dom';
        import Header from './Header';
        import Footer from './Footer';

        const Layout: React.FC = () => (
          <>
            <Header />
            <main style={{ padding: '1rem', minHeight: '80vh' }}>
              <Outlet />
            </main>
            <Footer />
          </>
        );

        export default Layout;
    '''),

    'frontend/src/styles/layout.module.css': textwrap.dedent('''
        .header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 1rem;
          background: #282c34;
          color: #fff;
        }
        .header ul {
          display: flex;
          gap: 1rem;
          list-style: none;
          margin: 0;
          padding: 0;
        }
        .footer {
          text-align: center;
          padding: 1rem;
          background: #f0f0f0;
        }
    '''),

    'frontend/src/index.css': textwrap.dedent('''
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: sans-serif; }
        a { color: inherit; text-decoration: none; }
        ul { list-style: none; }
    '''),
}

# Add page stubs
auth_pages = {
    'LandingPage': 'Landing Page',
    'LoginPage': 'Login Page',
    'RegisterPage': 'Register Page',
}

dashboard_pages = {
    'dashboards/TeacherDashboard': 'Teacher Dashboard',
    'dashboards/StudentDashboard': 'Student Dashboard',
}

teacher_pages = {
    'teacher/CreateQuestions': 'Create Questions',
    'teacher/AnalyzeProgress': 'Analyze Progress',
    'teacher/MyTopics': 'My Topics',
}

student_pages = {
    'student/Quiz': 'Quiz',
    'student/MyProgress': 'My Progress',
}

# helper to build page content
page_template = lambda title: textwrap.dedent(f'''
    import React from 'react';
    const Component: React.FC = () => <div>{title}</div>;
    export default Component;
''')

for rel, title in auth_pages.items():
    project_files[f'frontend/src/pages/{rel}.tsx'] = page_template(title)

for rel, title in dashboard_pages.items():
    project_files[f'frontend/src/pages/{rel}.tsx'] = page_template(title)

for rel, title in teacher_pages.items():
    project_files[f'frontend/src/pages/{rel}.tsx'] = page_template(title)

for rel, title in student_pages.items():
    project_files[f'frontend/src/pages/{rel}.tsx'] = page_template(title)

# Create directories and files
created_files = []
for path, content in project_files.items():
    full_path = pathlib.Path(path)
    full_path.parent.mkdir(parents=True, exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
    created_files.append(str(full_path))

print(json.dumps({'created': created_files}, indent=2))