import React from 'react';
import { Box, Typography } from '@mui/material';

const Footer = () => (
  <Box sx={{ mt: 8, py: 4, textAlign: 'center', bgcolor: 'grey.100' }}>
    <Typography variant="body2" color="text.secondary">© {new Date().getFullYear()} DuoQuanto</Typography>
  </Box>
);

export default Footer;
