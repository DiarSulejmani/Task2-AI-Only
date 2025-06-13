import client from './client';

export const login = async (email: string, password: string) => {
  const { data } = await client.post('/auth/login', { email, password });
  return data; // expecting user object
};

export const register = async (email: string, password: string, role: 'student' | 'teacher') => {
  const { data } = await client.post('/auth/register', { email, password, role });
  return data;
};
