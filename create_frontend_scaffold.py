import os, json, textwrap, pathlib, sys

# Root directory
root = pathlib.Path('frontend')

files = {
    # index.html default
    root / 'index.html': textwrap.dedent('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8" />
          <meta name="viewport" content="width=device-width, initial-scale=1.0" />
          <title>DuoQuanto</title>
          <link rel="icon" type="image/svg+xml" href="/vite.svg" />
        </head>
        <body>
          <div id="root"></div>
          <script type="module" src="/src/main.tsx"></script>
        </body>
        </html>
    '''),

    # package.json minimal
    root / 'package.json': textwrap.dedent('''
        {
          "name": "duoquanto-frontend",
          "version": "0.0.1",
          "private": true,
          "type": "module",
          "scripts": {
            "dev": "vite",
            "build": "vite build",
            "preview": "vite preview"
          },
          "dependencies": {
            "@hookform/resolvers": "^3.0.0",
            "axios": "^1.6.0",
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-router-dom": "^6.17.0"
          },
          "devDependencies": {
            "@types/react": "^18.2.0",
            "@types/react-dom": "^18.2.0",
            "@vitejs/plugin-react": "^4.0.0",
            "autoprefixer": "^10.4.14",
            "postcss": "^8.4.27",
            "tailwindcss": "^3.3.5",
            "typescript": "^5.2.2",
            "vite": "^5.0.0"
          }
        }
    '''),

    # tsconfig
    root / 'tsconfig.json': textwrap.dedent('''
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
          "references": [{"path": "./tsconfig.node.json"}]
        }
    '''),

    # tsconfig.node.json
    root / 'tsconfig.node.json': textwrap.dedent('''
        {
          "compilerOptions": {
            "composite": true,
            "module": "ESNext",
            "moduleResolution": "Node",
            "allowSyntheticDefaultImports": true
          },
          "include": ["vite.config.ts"]
        }
    '''),

    # vite config
    root / 'vite.config.ts': textwrap.dedent('''
        import { defineConfig } from 'vite';
        import react from '@vitejs/plugin-react';

        export default defineConfig({
          plugins: [react()],
          server: {
            port: 5173,
            open: true,
          },
        });
    '''),

    # tailwind config
    root / 'tailwind.config.cjs': textwrap.dedent('''
        /** @type {import('tailwindcss').Config} */
        module.exports = {
          content: [
            './index.html',
            './src/**/*.{js,ts,jsx,tsx}',
          ],
          theme: {
            extend: {},
          },
          plugins: [],
        };
    '''),

    # postcss config
    root / 'postcss.config.cjs': textwrap.dedent('''
        module.exports = {
          plugins: {
            tailwindcss: {},
            autoprefixer: {},
          },
        };
    '''),

    # src/main.tsx
    root / 'src' / 'main.tsx': textwrap.dedent('''
        import React from 'react';
        import ReactDOM from 'react-dom/client';
        import { BrowserRouter } from 'react-router-dom';
        import App from './App';
        import './index.css';

        ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
          <React.StrictMode>
            <BrowserRouter>
              <App />
            </BrowserRouter>
          </React.StrictMode>
        );
    '''),

    # src/index.css (Tailwind imports)
    root / 'src' / 'index.css': textwrap.dedent('''
        @tailwind base;
        @tailwind components;
        @tailwind utilities;
    '''),

    # src/App.tsx
    root / 'src' / 'App.tsx': textwrap.dedent('''
        import React from 'react';
        import { Routes, Route, Navigate } from 'react-router-dom';
        import Header from './components/Header';
        import Footer from './components/Footer';
        import LandingPage from './pages/LandingPage';
        import LoginPage from './pages/LoginPage';
        import RegisterPage from './pages/RegisterPage';
        import TeacherDashboard from './pages/teacher/Dashboard';
        import CreateQuestions from './pages/teacher/CreateQuestions';
        import StudentDashboard from './pages/student/Dashboard';
        import TopicsPage from './pages/student/TopicsPage';
        import ProgressPage from './pages/student/ProgressPage';
        import ProtectedRoute from './components/ProtectedRoute';
        import { AuthProvider } from './contexts/AuthContext';

        const App: React.FC = () => {
          return (
            <AuthProvider>
              <div className="flex flex-col min-h-screen">
                <Header />
                <main className="flex-1 container mx-auto p-4">
                  <Routes>
                    <Route path="/" element={<LandingPage />} />
                    <Route path="/login" element={<LoginPage />} />
                    <Route path="/register" element={<RegisterPage />} />

                    {/* Teacher routes */}
                    <Route
                      path="/teacher/dashboard"
                      element={
                        <ProtectedRoute role="teacher">
                          <TeacherDashboard />
                        </ProtectedRoute>
                      }
                    />
                    <Route
                      path="/teacher/create-questions"
                      element={
                        <ProtectedRoute role="teacher">
                          <CreateQuestions />
                        </ProtectedRoute>
                      }
                    />

                    {/* Student routes */}
                    <Route
                      path="/student/dashboard"
                      element={
                        <ProtectedRoute role="student">
                          <StudentDashboard />
                        </ProtectedRoute>
                      }
                    />
                    <Route
                      path="/student/topics"
                      element={
                        <ProtectedRoute role="student">
                          <TopicsPage />
                        </ProtectedRoute>
                      }
                    />
                    <Route
                      path="/student/progress"
                      element={
                        <ProtectedRoute role="student">
                          <ProgressPage />
                        </ProtectedRoute>
                      }
                    />

                    {/* Catch-all */}
                    <Route path="*" element={<Navigate to="/" replace />} />
                  </Routes>
                </main>
                <Footer />
              </div>
            </AuthProvider>
          );
        };

        export default App;
    '''),

    # components/Header.tsx
    root / 'src' / 'components' / 'Header.tsx': textwrap.dedent('''
        import React from 'react';
        import { Link, useNavigate } from 'react-router-dom';
        import { useAuth } from '../hooks/useAuth';

        const Header: React.FC = () => {
          const { user, logout } = useAuth();
          const navigate = useNavigate();

          const handleLogout = () => {
            logout();
            navigate('/');
          };

          return (
            <header className="bg-blue-600 text-white p-4">
              <nav className="container mx-auto flex justify-between items-center">
                <Link to="/" className="font-bold text-lg">DuoQuanto</Link>
                <div className="space-x-4">
                  {!user && (
                    <>
                      <Link to="/login" className="hover:underline">Login</Link>
                      <Link to="/register" className="hover:underline">Register</Link>
                    </>
                  )}
                  {user?.role === 'teacher' && (
                    <>
                      <Link to="/teacher/dashboard" className="hover:underline">Dashboard</Link>
                      <Link to="/teacher/create-questions" className="hover:underline">Create Questions</Link>
                    </>
                  )}
                  {user?.role === 'student' && (
                    <>
                      <Link to="/student/dashboard" className="hover:underline">Dashboard</Link>
                      <Link to="/student/topics" className="hover:underline">Topics</Link>
                      <Link to="/student/progress" className="hover:underline">Progress</Link>
                    </>
                  )}
                  {user && (
                    <button onClick={handleLogout} className="ml-2 bg-red-500 px-3 py-1 rounded">Logout</button>
                  )}
                </div>
              </nav>
            </header>
          );
        };

        export default Header;
    '''),

    # components/Footer.tsx
    root / 'src' / 'components' / 'Footer.tsx': textwrap.dedent('''
        import React from 'react';

        const Footer: React.FC = () => (
          <footer className="bg-gray-100 text-center p-4 text-sm text-gray-600">
            © {new Date().getFullYear()} DuoQuanto. All rights reserved.
          </footer>
        );

        export default Footer;
    '''),

    # components/ProtectedRoute.tsx
    root / 'src' / 'components' / 'ProtectedRoute.tsx': textwrap.dedent('''
        import React from 'react';
        import { Navigate } from 'react-router-dom';
        import { useAuth } from '../hooks/useAuth';

        interface Props {
          role?: 'student' | 'teacher';
          children: JSX.Element;
        }

        const ProtectedRoute: React.FC<Props> = ({ children, role }) => {
          const { user } = useAuth();

          if (!user) return <Navigate to="/login" replace />;
          if (role && user.role !== role) return <Navigate to="/" replace />;
          return children;
        };

        export default ProtectedRoute;
    '''),

    # pages/LandingPage.tsx
    root / 'src' / 'pages' / 'LandingPage.tsx': textwrap.dedent('''
        import React from 'react';
        import { Link } from 'react-router-dom';
        import { useAuth } from '../hooks/useAuth';

        const LandingPage: React.FC = () => {
          const { user } = useAuth();
          return (
            <div className="text-center mt-10">
              <h1 className="text-4xl font-bold mb-4">Welcome to DuoQuanto!</h1>
              {!user && (
                <p>
                  <Link to="/login" className="text-blue-600 underline mr-2">Login</Link>
                  or
                  <Link to="/register" className="text-blue-600 underline ml-2">Register</Link>
                </p>
              )}
            </div>
          );
        };
        export default LandingPage;
    '''),

    # pages/LoginPage.tsx
    root / 'src' / 'pages' / 'LoginPage.tsx': textwrap.dedent('''
        import React from 'react';
        import { useForm } from 'react-hook-form';
        import { zodResolver } from '@hookform/resolvers/zod';
        import * as z from 'zod';
        import { useNavigate } from 'react-router-dom';
        import { useAuth } from '../hooks/useAuth';

        const schema = z.object({
          email: z.string().email(),
          password: z.string().min(6),
        });
        type FormData = z.infer<typeof schema>;

        const LoginPage: React.FC = () => {
          const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
            resolver: zodResolver(schema),
          });
          const { login } = useAuth();
          const navigate = useNavigate();

          const onSubmit = async (data: FormData) => {
            const success = await login(data.email, data.password);
            if (success) navigate('/');
          };

          return (
            <div className="max-w-md mx-auto mt-10">
              <h2 className="text-2xl mb-4 text-center">Login</h2>
              <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                <div>
                  <label className="block mb-1">Email</label>
                  <input {...register('email')} className="w-full border p-2" />
                  {errors.email && <p className="text-red-500 text-sm">{errors.email.message}</p>}
                </div>
                <div>
                  <label className="block mb-1">Password</label>
                  <input type="password" {...register('password')} className="w-full border p-2" />
                  {errors.password && <p className="text-red-500 text-sm">{errors.password.message}</p>}
                </div>
                <button type="submit" className="w-full bg-blue-600 text-white py-2">Login</button>
              </form>
            </div>
          );
        };
        export default LoginPage;
    '''),

    # pages/RegisterPage.tsx
    root / 'src' / 'pages' / 'RegisterPage.tsx': textwrap.dedent('''
        import React from 'react';
        import { useForm } from 'react-hook-form';
        import { zodResolver } from '@hookform/resolvers/zod';
        import * as z from 'zod';
        import { useNavigate } from 'react-router-dom';
        import { useAuth } from '../hooks/useAuth';

        const schema = z
          .object({
            email: z.string().email(),
            password: z.string().min(6),
            confirmPassword: z.string().min(6),
            role: z.enum(['student', 'teacher']),
          })
          .refine((data) => data.password === data.confirmPassword, {
            message: "Passwords don't match",
            path: ['confirmPassword'],
          });
        type FormData = z.infer<typeof schema>;

        const RegisterPage: React.FC = () => {
          const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
            resolver: zodResolver(schema),
          });
          const { register: registerUser } = useAuth();
          const navigate = useNavigate();

          const onSubmit = async (data: FormData) => {
            const success = await registerUser(data.email, data.password, data.role);
            if (success) navigate('/');
          };

          return (
            <div className="max-w-md mx-auto mt-10">
              <h2 className="text-2xl mb-4 text-center">Register</h2>
              <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                <div>
                  <label className="block mb-1">Email</label>
                  <input {...register('email')} className="w-full border p-2" />
                  {errors.email && <p className="text-red-500 text-sm">{errors.email.message}</p>}
                </div>
                <div>
                  <label className="block mb-1">Password</label>
                  <input type="password" {...register('password')} className="w-full border p-2" />
                  {errors.password && <p className="text-red-500 text-sm">{errors.password.message}</p>}
                </div>
                <div>
                  <label className="block mb-1">Confirm Password</label>
                  <input type="password" {...register('confirmPassword')} className="w-full border p-2" />
                  {errors.confirmPassword && <p className="text-red-500 text-sm">{errors.confirmPassword.message}</p>}
                </div>
                <div>
                  <label className="block mb-1">Role</label>
                  <select {...register('role')} className="w-full border p-2">
                    <option value="student">Student</option>
                    <option value="teacher">Teacher</option>
                  </select>
                  {errors.role && <p className="text-red-500 text-sm">{errors.role.message}</p>}
                </div>
                <button type="submit" className="w-full bg-blue-600 text-white py-2">Register</button>
              </form>
            </div>
          );
        };
        export default RegisterPage;
    '''),

    # Teacher Dashboard
    root / 'src' / 'pages' / 'teacher' / 'Dashboard.tsx': textwrap.dedent('''
        import React from 'react';

        const TeacherDashboard: React.FC = () => (
          <div>
            <h2 className="text-2xl font-bold mb-4">Teacher Dashboard</h2>
            <p>Welcome, teacher! This is your dashboard.</p>
          </div>
        );

        export default TeacherDashboard;
    '''),

    # CreateQuestions
    root / 'src' / 'pages' / 'teacher' / 'CreateQuestions.tsx': textwrap.dedent('''
        import React from 'react';

        const CreateQuestions: React.FC = () => (
          <div>
            <h2 className="text-2xl font-bold mb-4">Create Questions</h2>
            <p>Tab interface placeholder for creating questions.</p>
          </div>
        );

        export default CreateQuestions;
    '''),

    # Student Dashboard
    root / 'src' / 'pages' / 'student' / 'Dashboard.tsx': textwrap.dedent('''
        import React from 'react';

        const StudentDashboard: React.FC = () => (
          <div>
            <h2 className="text-2xl font-bold mb-4">Student Dashboard</h2>
            <p>Welcome, student! This is your dashboard.</p>
          </div>
        );

        export default StudentDashboard;
    '''),

    # TopicsPage
    root / 'src' / 'pages' / 'student' / 'TopicsPage.tsx': textwrap.dedent('''
        import React from 'react';

        const TopicsPage: React.FC = () => (
          <div>
            <h2 className="text-2xl font-bold mb-4">Topics</h2>
            <p>List of topics will go here.</p>
          </div>
        );

        export default TopicsPage;
    '''),

    # ProgressPage
    root / 'src' / 'pages' / 'student' / 'ProgressPage.tsx': textwrap.dedent('''
        import React from 'react';

        const ProgressPage: React.FC = () => (
          <div>
            <h2 className="text-2xl font-bold mb-4">Progress</h2>
            <p>Your progress will be displayed here.</p>
          </div>
        );

        export default ProgressPage;
    '''),

    # AuthContext
    root / 'src' / 'contexts' / 'AuthContext.tsx': textwrap.dedent('''
        import React, { createContext, useState, useEffect } from 'react';
        import { login as loginApi, register as registerApi } from '../api/auth';

        interface User {
          id: string;
          role: 'student' | 'teacher';
          email: string;
        }

        interface AuthContextProps {
          user: User | null;
          login: (email: string, password: string) => Promise<boolean>;
          register: (email: string, password: string, role: 'student' | 'teacher') => Promise<boolean>;
          logout: () => void;
        }

        export const AuthContext = createContext<AuthContextProps>({
          user: null,
          login: async () => false,
          register: async () => false,
          logout: () => {},
        });

        export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
          const [user, setUser] = useState<User | null>(null);

          useEffect(() => {
            // TODO: fetch session from backend cookie if exists
          }, []);

          const login = async (email: string, password: string) => {
            try {
              const res = await loginApi(email, password);
              setUser(res);
              return true;
            } catch (err) {
              console.error(err);
              return false;
            }
          };

          const register = async (email: string, password: string, role: 'student' | 'teacher') => {
            try {
              const res = await registerApi(email, password, role);
              setUser(res);
              return true;
            } catch (err) {
              console.error(err);
              return false;
            }
          };

          const logout = () => {
            setUser(null);
            // TODO: call backend logout
          };

          return (
            <AuthContext.Provider value={{ user, login, register, logout }}>
              {children}
            </AuthContext.Provider>
          );
        };
    '''),

    # hooks/useAuth.ts
    root / 'src' / 'hooks' / 'useAuth.ts': textwrap.dedent('''
        import { useContext } from 'react';
        import { AuthContext } from '../contexts/AuthContext';

        export const useAuth = () => useContext(AuthContext);
    '''),

    # api/client.ts
    root / 'src' / 'api' / 'client.ts': textwrap.dedent('''
        import axios from 'axios';

        const client = axios.create({
          baseURL: 'http://localhost:8000',
          withCredentials: true,
        });

        export default client;
    '''),

    # api/auth.ts
    root / 'src' / 'api' / 'auth.ts': textwrap.dedent('''
        import client from './client';

        export const login = async (email: string, password: string) => {
          const { data } = await client.post('/auth/login', { email, password });
          return data; // expecting user object
        };

        export const register = async (email: string, password: string, role: 'student' | 'teacher') => {
          const { data } = await client.post('/auth/register', { email, password, role });
          return data;
        };
    '''),
}

# Create directories and write files
for path, content in files.items():
    os.makedirs(path.parent, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.lstrip('\n'))

print('Frontend scaffold generated successfully.')