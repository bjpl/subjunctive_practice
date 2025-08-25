#!/usr/bin/env python3
"""
UI Test Validation Script for Spanish Subjunctive Practice App

This script performs comprehensive UI testing to validate:
1. Application launch and basic functionality
2. Text readability improvements
3. Red box fixes
4. Progress indication functionality
5. Overall user experience

Author: Claude Code - UI Testing Agent
Date: 2025-08-25
"""

import sys
import os
import logging
import traceback
import time
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'src'))

# Import PyQt5
try:
    from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
    from PyQt5.QtCore import QTimer, Qt
    from PyQt5.QtTest import QTest
    from PyQt5.QtGui import QFont, QColor
    PYQT_AVAILABLE = True
except ImportError as e:
    print(f"PyQt5 not available: {e}")
    PYQT_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class UITestValidator:
    """
    Comprehensive UI test validator for the Spanish subjunctive practice application.
    """
    
    def __init__(self):
        self.results = {
            'test_timestamp': datetime.now().isoformat(),
            'test_summary': {},
            'detailed_results': {},
            'issues_found': [],
            'recommendations': []
        }
        self.app = None
        self.main_window = None
        
    def run_all_tests(self) -> Dict[str, Any]:
        """
        Run all UI validation tests and return comprehensive results.
        """
        logger.info("Starting comprehensive UI validation tests")
        
        tests = [
            ('Environment Check', self.test_environment),
            ('Application Launch', self.test_application_launch),
            ('UI Components Load', self.test_ui_components_load),
            ('Text Readability', self.test_text_readability),
            ('Red Box Issues', self.test_red_box_fixes),
            ('Progress Indicators', self.test_progress_indicators),
            ('Form Styling', self.test_form_styling),
            ('Accessibility Features', self.test_accessibility_features),
            ('Error Handling', self.test_error_handling),
            ('Responsiveness', self.test_responsiveness)
        ]
        
        for test_name, test_func in tests:
            logger.info(f"Running test: {test_name}")
            try:
                result = test_func()
                self.results['detailed_results'][test_name] = result
                logger.info(f"Test {test_name}: {'PASS' if result.get('success', False) else 'FAIL'}")
            except Exception as e:
                error_result = {
                    'success': False,
                    'error': str(e),
                    'traceback': traceback.format_exc()
                }
                self.results['detailed_results'][test_name] = error_result
                logger.error(f"Test {test_name} failed with exception: {e}")
        
        # Generate summary
        self._generate_summary()
        
        return self.results
    
    def test_environment(self) -> Dict[str, Any]:
        """Test the basic environment setup."""
        result = {
            'success': True,
            'checks': {},
            'issues': []
        }
        
        # Check Python version
        python_version = sys.version_info
        result['checks']['python_version'] = f"{python_version.major}.{python_version.minor}.{python_version.micro}"
        
        if python_version < (3, 7):
            result['issues'].append("Python version too old, recommend 3.7+")
            result['success'] = False
        
        # Check PyQt5 availability
        result['checks']['pyqt5_available'] = PYQT_AVAILABLE
        if not PYQT_AVAILABLE:
            result['issues'].append("PyQt5 not available - cannot run GUI tests")
            result['success'] = False
            return result
        
        # Check project files
        required_files = ['main.py', 'src/', '.env']
        for file_path in required_files:
            exists = (project_root / file_path).exists()
            result['checks'][f'{file_path}_exists'] = exists
            if not exists:
                result['issues'].append(f"Required file/directory missing: {file_path}")
                result['success'] = False
        
        # Check environment variables
        from dotenv import load_dotenv
        load_dotenv()
        api_key_set = bool(os.getenv('OPENAI_API_KEY'))
        result['checks']['openai_api_key_set'] = api_key_set
        if not api_key_set:
            result['issues'].append("OpenAI API key not set - some features may not work")
        
        return result
    
    def test_application_launch(self) -> Dict[str, Any]:
        """Test basic application launch functionality."""
        result = {
            'success': False,
            'launch_time': None,
            'errors': [],
            'warnings': []
        }
        
        if not PYQT_AVAILABLE:
            result['errors'].append("PyQt5 not available")
            return result
        
        try:
            start_time = time.time()
            
            # Create QApplication if it doesn't exist
            if not QApplication.instance():
                self.app = QApplication([])
            else:
                self.app = QApplication.instance()
            
            # Import main application module
            try:
                from main import SpanishSubjunctivePracticeGUI
                logger.info("Successfully imported main application class")
            except ImportError as e:
                result['errors'].append(f"Failed to import main application: {e}")
                return result
            
            # Create main window
            try:
                self.main_window = SpanishSubjunctivePracticeGUI()
                logger.info("Successfully created main window instance")
            except Exception as e:
                result['errors'].append(f"Failed to create main window: {e}")
                return result
            
            # Test window properties
            launch_time = time.time() - start_time
            result['launch_time'] = f"{launch_time:.2f}s"
            
            # Check window is properly initialized
            if self.main_window.windowTitle():
                result['window_title'] = self.main_window.windowTitle()
                logger.info(f"Window title: {self.main_window.windowTitle()}")
            
            # Check window size
            size = self.main_window.size()
            result['window_size'] = f"{size.width()}x{size.height()}"
            
            if size.width() < 800 or size.height() < 600:
                result['warnings'].append(f"Window size might be too small: {result['window_size']}")
            
            result['success'] = True
            logger.info("Application launch test passed")
            
        except Exception as e:
            result['errors'].append(f"Application launch failed: {e}")
            result['traceback'] = traceback.format_exc()
            logger.error(f"Application launch test failed: {e}")
        
        return result
    
    def test_ui_components_load(self) -> Dict[str, Any]:
        """Test that UI components load properly without crashes."""
        result = {
            'success': False,
            'components_found': {},
            'missing_components': [],
            'error_components': []
        }
        
        if not self.main_window:
            result['missing_components'].append("Main window not available")
            return result
        
        # Key UI components to check
        component_checks = {
            'sentence_label': 'Main sentence display',
            'stats_label': 'Statistics display',
            'trigger_checkboxes': 'Subjunctive trigger checkboxes',
            'tense_checkboxes': 'Tense selection checkboxes',
            'person_checkboxes': 'Person selection checkboxes',
            'free_response_input': 'Free response input field',
            'feedback_text': 'Feedback display area'
        }
        
        for component, description in component_checks.items():
            try:
                if hasattr(self.main_window, component):
                    attr = getattr(self.main_window, component)
                    result['components_found'][component] = {
                        'description': description,
                        'found': True,
                        'type': type(attr).__name__
                    }
                    
                    # Additional checks for specific components
                    if component == 'trigger_checkboxes' and isinstance(attr, list):
                        result['components_found'][component]['count'] = len(attr)
                    elif component.endswith('_checkboxes') and isinstance(attr, dict):
                        result['components_found'][component]['count'] = len(attr)
                        
                else:
                    result['missing_components'].append(f"{component} ({description})")
                    result['components_found'][component] = {
                        'description': description,
                        'found': False
                    }
            except Exception as e:
                result['error_components'].append(f"{component}: {e}")
        
        # Calculate success rate
        total_components = len(component_checks)
        found_components = sum(1 for comp in result['components_found'].values() if comp.get('found', False))
        success_rate = found_components / total_components
        
        result['success_rate'] = f"{success_rate:.1%}"
        result['success'] = success_rate >= 0.8  # 80% success rate required
        
        return result
    
    def test_text_readability(self) -> Dict[str, Any]:
        """Test text readability improvements."""
        result = {
            'success': True,
            'font_checks': {},
            'readability_issues': []
        }
        
        if not self.main_window:
            result['readability_issues'].append("Main window not available")
            result['success'] = False
            return result
        
        try:
            # Check default font
            app_font = self.app.font() if self.app else QFont()
            result['font_checks']['app_font_family'] = app_font.family()
            result['font_checks']['app_font_size'] = app_font.pointSize()
            
            # Check if font size is reasonable
            if app_font.pointSize() < 10:
                result['readability_issues'].append(f"Font size too small: {app_font.pointSize()}pt")
                result['success'] = False
            elif app_font.pointSize() > 16:
                result['readability_issues'].append(f"Font size too large: {app_font.pointSize()}pt")
            
            # Check specific component fonts
            components_to_check = [
                ('sentence_label', 'Main sentence'),
                ('stats_label', 'Statistics'),
                ('feedback_text', 'Feedback area')
            ]
            
            for component_name, description in components_to_check:
                if hasattr(self.main_window, component_name):
                    component = getattr(self.main_window, component_name)
                    font = component.font()
                    
                    result['font_checks'][f'{component_name}_font'] = {
                        'family': font.family(),
                        'size': font.pointSize(),
                        'bold': font.bold()
                    }
                    
                    # Check readability
                    if font.pointSize() < 9:
                        result['readability_issues'].append(f"{description} font too small: {font.pointSize()}pt")
                        result['success'] = False
            
            # Check contrast (basic check for stylesheet colors)
            if hasattr(self.main_window, 'translation_label'):
                style = self.main_window.translation_label.styleSheet()
                if 'gray' in style.lower() and 'background' not in style.lower():
                    # Gray text without explicit background might have contrast issues
                    result['readability_issues'].append("Gray text may have contrast issues")
            
        except Exception as e:
            result['readability_issues'].append(f"Error checking fonts: {e}")
            result['success'] = False
        
        return result
    
    def test_red_box_fixes(self) -> Dict[str, Any]:
        """Test that red box form styling issues are fixed."""
        result = {
            'success': True,
            'form_elements_checked': {},
            'red_box_issues': []
        }
        
        if not self.main_window:
            result['red_box_issues'].append("Main window not available")
            result['success'] = False
            return result
        
        try:
            # Check form elements that commonly have red box issues
            form_elements = [
                ('trigger_checkboxes', list),
                ('tense_checkboxes', dict),
                ('person_checkboxes', dict),
                ('free_response_input', object),
                ('custom_context_input', object),
                ('verbs_input', object)
            ]
            
            for element_name, expected_type in form_elements:
                if hasattr(self.main_window, element_name):
                    element = getattr(self.main_window, element_name)
                    
                    # For checkbox collections
                    if element_name.endswith('_checkboxes') and isinstance(element, (list, dict)):
                        elements_to_check = element if isinstance(element, list) else element.values()
                        
                        for i, checkbox in enumerate(elements_to_check):
                            # Check if checkbox has any red styling indicators
                            style = checkbox.styleSheet() if hasattr(checkbox, 'styleSheet') else ""
                            
                            # Common red box indicators
                            red_indicators = ['border: 1px solid red', 'background: red', 'background-color: red']
                            has_red_styling = any(indicator in style.lower() for indicator in red_indicators)
                            
                            result['form_elements_checked'][f'{element_name}_{i}'] = {
                                'has_red_styling': has_red_styling,
                                'style_length': len(style),
                                'has_styling': bool(style.strip())
                            }
                            
                            if has_red_styling:
                                result['red_box_issues'].append(f"Red styling found in {element_name}[{i}]")
                                result['success'] = False
                    
                    # For input elements
                    elif hasattr(element, 'styleSheet'):
                        style = element.styleSheet()
                        red_indicators = ['border: 1px solid red', 'background: red', 'background-color: red']
                        has_red_styling = any(indicator in style.lower() for indicator in red_indicators)
                        
                        result['form_elements_checked'][element_name] = {
                            'has_red_styling': has_red_styling,
                            'style_length': len(style),
                            'has_styling': bool(style.strip())
                        }
                        
                        if has_red_styling:
                            result['red_box_issues'].append(f"Red styling found in {element_name}")
                            result['success'] = False
            
            # Check for form integration manager
            if hasattr(self.main_window, 'form_integration_manager'):
                result['form_integration_manager_present'] = True
                logger.info("Form integration manager is present")
            else:
                result['form_integration_manager_present'] = False
                result['red_box_issues'].append("Form integration manager not found")
        
        except Exception as e:
            result['red_box_issues'].append(f"Error checking form styling: {e}")
            result['success'] = False
        
        return result
    
    def test_progress_indicators(self) -> Dict[str, Any]:
        """Test progress indication functionality."""
        result = {
            'success': True,
            'progress_features': {},
            'issues': []
        }
        
        if not self.main_window:
            result['issues'].append("Main window not available")
            result['success'] = False
            return result
        
        try:
            # Check for progress manager
            if hasattr(self.main_window, 'progress_manager'):
                result['progress_features']['progress_manager_present'] = True
                progress_manager = self.main_window.progress_manager
                
                # Check if progress manager has expected methods
                expected_methods = ['show_loading', 'hide_loading', 'update_progress']
                for method in expected_methods:
                    result['progress_features'][f'has_{method}'] = hasattr(progress_manager, method)
                    if not hasattr(progress_manager, method):
                        result['issues'].append(f"Progress manager missing method: {method}")
                        result['success'] = False
            else:
                result['progress_features']['progress_manager_present'] = False
                result['issues'].append("Progress manager not found")
                result['success'] = False
            
            # Check for progress overlay
            if hasattr(self.main_window, 'progress_overlay'):
                result['progress_features']['progress_overlay_present'] = True
            else:
                result['progress_features']['progress_overlay_present'] = False
                result['issues'].append("Progress overlay not found")
            
            # Check for loading states tracking
            if hasattr(self.main_window, 'loading_states'):
                loading_states = self.main_window.loading_states
                if isinstance(loading_states, dict):
                    result['progress_features']['loading_states_count'] = len(loading_states)
                    result['progress_features']['loading_states'] = list(loading_states.keys())
                else:
                    result['issues'].append("Loading states not a dictionary")
                    result['success'] = False
            else:
                result['issues'].append("Loading states tracking not found")
                result['success'] = False
            
            # Check for constants availability
            try:
                progress_available = getattr(self.main_window, 'PROGRESS_INDICATORS_AVAILABLE', False)
                result['progress_features']['progress_indicators_available'] = progress_available
                if not progress_available:
                    result['issues'].append("Progress indicators module not available")
            except:
                result['issues'].append("Cannot determine progress indicators availability")
        
        except Exception as e:
            result['issues'].append(f"Error checking progress indicators: {e}")
            result['success'] = False
        
        return result
    
    def test_form_styling(self) -> Dict[str, Any]:
        """Test form styling integration."""
        result = {
            'success': True,
            'styling_features': {},
            'issues': []
        }
        
        if not self.main_window:
            result['issues'].append("Main window not available")
            result['success'] = False
            return result
        
        try:
            # Check for form integration manager
            if hasattr(self.main_window, 'form_integration_manager'):
                result['styling_features']['form_integration_manager'] = True
                
                fim = self.main_window.form_integration_manager
                if fim:
                    # Check manager methods
                    expected_methods = ['initialize_form_styling', 'refresh_styling', 'set_form_validation_state']
                    for method in expected_methods:
                        has_method = hasattr(fim, method)
                        result['styling_features'][f'manager_has_{method}'] = has_method
                        if not has_method:
                            result['issues'].append(f"Form integration manager missing: {method}")
                            result['success'] = False
                else:
                    result['issues'].append("Form integration manager is None")
                    result['success'] = False
            else:
                result['styling_features']['form_integration_manager'] = False
                result['issues'].append("Form integration manager not found")
                result['success'] = False
            
            # Check for styling manager
            if hasattr(self.main_window, 'style_manager'):
                result['styling_features']['style_manager_present'] = True
            else:
                result['styling_features']['style_manager_present'] = False
            
            # Check for spacing optimizer
            if hasattr(self.main_window, 'spacing_optimizer'):
                result['styling_features']['spacing_optimizer_present'] = True
            else:
                result['styling_features']['spacing_optimizer_present'] = False
                result['issues'].append("Spacing optimizer not found")
        
        except Exception as e:
            result['issues'].append(f"Error checking form styling: {e}")
            result['success'] = False
        
        return result
    
    def test_accessibility_features(self) -> Dict[str, Any]:
        """Test accessibility features integration."""
        result = {
            'success': True,
            'accessibility_features': {},
            'issues': []
        }
        
        if not self.main_window:
            result['issues'].append("Main window not available")
            result['success'] = False
            return result
        
        try:
            # Check accessibility manager
            if hasattr(self.main_window, 'accessibility_manager'):
                result['accessibility_features']['accessibility_manager_present'] = True
            else:
                result['accessibility_features']['accessibility_manager_present'] = False
                result['issues'].append("Accessibility manager not found")
            
            # Check if accessibility functions are available
            accessibility_functions = [
                'integrate_accessibility',
                'add_accessibility_startup_check'
            ]
            
            for func_name in accessibility_functions:
                # These are usually imported at module level
                if func_name in globals() or hasattr(self.main_window, func_name):
                    result['accessibility_features'][f'{func_name}_available'] = True
                else:
                    result['accessibility_features'][f'{func_name}_available'] = False
            
            # Check for accessibility settings
            accessibility_settings_path = project_root / 'config' / 'accessibility_settings.json'
            if accessibility_settings_path.exists():
                result['accessibility_features']['settings_file_exists'] = True
                try:
                    with open(accessibility_settings_path, 'r') as f:
                        settings = json.load(f)
                        result['accessibility_features']['settings_keys'] = list(settings.keys())
                except Exception as e:
                    result['issues'].append(f"Error reading accessibility settings: {e}")
            else:
                result['accessibility_features']['settings_file_exists'] = False
                result['issues'].append("Accessibility settings file not found")
        
        except Exception as e:
            result['issues'].append(f"Error checking accessibility features: {e}")
            result['success'] = False
        
        return result
    
    def test_error_handling(self) -> Dict[str, Any]:
        """Test error handling improvements."""
        result = {
            'success': True,
            'error_handling_features': {},
            'issues': []
        }
        
        if not self.main_window:
            result['issues'].append("Main window not available")
            result['success'] = False
            return result
        
        try:
            # Check for API module availability
            api_available = getattr(self.main_window, 'API_MODULE_AVAILABLE', False)
            result['error_handling_features']['api_module_available'] = api_available
            
            # Check for client initialization
            has_client = hasattr(self.main_window, 'client') or 'client' in globals()
            result['error_handling_features']['client_initialized'] = has_client
            
            # Check for error fixes integration
            try:
                from src.error_fixes import ErrorFixes
                result['error_handling_features']['error_fixes_module_available'] = True
            except ImportError:
                result['error_handling_features']['error_fixes_module_available'] = False
                result['issues'].append("Error fixes module not available")
            
            # Check logging configuration
            if logger.handlers:
                result['error_handling_features']['logging_configured'] = True
                result['error_handling_features']['log_handlers'] = len(logger.handlers)
            else:
                result['error_handling_features']['logging_configured'] = False
                result['issues'].append("Logging not properly configured")
        
        except Exception as e:
            result['issues'].append(f"Error checking error handling: {e}")
            result['success'] = False
        
        return result
    
    def test_responsiveness(self) -> Dict[str, Any]:
        """Test UI responsiveness features."""
        result = {
            'success': True,
            'responsive_features': {},
            'issues': []
        }
        
        if not self.main_window:
            result['issues'].append("Main window not available")
            result['success'] = False
            return result
        
        try:
            # Check initial window size
            initial_size = self.main_window.size()
            result['responsive_features']['initial_size'] = f"{initial_size.width()}x{initial_size.height()}"
            
            # Check minimum size
            min_size = self.main_window.minimumSize()
            result['responsive_features']['minimum_size'] = f"{min_size.width()}x{min_size.height()}"
            
            # Check if responsive design is available
            responsive_available = getattr(self.main_window, 'RESPONSIVE_DESIGN_AVAILABLE', False)
            result['responsive_features']['responsive_design_available'] = responsive_available
            
            if not responsive_available:
                result['issues'].append("Responsive design module not available")
                result['success'] = False
            
            # Check splitter (should be responsive)
            if hasattr(self.main_window, 'centralWidget'):
                central_widget = self.main_window.centralWidget()
                if central_widget:
                    # Look for splitter in the layout
                    from PyQt5.QtWidgets import QSplitter
                    splitters = central_widget.findChildren(QSplitter)
                    result['responsive_features']['splitter_count'] = len(splitters)
                    
                    if splitters:
                        result['responsive_features']['has_splitter'] = True
                    else:
                        result['responsive_features']['has_splitter'] = False
                        result['issues'].append("No responsive splitter found")
        
        except Exception as e:
            result['issues'].append(f"Error checking responsiveness: {e}")
            result['success'] = False
        
        return result
    
    def _generate_summary(self):
        """Generate test summary."""
        detailed = self.results['detailed_results']
        
        total_tests = len(detailed)
        passed_tests = sum(1 for result in detailed.values() if result.get('success', False))
        
        self.results['test_summary'] = {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': total_tests - passed_tests,
            'success_rate': f"{(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "0%",
            'overall_status': 'PASS' if passed_tests >= total_tests * 0.8 else 'FAIL'
        }
        
        # Collect all issues
        all_issues = []
        for test_name, result in detailed.items():
            if not result.get('success', False):
                issues = result.get('issues', result.get('errors', result.get('red_box_issues', [])))
                for issue in issues:
                    all_issues.append(f"{test_name}: {issue}")
        
        self.results['issues_found'] = all_issues
        
        # Generate recommendations
        recommendations = []
        
        if not detailed.get('Environment Check', {}).get('success', False):
            recommendations.append("Fix environment setup issues before running the application")
        
        if not detailed.get('Application Launch', {}).get('success', False):
            recommendations.append("Address application launch failures - check imports and dependencies")
        
        if not detailed.get('Red Box Issues', {}).get('success', False):
            recommendations.append("Form styling fixes need attention - red box issues persist")
        
        if not detailed.get('Text Readability', {}).get('success', False):
            recommendations.append("Text readability improvements need refinement")
        
        if not detailed.get('Progress Indicators', {}).get('success', False):
            recommendations.append("Progress indication system needs improvement")
        
        self.results['recommendations'] = recommendations
    
    def cleanup(self):
        """Clean up test resources."""
        if self.main_window:
            try:
                self.main_window.close()
            except:
                pass
        
        if self.app:
            try:
                self.app.quit()
            except:
                pass


