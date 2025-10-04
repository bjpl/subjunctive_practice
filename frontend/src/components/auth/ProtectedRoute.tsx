import React, { useEffect, useState } from 'react';
import { FullPageSpinner } from '../ui/Spinner';

interface ProtectedRouteProps {
  children: React.ReactNode;
  isAuthenticated: boolean;
  onUnauthenticated: () => void;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  children,
  isAuthenticated,
  onUnauthenticated,
}) => {
  const [isChecking, setIsChecking] = useState(true);

  useEffect(() => {
    // Simulate checking authentication status
    const checkAuth = async () => {
      // In a real app, this would check token validity, etc.
      await new Promise((resolve) => setTimeout(resolve, 100));
      setIsChecking(false);

      if (!isAuthenticated) {
        onUnauthenticated();
      }
    };

    checkAuth();
  }, [isAuthenticated, onUnauthenticated]);

  if (isChecking) {
    return <FullPageSpinner label="Verifying authentication" />;
  }

  if (!isAuthenticated) {
    return null; // Will redirect via onUnauthenticated
  }

  return <>{children}</>;
};
