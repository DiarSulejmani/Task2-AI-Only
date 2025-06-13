import React from 'react';
import { Container, Typography } from '@mui/material';

const Landing = () => (
  <Container sx={{ py: 8 }}>
    <Typography variant="h3" gutterBottom>Welcome to DuoQuanto</Typography>
    <Typography>Interactive language learning platform.</Typography>
  </Container>
);

export default Landing;
