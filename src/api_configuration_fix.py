"""
OpenAI API Configuration and Error Handling Module

This module provides robust API configuration, error handling, rate limiting, 
and fallback mechanisms for OpenAI API integration.

Author: Backend API Developer
Version: 1.0.0
"""

import os
import time
import json
import logging
import hashlib
from typing import Dict, List, Optional, Union, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import threading
from functools import wraps
import random

try:
    from openai import OpenAI
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    OpenAI = None
    openai = None

from dotenv import load_dotenv


class APIError(Exception):
    """Custom API error class"""
    def __init__(self, message: str, error_type: str = "generic", retry_after: Optional[int] = None):
        super().__init__(message)
        self.error_type = error_type
        self.retry_after = retry_after


class APIStatus(Enum):
    """API status enumeration"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"
    RATE_LIMITED = "rate_limited"
    AUTHENTICATION_FAILED = "auth_failed"


@dataclass
class APIMetrics:
    """API performance metrics"""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    rate_limit_hits: int = 0
    average_response_time: float = 0.0
    last_request_time: Optional[datetime] = None
    last_error: Optional[str] = None
    uptime_start: datetime = None
    
    def __post_init__(self):
        if self.uptime_start is None:
            self.uptime_start = datetime.now()
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate percentage"""
        if self.total_requests == 0:
            return 0.0
        return (self.successful_requests / self.total_requests) * 100
    
    @property
    def uptime_duration(self) -> timedelta:
        """Calculate uptime duration"""
        return datetime.now() - self.uptime_start


class RateLimiter:
    """Token bucket rate limiter for API requests"""
    
    def __init__(self, requests_per_minute: int = 60, burst_size: int = 10):
        self.requests_per_minute = requests_per_minute
        self.burst_size = burst_size
        self.tokens = burst_size
        self.last_refill = time.time()
        self.lock = threading.Lock()
        self.request_times = []  # Track request times for sliding window
    
    def acquire(self, timeout: Optional[float] = None) -> bool:
        """
        Acquire permission to make a request
        
        Args:
            timeout: Maximum time to wait for permission (seconds)
        
        Returns:
            bool: True if permission granted, False if timeout
        """
        start_time = time.time()
        
        while True:
            with self.lock:
                now = time.time()
                
                # Refill tokens based on time elapsed
                time_passed = now - self.last_refill
                tokens_to_add = time_passed * (self.requests_per_minute / 60.0)
                self.tokens = min(self.burst_size, self.tokens + tokens_to_add)
                self.last_refill = now
                
                # Clean old request times (sliding window)
                cutoff_time = now - 60.0  # 1 minute window
                self.request_times = [t for t in self.request_times if t > cutoff_time]
                
                # Check if we can make a request
                if (self.tokens >= 1.0 and 
                    len(self.request_times) < self.requests_per_minute):
                    self.tokens -= 1.0
                    self.request_times.append(now)
                    return True
                
                # Check timeout
                if timeout and (now - start_time) >= timeout:
                    return False
                
                # Calculate wait time
                if self.tokens < 1.0:
                    wait_time = (1.0 - self.tokens) * (60.0 / self.requests_per_minute)
                else:
                    wait_time = max(0, (self.request_times[0] + 60.0 - now))
                
                wait_time = min(0.1, wait_time)  # Don't wait too long in tight loops
            
            time.sleep(wait_time)
    
    def get_retry_after(self) -> float:
        """Get recommended wait time before next request"""
        with self.lock:
            now = time.time()
            if self.tokens >= 1.0 and len(self.request_times) < self.requests_per_minute:
                return 0.0
            
            if self.tokens < 1.0:
                return (1.0 - self.tokens) * (60.0 / self.requests_per_minute)
            else:
                return max(0, (self.request_times[0] + 60.0 - now))


