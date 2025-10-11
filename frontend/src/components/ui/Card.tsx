import React from 'react';
import { CardProps } from '../../types';
import './Card.css';

export const Card: React.FC<CardProps> = ({
  children,
  className = '',
  elevated = false,
  interactive = false,
  onClick,
}) => {
  const baseClass = 'card';
  const elevatedClass = elevated ? 'card-elevated' : '';
  const interactiveClass = interactive ? 'card-interactive' : '';

  const classes = [
    baseClass,
    elevatedClass,
    interactiveClass,
    className,
  ].filter(Boolean).join(' ');

  const Component = interactive ? 'button' : 'div';

  return (
    <Component
      className={classes}
      onClick={onClick}
      role={interactive && !onClick ? 'button' : undefined}
      tabIndex={interactive ? 0 : undefined}
    >
      {children}
    </Component>
  );
};
