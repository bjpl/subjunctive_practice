"""
AI Service Demo Script

Demonstrates how to use the Claude AI service in the Spanish Subjunctive Practice app.
This is a standalone example that can be run to test the AI service functionality.

Requirements:
- Set ANTHROPIC_API_KEY in your .env file
- Ensure anthropic package is installed: pip install anthropic

Usage:
    python examples/ai_service_demo.py
"""

import asyncio
import sys
from pathlib import Path

# Add backend to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.ai_service import get_ai_service, AIServiceUnavailableError


async def demo_feedback_generation():
    """Demo: Generate personalized feedback for exercise answers."""
    print("\n" + "="*70)
    print("DEMO 1: Personalized Feedback Generation")
    print("="*70)

    ai_service = get_ai_service()

    if not ai_service.is_enabled:
        print("⚠️  AI service is not enabled. Set ANTHROPIC_API_KEY in .env file.")
        return

    # Example 1: Correct answer
    print("\n📝 Example 1: Correct Answer")
    print("-" * 50)

    exercise_context = {
        "verb": "hablar",
        "tense": "present_subjunctive",
        "person": "yo",
        "trigger": "Es importante que",
        "sentence": "Es importante que yo ___ español en clase"
    }

    print(f"Sentence: {exercise_context['sentence']}")
    print(f"User answer: 'hable'")
    print(f"Correct answer: 'hable'")
    print("\nGenerating AI feedback...")

    try:
        feedback = await ai_service.generate_feedback(
            user_answer="hable",
            correct_answer="hable",
            exercise_context=exercise_context
        )
        print(f"\n💬 AI Feedback:\n{feedback}")
    except AIServiceUnavailableError as e:
        print(f"❌ Error: {e}")

    # Example 2: Incorrect answer
    print("\n\n📝 Example 2: Incorrect Answer")
    print("-" * 50)

    print(f"Sentence: {exercise_context['sentence']}")
    print(f"User answer: 'hablo' (indicative - wrong!)")
    print(f"Correct answer: 'hable' (subjunctive)")
    print("\nGenerating AI feedback...")

    try:
        feedback = await ai_service.generate_feedback(
            user_answer="hablo",
            correct_answer="hable",
            exercise_context=exercise_context
        )
        print(f"\n💬 AI Feedback:\n{feedback}")
    except AIServiceUnavailableError as e:
        print(f"❌ Error: {e}")


async def demo_learning_insights():
    """Demo: Generate learning insights from user statistics."""
    print("\n\n" + "="*70)
    print("DEMO 2: Learning Insights Generation")
    print("="*70)

    ai_service = get_ai_service()

    if not ai_service.is_enabled:
        print("⚠️  AI service is not enabled.")
        return

    # Simulated user statistics
    user_stats = {
        "total_exercises": 150,
        "accuracy": 0.72,
        "total_study_time_minutes": 300,
        "total_sessions": 15,
        "verbs_mastered": 12,
        "verbs_learning": 8
    }

    weak_areas = [
        {"area": "imperfect_subjunctive", "accuracy": 0.55},
        {"area": "irregular_verbs", "accuracy": 0.60},
        {"area": "stem_changing_verbs", "accuracy": 0.65}
    ]

    print("\n📊 User Statistics:")
    print(f"  - Total exercises: {user_stats['total_exercises']}")
    print(f"  - Overall accuracy: {user_stats['accuracy']:.0%}")
    print(f"  - Study time: {user_stats['total_study_time_minutes']} minutes")
    print(f"  - Sessions: {user_stats['total_sessions']}")

    print("\n📉 Weak Areas:")
    for area in weak_areas:
        print(f"  - {area['area']}: {area['accuracy']:.0%} accuracy")

    print("\n\nGenerating personalized learning insights...")

    try:
        insights = await ai_service.generate_learning_insights(user_stats, weak_areas)

        print(f"\n💡 AI-Generated Insights ({len(insights)} recommendations):\n")
        for i, insight in enumerate(insights, 1):
            print(f"{i}. {insight}\n")

    except AIServiceUnavailableError as e:
        print(f"❌ Error: {e}")


async def demo_personalized_hints():
    """Demo: Generate contextual hints for exercises."""
    print("\n" + "="*70)
    print("DEMO 3: Personalized Hints")
    print("="*70)

    ai_service = get_ai_service()

    if not ai_service.is_enabled:
        print("⚠️  AI service is not enabled.")
        return

    # Example exercise
    exercise = {
        "verb": "tener",
        "tense": "present_subjunctive",
        "person": "nosotros",
        "trigger": "Es posible que",
        "sentence": "Es posible que nosotros ___ tiempo mañana"
    }

    # Simulated user history showing they struggle with stem changes
    user_history = [
        {"verb": "tener", "error_type": "stem_change_missed"},
        {"verb": "venir", "error_type": "stem_change_missed"},
        {"verb": "hacer", "error_type": "irregular_yo_form"}
    ]

    print("\n📝 Exercise:")
    print(f"  Sentence: {exercise['sentence']}")
    print(f"  Verb: {exercise['verb']} ({exercise['tense']})")
    print(f"  Person: {exercise['person']}")
    print(f"  Trigger: {exercise['trigger']}")

    print("\n📜 User's Recent Errors:")
    for error in user_history:
        print(f"  - {error['verb']}: {error['error_type']}")

    print("\n\nGenerating personalized hint...")

    try:
        hint = await ai_service.generate_personalized_hint(exercise, user_history)
        print(f"\n💡 AI Hint:\n{hint}")

    except AIServiceUnavailableError as e:
        print(f"❌ Error: {e}")


