import React from 'react';
import { Exercise } from '../../types';
import { Card } from '@/components/ui/card';
import './ExerciseCard.css';

interface ExerciseCardProps {
  exercise: Exercise;
  exerciseNumber: number;
  totalExercises: number;
  children: React.ReactNode;
}

export const ExerciseCard: React.FC<ExerciseCardProps> = ({
  exercise,
  exerciseNumber,
  totalExercises,
  children,
}) => {
  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner':
        return 'difficulty-beginner';
      case 'intermediate':
        return 'difficulty-intermediate';
      case 'advanced':
        return 'difficulty-advanced';
      default:
        return '';
    }
  };

  return (
    <Card className="exercise-card" elevated>
      <div className="exercise-card-header">
        <div className="exercise-card-meta">
          <span className="exercise-number">
            Question {exerciseNumber} of {totalExercises}
          </span>
          <span className={`exercise-difficulty ${getDifficultyColor(exercise.difficulty)}`}>
            {exercise.difficulty.charAt(0).toUpperCase() + exercise.difficulty.slice(1)}
          </span>
        </div>

        <div className="exercise-card-type">
          <span className="exercise-type-label">
            {exercise.type.replace('-', ' ').toUpperCase()}
          </span>
        </div>
      </div>

      <div className="exercise-card-content">
        <div className="exercise-verb-info">
          <span className="exercise-verb">{exercise.verb}</span>
          <span className="exercise-tense">{exercise.tense}</span>
        </div>

        <div className="exercise-sentence" role="main" aria-label="Exercise sentence">
          <p>{exercise.sentence}</p>
        </div>

        {children}
      </div>
    </Card>
  );
};
