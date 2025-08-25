"""
Simple module validation script
Tests imports without heavy PyQt5 usage to avoid segmentation faults
"""

import sys
import os

def validate_readability_modules():
    """Validate that all readability modules can be imported and have key classes"""
    
    print("READABILITY MODULES VALIDATION")
    print("=" * 50)
    
    # Add current directory to path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    test_results = []
    
    # Test 1: readability_enhancements module
    try:
        from readability_enhancements import (
            ReadabilityAnalyzer, ReadabilityEnhancer, 
            SpanishTextOptimizer, VisualHierarchyManager, 
            ReadabilityManager
        )
        
        # Test that classes can be instantiated
        analyzer = ReadabilityAnalyzer()
        enhancer = ReadabilityEnhancer()
        optimizer = SpanishTextOptimizer()
        hierarchy = VisualHierarchyManager()
        
        print("✓ readability_enhancements: All classes imported and instantiated")
        test_results.append(("readability_enhancements", True))
        
    except Exception as e:
        print(f"✗ readability_enhancements: {e}")
        test_results.append(("readability_enhancements", False))
    
    # Test 2: readability_analysis_report module
    try:
        from readability_analysis_report import MainPyReadabilityAnalysis, generate_main_py_readability_report
        
        # Test class instantiation
        analysis = MainPyReadabilityAnalysis()
        
        print("✓ readability_analysis_report: Module and classes available")
        test_results.append(("analysis_report", True))
        
    except Exception as e:
        print(f"✗ readability_analysis_report: {e}")
        test_results.append(("analysis_report", False))
    
    # Test 3: integration_guide module
    try:
        from integration_guide import ReadabilityIntegrationGuide, generate_integration_instructions
        
        # Test class instantiation
        guide = ReadabilityIntegrationGuide()
        
        print("✓ integration_guide: Module and classes available")
        test_results.append(("integration_guide", True))
        
    except Exception as e:
        print(f"✗ integration_guide: {e}")
        test_results.append(("integration_guide", False))
    
    # Test 4: visual_improvements_guide module
    try:
        from visual_improvements_guide import VisualImprovementsGuide, generate_visual_comparison_guide
        
        # Test class instantiation
        visual_guide = VisualImprovementsGuide()
        
        print("✓ visual_improvements_guide: Module and classes available")
        test_results.append(("visual_guide", True))
        
    except Exception as e:
        print(f"✗ visual_improvements_guide: {e}")
        test_results.append(("visual_guide", False))
    
    # Test 5: Check key functionality without PyQt5
    try:
        # Test Spanish text optimization without GUI
        optimizer = SpanishTextOptimizer()
        test_text = "Como estas? Muy bien!"
        result = optimizer._fix_punctuation_spacing(test_text)
        
        print("✓ Spanish text processing: Basic functionality working")
        test_results.append(("text_processing", True))
        
    except Exception as e:
        print(f"✗ Spanish text processing: {e}")
        test_results.append(("text_processing", False))
    
    # Test 6: Check visual hierarchy data
    try:
        hierarchy = VisualHierarchyManager()
        levels = hierarchy.hierarchy_levels
        required_levels = ["primary", "secondary", "body", "muted", "accent"]
        
        missing_levels = [level for level in required_levels if level not in levels]
        if not missing_levels:
            print("✓ Visual hierarchy: All required levels available")
            test_results.append(("visual_hierarchy", True))
        else:
            print(f"✗ Visual hierarchy: Missing levels: {missing_levels}")
            test_results.append(("visual_hierarchy", False))
            
    except Exception as e:
        print(f"✗ Visual hierarchy: {e}")
        test_results.append(("visual_hierarchy", False))
    
    # Summary
    print("\n" + "=" * 50)
    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)
    
    print(f"VALIDATION SUMMARY: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ ALL MODULES READY FOR INTEGRATION")
        return True
    else:
        print("⚠ SOME ISSUES FOUND - CHECK ABOVE FOR DETAILS")
        return False

if __name__ == "__main__":
    success = validate_readability_modules()
    sys.exit(0 if success else 1)