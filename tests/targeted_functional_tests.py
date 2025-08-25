#!/usr/bin/env python3
"""
Targeted Functional Tests for Spanish Subjunctive Practice Application

Focused testing approach that works around import issues and tests
core functionality systematically.
"""

import sys
import os
import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TestAnalysis:
    """Comprehensive analysis of the Spanish Subjunctive Practice application"""
    
    def __init__(self):
        self.results = {
            'startup_analysis': {},
            'code_structure': {},
            'ui_components': {},
            'exercise_workflow': {},
            'enhancement_modules': {},
            'critical_issues': [],
            'recommendations': []
        }
    
    def analyze_application_startup(self):
        """Analyze application startup and initialization"""
        logger.info("Analyzing application startup...")
        
        startup_issues = []
        
        # Test 1: Main module structure
        try:
            main_path = "main.py"
            if os.path.exists(main_path):
                with open(main_path, 'r', encoding='utf-8') as f:
                    main_content = f.read()
                
                # Check for essential components
                essential_components = {
                    'QApplication import': 'from PyQt5.QtWidgets import' in main_content,
                    'Main GUI class': 'class SpanishSubjunctivePracticeGUI' in main_content,
                    'OpenAI client': 'from openai import OpenAI' in main_content,
                    'Environment variables': 'load_dotenv()' in main_content,
                    'Logging setup': 'logging.getLogger' in main_content,
                    'API validation': 'def validate_api_key' in main_content
                }
                
                missing_components = [comp for comp, found in essential_components.items() if not found]
                if missing_components:
                    startup_issues.append(f"Missing components: {missing_components}")
                
                self.results['startup_analysis'] = {
                    'main_file_exists': True,
                    'essential_components': essential_components,
                    'missing_components': missing_components,
                    'file_size': len(main_content),
                    'line_count': len(main_content.splitlines())
                }
                
            else:
                startup_issues.append("Main.py file not found")
                self.results['startup_analysis']['main_file_exists'] = False
                
        except Exception as e:
            startup_issues.append(f"Error reading main.py: {str(e)}")
        
        # Test 2: Dependencies check
        try:
            dependencies = self._check_dependencies()
            self.results['startup_analysis']['dependencies'] = dependencies
            
            missing_deps = [dep for dep, available in dependencies.items() if not available]
            if missing_deps:
                startup_issues.append(f"Missing dependencies: {missing_deps}")
                
        except Exception as e:
            startup_issues.append(f"Error checking dependencies: {str(e)}")
        
        # Test 3: Configuration files
        config_files = {
            'pyproject.toml': os.path.exists('pyproject.toml'),
            'requirements.txt': os.path.exists('requirements.txt'),
            '.env.example': os.path.exists('.env.example'),
            '.env': os.path.exists('.env')
        }
        
        self.results['startup_analysis']['config_files'] = config_files
        
        # Test 4: Data directories
        data_dirs = {
            'user_data': os.path.exists('user_data'),
            'tests': os.path.exists('tests'),
            'src': os.path.exists('src'),
            'docs': os.path.exists('docs')
        }
        
        self.results['startup_analysis']['data_directories'] = data_dirs
        
        if startup_issues:
            self.results['critical_issues'].extend(startup_issues)
            logger.warning(f"Startup issues found: {startup_issues}")
        else:
            logger.info("Startup analysis completed successfully")
    
    def _check_dependencies(self):
        """Check if required dependencies are available"""
        dependencies = {}
        
        try:
            from PyQt5.QtWidgets import QApplication
            dependencies['PyQt5'] = True
        except ImportError:
            dependencies['PyQt5'] = False
        
        try:
            import openai
            dependencies['openai'] = True
        except ImportError:
            dependencies['openai'] = False
        
        try:
            from dotenv import load_dotenv
            dependencies['python-dotenv'] = True
        except ImportError:
            dependencies['python-dotenv'] = False
        
        try:
            import json
            dependencies['json'] = True
        except ImportError:
            dependencies['json'] = False
        
        return dependencies
    
    def analyze_code_structure(self):
        """Analyze code structure and architecture"""
        logger.info("Analyzing code structure...")
        
        structure_analysis = {}
        
        # Analyze main.py structure
        try:
            with open('main.py', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Count classes and methods
            import re
            classes = re.findall(r'class\s+(\w+)', content)
            methods = re.findall(r'def\s+(\w+)', content)
            imports = re.findall(r'^(import\s+\w+|from\s+\w+.*import.*)', content, re.MULTILINE)
            
            structure_analysis['main_file'] = {
                'classes': len(classes),
                'methods': len(methods),
                'imports': len(imports),
                'class_names': classes,
                'lines_of_code': len(content.splitlines())
            }
            
        except Exception as e:
            structure_analysis['main_file_error'] = str(e)
        
        # Analyze enhancement modules
        src_modules = {}
        if os.path.exists('src'):
            for filename in os.listdir('src'):
                if filename.endswith('.py') and filename != '__init__.py':
                    try:
                        with open(f'src/{filename}', 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        src_modules[filename] = {
                            'size': len(content),
                            'lines': len(content.splitlines()),
                            'has_main_class': 'class ' in content,
                            'has_functions': 'def ' in content
                        }
                    except Exception as e:
                        src_modules[filename] = {'error': str(e)}
        
        structure_analysis['src_modules'] = src_modules
        
        # Analyze supporting modules
        support_modules = {}
        support_files = [
            'learning_analytics.py',
            'session_manager.py', 
            'tblt_scenarios.py',
            'conjugation_reference.py'
        ]
        
        for filename in support_files:
            if os.path.exists(filename):
                try:
                    with open(filename, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    support_modules[filename] = {
                        'exists': True,
                        'size': len(content),
                        'lines': len(content.splitlines())
                    }
                except Exception as e:
                    support_modules[filename] = {'error': str(e)}
            else:
                support_modules[filename] = {'exists': False}
        
        structure_analysis['support_modules'] = support_modules
        
        self.results['code_structure'] = structure_analysis
        logger.info(f"Code structure analysis completed. Found {len(src_modules)} src modules")
    
    def analyze_ui_components(self):
        """Analyze UI component definitions"""
        logger.info("Analyzing UI components...")
        
        ui_analysis = {}
        
        try:
            with open('main.py', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Search for UI component initializations
            ui_components = {
                'QLabel': content.count('QLabel('),
                'QPushButton': content.count('QPushButton('),
                'QLineEdit': content.count('QLineEdit('),
                'QTextEdit': content.count('QTextEdit('),
                'QComboBox': content.count('QComboBox('),
                'QCheckBox': content.count('QCheckBox('),
                'QRadioButton': content.count('QRadioButton('),
                'QProgressBar': content.count('QProgressBar('),
                'QGroupBox': content.count('QGroupBox('),
                'QScrollArea': content.count('QScrollArea('),
                'QStackedWidget': content.count('QStackedWidget('),
                'QSplitter': content.count('QSplitter('),
                'QVBoxLayout': content.count('QVBoxLayout('),
                'QHBoxLayout': content.count('QHBoxLayout(')
            }
            
            # Check for specific UI elements
            specific_elements = {
                'sentence_label': 'sentence_label' in content,
                'translation_label': 'translation_label' in content,
                'feedback_text': 'feedback_text' in content,
                'submit_button': 'submit_button' in content,
                'next_button': 'next_button' in content,
                'prev_button': 'prev_button' in content,
                'hint_button': 'hint_button' in content,
                'progress_bar': 'progress_bar' in content,
                'mode_combo': 'mode_combo' in content,
                'difficulty_combo': 'difficulty_combo' in content,
                'task_type_combo': 'task_type_combo' in content
            }
            
            # Check for event handlers
            event_handlers = {
                'submitAnswer': 'def submitAnswer' in content,
                'nextExercise': 'def nextExercise' in content,
                'prevExercise': 'def prevExercise' in content,
                'provideHint': 'def provideHint' in content,
                'updateExercise': 'def updateExercise' in content,
                'generateNewExercise': 'def generateNewExercise' in content,
                'toggleTheme': 'def toggleTheme' in content,
                'toggleTranslation': 'def toggleTranslation' in content
            }
            
            ui_analysis = {
                'ui_components': ui_components,
                'specific_elements': specific_elements,
                'event_handlers': event_handlers,
                'total_ui_components': sum(ui_components.values()),
                'missing_elements': [elem for elem, found in specific_elements.items() if not found],
                'missing_handlers': [handler for handler, found in event_handlers.items() if not found]
            }
            
        except Exception as e:
            ui_analysis['error'] = str(e)
        
        self.results['ui_components'] = ui_analysis
        
        if ui_analysis.get('missing_elements'):
            self.results['critical_issues'].append(f"Missing UI elements: {ui_analysis['missing_elements']}")
        
        if ui_analysis.get('missing_handlers'):
            self.results['critical_issues'].append(f"Missing event handlers: {ui_analysis['missing_handlers']}")
        
        logger.info(f"UI analysis completed. Found {ui_analysis.get('total_ui_components', 0)} UI components")
    
    def analyze_exercise_workflow(self):
        """Analyze exercise generation and management workflow"""
        logger.info("Analyzing exercise workflow...")
        
        workflow_analysis = {}
        
        try:
            with open('main.py', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check exercise workflow methods
            workflow_methods = {
                'generateNewExercise': 'def generateNewExercise' in content,
                'handleNewExerciseResult': 'def handleNewExerciseResult' in content,
                'updateExercise': 'def updateExercise' in content,
                'submitAnswer': 'def submitAnswer' in content,
                'getUserAnswer': 'def getUserAnswer' in content,
                'generateGPTExplanationAsync': 'def generateGPTExplanationAsync' in content,
                'populateMultipleChoice': 'def populateMultipleChoice' in content,
                'switchMode': 'def switchMode' in content
            }
            
            # Check data structures
            data_structures = {
                'exercises_list': 'self.exercises' in content,
                'current_exercise': 'self.current_exercise' in content,
                'total_exercises': 'self.total_exercises' in content,
                'correct_count': 'self.correct_count' in content,
                'session_stats': 'self.session_stats' in content,
                'responses': 'self.responses' in content
            }
            
            # Check exercise types
            exercise_types = {
                'traditional': 'traditional' in content or 'Traditional' in content,
                'tblt': 'tblt' in content or 'TBLT' in content,
                'contrast': 'contrast' in content or 'Contrast' in content,
                'review': 'review' in content or 'Review' in content
            }
            
            # Check validation logic
            validation_checks = {
                'tense_selection': 'getSelectedTenses' in content,
                'person_selection': 'getSelectedPersons' in content,
                'trigger_selection': 'getSelectedTriggers' in content,
                'input_validation': 'len(answer) > 100' in content or 'strip()' in content,
                'answer_comparison': 'user_answer == correct_answer' in content or 'lower()' in content
            }
            
            workflow_analysis = {
                'workflow_methods': workflow_methods,
                'data_structures': data_structures,
                'exercise_types': exercise_types,
                'validation_checks': validation_checks,
                'missing_methods': [method for method, found in workflow_methods.items() if not found],
                'missing_structures': [struct for struct, found in data_structures.items() if not found],
                'available_types': [ex_type for ex_type, available in exercise_types.items() if available]
            }
            
        except Exception as e:
            workflow_analysis['error'] = str(e)
        
        self.results['exercise_workflow'] = workflow_analysis
        
        if workflow_analysis.get('missing_methods'):
            self.results['critical_issues'].append(f"Missing workflow methods: {workflow_analysis['missing_methods']}")
        
        logger.info(f"Exercise workflow analysis completed. Found {len(workflow_analysis.get('available_types', []))} exercise types")
    
    def analyze_enhancement_modules(self):
        """Analyze enhancement module integration"""
        logger.info("Analyzing enhancement modules...")
        
        enhancement_analysis = {}
        
        # Check src directory modules
        src_modules = {}
        if os.path.exists('src'):
            for filename in os.listdir('src'):
                if filename.endswith('.py') and filename != '__init__.py':
                    module_name = filename[:-3]  # Remove .py
                    src_modules[module_name] = {
                        'file_exists': True,
                        'importable': False,
                        'integrated': False
                    }
                    
                    # Test importability
                    try:
                        exec(f"from src.{module_name} import *")
                        src_modules[module_name]['importable'] = True
                    except Exception as e:
                        src_modules[module_name]['import_error'] = str(e)
                    
                    # Check integration in main.py
                    try:
                        with open('main.py', 'r', encoding='utf-8') as f:
                            main_content = f.read()
                        
                        if f"from src.{module_name}" in main_content:
                            src_modules[module_name]['integrated'] = True
                    except Exception:
                        pass
        
        # Check analytics modules
        analytics_modules = {}
        analytics_files = ['learning_analytics.py', 'session_manager.py']
        
        for filename in analytics_files:
            if os.path.exists(filename):
                module_name = filename[:-3]
                analytics_modules[module_name] = {
                    'file_exists': True,
                    'importable': False,
                    'integrated': False
                }
                
                # Test importability
                try:
                    exec(f"import {module_name}")
                    analytics_modules[module_name]['importable'] = True
                except Exception as e:
                    analytics_modules[module_name]['import_error'] = str(e)
                
                # Check integration
                try:
                    with open('main.py', 'r', encoding='utf-8') as f:
                        main_content = f.read()
                    
                    if f"from {module_name}" in main_content or f"import {module_name}" in main_content:
                        analytics_modules[module_name]['integrated'] = True
                except Exception:
                    pass
            else:
                analytics_modules[filename[:-3]] = {'file_exists': False}
        
        enhancement_analysis = {
            'src_modules': src_modules,
            'analytics_modules': analytics_modules,
            'total_src_modules': len(src_modules),
            'importable_src_modules': sum(1 for m in src_modules.values() if m.get('importable')),
            'integrated_src_modules': sum(1 for m in src_modules.values() if m.get('integrated')),
            'importable_analytics_modules': sum(1 for m in analytics_modules.values() if m.get('importable')),
            'integrated_analytics_modules': sum(1 for m in analytics_modules.values() if m.get('integrated'))
        }
        
        self.results['enhancement_modules'] = enhancement_analysis
        logger.info(f"Enhancement module analysis completed. Found {len(src_modules)} src modules")
    
    def identify_critical_issues(self):
        """Identify critical issues that need immediate attention"""
        logger.info("Identifying critical issues...")
        
        critical_issues = []
        
        # Check startup issues
        startup = self.results.get('startup_analysis', {})
        if not startup.get('main_file_exists'):
            critical_issues.append("CRITICAL: main.py file not found")
        
        dependencies = startup.get('dependencies', {})
        missing_deps = [dep for dep, available in dependencies.items() if not available]
        if 'PyQt5' in missing_deps:
            critical_issues.append("CRITICAL: PyQt5 not available - GUI will not work")
        if 'openai' in missing_deps:
            critical_issues.append("CRITICAL: OpenAI library not available - exercise generation will fail")
        
        # Check UI issues
        ui_components = self.results.get('ui_components', {})
        missing_elements = ui_components.get('missing_elements', [])
        if 'submit_button' in missing_elements:
            critical_issues.append("CRITICAL: Submit button not found")
        if 'sentence_label' in missing_elements:
            critical_issues.append("CRITICAL: Sentence display label not found")
        
        missing_handlers = ui_components.get('missing_handlers', [])
        if 'submitAnswer' in missing_handlers:
            critical_issues.append("CRITICAL: Submit answer handler not found")
        if 'generateNewExercise' in missing_handlers:
            critical_issues.append("CRITICAL: Exercise generation handler not found")
        
        # Check workflow issues
        workflow = self.results.get('exercise_workflow', {})
        missing_methods = workflow.get('missing_methods', [])
        if missing_methods:
            critical_issues.append(f"CRITICAL: Missing workflow methods: {missing_methods}")
        
        missing_structures = workflow.get('missing_structures', [])
        if 'exercises_list' in missing_structures:
            critical_issues.append("CRITICAL: Exercise data structure not found")
        
        # Add to results
        self.results['critical_issues'].extend(critical_issues)
        
        logger.info(f"Identified {len(critical_issues)} critical issues")
    
    def generate_recommendations(self):
        """Generate recommendations based on analysis"""
        logger.info("Generating recommendations...")
        
        recommendations = []
        
        # Startup recommendations
        startup = self.results.get('startup_analysis', {})
        missing_deps = [dep for dep, available in startup.get('dependencies', {}).items() if not available]
        if missing_deps:
            recommendations.append(f"📦 Install missing dependencies: {', '.join(missing_deps)}")
        
        if not startup.get('config_files', {}).get('.env'):
            recommendations.append("🔐 Create .env file with OpenAI API key for full functionality")
        
        # UI recommendations
        ui_components = self.results.get('ui_components', {})
        if ui_components.get('total_ui_components', 0) < 20:
            recommendations.append("🎨 Consider expanding UI components for better user experience")
        
        # Enhancement module recommendations
        enhancement = self.results.get('enhancement_modules', {})
        total_src = enhancement.get('total_src_modules', 0)
        importable_src = enhancement.get('importable_src_modules', 0)
        
        if total_src > 0 and importable_src < total_src:
            recommendations.append(f"🔧 Fix import issues in {total_src - importable_src} src modules")
        
        integrated_src = enhancement.get('integrated_src_modules', 0)
        if importable_src > integrated_src:
            recommendations.append(f"🔗 Integrate {importable_src - integrated_src} available enhancement modules")
        
        # Code quality recommendations
        structure = self.results.get('code_structure', {})
        main_file = structure.get('main_file', {})
        if main_file.get('lines_of_code', 0) > 1500:
            recommendations.append("📝 Consider refactoring main.py - it's getting large (>1500 lines)")
        
        # Security recommendations
        if 'python-dotenv' in startup.get('dependencies', {}):
            recommendations.append("🔒 Environment variable loading detected - ensure secure API key management")
        
        self.results['recommendations'] = recommendations
        logger.info(f"Generated {len(recommendations)} recommendations")
    
    def run_comprehensive_analysis(self):
        """Run all analysis components"""
        logger.info("Starting comprehensive application analysis...")
        
        start_time = time.time()
        
        # Run all analysis components
        self.analyze_application_startup()
        self.analyze_code_structure()
        self.analyze_ui_components()
        self.analyze_exercise_workflow()
        self.analyze_enhancement_modules()
        self.identify_critical_issues()
        self.generate_recommendations()
        
        execution_time = time.time() - start_time
        
        # Add summary
        self.results['analysis_summary'] = {
            'execution_time': round(execution_time, 3),
            'timestamp': datetime.now().isoformat(),
            'total_critical_issues': len(self.results['critical_issues']),
            'total_recommendations': len(self.results['recommendations'])
        }
        
        logger.info(f"Comprehensive analysis completed in {execution_time:.3f}s")
        return self.results
    
    def save_report(self, filename: str = None):
        """Save analysis report to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tests/functional_analysis_report_{timestamp}.json"
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        return filename
    
    def print_report(self):
        """Print analysis report to console"""
        print("\n" + "="*80)
        print("FUNCTIONAL ANALYSIS REPORT - Spanish Subjunctive Practice Application")
        print("="*80)
        
        # Summary
        summary = self.results.get('analysis_summary', {})
        print(f"\n📊 ANALYSIS SUMMARY:")
        print(f"   Execution Time:     {summary.get('execution_time', 0)}s")
        print(f"   Critical Issues:    {summary.get('total_critical_issues', 0)}")
        print(f"   Recommendations:    {summary.get('total_recommendations', 0)}")
        
        # Startup Analysis
        startup = self.results.get('startup_analysis', {})
        print(f"\n🚀 STARTUP ANALYSIS:")
        print(f"   Main File Exists:   {startup.get('main_file_exists', False)}")
        if startup.get('dependencies'):
            deps = startup['dependencies']
            available_deps = sum(1 for available in deps.values() if available)
            total_deps = len(deps)
            print(f"   Dependencies:       {available_deps}/{total_deps} available")
            
            missing = [dep for dep, avail in deps.items() if not avail]
            if missing:
                print(f"   Missing:            {', '.join(missing)}")
        
        # Code Structure
        structure = self.results.get('code_structure', {})
        main_file = structure.get('main_file', {})
        if main_file:
            print(f"\n🏗️  CODE STRUCTURE:")
            print(f"   Classes:            {main_file.get('classes', 0)}")
            print(f"   Methods:            {main_file.get('methods', 0)}")
            print(f"   Lines of Code:      {main_file.get('lines_of_code', 0)}")
            
        src_modules = structure.get('src_modules', {})
        if src_modules:
            print(f"   Enhancement Modules: {len(src_modules)} found")
        
        # UI Components
        ui = self.results.get('ui_components', {})
        if ui:
            print(f"\n🎨 UI COMPONENTS:")
            print(f"   Total Components:   {ui.get('total_ui_components', 0)}")
            
            missing_elements = ui.get('missing_elements', [])
            if missing_elements:
                print(f"   Missing Elements:   {', '.join(missing_elements)}")
            
            missing_handlers = ui.get('missing_handlers', [])
            if missing_handlers:
                print(f"   Missing Handlers:   {', '.join(missing_handlers)}")
        
        # Exercise Workflow
        workflow = self.results.get('exercise_workflow', {})
        if workflow:
            print(f"\n⚙️  EXERCISE WORKFLOW:")
            available_types = workflow.get('available_types', [])
            print(f"   Exercise Types:     {', '.join(available_types) if available_types else 'None found'}")
            
            missing_methods = workflow.get('missing_methods', [])
            if missing_methods:
                print(f"   Missing Methods:    {', '.join(missing_methods)}")
        
        # Enhancement Modules
        enhancement = self.results.get('enhancement_modules', {})
        if enhancement:
            print(f"\n🔧 ENHANCEMENT MODULES:")
            total_src = enhancement.get('total_src_modules', 0)
            importable_src = enhancement.get('importable_src_modules', 0)
            integrated_src = enhancement.get('integrated_src_modules', 0)
            
            print(f"   Source Modules:     {total_src} total, {importable_src} importable, {integrated_src} integrated")
            
            importable_analytics = enhancement.get('importable_analytics_modules', 0)
            integrated_analytics = enhancement.get('integrated_analytics_modules', 0)
            print(f"   Analytics Modules:  {importable_analytics} importable, {integrated_analytics} integrated")
        
        # Critical Issues
        critical = self.results.get('critical_issues', [])
        if critical:
            print(f"\n🚨 CRITICAL ISSUES:")
            for issue in critical:
                print(f"   - {issue}")
        
        # Recommendations
        recommendations = self.results.get('recommendations', [])
        if recommendations:
            print(f"\n💡 RECOMMENDATIONS:")
            for rec in recommendations:
                print(f"   {rec}")
        
        print("\n" + "="*80)


def main():
    """Main execution function"""
    # Change to project directory
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Run analysis
    analyzer = TestAnalysis()
    results = analyzer.run_comprehensive_analysis()
    
    # Save report
    report_file = analyzer.save_report()
    
    # Print report
    analyzer.print_report()
    
    print(f"\nDetailed report saved to: {report_file}")
    
    # Return analysis results
    return results


if __name__ == "__main__":
    results = main()