"""
Learning analytics and intelligent error analysis
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from collections import Counter, defaultdict

class StreakTracker:
    """Track practice streaks to motivate consistent learning"""
    
    def __init__(self, data_file: str = "user_data/streaks.json"):
        self.data_file = data_file
        self.ensure_data_dir()
        self.data = self.load_data()
    
    def ensure_data_dir(self):
        """Ensure data directory exists"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
    
    def load_data(self) -> Dict:
        """Load streak data from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "current_streak": 0,
            "best_streak": 0,
            "last_practice": None,
            "total_days": 0,
            "practice_dates": []
        }
    
    def save_data(self):
        """Save streak data to file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def record_practice(self) -> Dict:
        """Record a practice session and update streak"""
        today = datetime.now().date().isoformat()
        
        if self.data["last_practice"]:
            last_date = datetime.fromisoformat(self.data["last_practice"]).date()
            today_date = datetime.now().date()
            days_diff = (today_date - last_date).days
            
            if days_diff == 0:
                # Already practiced today
                return self.get_streak_info()
            elif days_diff == 1:
                # Streak continues!
                self.data["current_streak"] += 1
                if self.data["current_streak"] > self.data["best_streak"]:
                    self.data["best_streak"] = self.data["current_streak"]
            else:
                # Streak broken
                self.data["current_streak"] = 1
        else:
            # First practice
            self.data["current_streak"] = 1
            self.data["best_streak"] = 1
        
        self.data["last_practice"] = today
        if today not in self.data["practice_dates"]:
            self.data["practice_dates"].append(today)
            self.data["total_days"] += 1
        
        self.save_data()
        return self.get_streak_info()
    
    def get_streak_info(self) -> Dict:
        """Get current streak information"""
        return {
            "current": self.data["current_streak"],
            "best": self.data["best_streak"],
            "total_days": self.data["total_days"],
            "message": self._get_motivational_message()
        }
    
    def _get_motivational_message(self) -> str:
        """Get motivational message based on streak"""
        streak = self.data["current_streak"]
        
        if streak == 0:
            return "¡Comienza tu racha hoy!"
        elif streak < 3:
            return f"¡{streak} día{'s' if streak > 1 else ''}! Sigue así."
        elif streak < 7:
            return f"¡{streak} días seguidos! Excelente progreso."
        elif streak < 14:
            return f"¡{streak} días! ¡Una semana completa!"
        elif streak < 30:
            return f"¡{streak} días! ¡Eres imparable!"
        else:
            return f"¡{streak} días! ¡Maestro del subjuntivo!"

