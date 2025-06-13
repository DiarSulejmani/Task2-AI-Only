import React from 'react';
import { Container, Typography } from '@mui/material';

const StudentDashboard = () => (
  <Container sx={{ py: 8 }}>
    <Typography variant="h4">Student Dashboard</Typography>
    <Typography>Protected area for students.</Typography>
  </Container>
);

export default StudentDashboard;
