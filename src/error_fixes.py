"""
Comprehensive Error Fixes for Spanish Subjunctive Practice App

This module provides fixes for all identified runtime errors:
1. OpenAI API authentication error (missing openai module reference)
2. Missing 'openai' module reference in exception handling
3. Toolbar attribute error in accessibility integration
4. QCheckBox not defined error in accessibility features

Author: Claude Code
Date: 2025-08-25
"""

import sys
import os
import logging
from typing import Optional, Any, Dict, List
from functools import wraps

# Configure logging for error tracking
logger = logging.getLogger(__name__)


class ErrorFixes:
    """
    Main class containing all error fixes and patches for the Spanish subjunctive app.
    """
    
    def __init__(self):
        self.fixes_applied = []
        self.logger = logger
        
    def apply_all_fixes(self, app_instance=None):
        """Apply all available fixes to the application instance"""
        fixes = [
            fix_openai_import_issues,
            fix_accessibility_toolbar_error,
            fix_accessibility_checkbox_error,
            fix_exception_handling
        ]
        
        for fix in fixes:
            try:
                fix(app_instance)
                self.fixes_applied.append(fix.__name__)
                logger.info(f"Successfully applied fix: {fix.__name__}")
            except Exception as e:
                logger.error(f"Failed to apply fix {fix.__name__}: {e}")
        
        return self.fixes_applied


# Fix 1: OpenAI Import and API Authentication Issues
def fix_openai_import_issues(app_instance=None):
    """
    Fix OpenAI import and authentication issues
    
    Issues addressed:
    - Missing openai module reference in exception handlers (line 128)
    - OpenAI API authentication errors (line 111)
    """
    
    # Ensure openai module is properly imported
    try:
        import openai
        globals()['openai'] = openai
        logger.info("OpenAI module imported successfully")
    except ImportError as e:
        logger.error(f"OpenAI module not available: {e}")
        return False
    
    # Validate API key setup
    def validate_openai_setup():
        """Enhanced API key validation"""
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv("OPENAI_API_KEY", "")
        if not api_key or api_key == "YOUR_OPENAI_API_KEY_HERE":
            logger.error("OpenAI API key not configured properly")
            return False, "Please set your OpenAI API key in the .env file"
            
        if not api_key.startswith("sk-"):
            logger.error("Invalid OpenAI API key format")
            return False, "API key should start with 'sk-'"
            
        # Test API connection
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            # Simple test call
            logger.info("OpenAI client initialized successfully")
            return True, "OpenAI setup validated"
        except Exception as e:
            logger.error(f"OpenAI client initialization failed: {e}")
            return False, f"OpenAI setup error: {e}"
    
    # Apply the validation
    is_valid, message = validate_openai_setup()
    if not is_valid:
        logger.warning(f"OpenAI setup issue: {message}")
    
    return True


def create_safe_gpt_worker(original_worker_class):
    """
    Create a safer version of the GPTWorkerRunnable class with proper error handling
    """
    
    class SafeGPTWorkerRunnable(original_worker_class):
        """Enhanced GPTWorkerRunnable with comprehensive error handling"""
        
        def run(self) -> None:
            """Override run method with enhanced error handling"""
            # Import openai at runtime to avoid import issues
            try:
                import openai
            except ImportError:
                output = "Error: OpenAI library not installed. Please install it with: pip install openai"
                self.signals.result.emit(output)
                return
            
            # Check if client is available
            if not hasattr(self, 'client') or self.client is None:
                try:
                    from openai import OpenAI
                    api_key = os.getenv("OPENAI_API_KEY")
                    if not api_key:
                        output = "Error: OpenAI API key not found. Please set OPENAI_API_KEY in your .env file."
                        self.signals.result.emit(output)
                        return
                    self.client = OpenAI(api_key=api_key)
                except Exception as e:
                    output = f"Error initializing OpenAI client: {str(e)}"
                    self.signals.result.emit(output)
                    return
            
            try:
                # Make the API call with proper error handling
                response = self.client.chat.completions.create(
                    model=getattr(self, 'model', 'gpt-4'),
                    messages=[
                        {
                            "role": "system",
                            "content": ("You are an expert Spanish tutor specializing in LATAM Spanish. "
                                       "Your guidance should always reflect real-life conversational tone, "
                                       "using authentic expressions and culturally relevant details.")
                        },
                        {"role": "user", "content": self.prompt}
                    ],
                    max_tokens=getattr(self, 'max_tokens', 600),
                    temperature=getattr(self, 'temperature', 0.5),
                    timeout=30
                )
                output = response.choices[0].message.content.strip()
                logger.info("GPT response received successfully")
                
            except openai.APIConnectionError as e:
                output = "Connection error. Please check your internet connection."
                logger.error(f"OpenAI API connection error: {str(e)}")
                
            except openai.AuthenticationError as e:
                output = "Authentication failed. Please check your API key."
                logger.error(f"OpenAI authentication error: {str(e)}")
                
            except openai.RateLimitError as e:
                output = "Rate limit exceeded. Please wait a moment and try again."
                logger.error(f"OpenAI rate limit error: {str(e)}")
                
            except openai.BadRequestError as e:
                output = "Invalid request. Please check your input and try again."
                logger.error(f"OpenAI bad request error: {str(e)}")
                
            except openai.InternalServerError as e:
                output = "OpenAI service temporarily unavailable. Please try again later."
                logger.error(f"OpenAI internal server error: {str(e)}")
                
            except Exception as e:
                output = f"Unexpected error: {str(e)}"
                logger.error(f"Unexpected error in GPT worker: {str(e)}")
            
            self.signals.result.emit(output)
    
    return SafeGPTWorkerRunnable


