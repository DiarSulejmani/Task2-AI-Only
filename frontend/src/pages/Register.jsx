import React, { useState } from 'react';
import { Container, TextField, Button, Box, Typography, MenuItem } from '@mui/material';
import { useAuth } from '../context/AuthContext';

const Register = () => {
  const { register } = useAuth();
  const [form, setForm] = useState({ name: '', email: '', password: '', role: 'student' });

  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value });
  const handleSubmit = async e => {
    e.preventDefault();
    await register(form);
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 8 }}>
      <Typography variant="h4" gutterBottom>Register</Typography>
      <Box component="form" onSubmit={handleSubmit}>
        <TextField label="Name" name="name" fullWidth margin="normal" value={form.name} onChange={handleChange} />
        <TextField label="Email" name="email" fullWidth margin="normal" value={form.email} onChange={handleChange} />
        <TextField label="Password" type="password" name="password" fullWidth margin="normal" value={form.password} onChange={handleChange} />
        <TextField label="Role" name="role" select fullWidth margin="normal" value={form.role} onChange={handleChange}>
          <MenuItem value="student">Student</MenuItem>
          <MenuItem value="teacher">Teacher</MenuItem>
        </TextField>
        <Button variant="contained" type="submit" fullWidth sx={{ mt: 2 }}>Register</Button>
      </Box>
    </Container>
  );
};

export default Register;
