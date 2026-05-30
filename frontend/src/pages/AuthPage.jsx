// src/pages/AuthPage.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './AuthStyle.css';
import { validatePassword, passwordsMatch, getMissingRequirements, passwordRequirements } from '../utils/passwordValidator';

const AuthPage = ({ initialMode, onClose }) => {
  const navigate = useNavigate(); 
  const [isLogin, setIsLogin] = useState(initialMode === 'login');
  
  // Form State
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [isAdminMode, setIsAdminMode] = useState(false);
  
  // UI State
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const [message, setMessage] = useState("");
  const [isSuccess, setIsSuccess] = useState(false);
  const [showRequirements, setShowRequirements] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [showSuccessPopup, setShowSuccessPopup] = useState(false);

  // --- Password Strength Calculator ---
  const passwordValidation = validatePassword(password);
  const missingRequirements = getMissingRequirements(passwordValidation);
  const passwordsMatching = passwordsMatch(password, confirmPassword);
  const canSubmit = !isLogin && passwordValidation.isValid && passwordsMatching;

  const handleAuth = async (e) => {
    e.preventDefault();
    setMessage(""); 
    setIsLoading(true);
    
    // Validate registration requirements
    if (!isLogin) {
      if (!passwordValidation.isValid) {
        setIsSuccess(false);
        setMessage("Password does not meet security requirements.");
        setIsLoading(false);
        return;
      }
      if (!passwordsMatching) {
        setIsSuccess(false);
        setMessage("Passwords do not match.");
        setIsLoading(false);
        return;
      }
    }

    const path = isLogin ? "login" : "register";
    const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';
    
    try {
      const response = await fetch(`${API_URL}/${path}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });
      
      const data = await response.json();
      
      if (response.ok) {
        setIsSuccess(true);
        
        if (isLogin) {
          // Show success popup instead of immediate redirect
          localStorage.setItem('username', data.user);
          setShowSuccessPopup(true);
          setUsername(""); 
          setPassword(""); 
          setConfirmPassword("");
        } else {
          setMessage("Account created successfully! You can now log in.");
          // Reset form after successful registration
          setTimeout(() => {
            setUsername("");
            setPassword("");
            setConfirmPassword("");
            setShowRequirements(false);
            setIsLogin(true);
            setMessage("");
          }, 2000);
        }
      } else {
        setIsSuccess(false);
        setMessage(data.detail || "Invalid Username or Password");
      }
    } catch (err) {
      setIsSuccess(false);
      setMessage("Connection to backend failed.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleTabSwitch = (toLogin) => {
    setIsLogin(toLogin);
    setMessage("");
    setPassword("");
    setConfirmPassword("");
  };

  const handleContinueClick = () => {
    setShowSuccessPopup(false);
    onClose(); // Close the auth modal first
    navigate('/'); // Navigate back to landing page
  };

  return (
    <div className="card auth-modal-card">
      <button className="exit-btn" onClick={onClose} aria-label="Close">&times;</button>

      <div className="tab-nav">
        <button className={`tab-btn ${isLogin ? 'active' : ''}`} onClick={() => handleTabSwitch(true)}>Login</button>
        <button className={`tab-btn ${!isLogin ? 'active' : ''}`} onClick={() => handleTabSwitch(false)}>Register</button>
      </div>

      <form onSubmit={handleAuth} className="screen active">
        
        {/* 🔥 WharfIntel Logo inserted specifically for Login */}
        {isLogin && (
          <div className="auth-brand-logo">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M10 4L10 13L3 13L10 4Z" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M13 6L13 13L19 13L13 6Z" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M2 15L22 15C22 15 19 18 12 18C5 18 2 15 2 15Z" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M2 21.5 Q 4.5 19.5 7 21.5 T 12 21.5 T 17 21.5 T 22 21.5" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            Wharf<span>Intel</span>
          </div>
        )}

        {/* --- DYNAMIC TITLE & SUBTITLE --- */}
        <div className="screen-title">
          {isAdminMode 
            ? "System Overwatch" 
            : (isLogin ? "Welcome back" : "Create account")}
        </div>
        
        <div className="screen-subtitle">
          {isAdminMode 
            ? "Provide clearance credentials for Admin access." 
            : (isLogin 
                ? "Secure access for WharfIntel Port Management." 
                : "Passwords are hashed with a unique salt & pepper.")}
        </div>

        <div className="form-group">
          <label>Username</label>
          <div className="input-wrap">
            <input 
              type="text" 
              placeholder={isLogin ? "your_username" : "choose_a_username"} 
              value={username} 
              onChange={(e) => setUsername(e.target.value)} 
              required 
            />
          </div>
        </div>

        <div className="form-group">
          <label>Password</label>
          <div className="input-wrap">
            <input 
              type={showPassword ? "text" : "password"} 
              placeholder={isLogin ? "••••••••" : "Min. 12 chars with uppercase, lowercase, digit & symbol"} 
              value={password} 
              onChange={(e) => setPassword(e.target.value)}
              required 
            />
            <button type="button" className="eye-btn" onClick={() => setShowPassword(!showPassword)}>
              {showPassword ? (
                <svg viewBox="0 0 24 24"><path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19m-6.72-1.07a3 3 0 11-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
              ) : (
                <svg viewBox="0 0 24 24"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
              )}
            </button>
          </div>
          
          {!isLogin && password && (
            <>
              {/* Password Strength Meter */}
              <div className="password-strength-container">
                <div className="strength-bar">
                  <div className={`strength-fill ${passwordValidation.strengthColor}`} style={{ width: `${passwordValidation.score}%` }}></div>
                </div>
                <div className={`strength-label ${passwordValidation.strengthColor}`}>
                  {passwordValidation.message}
                </div>
              </div>
            </>
          )}
        </div>

        {!isLogin && (
          <div className="form-group">
            <label className="con-firm">Confirm Password</label>
            <div className="input-wrap">
              <input 
                type={showConfirm ? "text" : "password"} 
                placeholder="Repeat your password" 
                value={confirmPassword} 
                onChange={(e) => setConfirmPassword(e.target.value)}
                required 
              />
              <button type="button" className="eye-btn" onClick={() => setShowConfirm(!showConfirm)}>
                {showConfirm ? (
                  <svg viewBox="0 0 24 24"><path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19m-6.72-1.07a3 3 0 11-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
                ) : (
                  <svg viewBox="0 0 24 24"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                )}
              </button>
            </div>
            {password && confirmPassword && !passwordsMatching && (
              <div className="password-mismatch-alert">
                ⚠ Passwords do not match
              </div>
            )}
          </div>
        )}

        {/* This wrapper forces the button to the bottom if the form is short */}
        <div className="form-footer" style={{ marginTop: 'auto' }}>
          <button 
            type="submit" 
            className="btn-primary"
            disabled={!isLogin && (!passwordValidation.isValid || !passwordsMatching || !username || isLoading)}
            style={{
              opacity: (!isLogin && (!passwordValidation.isValid || !passwordsMatching || !username)) ? 0.5 : 1,
              cursor: (!isLogin && (!passwordValidation.isValid || !passwordsMatching || !username)) ? 'not-allowed' : 'pointer'
            }}
          >
            {isLoading ? 'Processing...' : (isLogin ? "Sign In" : "Create Account")}
          </button>

          {/* --- NEW ADMIN LOGIN LINK --- */}
          {isLogin && (
            <div className="admin-toggle-wrap">
              <button 
                type="button" 
                className="admin-toggle-btn"
                onClick={() => setIsAdminMode(!isAdminMode)}
              >
                {isAdminMode ? "Return to Commander Login" : "Admin Login?"}
              </button>
            </div>
          )}
          
          {message && (
            <div className={`alert ${isSuccess ? 'alert-success show' : 'alert-error show'}`}>
              <span className="alert-icon">{isSuccess ? '✅' : '⚠️'}</span>
              <span>{message}</span>
            </div>
          )}
        </div>
      </form>

      {/* Success Popup Modal */}
      {showSuccessPopup && (
        <div className="success-popup-overlay">
          <div className="success-popup-card">
            <div className="popup-icon">✅</div>
            <h2>Login Successful</h2>
            <p>Welcome back!</p>
            <button className="popup-continue-btn" onClick={handleContinueClick}>
              Continue
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default AuthPage;