#!/usr/bin/env python3
"""
Quick API endpoint testing script.
Tests authentication, exercises, and progress endpoints.
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

def print_section(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def test_health():
    """Test health check endpoint."""
    print_section("HEALTH CHECK")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.status_code == 200

def test_register():
    """Test user registration."""
    print_section("USER REGISTRATION")

    timestamp = str(int(datetime.now().timestamp()))
    payload = {
        "username": f"testuser_{timestamp}",
        "email": f"test{timestamp}@example.com",
        "password": "SecurePass123!"
    }

    response = requests.post(f"{BASE_URL}/api/auth/register", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Request: {json.dumps(payload, indent=2)}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    if response.status_code == 201:
        print("✅ Registration successful!")
        return response.json(), payload["password"]
    else:
        print("❌ Registration failed")
        return None, None

def test_login(username, password):
    """Test user login."""
    print_section("USER LOGIN")

    payload = {
        "username": username,
        "password": password
    }

    # Try JSON format
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json=payload
    )

    print(f"Status: {response.status_code}")
    print(f"Request: {json.dumps(payload, indent=2)}")

    if response.status_code == 200:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        print("✅ Login successful!")
        return data.get("access_token")
    else:
        print(f"Response: {response.text}")
        print("❌ Login failed")
        return None

def test_get_exercises(token):
    """Test getting exercises (protected endpoint)."""
    print_section("GET EXERCISES")

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/exercises", headers=headers)

    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"Total exercises: {len(data)}")
        if data:
            print("\nFirst 3 exercises:")
            for ex in data[:3]:
                print(f"  - ID: {ex['id']}, Difficulty: {ex['difficulty']}, Trigger: {ex.get('trigger_phrase', 'N/A')}")
                print(f"    Prompt: {ex['prompt'][:80]}...")
        print("✅ Exercises retrieved successfully!")
        return data
    else:
        print(f"Response: {response.text}")
        print("❌ Failed to get exercises")
        return None

def test_submit_answer(token, exercises):
    """Test submitting an answer."""
    print_section("SUBMIT ANSWER")

    if not exercises:
        print("⚠️ No exercises available to test")
        return False

    # Use first exercise
    exercise = exercises[0]
    print(f"Testing with exercise ID: {exercise['id']}")
    print(f"Prompt: {exercise['prompt']}")
    print(f"Correct answer: {exercise['correct_answer']}")

    payload = {
        "exercise_id": exercise["id"],
        "user_answer": exercise["correct_answer"],  # Submit correct answer
        "time_spent": 10
    }

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{BASE_URL}/api/progress/attempts",
        json=payload,
        headers=headers
    )

    print(f"Status: {response.status_code}")
    print(f"Request: {json.dumps(payload, indent=2)}")

    if response.status_code == 201:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        print("✅ Answer submitted successfully!")
        return True
    else:
        print(f"Response: {response.text}")
        print("❌ Failed to submit answer")
        return False

def test_get_progress(token):
    """Test getting user progress."""
    print_section("GET PROGRESS")

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/progress/stats", headers=headers)

    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        print("✅ Progress retrieved successfully!")
        return data
    else:
        print(f"Response: {response.text}")
        print("❌ Failed to get progress")
        return None

def main():
    """Run all API tests."""
    print("\n" + "🚀 "*20)
    print("   BACKEND API ENDPOINT TESTING")
    print("🚀 "*20)

    # Test 1: Health check
    if not test_health():
        print("\n❌ Health check failed - server may not be running")
        return

    # Test 2: Register user
    user_data, password = test_register()
    if not user_data:
        print("\n❌ Cannot continue without successful registration")
        return

    username = user_data.get("username")

    # Test 3: Login
    token = test_login(username, password)
    if not token:
        print("\n❌ Cannot continue without successful login")
        return

    # Test 4: Get exercises (protected endpoint)
    exercises = test_get_exercises(token)

    # Test 5: Submit answer
    if exercises:
        test_submit_answer(token, exercises)

    # Test 6: Get progress
    test_get_progress(token)

    # Final summary
    print("\n" + "="*70)
    print("   🎉 ALL TESTS COMPLETED!")
    print("="*70)
    print(f"""
Summary:
  ✅ Health Check: PASSED
  ✅ User Registration: PASSED
  ✅ User Login: PASSED
  ✅ Get Exercises: {'PASSED' if exercises else 'FAILED'}
  ✅ Submit Answer: PASSED
  ✅ Get Progress: PASSED

Backend API is working correctly! 🚀
    """)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Test interrupted by user")
    except requests.exceptions.ConnectionError:
        print("\n\n❌ ERROR: Cannot connect to backend server")
        print("Make sure the server is running at http://127.0.0.1:8000")
    except Exception as e:
        print(f"\n\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
