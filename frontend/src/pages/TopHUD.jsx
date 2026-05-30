/**
 * 📊 TOP HUD COMPONENT - DEMO/PLACEHOLDER
 * 
 * ⚠️  IMPORTANT: This is a placeholder/demo component.
 * Only the Authentication (Login/Register) system is fully implemented with security.
 * This HUD component does not have backend integration or production-level security.
 */

// TopHUD.jsx
import React from 'react';
import './Simulation.css'; 

const TopHUD = ({ resources }) => {
  return (
    <div className="stats-hud">
      <div className="stat-item">
        <span className="label">CREDITS:</span>
        <span className="value money">${resources.money.toLocaleString()}</span>
      </div>
      <div className="stat-item">
        <span className="label">PORT REP:</span>
        <div className="rep-bar-container">
          <div 
            className="rep-bar-fill" 
            style={{ width: `${resources.reputation}%`, background: 'linear-gradient(90deg, #f59e0b, #2ecc71)' }}>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TopHUD;