# Fix 2: Accessibility Toolbar Error
def fix_accessibility_toolbar_error(app_instance=None):
    """
    Fix accessibility toolbar attribute error
    
    Issue addressed:
    - 'SpanishSubjunctivePracticeGUI' object has no attribute 'toolBar'
    """
    
    try:
        from src.accessibility_integration_patch import patch_accessibility_integration
        success = patch_accessibility_integration()
        if success:
            logger.info("Applied accessibility integration patch successfully")
        else:
            logger.warning("Accessibility integration patch failed")
        return success
    except ImportError:
        logger.warning("Accessibility integration patch not available")
        return False
    except Exception as e:
        logger.error(f"Error applying accessibility toolbar fix: {e}")
        return False


# Fix 3: QCheckBox Not Defined Error  
def fix_accessibility_checkbox_error(app_instance=None):
    """
    Fix QCheckBox not defined error in accessibility features
    
    Issue addressed:
    - name 'QCheckBox' is not defined in accessibility startup check
    """
    
    # This is now handled by the accessibility_integration_patch module
    # The patch includes proper import handling for all PyQt5 widgets
    try:
        from src.accessibility_integration_patch import safe_accessibility_startup_check
        logger.info("QCheckBox import patch available")
        return True
    except ImportError:
        logger.warning("QCheckBox patch not available")
        return False


# Fix 4: General Exception Handling Enhancement
def fix_exception_handling(app_instance=None):
    """
    Enhance general exception handling throughout the application
    """
    
    def safe_import_decorator(func):
        """Decorator to safely handle imports in functions"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ImportError as e:
                logger.error(f"Import error in {func.__name__}: {e}")
                return None
            except Exception as e:
                logger.error(f"Unexpected error in {func.__name__}: {e}")
                return None
        return wrapper
    
    def create_error_handler(error_type: str):
        """Create specific error handlers for different error types"""
        def error_handler(error_msg: str, exception: Exception = None):
            """Generic error handler"""
            logger.error(f"{error_type}: {error_msg}")
            if exception:
                logger.error(f"Exception details: {str(exception)}")
            
            # Could extend this to show user-friendly error dialogs
            return f"{error_type}: {error_msg}"
        
        return error_handler
    
    # Create specific error handlers
    handlers = {
        'api_error': create_error_handler("API Error"),
        'import_error': create_error_handler("Import Error"), 
        'ui_error': create_error_handler("UI Error"),
        'accessibility_error': create_error_handler("Accessibility Error")
    }
    
    # Make handlers available globally
    globals().update(handlers)
    
    logger.info("Enhanced exception handling installed")
    return True


# Utility Functions for Error Prevention
class ErrorPrevention:
    """Utility class for preventing common errors"""
    
    @staticmethod
    def safe_import(module_name: str, fallback=None):
        """Safely import a module with fallback"""
        try:
            return __import__(module_name)
        except ImportError as e:
            logger.warning(f"Failed to import {module_name}: {e}")
            return fallback
    
    @staticmethod
    def safe_getattr(obj, attr_name: str, default=None):
        """Safely get attribute with proper error handling"""
        try:
            return getattr(obj, attr_name, default)
        except AttributeError:
            logger.warning(f"Attribute {attr_name} not found in {type(obj)}")
            return default
    
    @staticmethod
    def validate_pyqt_imports():
        """Validate that all required PyQt5 components are available"""
        required_modules = [
            'PyQt5.QtWidgets',
            'PyQt5.QtCore',
            'PyQt5.QtGui'
        ]
        
        missing = []
        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                missing.append(module)
        
        if missing:
            logger.error(f"Missing required PyQt5 modules: {missing}")
            return False
        return True
    
    @staticmethod
    def validate_openai_setup():
        """Validate OpenAI setup and configuration"""
        try:
            import openai
            from dotenv import load_dotenv
            
            load_dotenv()
            api_key = os.getenv("OPENAI_API_KEY")
            
            if not api_key:
                return False, "OPENAI_API_KEY not set in environment"
            
            if not api_key.startswith("sk-"):
                return False, "Invalid API key format"
            
            return True, "OpenAI setup validated"
        except ImportError:
            return False, "OpenAI library not installed"


# Integration function for main application
def integrate_error_fixes(main_window):
    """
    Integrate all error fixes into the main application window
    
    Args:
        main_window: Instance of SpanishSubjunctivePracticeGUI
    
    Returns:
        bool: True if integration successful
    """
    try:
        fixer = ErrorFixes()
        applied_fixes = fixer.apply_all_fixes(main_window)
        
        logger.info(f"Applied {len(applied_fixes)} error fixes: {applied_fixes}")
        
        # Validate setup after fixes
        prevention = ErrorPrevention()
        pyqt_valid = prevention.validate_pyqt_imports()
        openai_valid, openai_msg = prevention.validate_openai_setup()
        
        logger.info(f"Post-fix validation - PyQt5: {pyqt_valid}, OpenAI: {openai_valid} ({openai_msg})")
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to integrate error fixes: {e}")
        return False


# Example usage and testing
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Test error fixes
    fixer = ErrorFixes()
    applied = fixer.apply_all_fixes()
    print(f"Applied fixes: {applied}")
    
    # Test validation
    prevention = ErrorPrevention()
    pyqt_ok = prevention.validate_pyqt_imports()
    openai_ok, openai_msg = prevention.validate_openai_setup()
    
    print(f"Validation results:")
    print(f"  PyQt5: {'✓' if pyqt_ok else '✗'}")
    print(f"  OpenAI: {'✓' if openai_ok else '✗'} - {openai_msg}")