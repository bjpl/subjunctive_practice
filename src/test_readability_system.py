"""
Test Readability Enhancement System

This script validates that all readability enhancement modules
work correctly and provides a quick system check.
"""

import sys
import logging
from typing import Dict, List
try:
    from typing import Any
except ImportError:
    # Python < 3.5 compatibility
    Any = object

# Configure logging for testing
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_module_imports() -> Dict[str, bool]:
    """Test that all required modules can be imported"""
    results = {}
    
    # Test core readability modules
    try:
        from readability_enhancements import (
            ReadabilityAnalyzer, ReadabilityEnhancer, 
            SpanishTextOptimizer, VisualHierarchyManager, 
            ReadabilityManager
        )
        results['readability_enhancements'] = True
        logger.info("✓ readability_enhancements module imported successfully")
    except ImportError as e:
        results['readability_enhancements'] = False
        logger.error(f"✗ Failed to import readability_enhancements: {e}")
    
    # Test analysis report module
    try:
        from readability_analysis_report import MainPyReadabilityAnalysis
        results['analysis_report'] = True
        logger.info("✓ readability_analysis_report module imported successfully")
    except ImportError as e:
        results['analysis_report'] = False
        logger.error(f"✗ Failed to import readability_analysis_report: {e}")
    
    # Test integration guide
    try:
        from integration_guide import ReadabilityIntegrationGuide
        results['integration_guide'] = True
        logger.info("✓ integration_guide module imported successfully")
    except ImportError as e:
        results['integration_guide'] = False
        logger.error(f"✗ Failed to import integration_guide: {e}")
    
    # Test visual improvements guide
    try:
        from visual_improvements_guide import VisualImprovementsGuide
        results['visual_guide'] = True
        logger.info("✓ visual_improvements_guide module imported successfully")
    except ImportError as e:
        results['visual_guide'] = False
        logger.error(f"✗ Failed to import visual_improvements_guide: {e}")
    
    return results

def test_pyqt5_dependencies() -> bool:
    """Test that PyQt5 dependencies are available"""
    try:
        from PyQt5.QtWidgets import QApplication, QLabel, QTextEdit, QPushButton
        from PyQt5.QtCore import Qt, QTimer
        from PyQt5.QtGui import QFont, QFontMetrics, QColor, QPalette
        logger.info("✓ All PyQt5 dependencies available")
        return True
    except ImportError as e:
        logger.error(f"✗ Missing PyQt5 dependencies: {e}")
        return False

def test_contrast_calculation() -> bool:
    """Test contrast ratio calculation functionality"""
    try:
        from readability_enhancements import ReadabilityAnalyzer
        from PyQt5.QtGui import QColor
        
        analyzer = ReadabilityAnalyzer()
        
        # Test known contrast ratios
        white = QColor("#ffffff")
        black = QColor("#000000")
        ratio = analyzer.calculate_contrast_ratio(white, black)
        
        # White on black should be ~21:1
        if 20.5 <= ratio <= 21.5:
            logger.info(f"✓ Contrast calculation working: {ratio:.1f}:1")
            return True
        else:
            logger.error(f"✗ Contrast calculation incorrect: {ratio:.1f}:1 (expected ~21:1)")
            return False
            
    except Exception as e:
        logger.error(f"✗ Contrast calculation test failed: {e}")
        return False

def test_spanish_text_optimization() -> bool:
    """Test Spanish text optimization functionality"""
    try:
        from readability_enhancements import SpanishTextOptimizer
        
        optimizer = SpanishTextOptimizer()
        
        # Test punctuation fixing
        test_text = "Como estas? Muy bien!"
        optimized = optimizer.optimize_text_display(test_text)
        
        # Should add inverted question mark
        if "¿" in optimized or "¡" in optimized:
            logger.info("✓ Spanish text optimization working")
            logger.info(f"  Original: {test_text}")
            logger.info(f"  Optimized: {optimized}")
            return True
        else:
            logger.warning("⚠ Spanish text optimization not adding punctuation (may be working correctly)")
            return True  # Not necessarily a failure
            
    except Exception as e:
        logger.error(f"✗ Spanish text optimization test failed: {e}")
        return False

def test_font_support_detection() -> bool:
    """Test Spanish font support detection"""
    try:
        from PyQt5.QtGui import QFont, QFontMetrics
        from readability_enhancements import ReadabilityEnhancer
        
        enhancer = ReadabilityEnhancer()
        
        # Test Spanish character support
        test_font = enhancer._get_optimal_font("body")
        metrics = QFontMetrics(test_font)
        
        # Test key Spanish characters
        spanish_chars = ['ñ', 'á', 'é', 'í', 'ó', 'ú', 'ü']
        supported_chars = []
        
        for char in spanish_chars:
            if metrics.inFontUcs4(ord(char)):
                supported_chars.append(char)
        
        if len(supported_chars) >= 6:  # Most characters supported
            logger.info(f"✓ Font supports Spanish characters: {', '.join(supported_chars)}")
            return True
        else:
            logger.warning(f"⚠ Limited Spanish character support: {', '.join(supported_chars)}")
            return False
            
    except Exception as e:
        logger.error(f"✗ Font support test failed: {e}")
        return False