class FallbackContentGenerator:
    """Generates fallback content when API is unavailable"""
    
    # Predefined exercise templates for different categories
    EXERCISE_TEMPLATES = {
        "traditional": [
            {
                "context": "Expressing doubt",
                "sentence": "No creo que él _____ (venir) mañana.",
                "answer": "venga",
                "choices": ["viene", "venga", "viniera", "vino"],
                "translation": "I don't think he will come tomorrow."
            },
            {
                "context": "Expressing emotion", 
                "sentence": "Me alegra que tú _____ (estar) aquí.",
                "answer": "estés",
                "choices": ["estás", "estés", "estarás", "estabas"],
                "translation": "I'm happy that you are here."
            }
        ],
        "tblt": [
            {
                "context": "Restaurant scenario",
                "sentence": "Busco un restaurante que _____ (servir) comida vegana.",
                "answer": "sirva",
                "choices": ["sirve", "sirva", "sirviera", "servirá"],
                "translation": "I'm looking for a restaurant that serves vegan food."
            }
        ],
        "contrast": [
            {
                "context": "Indicative vs Subjunctive",
                "sentence": "Sé que María _____ (trabajar) mucho vs. Dudo que María _____ mucho.",
                "answer": "trabaje",
                "choices": ["trabaja", "trabaje", "trabajara", "trabajó"],
                "translation": "I know Maria works a lot vs. I doubt Maria works a lot."
            }
        ]
    }
    
    @classmethod
    def generate_exercises(cls, exercise_type: str = "traditional", count: int = 5) -> List[Dict]:
        """
        Generate fallback exercises when API is unavailable
        
        Args:
            exercise_type: Type of exercises (traditional, tblt, contrast)
            count: Number of exercises to generate
        
        Returns:
            List of exercise dictionaries
        """
        templates = cls.EXERCISE_TEMPLATES.get(exercise_type, cls.EXERCISE_TEMPLATES["traditional"])
        exercises = []
        
        for i in range(count):
            template = templates[i % len(templates)]
            # Create a copy and modify slightly for variety
            exercise = template.copy()
            exercises.append(exercise)
        
        return exercises
    
    @classmethod
    def generate_explanation(cls, user_answer: str, correct_answer: str, is_correct: bool) -> str:
        """Generate fallback explanations"""
        if is_correct:
            return f"¡Correcto! '{correct_answer}' es la forma correcta del subjuntivo en este contexto."
        else:
            return (f"Incorrecto. La respuesta correcta es '{correct_answer}'. "
                   f"Recuerda que el subjuntivo se usa para expresar duda, emoción, deseo o situaciones hipotéticas.")
    
    @classmethod
    def generate_hint(cls, correct_answer: str) -> str:
        """Generate fallback hints"""
        hints = [
            "Piensa en si la situación expresa certeza o incertidumbre.",
            "¿Se trata de una emoción, deseo o duda?",
            "Considera si el verbo principal requiere subjuntivo.",
            "Recuerda las terminaciones del subjuntivo presente."
        ]
        return random.choice(hints)


