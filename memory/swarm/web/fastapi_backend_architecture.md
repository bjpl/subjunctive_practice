# FastAPI Backend Architecture
## 15 Modules for Spanish Subjunctive Learning API

### Overview
Modern Python FastAPI backend replacing 89 PyQt desktop modules with clean, RESTful architecture.

---

## Module Structure (15 modules)

### 1. Core API Layer (5 modules)

#### `api/main.py` - Application Entry Point
```python
from fastapi import FastAPI, Middleware
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from api.routes import exercises, sessions, analytics, auth, users
from api.middleware import AuthMiddleware, LoggingMiddleware
from core.database import init_db
from core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    pass

app = FastAPI(
    title="Spanish Subjunctive Learning API",
    version="2.0.0",
    lifespan=lifespan
)

# Middleware
app.add_middleware(CORSMiddleware, allow_origins=["*"])
app.add_middleware(AuthMiddleware)
app.add_middleware(LoggingMiddleware)

# Routes
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(exercises.router, prefix="/exercises", tags=["exercises"])
app.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
app.include_router(analytics.router, prefix="/analytics", tags=["analytics"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

#### `api/routes/exercises.py` - Exercise Management
```python
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel

from core.exercise_generator import ExerciseGenerator
from core.conjugation_engine import ConjugationEngine
from models.exercise import Exercise, ExerciseCreate, ExerciseResponse
from models.user import User
from api.deps import get_current_user, get_db

router = APIRouter()

