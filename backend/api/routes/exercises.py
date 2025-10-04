"""
Exercise routes: get exercises, submit answers, validation.
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, status, Depends, Query
import json
import random
from pathlib import Path
from datetime import datetime

from core.security import get_current_active_user
from models.schemas import (
    ExerciseResponse,
    AnswerSubmit,
    AnswerValidation,
    ExerciseListResponse
)


router = APIRouter(prefix="/exercises", tags=["Exercises"])


# Exercise data file
EXERCISE_DATA_FILE = Path("user_data/fallback_exercises.json")


def load_exercises() -> List[Dict[str, Any]]:
    """Load exercises from JSON file."""
    if EXERCISE_DATA_FILE.exists():
        with open(EXERCISE_DATA_FILE, "r") as f:
            data = json.load(f)
            return data.get("subjunctive_exercises", [])
    return []


def normalize_answer(answer: str) -> str:
    """Normalize answer for comparison."""
    return answer.strip().lower()


def validate_answer(user_answer: str, correct_answer: str) -> bool:
    """
    Validate if user answer matches correct answer.
    Handles multiple acceptable answers separated by '/'.
    """
    user_normalized = normalize_answer(user_answer)

    # Split correct answer by '/' for alternatives
    correct_alternatives = [normalize_answer(ans) for ans in correct_answer.split('/')]

    return user_normalized in correct_alternatives


@router.get("", response_model=ExerciseListResponse)
async def get_exercises(
    difficulty: Optional[int] = Query(None, ge=1, le=5, description="Filter by difficulty"),
    exercise_type: Optional[str] = Query(None, description="Filter by subjunctive type"),
    limit: int = Query(10, ge=1, le=50, description="Number of exercises to return"),
    random_order: bool = Query(True, description="Randomize exercise order"),
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """
    Get practice exercises with optional filtering.

    - **difficulty**: Filter by difficulty level (1-5)
    - **exercise_type**: Filter by subjunctive type (present_subjunctive, imperfect_subjunctive, etc.)
    - **limit**: Number of exercises to return (default: 10)
    - **random_order**: Randomize exercise order (default: true)

    Requires authentication.
    """
    exercises = load_exercises()

    if not exercises:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No exercises available"
        )

    # Apply filters
    filtered_exercises = exercises

    if difficulty is not None:
        filtered_exercises = [ex for ex in filtered_exercises if ex.get("difficulty") == difficulty]

    if exercise_type:
        filtered_exercises = [ex for ex in filtered_exercises if ex.get("type") == exercise_type]

    # Randomize if requested
    if random_order:
        filtered_exercises = random.sample(
            filtered_exercises,
            min(len(filtered_exercises), limit)
        )
    else:
        filtered_exercises = filtered_exercises[:limit]

    # Convert to response models (exclude answers)
    exercise_responses = [
        ExerciseResponse(
            id=ex["id"],
            type=ex["type"],
            prompt=ex["prompt"],
            difficulty=ex["difficulty"],
            explanation=ex.get("explanation"),
            hints=ex.get("hints", []),
            tags=ex.get("tags", [])
        )
        for ex in filtered_exercises
    ]

    return ExerciseListResponse(
        exercises=exercise_responses,
        total=len(exercise_responses),
        page=1,
        page_size=limit,
        has_more=len(exercises) > limit
    )


@router.get("/{exercise_id}", response_model=ExerciseResponse)
async def get_exercise_by_id(
    exercise_id: str,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """
    Get a specific exercise by ID.

    - **exercise_id**: Unique exercise identifier

    Requires authentication.
    """
    exercises = load_exercises()

    exercise = next((ex for ex in exercises if ex["id"] == exercise_id), None)

    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise {exercise_id} not found"
        )

    return ExerciseResponse(
        id=exercise["id"],
        type=exercise["type"],
        prompt=exercise["prompt"],
        difficulty=exercise["difficulty"],
        explanation=exercise.get("explanation"),
        hints=exercise.get("hints", []),
        tags=exercise.get("tags", [])
    )


@router.post("/submit", response_model=AnswerValidation)
async def submit_answer(
    submission: AnswerSubmit,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """
    Submit an answer for validation.

    - **exercise_id**: Exercise identifier
    - **user_answer**: User's submitted answer
    - **time_taken**: Optional time taken in seconds

    Returns validation result with feedback and score.
    Requires authentication.
    """
    exercises = load_exercises()

    exercise = next((ex for ex in exercises if ex["id"] == submission.exercise_id), None)

    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise {submission.exercise_id} not found"
        )

    correct_answer = exercise["answer"]
    is_correct = validate_answer(submission.user_answer, correct_answer)

    # Calculate score based on correctness and time
    base_score = 100 if is_correct else 0

    # Time bonus (if answer is correct and quick)
    if is_correct and submission.time_taken:
        if submission.time_taken < 10:
            base_score = min(100, base_score + 10)
        elif submission.time_taken < 20:
            base_score = min(100, base_score + 5)

    # Generate feedback
    if is_correct:
        feedback = "Excellent! Your answer is correct."
    else:
        feedback = f"Not quite. The correct answer is '{correct_answer}'."

    # Get alternative answers
    alternative_answers = correct_answer.split('/') if '/' in correct_answer else []

    # Save user's attempt (in production, save to database)
    save_user_attempt(
        current_user["sub"],
        submission.exercise_id,
        submission.user_answer,
        is_correct,
        base_score
    )

    return AnswerValidation(
        is_correct=is_correct,
        correct_answer=correct_answer,
        user_answer=submission.user_answer,
        feedback=feedback,
        explanation=exercise.get("explanation", ""),
        score=base_score,
        alternative_answers=alternative_answers
    )


def save_user_attempt(
    user_id: str,
    exercise_id: str,
    user_answer: str,
    is_correct: bool,
    score: int
):
    """Save user attempt to file (in production, use database)."""
    attempts_file = Path(f"user_data/attempts_{user_id}.json")
    attempts_file.parent.mkdir(exist_ok=True)

    attempts = []
    if attempts_file.exists():
        with open(attempts_file, "r") as f:
            attempts = json.load(f)

    attempts.append({
        "exercise_id": exercise_id,
        "user_answer": user_answer,
        "is_correct": is_correct,
        "score": score,
        "timestamp": datetime.utcnow().isoformat()
    })

    with open(attempts_file, "w") as f:
        json.dump(attempts, f, indent=2)


@router.get("/types/available", response_model=List[str])
async def get_available_exercise_types(
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """
    Get list of available exercise types.

    Requires authentication.
    """
    exercises = load_exercises()
    types = list(set(ex["type"] for ex in exercises))
    return sorted(types)
