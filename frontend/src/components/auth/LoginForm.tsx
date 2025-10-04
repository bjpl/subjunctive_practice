import React, { useState } from 'react';
import { Input } from '../ui/Input';
import { Button } from '../ui/Button';
import './AuthForms.css';

interface LoginFormProps {
  onSubmit: (email: string, password: string) => Promise<void>;
  onForgotPassword?: () => void;
  onSignUp?: () => void;
}

export const LoginForm: React.FC<LoginFormProps> = ({
  onSubmit,
  onForgotPassword,
  onSignUp,
}) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState<{ email?: string; password?: string }>({});
  const [isLoading, setIsLoading] = useState(false);

  const validate = (): boolean => {
    const newErrors: { email?: string; password?: string } = {};

    if (!email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      newErrors.email = 'Please enter a valid email address';
    }

    if (!password) {
      newErrors.password = 'Password is required';
    } else if (password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validate()) return;

    setIsLoading(true);
    try {
      await onSubmit(email, password);
    } catch (error) {
      setErrors({
        email: 'Invalid email or password',
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form className="auth-form" onSubmit={handleSubmit} noValidate>
      <div className="auth-form-header">
        <h1>Welcome Back</h1>
        <p>Sign in to continue your Spanish learning journey</p>
      </div>

      <div className="auth-form-content">
        <Input
          id="email"
          name="email"
          label="Email Address"
          type="email"
          value={email}
          onChange={setEmail}
          error={errors.email}
          placeholder="you@example.com"
          autoComplete="email"
          required
        />

        <Input
          id="password"
          name="password"
          label="Password"
          type="password"
          value={password}
          onChange={setPassword}
          error={errors.password}
          placeholder="Enter your password"
          autoComplete="current-password"
          required
        />

        {onForgotPassword && (
          <button
            type="button"
            className="auth-link"
            onClick={onForgotPassword}
          >
            Forgot password?
          </button>
        )}

        <Button
          type="submit"
          variant="primary"
          size="lg"
          fullWidth
          loading={isLoading}
        >
          Sign In
        </Button>

        {onSignUp && (
          <div className="auth-alternate">
            <p>
              Don't have an account?{' '}
              <button
                type="button"
                className="auth-link"
                onClick={onSignUp}
              >
                Sign Up
              </button>
            </p>
          </div>
        )}
      </div>
    </form>
  );
};
