import React from 'react';
import { AppBar, Toolbar, Typography, Button } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Header = () => {
  const { user, role, logout } = useAuth();
  return (
    <AppBar position="static">
      <Toolbar sx={{ display: 'flex', justifyContent: 'space-between' }}>
        <Typography variant="h6" component={RouterLink} to="/" color="inherit" sx={{ textDecoration: 'none' }}>
          DuoQuanto
        </Typography>
        <div>
          {!user && (
            <>
              <Button color="inherit" component={RouterLink} to="/login">Login</Button>
              <Button color="inherit" component={RouterLink} to="/register">Register</Button>
            </>
          )}
          {user && (
            <>
              {role === 'teacher' && <Button color="inherit" component={RouterLink} to="/teacher">Dashboard</Button>}
              {role === 'student' && <Button color="inherit" component={RouterLink} to="/student">Dashboard</Button>}
              <Button color="inherit" onClick={logout}>Logout</Button>
            </>
          )}
        </div>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