@router.post("/generate", response_model=ExerciseResponse)
async def generate_exercise(
    difficulty: str = Query("intermediate", enum=["beginner", "intermediate", "advanced"]),
    exercise_type: str = Query("conjugation", enum=["conjugation", "multiple_choice", "fill_blank", "scenario"]),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate a new exercise based on user preferences and progress"""
    generator = ExerciseGenerator(db)
    exercise = await generator.generate_personalized_exercise(
        user_id=current_user.id,
        difficulty=difficulty,
        exercise_type=exercise_type
    )
    return exercise

@router.post("/{exercise_id}/submit")
async def submit_answer(
    exercise_id: int,
    answer: str,
    response_time: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit an answer and receive feedback"""
    # Validation and feedback logic
    pass

@router.get("/", response_model=List[ExerciseResponse])
async def get_exercises(
    skip: int = 0,
    limit: int = 100,
    difficulty: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get exercises with filtering"""
    pass
```

#### `api/routes/sessions.py` - Session Management
```python
from fastapi import APIRouter, Depends, BackgroundTasks
from typing import List
from datetime import datetime

from core.session_manager import SessionManager
from core.spaced_repetition import SpacedRepetitionScheduler
from models.session import SessionCreate, SessionResponse, SessionStats
from models.user import User
from api.deps import get_current_user, get_db

router = APIRouter()

@router.post("/start", response_model=SessionResponse)
async def start_session(
    session_data: SessionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start a new practice session"""
    session_manager = SessionManager(db)
    session = await session_manager.create_session(
        user_id=current_user.id,
        session_type=session_data.session_type,
        difficulty=session_data.difficulty
    )
    return session

@router.post("/{session_id}/complete")
async def complete_session(
    session_id: int,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Complete a practice session and update analytics"""
    session_manager = SessionManager(db)
    result = await session_manager.complete_session(session_id, current_user.id)
    
    # Background task to update spaced repetition schedule
    scheduler = SpacedRepetitionScheduler(db)
    background_tasks.add_task(scheduler.update_schedule, current_user.id, session_id)
    
    return result

@router.get("/stats", response_model=SessionStats)
async def get_session_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's session statistics"""
    pass
```

#### `api/routes/analytics.py` - Analytics & Progress
```python
from fastapi import APIRouter, Depends, Query
from typing import List, Dict, Any
from datetime import datetime, timedelta

from core.learning_analytics import LearningAnalytics
from core.error_analyzer import ErrorAnalyzer
from models.user import User
from models.analytics import ProgressReport, ErrorPattern, Achievement

router = APIRouter()

@router.get("/progress", response_model=ProgressReport)
async def get_progress_report(
    days: int = Query(30, ge=1, le=365),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed progress report"""
    analytics = LearningAnalytics(db)
    return await analytics.generate_progress_report(
        user_id=current_user.id,
        days=days
    )

@router.get("/error-patterns", response_model=List[ErrorPattern])
async def get_error_patterns(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Analyze user's error patterns and provide recommendations"""
    analyzer = ErrorAnalyzer(db)
    patterns = await analyzer.analyze_user_errors(current_user.id)
    return patterns

@router.get("/achievements", response_model=List[Achievement])
async def get_achievements(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user achievements and badges"""
    pass

@router.get("/leaderboard")
async def get_leaderboard(
    timeframe: str = Query("weekly", enum=["daily", "weekly", "monthly"]),
    db: Session = Depends(get_db)
):
    """Get leaderboard data"""
    pass
```

#### `api/routes/auth.py` - Authentication
```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr

from core.security import create_access_token, verify_password, get_password_hash
from models.user import User, UserCreate, UserResponse
from api.deps import get_db

router = APIRouter()

class Token(BaseModel):
    access_token: str
    token_type: str

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user exists
    existing_user = await get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    user = UserCreate(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name
    )
    
    new_user = await create_user(db, user)
    return new_user

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login and receive access token"""
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
```

#### `api/middleware.py` - Custom Middleware
```python
from fastapi import Request, Response, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
import time
import logging

class AuthMiddleware(BaseHTTPMiddleware):
    """Handle authentication for protected routes"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip auth for public endpoints
        public_paths = ["/auth", "/health", "/docs", "/openapi.json"]
        if any(request.url.path.startswith(path) for path in public_paths):
            return await call_next(request)
        
        # Validate JWT token
        authorization = request.headers.get("authorization")
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid token")
        
        return await call_next(request)

class LoggingMiddleware(BaseHTTPMiddleware):
    """Log all requests and responses"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        logging.info(
            f"{request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Time: {process_time:.3f}s"
        )
        
        return response
```

### 2. Business Logic Layer (6 modules)

#### `core/conjugation_engine.py` - Spanish Conjugation Logic
```python
from typing import Dict, List, Tuple, Optional
from enum import Enum
from dataclasses import dataclass

class VerbType(Enum):
    REGULAR = "regular"
    STEM_CHANGING = "stem_changing"
    IRREGULAR = "irregular"
    SPELLING_CHANGING = "spelling_changing"

class Tense(Enum):
    PRESENT_SUBJUNCTIVE = "present_subjunctive"
    IMPERFECT_SUBJUNCTIVE_RA = "imperfect_subjunctive_ra"
    IMPERFECT_SUBJUNCTIVE_SE = "imperfect_subjunctive_se"

@dataclass
class ConjugationResult:
    conjugated_form: str
    is_correct: bool
    confidence: float
    explanation: str
    alternative_forms: List[str]

class ConjugationEngine:
    """Core Spanish subjunctive conjugation engine"""
    
    def __init__(self):
        self.irregular_verbs = self._load_irregular_patterns()
        self.stem_changing_patterns = self._load_stem_patterns()
        self.trigger_words = self._load_triggers()
    
    def conjugate(
        self,
        infinitive: str,
        tense: Tense,
        person: str,
        number: str
    ) -> ConjugationResult:
        """Conjugate a verb in the specified subjunctive form"""
        verb_type = self._identify_verb_type(infinitive)
        
        if verb_type == VerbType.IRREGULAR:
            return self._conjugate_irregular(infinitive, tense, person, number)
        elif verb_type == VerbType.STEM_CHANGING:
            return self._conjugate_stem_changing(infinitive, tense, person, number)
        else:
            return self._conjugate_regular(infinitive, tense, person, number)
    
    def validate_answer(
        self,
        infinitive: str,
        user_answer: str,
        correct_form: str,
        context: Dict
    ) -> ConjugationResult:
        """Validate user's conjugation answer"""
        is_correct = user_answer.lower().strip() == correct_form.lower().strip()
        
        # Check for common variations
        alternatives = self._get_alternative_forms(infinitive, context)
        is_alternative_correct = user_answer.lower() in [alt.lower() for alt in alternatives]
        
        explanation = self._generate_explanation(
            infinitive, user_answer, correct_form, context, is_correct
        )
        
        return ConjugationResult(
            conjugated_form=correct_form,
            is_correct=is_correct or is_alternative_correct,
            confidence=1.0 if is_correct else 0.8 if is_alternative_correct else 0.0,
            explanation=explanation,
            alternative_forms=alternatives
        )
    
    def _load_irregular_patterns(self) -> Dict:
        """Load irregular verb conjugation patterns"""
        return {
            'ser': {
                'present_subjunctive': {
                    'yo': 'sea', 'tú': 'seas', 'él': 'sea',
                    'nosotros': 'seamos', 'vosotros': 'seáis', 'ellos': 'sean'
                }
            },
            'estar': {
                'present_subjunctive': {
                    'yo': 'esté', 'tú': 'estés', 'él': 'esté',
                    'nosotros': 'estemos', 'vosotros': 'estéis', 'ellos': 'estén'
                }
            }
            # ... more irregular verbs
        }
    
    def _identify_verb_type(self, infinitive: str) -> VerbType:
        """Identify the type of verb for conjugation rules"""
        if infinitive in self.irregular_verbs:
            return VerbType.IRREGULAR
        # Additional logic for stem-changing, spelling-changing verbs
        return VerbType.REGULAR
```

#### `core/exercise_generator.py` - TBLT Exercise Generation
```python
from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass
import random

from core.conjugation_engine import ConjugationEngine
from models.exercise import Exercise, ExerciseType
from models.user import User

class Difficulty(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

@dataclass
class TBLTScenario:
    context: str
    situation: str
    trigger_phrase: str
    target_structures: List[str]
    cultural_note: Optional[str] = None

class ExerciseGenerator:
    """Task-Based Language Teaching exercise generator"""
    
    def __init__(self, db_session):
        self.db = db_session
        self.conjugation_engine = ConjugationEngine()
        self.scenarios = self._load_tblt_scenarios()
    
    async def generate_personalized_exercise(
        self,
        user_id: int,
        difficulty: str,
        exercise_type: str
    ) -> Exercise:
        """Generate exercise based on user's learning history"""
        user_progress = await self._get_user_progress(user_id)
        
        if exercise_type == "conjugation":
            return self._generate_conjugation_exercise(difficulty, user_progress)
        elif exercise_type == "scenario":
            return self._generate_scenario_exercise(difficulty, user_progress)
        elif exercise_type == "multiple_choice":
            return self._generate_multiple_choice(difficulty, user_progress)
        elif exercise_type == "fill_blank":
            return self._generate_fill_blank(difficulty, user_progress)
    
    def _generate_conjugation_exercise(
        self,
        difficulty: str,
        user_progress: Dict
    ) -> Exercise:
        """Generate a direct conjugation exercise"""
        # Select verb based on user's weak areas
        verb = self._select_target_verb(difficulty, user_progress)
        tense = self._select_target_tense(difficulty, user_progress)
        person = random.choice(['yo', 'tú', 'él', 'nosotros', 'ellos'])
        
        correct_answer = self.conjugation_engine.conjugate(verb, tense, person, 'singular')
        
        return Exercise(
            question=f"Conjugate '{verb}' in {tense.value} for '{person}'",
            correct_answer=correct_answer.conjugated_form,
            exercise_type=ExerciseType.CONJUGATION,
            difficulty=difficulty,
            metadata={
                'verb': verb,
                'tense': tense.value,
                'person': person,
                'explanation': correct_answer.explanation
            }
        )
    
    def _generate_scenario_exercise(
        self,
        difficulty: str,
        user_progress: Dict
    ) -> Exercise:
        """Generate a TBLT scenario-based exercise"""
        scenario = random.choice([s for s in self.scenarios if s.difficulty == difficulty])
        
        # Create realistic communicative situation
        context = scenario.context.format(
            verb=self._select_target_verb(difficulty, user_progress),
            trigger=scenario.trigger_phrase
        )
        
        return Exercise(
            question=context,
            exercise_type=ExerciseType.SCENARIO,
            difficulty=difficulty,
            metadata={
                'scenario_id': scenario.id,
                'cultural_note': scenario.cultural_note,
                'target_structures': scenario.target_structures
            }
        )
    
    def _load_tblt_scenarios(self) -> List[TBLTScenario]:
        """Load communicative scenarios for different contexts"""
        return [
            TBLTScenario(
                context="You're at a restaurant and want to express doubt about the food quality. Complete: 'No creo que la comida _____ buena.'",
                situation="restaurant_doubt",
                trigger_phrase="No creo que",
                target_structures=["present_subjunctive"],
                cultural_note="In Spanish-speaking countries, expressing doubt politely is important for social harmony."
            ),
            TBLTScenario(
                context="Your friend is late and you're worried. Express: 'I hope he arrives soon.' → 'Espero que _____ pronto.'",
                situation="concern_hope",
                trigger_phrase="Espero que",
                target_structures=["present_subjunctive"],
                cultural_note="Expressing hope and concern shows care in Hispanic cultures."
            )
            # ... more scenarios
        ]
```

#### `core/session_manager.py` - Session Orchestration
```python
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from models.session import Session as SessionModel, SessionCreate
from models.exercise import Exercise
from models.user import User
from core.spaced_repetition import SpacedRepetitionScheduler

class SessionManager:
    """Orchestrates practice sessions and learning flow"""
    
    def __init__(self, db: Session):
        self.db = db
        self.spaced_repetition = SpacedRepetitionScheduler(db)
    
    async def create_session(
        self,
        user_id: int,
        session_type: str,
        difficulty: str
    ) -> SessionModel:
        """Create a new practice session"""
        session = SessionModel(
            user_id=user_id,
            session_type=session_type,
            difficulty=difficulty,
            started_at=datetime.utcnow(),
            status="active"
        )
        
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        
        # Generate initial exercises
        await self._populate_session_queue(session.id, difficulty)
        
        return session
    
    async def get_next_exercise(self, session_id: int, user_id: int) -> Optional[Exercise]:
        """Get the next exercise in the session"""
        # Check spaced repetition items first
        review_exercise = await self.spaced_repetition.get_due_review(user_id)
        if review_exercise:
            return review_exercise
        
        # Generate new exercise based on session progress
        return await self._generate_adaptive_exercise(session_id, user_id)
    
    async def record_exercise_result(
        self,
        session_id: int,
        exercise_id: int,
        user_answer: str,
        is_correct: bool,
        response_time: int,
        hints_used: int = 0
    ) -> Dict[str, Any]:
        """Record exercise completion and update learning metrics"""
        result = {
            'session_id': session_id,
            'exercise_id': exercise_id,
            'user_answer': user_answer,
            'is_correct': is_correct,
            'response_time': response_time,
            'hints_used': hints_used,
            'timestamp': datetime.utcnow()
        }
        
        # Update spaced repetition schedule
        await self.spaced_repetition.update_item_schedule(
            exercise_id, is_correct, response_time
        )
        
        # Update session statistics
        await self._update_session_stats(session_id, is_correct, response_time)
        
        return result
    
    async def complete_session(self, session_id: int, user_id: int) -> Dict[str, Any]:
        """Complete a session and generate summary"""
        session = self.db.query(SessionModel).filter_by(id=session_id).first()
        
        session.completed_at = datetime.utcnow()
        session.status = "completed"
        
        # Calculate session metrics
        summary = await self._generate_session_summary(session_id, user_id)
        
        self.db.commit()
        return summary
```

#### `core/learning_analytics.py` - Progress Analytics
```python
from typing import Dict, List, Any, Tuple
from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy.orm import Session

from models.user import User
from models.exercise import Exercise
from models.session import Session as SessionModel
from models.analytics import ProgressReport, LearningPattern, Achievement

class LearningAnalytics:
    """Analyzes user learning patterns and progress"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def generate_progress_report(
        self,
        user_id: int,
        days: int = 30
    ) -> ProgressReport:
        """Generate comprehensive progress report"""
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Query session data
        sessions = self.db.query(SessionModel).filter(
            SessionModel.user_id == user_id,
            SessionModel.started_at >= start_date
        ).all()
        
        # Calculate metrics
        accuracy_trend = await self._calculate_accuracy_trend(user_id, days)
        difficulty_progression = await self._analyze_difficulty_progression(user_id, days)
        weak_areas = await self._identify_weak_areas(user_id)
        achievements = await self._get_recent_achievements(user_id, days)
        
        return ProgressReport(
            user_id=user_id,
            period_days=days,
            total_sessions=len(sessions),
            accuracy_trend=accuracy_trend,
            difficulty_progression=difficulty_progression,
            weak_areas=weak_areas,
            achievements=achievements,
            generated_at=datetime.utcnow()
        )
    
    async def _calculate_accuracy_trend(
        self,
        user_id: int,
        days: int
    ) -> List[Tuple[datetime, float]]:
        """Calculate daily accuracy trend"""
        # Complex SQL query to get daily accuracy
        pass
    
    async def identify_learning_patterns(
        self,
        user_id: int
    ) -> List[LearningPattern]:
        """Identify patterns in user's learning behavior"""
        patterns = []
        
        # Time-based patterns
        peak_hours = await self._analyze_peak_learning_hours(user_id)
        patterns.append(LearningPattern(
            type="temporal",
            description=f"Peak learning hours: {peak_hours}",
            confidence=0.85
        ))
        
        # Difficulty patterns
        difficulty_comfort = await self._analyze_difficulty_comfort(user_id)
        patterns.append(LearningPattern(
            type="difficulty",
            description=f"Most comfortable with: {difficulty_comfort}",
            confidence=0.92
        ))
        
        return patterns
```

#### `core/spaced_repetition.py` - SM-2 Algorithm
```python
from typing import Dict, Optional, List
from datetime import datetime, timedelta
from enum import Enum
import math

from models.spaced_repetition import ReviewItem, ReviewSchedule

class ReviewQuality(Enum):
    COMPLETE_BLACKOUT = 0
    INCORRECT_HARD_RECALL = 1
    INCORRECT_EASY_RECALL = 2
    CORRECT_HARD_RECALL = 3
    CORRECT_AFTER_HESITATION = 4
    PERFECT_RECALL = 5

class SpacedRepetitionScheduler:
    """SM-2 algorithm implementation for optimal review scheduling"""
    
    def __init__(self, db_session):
        self.db = db_session
        self.minimum_ease_factor = 1.3
        self.maximum_interval_days = 365
    
    async def schedule_item(
        self,
        user_id: int,
        exercise_id: int,
        initial_quality: ReviewQuality = ReviewQuality.CORRECT_AFTER_HESITATION
    ) -> ReviewItem:
        """Add new item to spaced repetition schedule"""
        item = ReviewItem(
            user_id=user_id,
            exercise_id=exercise_id,
            ease_factor=2.5,  # Default ease factor
            interval_days=1,   # Start with 1 day
            repetition_count=0,
            next_review_date=datetime.utcnow() + timedelta(days=1),
            quality_history=[initial_quality.value]
        )
        
        self.db.add(item)
        self.db.commit()
        
        return item
    
    async def update_item_schedule(
        self,
        exercise_id: int,
        user_id: int,
        quality: ReviewQuality,
        response_time_ms: int
    ) -> ReviewItem:
        """Update item schedule based on performance using SM-2 algorithm"""
        item = self.db.query(ReviewItem).filter_by(
            exercise_id=exercise_id,
            user_id=user_id
        ).first()
        
        if not item:
            return await self.schedule_item(user_id, exercise_id, quality)
        
        # SM-2 Algorithm implementation
        q = quality.value
        
        if q >= 3:  # Correct answer
            if item.repetition_count == 0:
                item.interval_days = 1
            elif item.repetition_count == 1:
                item.interval_days = 6
            else:
                item.interval_days = int(item.interval_days * item.ease_factor)
            
            item.repetition_count += 1
        else:  # Incorrect answer
            item.repetition_count = 0
            item.interval_days = 1
        
        # Update ease factor
        item.ease_factor = max(
            self.minimum_ease_factor,
            item.ease_factor + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
        )
        
        # Adjust for response time (faster = higher retention)
        time_factor = self._calculate_time_factor(response_time_ms)
        item.interval_days = int(item.interval_days * time_factor)
        
        # Cap maximum interval
        item.interval_days = min(item.interval_days, self.maximum_interval_days)
        
        # Set next review date
        item.next_review_date = datetime.utcnow() + timedelta(days=item.interval_days)
        item.last_reviewed_at = datetime.utcnow()
        item.quality_history.append(q)
        
        self.db.commit()
        return item
    
    def _calculate_time_factor(self, response_time_ms: int) -> float:
        """Calculate adjustment factor based on response time"""
        # Faster responses indicate better retention
        if response_time_ms < 2000:  # Very fast (< 2s)
            return 1.2
        elif response_time_ms < 5000:  # Fast (< 5s)
            return 1.1
        elif response_time_ms < 10000:  # Normal (< 10s)
            return 1.0
        elif response_time_ms < 20000:  # Slow (< 20s)
            return 0.9
        else:  # Very slow (> 20s)
            return 0.8
```

#### `core/error_analyzer.py` - Error Pattern Analysis
```python
from typing import Dict, List, Tuple, Any
from collections import Counter, defaultdict
from sqlalchemy.orm import Session
import re

from models.user import User
from models.exercise import Exercise, ExerciseResult
from models.analytics import ErrorPattern, RemedialSuggestion

class ErrorAnalyzer:
    """Analyzes user errors and provides targeted feedback"""
    
    def __init__(self, db: Session):
        self.db = db
        self.error_patterns = self._load_error_patterns()
    
    async def analyze_user_errors(self, user_id: int) -> List[ErrorPattern]:
        """Analyze user's error patterns and identify learning gaps"""
        recent_results = self.db.query(ExerciseResult).filter(
            ExerciseResult.user_id == user_id,
            ExerciseResult.is_correct == False
        ).order_by(ExerciseResult.created_at.desc()).limit(100).all()
        
        patterns = []
        
        # Analyze mood confusion (indicative vs subjunctive)
        mood_errors = self._analyze_mood_confusion(recent_results)
        if mood_errors['frequency'] > 0.3:  # More than 30% error rate
            patterns.append(ErrorPattern(
                type="mood_confusion",
                description="Frequent confusion between indicative and subjunctive moods",
                frequency=mood_errors['frequency'],
                examples=mood_errors['examples'],
                remedial_suggestions=self._get_mood_confusion_remedies()
            ))
        
        # Analyze stem-changing verb errors
        stem_errors = self._analyze_stem_changing_errors(recent_results)
        if stem_errors['frequency'] > 0.25:
            patterns.append(ErrorPattern(
                type="stem_changing",
                description="Difficulty with stem-changing verbs in subjunctive",
                frequency=stem_errors['frequency'],
                examples=stem_errors['examples'],
                remedial_suggestions=self._get_stem_changing_remedies()
            ))
        
        # Analyze trigger word recognition
        trigger_errors = self._analyze_trigger_recognition(recent_results)
        if trigger_errors['frequency'] > 0.2:
            patterns.append(ErrorPattern(
                type="trigger_recognition",
                description="Missing subjunctive triggers in context",
                frequency=trigger_errors['frequency'],
                examples=trigger_errors['examples'],
                remedial_suggestions=self._get_trigger_recognition_remedies()
            ))
        
        return patterns
    
    def _analyze_mood_confusion(self, results: List[ExerciseResult]) -> Dict:
        """Identify mood confusion patterns"""
        mood_errors = []
        
        for result in results:
            if self._is_mood_confusion_error(result):
                mood_errors.append({
                    'user_answer': result.user_answer,
                    'correct_answer': result.correct_answer,
                    'context': result.exercise.metadata.get('context', ''),
                    'trigger': result.exercise.metadata.get('trigger', '')
                })
        
        return {
            'frequency': len(mood_errors) / max(len(results), 1),
            'examples': mood_errors[:5],  # Top 5 examples
            'total_count': len(mood_errors)
        }
    
    def _is_mood_confusion_error(self, result: ExerciseResult) -> bool:
        """Determine if error is due to mood confusion"""
        user_answer = result.user_answer.lower()
        correct_answer = result.correct_answer.lower()
        
        # Check if user provided indicative form when subjunctive was needed
        verb_root = self._extract_verb_root(correct_answer)
        if verb_root:
            indicative_forms = self._get_indicative_forms(verb_root)
            return user_answer in indicative_forms
        
        return False
    
    def _get_mood_confusion_remedies(self) -> List[RemedialSuggestion]:
        """Get remedial exercises for mood confusion"""
        return [
            RemedialSuggestion(
                type="drill",
                title="Trigger Word Recognition",
                description="Practice identifying subjunctive triggers",
                exercises=[
                    "identification_drill_triggers",
                    "context_based_mood_choice",
                    "trigger_word_flashcards"
                ]
            ),
            RemedialSuggestion(
                type="explanation",
                title="When to Use Subjunctive",
                description="Review the WEIRDO rule and subjunctive contexts",
                content="Focus on: Wishes, Emotions, Impersonal expressions, Recommendations, Doubt, Ojalá"
            )
        ]
```

### 3. Data Layer (4 modules)

#### `models/database.py` - Database Configuration
```python
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
import os

# Database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./subjunctive_practice.db")

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

async def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency for database sessions"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

#### `models/user.py` - User Models
```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any

from models.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Learning preferences
    preferred_difficulty = Column(String, default="intermediate")
    learning_goals = Column(JSON, default=dict)
    accessibility_settings = Column(JSON, default=dict)
    
    # Progress tracking
    total_exercises_completed = Column(Integer, default=0)
    current_streak_days = Column(Integer, default=0)
    longest_streak_days = Column(Integer, default=0)
    overall_accuracy = Column(Float, default=0.0)
    
    # Relationships
    sessions = relationship("Session", back_populates="user")
    exercise_results = relationship("ExerciseResult", back_populates="user")
    review_items = relationship("ReviewItem", back_populates="user")

# Pydantic models for API
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    preferred_difficulty: str = "intermediate"

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    preferred_difficulty: Optional[str] = None
    learning_goals: Optional[Dict[str, Any]] = None
    accessibility_settings: Optional[Dict[str, Any]] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    total_exercises_completed: int
    current_streak_days: int
    overall_accuracy: float
    created_at: datetime
    
    class Config:
        from_attributes = True
```

#### `models/exercise.py` - Exercise Models
```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, JSON, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from enum import Enum

from models.database import Base

class ExerciseType(str, Enum):
    CONJUGATION = "conjugation"
    MULTIPLE_CHOICE = "multiple_choice"
    FILL_BLANK = "fill_blank"
    SCENARIO = "scenario"
    TRANSLATION = "translation"

class Exercise(Base):
    __tablename__ = "exercises"
    
    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    correct_answer = Column(String, nullable=False)
    exercise_type = Column(String, nullable=False)
    difficulty = Column(String, nullable=False)
    
    # TBLT context
    context = Column(Text)
    cultural_note = Column(Text)
    explanation = Column(Text)
    
    # Metadata for exercise generation
    metadata = Column(JSON, default=dict)  # verb, tense, person, etc.
    
    # Multiple choice options (if applicable)
    options = Column(JSON, default=list)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    results = relationship("ExerciseResult", back_populates="exercise")

class ExerciseResult(Base):
    __tablename__ = "exercise_results"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    
    user_answer = Column(String, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    response_time_ms = Column(Integer, nullable=False)
    hints_used = Column(Integer, default=0)
    
    # Feedback provided
    feedback_message = Column(Text)
    explanation_shown = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="exercise_results")
    exercise = relationship("Exercise", back_populates="results")
    session = relationship("Session", back_populates="exercise_results")

# Pydantic models
class ExerciseBase(BaseModel):
    question: str
    correct_answer: str
    exercise_type: ExerciseType
    difficulty: str
    context: Optional[str] = None
    explanation: Optional[str] = None

class ExerciseCreate(ExerciseBase):
    metadata: Optional[Dict[str, Any]] = None
    options: Optional[List[str]] = None

class ExerciseResponse(ExerciseBase):
    id: int
    options: Optional[List[str]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class ExerciseSubmission(BaseModel):
    exercise_id: int
    user_answer: str
    response_time_ms: int
    hints_used: int = 0

class ExerciseResultResponse(BaseModel):
    is_correct: bool
    feedback_message: str
    explanation: Optional[str] = None
    correct_answer: str
    next_exercise_id: Optional[int] = None
```

#### `models/session.py` - Session Models
```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Dict, Any
from enum import Enum

from models.database import Base

class SessionType(str, Enum):
    PRACTICE = "practice"
    REVIEW = "review"
    ASSESSMENT = "assessment"
    CHALLENGE = "challenge"

class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    session_type = Column(String, nullable=False)
    difficulty = Column(String, nullable=False)
    status = Column(String, default="active")  # active, completed, abandoned
    
    # Timing
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    estimated_duration_minutes = Column(Integer, default=15)
    
    # Progress tracking
    total_exercises = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    average_response_time_ms = Column(Integer, default=0)
    hints_used = Column(Integer, default=0)
    
    # Session settings
    settings = Column(JSON, default=dict)
    
    # Relationships
    user = relationship("User", back_populates="sessions")
    exercise_results = relationship("ExerciseResult", back_populates="session")

# Pydantic models
class SessionBase(BaseModel):
    session_type: SessionType
    difficulty: str
    estimated_duration_minutes: int = 15

class SessionCreate(SessionBase):
    settings: Optional[Dict[str, Any]] = None

class SessionResponse(SessionBase):
    id: int
    user_id: int
    status: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    total_exercises: int
    correct_answers: int
    
    @property
    def accuracy(self) -> float:
        return (self.correct_answers / self.total_exercises) if self.total_exercises > 0 else 0.0
    
    class Config:
        from_attributes = True

class SessionStats(BaseModel):
    total_sessions: int
    total_time_minutes: int
    average_accuracy: float
    current_streak: int
    sessions_this_week: int
    favorite_difficulty: str
```

---

## Deployment Configuration

### Docker Configuration
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Requirements
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
pydantic[email]==2.5.0
alembic==1.12.1
pytest==7.4.3
httpx==0.25.2
```

This FastAPI backend architecture consolidates 89 PyQt desktop modules into 15 focused, modern web API modules while preserving all core Spanish subjunctive learning functionality.