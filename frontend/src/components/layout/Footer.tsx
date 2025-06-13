import React from 'react';
import styles from '../../styles/layout.module.css';

const Footer: React.FC = () => (
  <footer className={styles.footer}>
    © {new Date().getFullYear()} DuoQuanto
  </footer>
);

export default Footer;
