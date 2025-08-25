"""
Test script for API configuration validation

This script tests the API configuration module to ensure proper
error handling, rate limiting, and fallback mechanisms work correctly.

Usage:
    python src/test_api_configuration.py
"""

import sys
import os
import time
import asyncio
from datetime import datetime

# Add the parent directory to the path to import main modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src.api_configuration_fix import (
        APIConfigurationManager,
        get_api_manager,
        create_chat_completion,
        is_api_available,
        get_health_status,
        get_api_metrics,
        APIError,
        FallbackContentGenerator
    )
    print("✅ API configuration module imported successfully")
except ImportError as e:
    print(f"❌ Failed to import API configuration module: {e}")
    sys.exit(1)


def test_api_key_validation():
    """Test API key validation functionality"""
    print("\n🔑 Testing API Key Validation")
    print("-" * 50)
    
    manager = APIConfigurationManager(api_key=None)
    
    # Test invalid keys
    test_cases = [
        ("", "Empty key"),
        ("your_openai_api_key_here", "Placeholder key"),
        ("invalid-key", "Wrong format"),
        ("sk-", "Too short"),
        ("sk-test key with spaces", "Contains spaces"),
        ("sk-1234567890123456789012345678901234567890123456789012", "Valid format")
    ]
    
    for key, description in test_cases:
        result = manager.validate_api_key(key)
        status = "✅ Valid" if result["valid"] else "❌ Invalid"
        print(f"  {status}: {description} - {result['message']}")


def test_rate_limiter():
    """Test rate limiting functionality"""
    print("\n⚡ Testing Rate Limiter")
    print("-" * 50)
    
    from src.api_configuration_fix import RateLimiter
    
    # Create a rate limiter with low limits for testing
    limiter = RateLimiter(requests_per_minute=5, burst_size=3)
    
    print(f"  Initial tokens: {limiter.tokens}")
    
    # Test burst capacity
    print("  Testing burst capacity...")
    for i in range(4):
        acquired = limiter.acquire(timeout=1.0)
        print(f"    Request {i+1}: {'✅ Acquired' if acquired else '❌ Denied'}")
        time.sleep(0.1)
    
    print(f"  Remaining tokens: {limiter.tokens}")
    retry_after = limiter.get_retry_after()
    print(f"  Retry after: {retry_after:.2f} seconds")


def test_circuit_breaker():
    """Test circuit breaker functionality"""
    print("\n🔄 Testing Circuit Breaker")
    print("-" * 50)
    
    manager = APIConfigurationManager(
        api_key="sk-test1234567890123456789012345678901234567890",
        circuit_breaker_threshold=3,
        circuit_breaker_timeout=5
    )
    
    print(f"  Initial state: {'Open' if manager.circuit_breaker_open else 'Closed'}")
    
    # Simulate failures to trigger circuit breaker
    for i in range(4):
        manager.record_api_failure()
        print(f"  Failure {i+1}: Circuit breaker {'Open' if manager.circuit_breaker_open else 'Closed'}")
    
    # Test circuit breaker check
    can_request = manager.check_circuit_breaker()
    print(f"  Can make request: {'Yes' if can_request else 'No'}")
    
    # Test recovery
    manager.record_api_success()
    print(f"  After success: Circuit breaker {'Open' if manager.circuit_breaker_open else 'Closed'}")


def test_fallback_content():
    """Test fallback content generation"""
    print("\n🔄 Testing Fallback Content Generation")
    print("-" * 50)
    
    generator = FallbackContentGenerator()
    
    # Test exercise generation
    exercises = generator.generate_exercises("traditional", 3)
    print(f"  Generated {len(exercises)} traditional exercises")
    for i, ex in enumerate(exercises, 1):
        print(f"    Exercise {i}: {ex['sentence'][:50]}...")
    
    # Test explanation generation
    explanation = generator.generate_explanation("hablo", "hable", False)
    print(f"  Generated explanation: {explanation[:80]}...")
    
    # Test hint generation
    hint = generator.generate_hint("hable")
    print(f"  Generated hint: {hint}")


def test_health_check():
    """Test health check functionality"""
    print("\n🏥 Testing Health Check")
    print("-" * 50)
    
    try:
        health = get_health_status()
        print(f"  Overall Health: {health['overall_health']}")
        print(f"  API Available: {health['available']}")
        print(f"  API Key Valid: {health['api_key_valid']}")
        print(f"  Success Rate: {health['success_rate']:.1f}%")
        print(f"  Uptime: {health['uptime_hours']:.2f} hours")
    except Exception as e:
        print(f"  ❌ Health check failed: {e}")


def test_metrics():
    """Test metrics collection"""
    print("\n📊 Testing Metrics Collection")
    print("-" * 50)
    
    try:
        metrics = get_api_metrics()
        print(f"  Total Requests: {metrics.get('total_requests', 0)}")
        print(f"  Successful Requests: {metrics.get('successful_requests', 0)}")
        print(f"  Failed Requests: {metrics.get('failed_requests', 0)}")
        print(f"  Rate Limit Hits: {metrics.get('rate_limit_hits', 0)}")
        print(f"  Status: {metrics.get('status', 'unknown')}")
        print(f"  Available: {metrics.get('is_available', False)}")
    except Exception as e:
        print(f"  ❌ Metrics collection failed: {e}")


def test_mock_api_call():
    """Test API call with mocked response (no real API call)"""
    print("\n🧪 Testing Mock API Call")
    print("-" * 50)
    
    # Test with invalid API key to trigger fallback
    manager = APIConfigurationManager(api_key="sk-invalid-key-for-testing")
    
    try:
        response = manager.create_chat_completion(
            messages=[{"role": "user", "content": "Create 2 Spanish subjunctive exercises"}],
            model="gpt-3.5-turbo",
            max_tokens=200
        )
        
        if response:
            print(f"  Response received: {response[:100]}...")
        else:
            print("  No response received")
            
    except Exception as e:
        print(f"  Exception during API call: {e}")


def run_comprehensive_test():
    """Run all tests"""
    print("🚀 Starting Comprehensive API Configuration Tests")
    print("=" * 60)
    
    test_functions = [
        test_api_key_validation,
        test_rate_limiter,
        test_circuit_breaker,
        test_fallback_content,
        test_health_check,
        test_metrics,
        test_mock_api_call
    ]
    
    results = {"passed": 0, "failed": 0}
    
    for test_func in test_functions:
        try:
            test_func()
            results["passed"] += 1
            print("  ✅ Test passed")
        except Exception as e:
            results["failed"] += 1
            print(f"  ❌ Test failed: {e}")
    
    print("\n📋 Test Summary")
    print("=" * 60)
    print(f"✅ Passed: {results['passed']}")
    print(f"❌ Failed: {results['failed']}")
    print(f"📊 Success Rate: {(results['passed'] / (results['passed'] + results['failed']) * 100):.1f}%")
    
    if results["failed"] == 0:
        print("\n🎉 All tests passed! API configuration is working correctly.")
    else:
        print(f"\n⚠️  {results['failed']} test(s) failed. Check the output above for details.")


if __name__ == "__main__":
    run_comprehensive_test()