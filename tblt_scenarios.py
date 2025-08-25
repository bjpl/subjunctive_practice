"""
Task-Based Language Teaching (TBLT) scenarios for subjunctive practice
Following Willis & Willis (2007) framework: Pre-task → Task Cycle → Language Focus
"""

from typing import Dict, List, Tuple
import random

# Real-world communicative scenarios requiring subjunctive
TBLT_SCENARIOS = {
    "workplace": {
        "title": "Professional Communication",
        "contexts": [
            {
                "situation": "You're a team leader giving feedback to an employee",
                "pre_task": "Think about constructive criticism in a professional setting",
                "task": "Express recommendations for improvement",
                "functional_language": ["sugiero que", "es importante que", "recomiendo que"],
                "example_prompts": [
                    "Suggest they improve their presentation skills",
                    "Recommend they arrive earlier to meetings",
                    "Express hope they'll take on more responsibilities"
                ]
            },
            {
                "situation": "You're negotiating a business deal",
                "pre_task": "Consider conditions and requirements in negotiations",
                "task": "Set conditions for agreement",
                "functional_language": ["con tal de que", "a menos que", "para que"],
                "example_prompts": [
                    "You'll sign the contract provided that...",
                    "The deal works unless...",
                    "We need guarantees so that..."
                ]
            }
        ]
    },
    "social": {
        "title": "Social Interactions",
        "contexts": [
            {
                "situation": "Planning a surprise party for a friend",
                "pre_task": "Think about organizing events and coordinating people",
                "task": "Give instructions and express desires for the party",
                "functional_language": ["quiero que", "es necesario que", "antes de que"],
                "example_prompts": [
                    "Tell someone to buy decorations",
                    "Express what you want the party to be like",
                    "Coordinate timing before the friend arrives"
                ]
            },
            {
                "situation": "Giving advice to a friend with relationship problems",
                "pre_task": "Consider how to give sensitive advice",
                "task": "Express opinions and recommendations tactfully",
                "functional_language": ["dudo que", "no creo que", "te aconsejo que"],
                "example_prompts": [
                    "Express doubt about their partner's intentions",
                    "Suggest they talk things through",
                    "Recommend they seek counseling"
                ]
            }
        ]
    },
    "travel": {
        "title": "Travel & Tourism",
        "contexts": [
            {
                "situation": "You're a tour guide giving safety instructions",
                "pre_task": "Think about safety concerns in tourism",
                "task": "Express rules and precautions",
                "functional_language": ["es prohibido que", "eviten que", "en caso de que"],
                "example_prompts": [
                    "Tell tourists not to wander off alone",
                    "Explain emergency procedures",
                    "Set expectations for the tour"
                ]
            },
            {
                "situation": "Making hotel complaints and requests",
                "pre_task": "Consider service issues and how to address them politely",
                "task": "Express dissatisfaction and request solutions",
                "functional_language": ["exijo que", "preferiría que", "molesta que"],
                "example_prompts": [
                    "Complain about room cleanliness",
                    "Request a room change",
                    "Express preferences for services"
                ]
            }
        ]
    },
    "health": {
        "title": "Health & Wellness",
        "contexts": [
            {
                "situation": "Doctor giving medical advice to a patient",
                "pre_task": "Think about health recommendations and lifestyle changes",
                "task": "Give medical recommendations and express concerns",
                "functional_language": ["es crucial que", "temo que", "evite que"],
                "example_prompts": [
                    "Recommend dietary changes",
                    "Express concern about symptoms",
                    "Prescribe preventive measures"
                ]
            }
        ]
    },
    "education": {
        "title": "Academic Settings",
        "contexts": [
            {
                "situation": "Teacher providing feedback on student work",
                "pre_task": "Consider constructive academic feedback",
                "task": "Express expectations and suggestions for improvement",
                "functional_language": ["espero que", "es fundamental que", "cuando + subjunctive"],
                "example_prompts": [
                    "Express hope for future improvement",
                    "Set requirements for passing",
                    "Explain what to do when revising"
                ]
            }
        ]
    }
}

