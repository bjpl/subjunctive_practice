import React from 'react';
import './AuthLayout.css';

interface AuthLayoutProps {
  children: React.ReactNode;
}

export const AuthLayout: React.FC<AuthLayoutProps> = ({ children }) => {
  return (
    <div className="auth-layout">
      <div className="auth-layout-background">
        <div className="auth-layout-pattern"></div>
      </div>

      <div className="auth-layout-content">
        <div className="auth-layout-card">
          <div className="auth-layout-logo">
            <svg
              width="48"
              height="48"
              viewBox="0 0 48 48"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <rect width="48" height="48" rx="8" fill="#6572f3" />
              <path
                d="M24 12C17.373 12 12 17.373 12 24C12 30.627 17.373 36 24 36C30.627 36 36 30.627 36 24C36 17.373 30.627 12 24 12ZM24 14C29.523 14 34 18.477 34 24C34 29.523 29.523 34 24 34C18.477 34 14 29.523 14 24C14 18.477 18.477 14 24 14Z"
                fill="white"
              />
              <path
                d="M24 18C20.686 18 18 20.686 18 24C18 27.314 20.686 30 24 30C27.314 30 30 27.314 30 24C30 20.686 27.314 18 24 18Z"
                fill="white"
              />
            </svg>
            <span className="auth-layout-logo-text">Subjunctive Practice</span>
          </div>

          {children}
        </div>

        <footer className="auth-layout-footer">
          <p>
            &copy; {new Date().getFullYear()} Spanish Subjunctive Practice. All rights
            reserved.
          </p>
        </footer>
      </div>
    </div>
  );
};