class ErrorAnalyzer:
    """Analyze errors to identify learning patterns and weaknesses"""
    
    def __init__(self):
        self.error_patterns = defaultdict(list)
        self.error_categories = {
            "person_confusion": "Confusing person endings",
            "tense_confusion": "Mixing tense forms",
            "mood_confusion": "Using indicative instead of subjunctive",
            "stem_change_missing": "Missing stem changes",
            "accent_missing": "Missing accent marks",
            "irregular_form": "Irregular verb confusion",
            "trigger_misunderstanding": "Misunderstanding trigger requirement"
        }
    
    def analyze_error(self, user_answer: str, correct_answer: str, context: Dict) -> Dict:
        """Analyze an error and categorize it"""
        user_clean = user_answer.lower().strip()
        correct_clean = correct_answer.lower().strip()
        
        analysis = {
            "error_type": [],
            "specific_issue": "",
            "suggestion": "",
            "pattern_detected": False
        }
        
        # Check for person confusion (wrong ending)
        if self._check_person_confusion(user_clean, correct_clean):
            analysis["error_type"].append("person_confusion")
            analysis["specific_issue"] = "Wrong person ending used"
            analysis["suggestion"] = "Review person endings for this tense"
        
        # Check for tense confusion
        if self._check_tense_confusion(user_clean, correct_clean):
            analysis["error_type"].append("tense_confusion")
            analysis["specific_issue"] = "Wrong tense form used"
            analysis["suggestion"] = "Focus on the time context of the sentence"
        
        # Check for mood confusion (indicative vs subjunctive)
        if self._check_mood_confusion(user_clean, correct_clean):
            analysis["error_type"].append("mood_confusion")
            analysis["specific_issue"] = "Used indicative instead of subjunctive"
            analysis["suggestion"] = "Remember: uncertainty/emotion/desire = subjunctive"
        
        # Check for missing stem changes
        if self._check_stem_change(user_clean, correct_clean):
            analysis["error_type"].append("stem_change_missing")
            analysis["specific_issue"] = "Stem change not applied"
            analysis["suggestion"] = "This verb has a stem change in subjunctive"
        
        # Check for accent marks
        if self._check_accents(user_clean, correct_clean):
            analysis["error_type"].append("accent_missing")
            analysis["specific_issue"] = "Accent mark missing or misplaced"
            analysis["suggestion"] = "Pay attention to accent marks in subjunctive"
        
        # Track this error pattern
        self._track_pattern(analysis["error_type"], context)
        
        return analysis
    
    def _check_person_confusion(self, user: str, correct: str) -> bool:
        """Check if error is due to person confusion"""
        # Common person ending patterns
        person_endings = {
            "1s": ["o", "e", "a"],
            "2s": ["as", "es", "s"],
            "3s": ["a", "e", ""],
            "1p": ["amos", "emos", "imos"],
            "2p": ["áis", "éis", "ís"],
            "3p": ["an", "en", "n"]
        }
        
        # Check if stems are similar but endings differ
        if len(user) > 3 and len(correct) > 3:
            if user[:3] == correct[:3] and user[-2:] != correct[-2:]:
                return True
        return False
    
    def _check_tense_confusion(self, user: str, correct: str) -> bool:
        """Check if error is due to tense confusion"""
        # Present vs imperfect subjunctive patterns
        if ("ara" in correct or "iera" in correct) and ("e" in user or "a" in user[-1:]):
            return True
        if ("e" in correct[-1:] or "a" in correct[-1:]) and ("ara" in user or "iera" in user):
            return True
        return False
    
    def _check_mood_confusion(self, user: str, correct: str) -> bool:
        """Check if indicative was used instead of subjunctive"""
        indicative_patterns = ["o", "as", "a", "amos", "áis", "an"]  # present indicative
        subjunctive_patterns = ["e", "es", "e", "emos", "éis", "en"]  # present subjunctive -ar
        
        # Simple check: if user answer looks like indicative
        for pattern in indicative_patterns:
            if user.endswith(pattern) and not correct.endswith(pattern):
                return True
        return False
    
    def _check_stem_change(self, user: str, correct: str) -> bool:
        """Check for missing stem changes"""
        stem_changes = [
            ("ie", "e"),  # quiero -> quiera
            ("ue", "o"),  # puedo -> pueda
            ("i", "e")    # pido -> pida
        ]
        
        for changed, original in stem_changes:
            if changed in correct and original in user:
                return True
        return False
    
    def _check_accents(self, user: str, correct: str) -> bool:
        """Check for missing or incorrect accent marks"""
        # Remove accents for comparison
        import unicodedata
        
        def remove_accents(text):
            return ''.join(c for c in unicodedata.normalize('NFD', text)
                          if unicodedata.category(c) != 'Mn')
        
        user_no_accent = remove_accents(user)
        correct_no_accent = remove_accents(correct)
        
        # If words are same without accents but different with them
        if user_no_accent == correct_no_accent and user != correct:
            return True
        return False
    
    def _track_pattern(self, error_types: List[str], context: Dict):
        """Track error patterns for personalized feedback"""
        for error_type in error_types:
            self.error_patterns[error_type].append({
                "timestamp": datetime.now().isoformat(),
                "context": context.get("trigger", ""),
                "tense": context.get("tense", "")
            })
    
    def get_weakness_report(self) -> Dict:
        """Generate a report of user's weak areas"""
        if not self.error_patterns:
            return {"weaknesses": [], "suggestions": []}
        
        # Count error frequencies
        error_counts = {
            error_type: len(instances) 
            for error_type, instances in self.error_patterns.items()
        }
        
        # Sort by frequency
        top_weaknesses = sorted(error_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        
        report = {
            "weaknesses": [],
            "suggestions": []
        }
        
        for error_type, count in top_weaknesses:
            report["weaknesses"].append({
                "type": self.error_categories.get(error_type, error_type),
                "frequency": count
            })
            
            # Add targeted suggestions
            if error_type == "person_confusion":
                report["suggestions"].append("Practice conjugation tables for 5 minutes daily")
            elif error_type == "mood_confusion":
                report["suggestions"].append("Focus on trigger words that require subjunctive")
            elif error_type == "stem_change_missing":
                report["suggestions"].append("Review stem-changing verbs like querer, poder, pedir")
        
        return report

class AdaptiveDifficulty:
    """Adjust difficulty based on performance"""
    
    def __init__(self):
        self.performance_history = []
        self.current_level = "Intermediate"
        self.adjustment_threshold = 5  # Number of exercises before adjusting
    
    def record_performance(self, correct: bool):
        """Record performance and potentially adjust difficulty"""
        self.performance_history.append(correct)
        
        # Check if we should adjust difficulty
        if len(self.performance_history) >= self.adjustment_threshold:
            recent = self.performance_history[-self.adjustment_threshold:]
            accuracy = sum(recent) / len(recent)
            
            if accuracy > 0.8 and self.current_level != "Advanced":
                # Increase difficulty
                if self.current_level == "Beginner":
                    self.current_level = "Intermediate"
                else:
                    self.current_level = "Advanced"
                return {"adjusted": True, "new_level": self.current_level, "reason": "High accuracy"}
            
            elif accuracy < 0.4 and self.current_level != "Beginner":
                # Decrease difficulty
                if self.current_level == "Advanced":
                    self.current_level = "Intermediate"
                else:
                    self.current_level = "Beginner"
                return {"adjusted": True, "new_level": self.current_level, "reason": "Low accuracy"}
        
        return {"adjusted": False, "current_level": self.current_level}
    
    def get_recommended_level(self) -> str:
        """Get the recommended difficulty level"""
        return self.current_level

class PracticeGoals:
    """Set and track practice goals"""
    
    def __init__(self, data_file: str = "user_data/goals.json"):
        self.data_file = data_file
        self.ensure_data_dir()
        self.goals = self.load_goals()
    
    def ensure_data_dir(self):
        """Ensure data directory exists"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
    
    def load_goals(self) -> Dict:
        """Load goals from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "daily_exercises": 10,
            "target_accuracy": 80,
            "weekly_minutes": 150,
            "focus_areas": [],
            "achievements": []
        }
    
    def save_goals(self):
        """Save goals to file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.goals, f, indent=2)
    
    def set_goal(self, goal_type: str, value):
        """Set a practice goal"""
        self.goals[goal_type] = value
        self.save_goals()
    
    def check_achievement(self, metric: str, value: float) -> List[str]:
        """Check if any achievements were earned"""
        new_achievements = []
        
        achievement_criteria = {
            "First Steps": {"metric": "total_exercises", "threshold": 10},
            "Dedicated Learner": {"metric": "streak", "threshold": 7},
            "Accuracy Master": {"metric": "accuracy", "threshold": 90},
            "Subjunctive Scholar": {"metric": "total_exercises", "threshold": 100},
            "Perfectionist": {"metric": "perfect_sessions", "threshold": 5}
        }
        
        for name, criteria in achievement_criteria.items():
            if criteria["metric"] == metric and value >= criteria["threshold"]:
                if name not in self.goals["achievements"]:
                    self.goals["achievements"].append(name)
                    new_achievements.append(name)
                    self.save_goals()
        
        return new_achievements