# Indicative vs Subjunctive contrast exercises
MOOD_CONTRAST_EXERCISES = [
    {
        "context": "Certainty vs Doubt",
        "indicative_triggers": ["sé que", "es obvio que", "es verdad que", "estoy seguro de que"],
        "subjunctive_triggers": ["dudo que", "no creo que", "es posible que", "no estoy seguro de que"],
        "base_sentence": "él tiene razón",
        "explanation": "Use indicative for certainty, subjunctive for doubt/uncertainty"
    },
    {
        "context": "Existence vs Non-existence",
        "indicative_triggers": ["hay alguien que", "conozco a alguien que", "existe algo que"],
        "subjunctive_triggers": ["no hay nadie que", "busco a alguien que", "no existe nada que"],
        "base_sentence": "puede ayudarnos",
        "explanation": "Use indicative for known/existing, subjunctive for unknown/non-existent"
    },
    {
        "context": "Habitual vs Future/Hypothetical",
        "indicative_triggers": ["siempre que", "cada vez que"],
        "subjunctive_triggers": ["cuando (future)", "en cuanto", "tan pronto como"],
        "base_sentence": "llegamos/lleguemos a casa",
        "explanation": "Use indicative for habitual actions, subjunctive for future events"
    }
]

# Spaced repetition intervals (in minutes for practice, days for real implementation)
SPACED_REPETITION_INTERVALS = [1, 5, 25, 120, 600, 3000]  # Based on SM-2 algorithm

class TBLTTaskGenerator:
    """Generate TBLT-based subjunctive practice tasks"""
    
    @staticmethod
    def generate_scenario_task(difficulty: str = "Intermediate") -> Dict:
        """Generate a complete TBLT task with pre-task, task, and language focus"""
        
        # Select random scenario category
        category = random.choice(list(TBLT_SCENARIOS.keys()))
        scenario_group = TBLT_SCENARIOS[category]
        context = random.choice(scenario_group["contexts"])
        
        # Adjust complexity based on difficulty
        complexity_modifiers = {
            "Beginner": {
                "vocab_level": "basic",
                "sentence_length": "short",
                "tense_variety": ["Present Subjunctive"],
                "support": "high"
            },
            "Intermediate": {
                "vocab_level": "varied",
                "sentence_length": "medium",
                "tense_variety": ["Present Subjunctive", "Imperfect Subjunctive"],
                "support": "moderate"
            },
            "Advanced": {
                "vocab_level": "sophisticated",
                "sentence_length": "complex",
                "tense_variety": ["All subjunctive tenses"],
                "support": "minimal"
            }
        }
        
        modifier = complexity_modifiers.get(difficulty, complexity_modifiers["Intermediate"])
        
        # Create task structure
        task = {
            "category": scenario_group["title"],
            "situation": context["situation"],
            "pre_task": {
                "instruction": context["pre_task"],
                "vocabulary_prep": context["functional_language"],
                "brainstorm": f"List 3 things you might need to express in this situation"
            },
            "task_cycle": {
                "task": context["task"],
                "prompt": random.choice(context["example_prompts"]),
                "planning_time": "30 seconds to plan your response",
                "performance": "Complete the communicative task using appropriate subjunctive forms"
            },
            "language_focus": {
                "analysis": "Identify the subjunctive triggers in your response",
                "practice": "Create two more similar expressions",
                "complexity": modifier
            }
        }
        
        return task
    
    @staticmethod
    def generate_contrast_exercise() -> Dict:
        """Generate indicative vs subjunctive contrast exercise"""
        
        exercise = random.choice(MOOD_CONTRAST_EXERCISES)
        
        # Create both versions
        ind_trigger = random.choice(exercise["indicative_triggers"])
        subj_trigger = random.choice(exercise["subjunctive_triggers"])
        
        return {
            "type": "mood_contrast",
            "context": exercise["context"],
            "sentence_pairs": [
                {
                    "trigger": ind_trigger,
                    "base": exercise["base_sentence"],
                    "mood": "indicative",
                    "complete": f"{ind_trigger} {exercise['base_sentence']}"
                },
                {
                    "trigger": subj_trigger,
                    "base": exercise["base_sentence"],
                    "mood": "subjunctive",
                    "complete": f"{subj_trigger} {exercise['base_sentence']}"
                }
            ],
            "explanation": exercise["explanation"],
            "task": "Choose the correct mood for each context"
        }

