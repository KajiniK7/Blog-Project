import React, { useState } from 'react';
import { loginUser, registerUser } from '../api/client';

/**
 * Authentication Modal: Login & Registration
 */
export default function AuthModal({ isOpen, onClose, onAuthSuccess, initialMode = 'login' }) {
  if (!isOpen) return null;

  const [mode, setMode] = useState(initialMode); // 'login' or 'register'
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMsg, setErrorMsg] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');

    const cleanUsername = username.trim();
    if (!cleanUsername) {
      setErrorMsg('Please enter your username.');
      return;
    }
    if (password.length < 4) {
      setErrorMsg('Password must be at least 4 characters long.');
      return;
    }

    setIsSubmitting(true);
    try {
      if (mode === 'register') {
        const user = await registerUser({ username: cleanUsername, password });
        onAuthSuccess(user);
        onClose();
      } else {
        const user = await loginUser({ username: cleanUsername, password });
        onAuthSuccess(user);
        onClose();
      }
    } catch (err) {
      const detail = err?.response?.data?.detail || err?.message || 'Authentication failed.';
      setErrorMsg(detail);
    } finally {
      setIsSubmitting(false);
    }
  };

  const switchMode = (newMode) => {
    setMode(newMode);
    setErrorMsg('');
  };

  return (
    <div className="auth-modal-backdrop" onClick={onClose} role="dialog" aria-modal="true">
      <div className="auth-modal-container" onClick={(e) => e.stopPropagation()}>
        <div className="auth-modal-header">
          <div className="auth-header-brand">
            {/* <span className="auth-brand-symbol">M</span> */}
            <span className="auth-brand-title">Blog Hub</span>
          </div>
          <button type="button" className="auth-close-btn" onClick={onClose} aria-label="Close modal">
            ✕
          </button>
        </div>

        <div className="auth-modal-body">
          <h2 className="auth-modal-title">
            {mode === 'login' ? 'Welcome back.' : 'Join the platform.'}
          </h2>
          <p className="auth-modal-subtitle">
            {mode === 'login'
              ? 'Sign in to create, draft, and publish your stories.'
              : 'Create an account to write and manage your articles.'}
          </p>

          {errorMsg && (
            <div className="auth-alert-error" role="alert">
              <span>⚠️</span> {errorMsg}
            </div>
          )}

          <form onSubmit={handleSubmit} className="auth-form">
            <div className="auth-field">
              <label htmlFor="auth-username">Username</label>
              <input
                id="auth-username"
                type="text"
                placeholder="Enter your username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                autoFocus
                required
                disabled={isSubmitting}
              />
            </div>

            <div className="auth-field">
              <label htmlFor="auth-password">Password</label>
              <input
                id="auth-password"
                type="password"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                disabled={isSubmitting}
              />
            </div>

            <button type="submit" className="auth-submit-btn" disabled={isSubmitting}>
              {isSubmitting
                ? 'Processing...'
                : mode === 'login'
                ? 'Sign In'
                : 'Create Account'}
            </button>
          </form>

          <div className="auth-switch-prompt">
            {mode === 'login' ? (
              <p>
                No account?{' '}
                <button type="button" onClick={() => switchMode('register')}>
                  Create one
                </button>
              </p>
            ) : (
              <p>
                Already have an account?{' '}
                <button type="button" onClick={() => switchMode('login')}>
                  Sign in
                </button>
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
