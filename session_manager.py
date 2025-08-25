"""
Session management for progress tracking and review
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class SessionManager:
    """Manage user sessions, progress, and review items"""
    
    def __init__(self, data_dir: str = "user_data"):
        self.data_dir = data_dir
        self.current_session = {
            "start_time": datetime.now().isoformat(),
            "exercises_completed": 0,
            "correct_answers": 0,
            "incorrect_items": [],  # Items to review
            "mastered_items": [],   # Items answered correctly multiple times
            "difficulty_progression": []
        }
        self.ensure_data_dir()
    
    def ensure_data_dir(self):
        """Create data directory if it doesn't exist"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def save_session(self, filename: Optional[str] = None) -> str:
        """Save current session to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"session_{timestamp}.json"
        
        filepath = os.path.join(self.data_dir, filename)
        
        # Add end time before saving
        self.current_session["end_time"] = datetime.now().isoformat()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.current_session, f, ensure_ascii=False, indent=2)
        
        return filepath
    
    def load_session(self, filename: str) -> Dict:
        """Load a saved session"""
        filepath = os.path.join(self.data_dir, filename)
        
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def add_exercise_result(self, exercise: Dict, user_answer: str, is_correct: bool):
        """Track exercise results"""
        self.current_session["exercises_completed"] += 1
        
        if is_correct:
            self.current_session["correct_answers"] += 1
            # Remove from incorrect if it was there
            self.current_session["incorrect_items"] = [
                item for item in self.current_session["incorrect_items"]
                if item["sentence"] != exercise.get("sentence")
            ]
            # Add to mastered after 3 correct answers
            if exercise.get("sentence") not in [m["sentence"] for m in self.current_session["mastered_items"]]:
                # Track how many times answered correctly
                correct_count = sum(1 for item in self.current_session.get("history", [])
                                  if item.get("sentence") == exercise.get("sentence") and item.get("correct"))
                if correct_count >= 2:  # 3rd correct answer
                    self.current_session["mastered_items"].append({
                        "sentence": exercise.get("sentence"),
                        "mastered_at": datetime.now().isoformat()
                    })
        else:
            # Add to review list if not already there
            if exercise.get("sentence") not in [item["sentence"] for item in self.current_session["incorrect_items"]]:
                self.current_session["incorrect_items"].append({
                    "sentence": exercise.get("sentence"),
                    "correct_answer": exercise.get("answer"),
                    "user_answer": user_answer,
                    "context": exercise.get("context", ""),
                    "attempts": 1
                })
            else:
                # Increment attempts
                for item in self.current_session["incorrect_items"]:
                    if item["sentence"] == exercise.get("sentence"):
                        item["attempts"] += 1
                        item["last_attempt"] = datetime.now().isoformat()
    
    def get_review_items(self) -> List[Dict]:
        """Get items that need review"""
        return self.current_session["incorrect_items"]
    
    def get_statistics(self) -> Dict:
        """Get session statistics"""
        total = self.current_session["exercises_completed"]
        correct = self.current_session["correct_answers"]
        
        return {
            "total_exercises": total,
            "correct_answers": correct,
            "accuracy": (correct / total * 100) if total > 0 else 0,
            "items_to_review": len(self.current_session["incorrect_items"]),
            "mastered_items": len(self.current_session["mastered_items"]),
            "session_duration": self._calculate_duration()
        }
    
    def _calculate_duration(self) -> str:
        """Calculate session duration"""
        start = datetime.fromisoformat(self.current_session["start_time"])
        duration = datetime.now() - start
        minutes = int(duration.total_seconds() / 60)
        return f"{minutes} minutes"
    
    def get_progress_report(self) -> str:
        """Generate a progress report"""
        stats = self.get_statistics()
        
        report = f"""
Progress Report
═══════════════
Session Duration: {stats['session_duration']}
Exercises Completed: {stats['total_exercises']}
Correct Answers: {stats['correct_answers']}
Accuracy: {stats['accuracy']:.1f}%
Items Mastered: {stats['mastered_items']}
Items to Review: {stats['items_to_review']}
"""
        
        if self.current_session["incorrect_items"]:
            report += "\n\nItems Needing Review:\n"
            for item in self.current_session["incorrect_items"][:5]:  # Show top 5
                report += f"• {item['sentence']} (Attempts: {item['attempts']})\n"
        
        return report

class ReviewQueue:
    """Manage review queue with priority"""
    
    def __init__(self):
        self.queue = []
        self.priority_weights = {
            "high_attempts": 3,    # Many failed attempts
            "recent_error": 2,     # Recently missed
            "never_correct": 4     # Never answered correctly
        }
    
    def add_item(self, item: Dict, priority: str = "normal"):
        """Add item to review queue with priority"""
        item["priority"] = self.priority_weights.get(priority, 1)
        item["added_at"] = datetime.now().isoformat()
        self.queue.append(item)
        self._sort_queue()
    
    def _sort_queue(self):
        """Sort queue by priority and recency"""
        self.queue.sort(key=lambda x: (-x["priority"], x["added_at"]))
    
    def get_next_item(self) -> Optional[Dict]:
        """Get next item for review"""
        if self.queue:
            return self.queue.pop(0)
        return None
    
    def get_queue_size(self) -> int:
        """Get number of items in queue"""
        return len(self.queue)
    
    def clear_queue(self):
        """Clear the review queue"""
        self.queue = []