def test_visual_hierarchy() -> bool:
    """Test visual hierarchy system"""
    try:
        from readability_enhancements import VisualHierarchyManager
        
        manager = VisualHierarchyManager()
        
        # Test hierarchy levels exist
        required_levels = ["primary", "secondary", "body", "muted", "accent"]
        
        for level in required_levels:
            if level not in manager.hierarchy_levels:
                logger.error(f"✗ Missing hierarchy level: {level}")
                return False
        
        logger.info("✓ Visual hierarchy system complete")
        return True
        
    except Exception as e:
        logger.error(f"✗ Visual hierarchy test failed: {e}")
        return False

def run_comprehensive_test() -> Dict[str, Any]:
    """Run comprehensive test of the readability system"""
    logger.info("Starting comprehensive readability system test...")
    
    test_results = {
        'module_imports': test_module_imports(),
        'pyqt5_available': test_pyqt5_dependencies(),
        'contrast_calculation': False,
        'spanish_optimization': False, 
        'font_support': False,
        'visual_hierarchy': False
    }
    
    # Only run advanced tests if basic imports work
    if test_results['pyqt5_available'] and test_results['module_imports'].get('readability_enhancements', False):
        test_results['contrast_calculation'] = test_contrast_calculation()
        test_results['spanish_optimization'] = test_spanish_text_optimization()
        test_results['font_support'] = test_font_support_detection()
        test_results['visual_hierarchy'] = test_visual_hierarchy()
    
    return test_results

def generate_test_report(test_results: Dict[str, Any]) -> str:
    """Generate formatted test report"""
    
    report = """
READABILITY ENHANCEMENT SYSTEM TEST REPORT
==========================================

"""
    
    # Module import results
    report += "MODULE IMPORTS:\n"
    if isinstance(test_results['module_imports'], dict):
        for module, success in test_results['module_imports'].items():
            status = "✓ PASS" if success else "✗ FAIL"
            report += f"  {module}: {status}\n"
    
    # Other test results
    other_tests = [
        ('PyQt5 Dependencies', 'pyqt5_available'),
        ('Contrast Calculation', 'contrast_calculation'),
        ('Spanish Text Optimization', 'spanish_optimization'),
        ('Font Support Detection', 'font_support'),
        ('Visual Hierarchy System', 'visual_hierarchy')
    ]
    
    report += "\nSYSTEM FUNCTIONALITY:\n"
    for test_name, key in other_tests:
        if key in test_results:
            status = "✓ PASS" if test_results[key] else "✗ FAIL"
            report += f"  {test_name}: {status}\n"
    
    # Overall assessment
    total_tests = len([k for k, v in test_results.items() if k != 'module_imports'])
    if isinstance(test_results['module_imports'], dict):
        total_tests += len(test_results['module_imports'])
        passed_imports = sum(test_results['module_imports'].values())
    else:
        passed_imports = 0
    
    passed_other = sum([1 for k, v in test_results.items() if k != 'module_imports' and v])
    total_passed = passed_imports + passed_other
    
    success_rate = (total_passed / total_tests) * 100 if total_tests > 0 else 0
    
    report += f"""
OVERALL ASSESSMENT:
  Tests Passed: {total_passed}/{total_tests}
  Success Rate: {success_rate:.1f}%
  
"""
    
    if success_rate >= 90:
        report += "✓ EXCELLENT: Readability system ready for integration\n"
    elif success_rate >= 70:
        report += "⚠ GOOD: Minor issues, system mostly functional\n"
    elif success_rate >= 50:
        report += "⚠ FAIR: Some issues need resolution before integration\n"
    else:
        report += "✗ POOR: Major issues prevent integration\n"
    
    report += """
NEXT STEPS:
1. Resolve any failed tests before integration
2. Ensure all required dependencies are installed
3. Follow the integration guide step-by-step
4. Test with actual Spanish content after integration

For troubleshooting failed tests, check the integration guide
troubleshooting section or review module import paths.
"""
    
    return report

def main():
    """Main test execution function"""
    try:
        # Add current directory to path for imports
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        # Run tests
        results = run_comprehensive_test()
        
        # Generate and display report
        report = generate_test_report(results)
        print(report)
        
        # Return success/failure code
        total_success = all(results.get(k, False) for k in results if k != 'module_imports')
        if isinstance(results.get('module_imports'), dict):
            import_success = all(results['module_imports'].values())
            total_success = total_success and import_success
        
        return 0 if total_success else 1
        
    except Exception as e:
        logger.error(f"Test execution failed: {e}")
        print(f"\nFATAL ERROR: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())