class APIConfigurationManager:
    """
    Comprehensive OpenAI API configuration and management
    
    Features:
    - API key validation and secure storage
    - Rate limiting and retry logic
    - Error handling and fallback mechanisms
    - Performance monitoring and metrics
    - Circuit breaker pattern for resilience
    """
    
    def __init__(self, 
                 api_key: Optional[str] = None,
                 requests_per_minute: int = 60,
                 max_retries: int = 3,
                 initial_retry_delay: float = 1.0,
                 max_retry_delay: float = 60.0,
                 circuit_breaker_threshold: int = 5,
                 circuit_breaker_timeout: int = 300):
        """
        Initialize API configuration manager
        
        Args:
            api_key: OpenAI API key (if None, will try to load from environment)
            requests_per_minute: Rate limit for requests
            max_retries: Maximum number of retries for failed requests
            initial_retry_delay: Initial delay between retries (seconds)
            max_retry_delay: Maximum delay between retries (seconds)
            circuit_breaker_threshold: Number of failures before opening circuit
            circuit_breaker_timeout: Circuit breaker timeout (seconds)
        """
        # Load environment variables
        load_dotenv()
        
        # API Configuration
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = None
        self.status = APIStatus.UNAVAILABLE
        
        # Rate limiting
        self.rate_limiter = RateLimiter(requests_per_minute=requests_per_minute)
        
        # Retry configuration
        self.max_retries = max_retries
        self.initial_retry_delay = initial_retry_delay
        self.max_retry_delay = max_retry_delay
        
        # Circuit breaker for API resilience
        self.circuit_breaker_threshold = circuit_breaker_threshold
        self.circuit_breaker_timeout = circuit_breaker_timeout
        self.circuit_breaker_failures = 0
        self.circuit_breaker_last_failure = None
        self.circuit_breaker_open = False
        
        # Metrics and monitoring
        self.metrics = APIMetrics()
        self.fallback_generator = FallbackContentGenerator()
        
        # Thread safety
        self.lock = threading.Lock()
        
        # Logging
        self.logger = logging.getLogger(__name__)
        
        # Initialize the API connection
        self.initialize_api()
    
    def validate_api_key(self, api_key: str) -> Dict[str, Union[bool, str]]:
        """
        Validate OpenAI API key format and basic requirements
        
        Args:
            api_key: API key to validate
        
        Returns:
            Dict with validation results
        """
        validation_result = {
            "valid": False,
            "message": "",
            "security_level": "unknown"
        }
        
        if not api_key:
            validation_result["message"] = "API key is empty or None"
            return validation_result
        
        if api_key == "your_openai_api_key_here" or api_key == "YOUR_OPENAI_API_KEY_HERE":
            validation_result["message"] = "API key is placeholder value"
            return validation_result
        
        if not api_key.startswith("sk-"):
            validation_result["message"] = "API key must start with 'sk-'"
            return validation_result
        
        if len(api_key) < 20:
            validation_result["message"] = "API key appears too short"
            return validation_result
        
        # Check for common security issues
        if " " in api_key:
            validation_result["message"] = "API key contains spaces"
            return validation_result
        
        # Basic format validation passed
        validation_result["valid"] = True
        validation_result["message"] = f"API key format valid (length: {len(api_key)})"
        validation_result["security_level"] = "basic"
        
        return validation_result
    
    def initialize_api(self) -> bool:
        """
        Initialize OpenAI API client with proper validation and error handling
        
        Returns:
            bool: True if initialization successful
        """
        try:
            if not OPENAI_AVAILABLE:
                self.logger.error("OpenAI library not available. Install with: pip install openai")
                self.status = APIStatus.UNAVAILABLE
                return False
            
            # Validate API key
            validation = self.validate_api_key(self.api_key)
            if not validation["valid"]:
                self.logger.error(f"API key validation failed: {validation['message']}")
                self.status = APIStatus.AUTHENTICATION_FAILED
                return False
            
            # Initialize client
            self.client = OpenAI(api_key=self.api_key)
            
            # Test the connection with a minimal request
            if self.test_api_connection():
                self.status = APIStatus.HEALTHY
                self.circuit_breaker_failures = 0
                self.circuit_breaker_open = False
                self.logger.info("OpenAI API initialized successfully")
                return True
            else:
                self.status = APIStatus.UNAVAILABLE
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to initialize OpenAI API: {str(e)}")
            self.status = APIStatus.UNAVAILABLE
            return False
    
    def test_api_connection(self) -> bool:
        """
        Test API connection with a minimal request
        
        Returns:
            bool: True if connection successful
        """
        try:
            if not self.client:
                return False
            
            # Make a minimal test request
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=1,
                timeout=10
            )
            
            return response is not None
            
        except openai.AuthenticationError:
            self.logger.error("API authentication failed - check API key")
            self.status = APIStatus.AUTHENTICATION_FAILED
            return False
        except openai.RateLimitError:
            self.logger.warning("API rate limit hit during connection test")
            self.status = APIStatus.RATE_LIMITED
            return True  # Connection works, just rate limited
        except Exception as e:
            self.logger.error(f"API connection test failed: {str(e)}")
            return False
    
    def check_circuit_breaker(self) -> bool:
        """
        Check if circuit breaker is open
        
        Returns:
            bool: True if circuit breaker allows requests
        """
        with self.lock:
            if not self.circuit_breaker_open:
                return True
            
            # Check if timeout has passed
            if (self.circuit_breaker_last_failure and
                datetime.now() - self.circuit_breaker_last_failure > 
                timedelta(seconds=self.circuit_breaker_timeout)):
                
                self.logger.info("Circuit breaker timeout passed, allowing test request")
                return True
            
            return False
    
    def record_api_failure(self):
        """Record an API failure for circuit breaker logic"""
        with self.lock:
            self.circuit_breaker_failures += 1
            self.circuit_breaker_last_failure = datetime.now()
            
            if self.circuit_breaker_failures >= self.circuit_breaker_threshold:
                self.circuit_breaker_open = True
                self.logger.warning(
                    f"Circuit breaker opened after {self.circuit_breaker_failures} failures"
                )
    
    def record_api_success(self):
        """Record an API success for circuit breaker logic"""
        with self.lock:
            if self.circuit_breaker_open:
                self.logger.info("Circuit breaker closed - API recovered")
            
            self.circuit_breaker_failures = 0
            self.circuit_breaker_open = False
    
    def exponential_backoff_delay(self, attempt: int) -> float:
        """
        Calculate exponential backoff delay with jitter
        
        Args:
            attempt: Current attempt number (0-based)
        
        Returns:
            float: Delay in seconds
        """
        delay = min(
            self.initial_retry_delay * (2 ** attempt),
            self.max_retry_delay
        )
        
        # Add jitter to prevent thundering herd
        jitter = random.uniform(0.8, 1.2)
        return delay * jitter
    
    def with_retry(self, func: Callable) -> Callable:
        """
        Decorator to add retry logic to API calls
        
        Args:
            func: Function to wrap with retry logic
        
        Returns:
            Wrapped function with retry logic
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(self.max_retries + 1):
                try:
                    # Check circuit breaker
                    if not self.check_circuit_breaker():
                        raise APIError(
                            "API circuit breaker is open",
                            error_type="circuit_breaker",
                            retry_after=self.circuit_breaker_timeout
                        )
                    
                    # Rate limiting
                    if not self.rate_limiter.acquire(timeout=30):
                        raise APIError(
                            "Rate limit exceeded - timeout waiting for quota",
                            error_type="rate_limit",
                            retry_after=int(self.rate_limiter.get_retry_after())
                        )
                    
                    # Execute the function
                    start_time = time.time()
                    result = func(*args, **kwargs)
                    response_time = time.time() - start_time
                    
                    # Record success metrics
                    self.metrics.successful_requests += 1
                    self.metrics.total_requests += 1
                    self.metrics.last_request_time = datetime.now()
                    
                    # Update average response time
                    if self.metrics.average_response_time == 0:
                        self.metrics.average_response_time = response_time
                    else:
                        self.metrics.average_response_time = (
                            self.metrics.average_response_time * 0.9 + response_time * 0.1
                        )
                    
                    self.record_api_success()
                    return result
                    
                except openai.RateLimitError as e:
                    self.metrics.rate_limit_hits += 1
                    self.status = APIStatus.RATE_LIMITED
                    last_exception = e
                    
                    # Extract retry-after from headers if available
                    retry_after = getattr(e, 'retry_after', None) or 60
                    
                    if attempt < self.max_retries:
                        delay = max(retry_after, self.exponential_backoff_delay(attempt))
                        self.logger.warning(f"Rate limited, retrying in {delay}s (attempt {attempt + 1})")
                        time.sleep(delay)
                    
                except openai.AuthenticationError as e:
                    self.status = APIStatus.AUTHENTICATION_FAILED
                    self.logger.error("Authentication failed - check API key")
                    raise APIError(
                        "Authentication failed - invalid API key",
                        error_type="authentication"
                    )
                
                except openai.APIConnectionError as e:
                    self.status = APIStatus.UNAVAILABLE
                    last_exception = e
                    
                    if attempt < self.max_retries:
                        delay = self.exponential_backoff_delay(attempt)
                        self.logger.warning(f"Connection error, retrying in {delay}s (attempt {attempt + 1})")
                        time.sleep(delay)
                
                except Exception as e:
                    last_exception = e
                    self.logger.error(f"API call failed (attempt {attempt + 1}): {str(e)}")
                    
                    if attempt < self.max_retries:
                        delay = self.exponential_backoff_delay(attempt)
                        time.sleep(delay)
            
            # All retries exhausted
            self.metrics.failed_requests += 1
            self.metrics.total_requests += 1
            self.metrics.last_error = str(last_exception)
            self.record_api_failure()
            
            raise APIError(
                f"API call failed after {self.max_retries + 1} attempts: {str(last_exception)}",
                error_type="max_retries_exceeded"
            )
        
        return wrapper
    
    @property
    def is_available(self) -> bool:
        """Check if API is available for requests"""
        return (self.status in [APIStatus.HEALTHY, APIStatus.DEGRADED] and 
                self.client is not None and 
                not self.circuit_breaker_open)
    
    def get_client(self) -> Optional[OpenAI]:
        """
        Get OpenAI client if available
        
        Returns:
            OpenAI client or None if unavailable
        """
        if self.is_available:
            return self.client
        return None
    
    def create_chat_completion(self, **kwargs) -> Optional[str]:
        """
        Create chat completion with error handling and fallback
        
        Args:
            **kwargs: Arguments for chat completion
        
        Returns:
            Generated text or fallback content
        """
        @self.with_retry
        def _make_request():
            if not self.client:
                raise APIError("API client not initialized", error_type="not_initialized")
            
            # Set reasonable defaults
            kwargs.setdefault("model", "gpt-3.5-turbo")
            kwargs.setdefault("max_tokens", 600)
            kwargs.setdefault("temperature", 0.5)
            kwargs.setdefault("timeout", 30)
            
            response = self.client.chat.completions.create(**kwargs)
            return response.choices[0].message.content.strip()
        
        try:
            return _make_request()
        except APIError as e:
            self.logger.error(f"API request failed: {e}")
            # Return fallback content based on request type
            return self._generate_fallback_response(**kwargs)
    
    def _generate_fallback_response(self, **kwargs) -> str:
        """
        Generate fallback response when API is unavailable
        
        Args:
            **kwargs: Original request parameters
        
        Returns:
            Fallback response string
        """
        messages = kwargs.get("messages", [])
        user_content = ""
        
        # Extract user message
        for message in messages:
            if message.get("role") == "user":
                user_content = message.get("content", "")
                break
        
        # Determine response type based on content
        if "exercise" in user_content.lower() or "json" in user_content.lower():
            exercises = self.fallback_generator.generate_exercises()
            return json.dumps(exercises, ensure_ascii=False)
        elif "hint" in user_content.lower():
            return self.fallback_generator.generate_hint("")
        elif "explanation" in user_content.lower():
            return self.fallback_generator.generate_explanation("", "", True)
        else:
            return "Lo siento, el servicio de IA no está disponible en este momento. Intenta de nuevo más tarde."
    
    def get_metrics(self) -> Dict:
        """
        Get API performance metrics
        
        Returns:
            Dictionary of metrics
        """
        metrics_dict = asdict(self.metrics)
        metrics_dict.update({
            "status": self.status.value,
            "is_available": self.is_available,
            "circuit_breaker_open": self.circuit_breaker_open,
            "circuit_breaker_failures": self.circuit_breaker_failures,
            "rate_limiter_tokens": self.rate_limiter.tokens
        })
        return metrics_dict
    
    def reset_metrics(self):
        """Reset performance metrics"""
        self.metrics = APIMetrics()
        self.logger.info("API metrics reset")
    
    def health_check(self) -> Dict[str, Union[str, bool, float]]:
        """
        Perform comprehensive health check
        
        Returns:
            Health check results
        """
        health_status = {
            "timestamp": datetime.now().isoformat(),
            "status": self.status.value,
            "available": self.is_available,
            "circuit_breaker_open": self.circuit_breaker_open,
            "api_key_valid": bool(self.api_key and self.validate_api_key(self.api_key)["valid"]),
            "openai_library_available": OPENAI_AVAILABLE,
            "success_rate": self.metrics.success_rate,
            "average_response_time": self.metrics.average_response_time,
            "total_requests": self.metrics.total_requests,
            "uptime_hours": self.metrics.uptime_duration.total_seconds() / 3600
        }
        
        # Determine overall health
        if (health_status["available"] and 
            health_status["api_key_valid"] and 
            health_status["success_rate"] > 80):
            health_status["overall_health"] = "healthy"
        elif health_status["success_rate"] > 50:
            health_status["overall_health"] = "degraded" 
        else:
            health_status["overall_health"] = "unhealthy"
        
        return health_status


# Global instance for easy access
_api_manager = None

def get_api_manager() -> APIConfigurationManager:
    """
    Get global API manager instance (singleton pattern)
    
    Returns:
        APIConfigurationManager instance
    """
    global _api_manager
    if _api_manager is None:
        _api_manager = APIConfigurationManager()
    return _api_manager


def initialize_api_manager(**kwargs) -> APIConfigurationManager:
    """
    Initialize global API manager with custom configuration
    
    Args:
        **kwargs: Configuration parameters for APIConfigurationManager
    
    Returns:
        APIConfigurationManager instance
    """
    global _api_manager
    _api_manager = APIConfigurationManager(**kwargs)
    return _api_manager


# Convenience functions for easy integration
def create_chat_completion(**kwargs) -> Optional[str]:
    """Create chat completion using global API manager"""
    return get_api_manager().create_chat_completion(**kwargs)


def get_api_metrics() -> Dict:
    """Get API metrics using global API manager"""
    return get_api_manager().get_metrics()


def is_api_available() -> bool:
    """Check if API is available using global API manager"""
    return get_api_manager().is_available


def get_health_status() -> Dict:
    """Get API health status using global API manager"""
    return get_api_manager().health_check()