class SpacedRepetitionTracker:
    """Track and schedule review based on spaced repetition"""
    
    def __init__(self):
        self.item_history = {}  # Track performance history for each item
        self.review_schedule = {}  # When to review each item next
    
    def calculate_next_interval(self, item_id: str, correct: bool, difficulty: float = 2.5) -> int:
        """Calculate next review interval using SM-2 algorithm"""
        
        if item_id not in self.item_history:
            self.item_history[item_id] = {
                "repetitions": 0,
                "ease_factor": 2.5,
                "interval": 1
            }
        
        history = self.item_history[item_id]
        
        if correct:
            if history["repetitions"] == 0:
                history["interval"] = 1
            elif history["repetitions"] == 1:
                history["interval"] = 6
            else:
                history["interval"] = round(history["interval"] * history["ease_factor"])
            
            history["repetitions"] += 1
            
            # Adjust ease factor
            history["ease_factor"] = max(1.3, history["ease_factor"] + (0.1 - (3 - difficulty) * (0.08 + (3 - difficulty) * 0.02)))
        else:
            history["repetitions"] = 0
            history["interval"] = 1
            history["ease_factor"] = max(1.3, history["ease_factor"] - 0.2)
        
        return history["interval"]
    
    def get_items_for_review(self, current_time: int) -> List[str]:
        """Get items that are due for review"""
        due_items = []
        for item_id, next_review in self.review_schedule.items():
            if current_time >= next_review:
                due_items.append(item_id)
        return due_items

# Pedagogical feedback templates
PEDAGOGICAL_FEEDBACK = {
    "correct": {
        "beginner": [
            "¡Excelente! Has usado el subjuntivo correctamente en este contexto comunicativo.",
            "¡Muy bien! Tu respuesta cumple la función comunicativa perfectamente.",
            "¡Correcto! Has completado la tarea con éxito."
        ],
        "intermediate": [
            "Buen uso del subjuntivo en esta situación. Nota cómo el contexto requiere expresar {function}.",
            "Correcto. Has identificado bien que esta situación communicativa necesita el subjuntivo.",
            "Excelente aplicación del subjuntivo para {function}."
        ],
        "advanced": [
            "Uso sofisticado del subjuntivo. Tu respuesta demuestra comprensión profunda del contexto pragmático.",
            "Perfecto. Has navegado la complejidad de esta tarea comunicativa con precisión.",
            "Excelente manejo de los matices del subjuntivo en este contexto."
        ]
    },
    "incorrect": {
        "beginner": [
            "Recuerda: en esta situación necesitas expresar {function}, lo cual requiere subjuntivo.",
            "Piensa en la función comunicativa: ¿estás expresando certeza o duda/deseo/emoción?",
            "Revisa el contexto: esta situación pide que uses el subjuntivo porque {reason}."
        ],
        "intermediate": [
            "Considera el contexto comunicativo: {explanation}. Esto requiere {correct_mood}.",
            "Analiza la función: cuando expresas {function}, necesitas usar {correct_form}.",
            "Recuerda la distinción: {mood_explanation}."
        ],
        "advanced": [
            "Matiz importante: en este registro y contexto, la forma apropiada sería {correct_form} porque {pragmatic_reason}.",
            "Considera las implicaciones pragmáticas: {detailed_explanation}.",
            "La sutileza aquí es que {advanced_explanation}."
        ]
    }
}

def get_pedagogical_feedback(correct: bool, level: str, function: str = "", reason: str = "") -> str:
    """Generate pedagogically-informed feedback"""
    feedback_pool = PEDAGOGICAL_FEEDBACK["correct" if correct else "incorrect"][level.lower()]
    feedback = random.choice(feedback_pool)
    
    # Replace placeholders
    feedback = feedback.replace("{function}", function)
    feedback = feedback.replace("{reason}", reason)
    
    return feedback