import React from 'react';
import { Card } from '@/components/ui/card';
import './StatsCard.css';

interface StatsCardProps {
  title: string;
  value: string | number;
  icon: React.ReactNode;
  trend?: {
    value: number;
    isPositive: boolean;
  };
  color?: 'primary' | 'success' | 'warning' | 'secondary';
}

export const StatsCard: React.FC<StatsCardProps> = ({
  title,
  value,
  icon,
  trend,
  color = 'primary',
}) => {
  return (
    <Card className={`stats-card stats-card-${color}`} elevated>
      <div className="stats-card-header">
        <div className="stats-card-icon">{icon}</div>
        {trend && (
          <div className={`stats-card-trend ${trend.isPositive ? 'trend-up' : 'trend-down'}`}>
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              {trend.isPositive ? (
                <polyline points="23 6 13.5 15.5 8.5 10.5 1 18" />
              ) : (
                <polyline points="23 18 13.5 8.5 8.5 13.5 1 6" />
              )}
            </svg>
            <span>{Math.abs(trend.value)}%</span>
          </div>
        )}
      </div>

      <div className="stats-card-content">
        <h3 className="stats-card-value">{value}</h3>
        <p className="stats-card-title">{title}</p>
      </div>
    </Card>
  );
};