async def demo_batch_operations():
    """Demo: Generate feedback for multiple exercises in parallel."""
    print("\n\n" + "="*70)
    print("DEMO 4: Batch Feedback Generation")
    print("="*70)

    ai_service = get_ai_service()

    if not ai_service.is_enabled:
        print("⚠️  AI service is not enabled.")
        return

    # Multiple feedback requests
    feedback_requests = [
        {
            "user_answer": "hable",
            "correct_answer": "hable",
            "exercise_context": {
                "verb": "hablar",
                "tense": "present_subjunctive",
                "sentence": "Espero que yo hable bien"
            }
        },
        {
            "user_answer": "comiera",
            "correct_answer": "coma",
            "exercise_context": {
                "verb": "comer",
                "tense": "present_subjunctive",
                "sentence": "Quiero que él coma verduras"
            }
        },
        {
            "user_answer": "viva",
            "correct_answer": "viva",
            "exercise_context": {
                "verb": "vivir",
                "tense": "present_subjunctive",
                "sentence": "Es bueno que ella viva cerca"
            }
        }
    ]

    print(f"\n📦 Processing {len(feedback_requests)} exercises in parallel...")

    for i, req in enumerate(feedback_requests, 1):
        print(f"\n  {i}. {req['exercise_context']['sentence']}")
        print(f"     User: '{req['user_answer']}' | Correct: '{req['correct_answer']}'")

    print("\n\nGenerating batch feedback...")

    try:
        import time
        start_time = time.time()

        results = await ai_service.batch_generate_feedback(feedback_requests)

        elapsed = time.time() - start_time

        print(f"\n✅ Generated {len(results)} feedback messages in {elapsed:.2f}s")
        print("\n📬 Results:\n")

        for i, feedback in enumerate(results, 1):
            print(f"{i}. {feedback}\n")

    except AIServiceUnavailableError as e:
        print(f"❌ Error: {e}")


async def demo_health_check():
    """Demo: Check AI service health."""
    print("\n" + "="*70)
    print("DEMO 5: Health Check")
    print("="*70)

    ai_service = get_ai_service()

    print("\n🏥 Performing health check...")

    health = await ai_service.health_check()

    print(f"\nStatus: {health['status'].upper()}")
    print(f"Configured: {health['configured']}")

    if health['status'] == 'healthy':
        print(f"Model: {health.get('model', 'N/A')}")
        print(f"Cache size: {health.get('cache_size', 0)} entries")
        print(f"Test response: {health.get('test_response', 'N/A')[:50]}...")
    elif health['status'] == 'disabled':
        print(f"Message: {health.get('message', 'N/A')}")
    else:
        print(f"Error: {health.get('error', 'Unknown error')}")


async def demo_caching():
    """Demo: Response caching behavior."""
    print("\n\n" + "="*70)
    print("DEMO 6: Response Caching")
    print("="*70)

    ai_service = get_ai_service()

    if not ai_service.is_enabled:
        print("⚠️  AI service is not enabled.")
        return

    exercise_context = {
        "verb": "ser",
        "tense": "present_subjunctive",
        "sentence": "Es necesario que yo sea honesto"
    }

    print("\n🔄 Making first request (will hit API)...")

    import time
    start_time = time.time()

    try:
        feedback1 = await ai_service.generate_feedback(
            "sea", "sea", exercise_context
        )
        time1 = time.time() - start_time

        print(f"✅ First request completed in {time1:.2f}s")
        print(f"Response: {feedback1[:100]}...")

        print("\n\n🔄 Making identical second request (should use cache)...")

        start_time = time.time()
        feedback2 = await ai_service.generate_feedback(
            "sea", "sea", exercise_context
        )
        time2 = time.time() - start_time

        print(f"✅ Second request completed in {time2:.2f}s")
        print(f"Response: {feedback2[:100]}...")

        print(f"\n📊 Performance:")
        print(f"  - First request: {time1:.2f}s")
        print(f"  - Cached request: {time2:.2f}s")
        print(f"  - Speed improvement: {(time1 / time2):.1f}x faster")
        print(f"  - Responses identical: {feedback1 == feedback2}")

    except AIServiceUnavailableError as e:
        print(f"❌ Error: {e}")


async def main():
    """Run all demos."""
    print("\n" + "="*70)
    print("  CLAUDE AI SERVICE DEMONSTRATION")
    print("  Spanish Subjunctive Practice Application")
    print("="*70)

    # Check if service is available
    ai_service = get_ai_service()

    if not ai_service.is_enabled:
        print("\n⚠️  WARNING: AI service is not configured!")
        print("    Set ANTHROPIC_API_KEY in your .env file to enable AI features.")
        print("\n    Example:")
        print("    ANTHROPIC_API_KEY=sk-ant-your-api-key-here")
        print("\n    Demos will show fallback behavior.\n")

    # Run all demos
    await demo_feedback_generation()
    await demo_learning_insights()
    await demo_personalized_hints()
    await demo_batch_operations()
    await demo_health_check()
    await demo_caching()

    # Final stats
    print("\n\n" + "="*70)
    print("  DEMO COMPLETE")
    print("="*70)

    if ai_service.is_enabled:
        cache_size = len(ai_service._cache)
        print(f"\n📊 Final Statistics:")
        print(f"  - Cache entries: {cache_size}")
        print(f"  - AI service status: Enabled")
        print(f"  - Model: {ai_service._client is not None}")

        if cache_size > 0:
            print(f"\n🧹 Clearing cache...")
            cleared = ai_service.clear_cache()
            print(f"   Cleared {cleared} entries")

    print("\n✅ All demos completed successfully!\n")


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