def main():
    """Main test execution function."""
    print("=" * 80)
    print("Spanish Subjunctive Practice App - UI Validation Test")
    print("=" * 80)
    
    # Create validator and run tests
    validator = UITestValidator()
    
    try:
        results = validator.run_all_tests()
        
        # Print summary
        summary = results['test_summary']
        print(f"\nTest Summary:")
        print(f"  Total Tests: {summary['total_tests']}")
        print(f"  Passed: {summary['passed_tests']}")
        print(f"  Failed: {summary['failed_tests']}")
        print(f"  Success Rate: {summary['success_rate']}")
        print(f"  Overall Status: {summary['overall_status']}")
        
        # Print issues
        if results['issues_found']:
            print(f"\nIssues Found ({len(results['issues_found'])}):")
            for i, issue in enumerate(results['issues_found'], 1):
                print(f"  {i}. {issue}")
        else:
            print("\n✓ No critical issues found!")
        
        # Print recommendations
        if results['recommendations']:
            print(f"\nRecommendations ({len(results['recommendations'])}):")
            for i, rec in enumerate(results['recommendations'], 1):
                print(f"  {i}. {rec}")
        
        # Save detailed results
        results_file = project_root / 'tests' / 'ui_validation_results.json'
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\nDetailed results saved to: {results_file}")
        
        # Determine exit code
        overall_success = summary['overall_status'] == 'PASS'
        print(f"\nTest Result: {'✓ PASS' if overall_success else '✗ FAIL'}")
        
        return 0 if overall_success else 1
        
    except Exception as e:
        print(f"\nTest execution failed: {e}")
        traceback.print_exc()
        return 1
        
    finally:
        validator.cleanup()


if __name__ == "__main__":
    sys.exit(main())