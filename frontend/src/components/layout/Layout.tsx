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
