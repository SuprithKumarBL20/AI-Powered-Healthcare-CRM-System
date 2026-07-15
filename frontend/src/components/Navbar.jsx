import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { openConfirm } from '../store/slices.js';
import { Activity, ShieldCheck, Database, RefreshCw } from 'lucide-react';

export default function Navbar() {
  const dispatch = useDispatch();
  const seeding = useSelector((state) => state.ui.seeding);

  const handleResetDb = () => {
    dispatch(openConfirm({
      title: 'Reset & Seed Database',
      message: 'Are you sure you want to reset and re-seed the database? This will clear all current logged interactions and restore default records.',
      onConfirmType: 'reset_db'
    }));
  };

  return (
    <header className="navbar">
      <div className="navbar-logo">
        <Activity className="logo-icon animate-pulse" />
        <span className="logo-text">AIVOA <span className="logo-highlight">CRM</span></span>
        <span className="logo-badge">HCP Portal v1.0</span>
      </div>

      <nav className="navbar-actions">
        <div className="status-indicator">
          <ShieldCheck className="status-icon" />
          <span>PhRMA Compliance Engine Active</span>
        </div>
        
        <button 
          className={`btn btn-secondary reset-btn ${seeding ? 'loading' : ''}`} 
          onClick={handleResetDb}
          disabled={seeding}
        >
          {seeding ? (
            <RefreshCw className="btn-icon spin" />
          ) : (
            <Database className="btn-icon" />
          )}
          Reset & Seed DB
        </button>
      </nav>
    </header>
  );
}
