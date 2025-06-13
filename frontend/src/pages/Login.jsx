import React, { useState } from 'react';
import { Container, TextField, Button, Box, Typography } from '@mui/material';
import { useAuth } from '../context/AuthContext';

const Login = () => {
  const { login } = useAuth();
  const [form, setForm] = useState({ email: '', password: '' });

  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value });
  const handleSubmit = async e => {
    e.preventDefault();
    await login(form.email, form.password);
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 8 }}>
      <Typography variant="h4" gutterBottom>Login</Typography>
      <Box component="form" onSubmit={handleSubmit}>
        <TextField label="Email" name="email" fullWidth margin="normal" value={form.email} onChange={handleChange} />
        <TextField label="Password" type="password" name="password" fullWidth margin="normal" value={form.password} onChange={handleChange} />
        <Button variant="contained" type="submit" fullWidth sx={{ mt: 2 }}>Login</Button>
      </Box>
    </Container>
  );
};

export default Login;
