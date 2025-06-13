import React from 'react';
import { Link } from 'react-router-dom';

function LandingPage() {
  return (
    <div className="text-center">
      <h1 className="display-4 mb-4">Welcome to DuoQuanto</h1>
      <p className="lead mb-4">Your platform for interactive learning and teaching.</p>
      <Link to="/register" className="btn btn-primary btn-lg me-2">Get Started</Link>
      <Link to="/login" className="btn btn-outline-secondary btn-lg">Login</Link>
    </div>
  );
}

export default LandingPage;
