"""
UI Performance Integration Module

This module provides easy integration of performance optimizations 
with the existing Spanish Subjunctive Practice application.

Usage:
    from src.ui_integration import integrate_performance_optimizations
    integrate_performance_optimizations(your_main_window)
"""

import sys
import weakref
from typing import Dict, Any, Optional
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer

from .ui_performance import (
    apply_performance_optimizations,
    BatchedUpdateManager,
    PerformantLabel, 
    PerformantTextEdit,
    PerformantProgressBar,
    OptimizedWidgetFactory,
    PerformanceProfiler,
    ResponsiveUIManager,
    throttle_updates,
    measure_performance
)


class MainWindowOptimizer:
    """
    Applies specific optimizations to the Spanish Subjunctive Practice main window
    """
    
    def __init__(self, main_window):
        self.main_window = weakref.ref(main_window)
        self.original_methods = {}
        self.batch_manager = BatchedUpdateManager()
        
    def optimize_main_window(self):
        """Apply all optimizations to the main window"""
        window = self.main_window()
        if not window:
            return
            
        # Optimize core UI update methods
        self._optimize_update_methods(window)
        
        # Optimize exercise display
        self._optimize_exercise_display(window)
        
        # Optimize statistics display
        self._optimize_stats_display(window)
        
        # Add performance monitoring
        self._add_performance_monitoring(window)
        
        print("Main window optimizations applied successfully!")
    
    def _optimize_update_methods(self, window):
        """Optimize frequently called update methods"""
        # Throttle updateStats to prevent excessive calls
        if hasattr(window, 'updateStats'):
            window.updateStats = throttle_updates(0.2)(window.updateStats)
        
        # Throttle updateStatus
        if hasattr(window, 'updateStatus'):
            window.updateStatus = throttle_updates(0.1)(window.updateStatus)
        
        # Optimize updateExercise with batching
        if hasattr(window, 'updateExercise'):
            original_update = window.updateExercise
            
            @measure_performance
            def optimized_update_exercise():
                # Batch multiple UI updates together
                def batch_update():
                    if hasattr(window, 'sentence_label') and window.sentence_label:
                        exercise = window.exercises[window.current_exercise] if window.exercises else {}
                        if "context" in exercise and exercise["context"]:
                            full_text = exercise["context"] + "\n\n" + exercise.get("sentence", "")
                        else:
                            full_text = exercise.get("sentence", "")
                        
                        # Use batched update for sentence
                        self.batch_manager.schedule_update(
                            window.sentence_label,
                            lambda w: w.setText(full_text),
                            priority=10
                        )
                    
                    # Update translation with batching
                    if hasattr(window, 'translation_label') and window.translation_label:
                        translation_text = ""
                        if (window.show_translation and window.exercises and 
                            window.current_exercise < len(window.exercises)):
                            exercise = window.exercises[window.current_exercise]
                            translation_text = exercise.get("translation", "")
                        
                        self.batch_manager.schedule_update(
                            window.translation_label,
                            lambda w: w.setText(translation_text),
                            priority=8
                        )
                    
                    # Update progress bar efficiently
                    if hasattr(window, 'progress_bar') and window.progress_bar:
                        value = window.current_exercise + 1 if window.exercises else 0
                        self.batch_manager.schedule_update(
                            window.progress_bar,
                            lambda w: w.setValue(value),
                            priority=5
                        )
                
                batch_update()
                
                # Call remaining original logic that doesn't involve UI updates
                try:
                    # Extract non-UI logic from original method if needed
                    if hasattr(window, 'updateStats'):
                        window.updateStats()
                except Exception as e:
                    print(f"Error in optimized update: {e}")
                    # Fallback to original
                    original_update()
            
            window.updateExercise = optimized_update_exercise
    
    def _optimize_exercise_display(self, window):
        """Optimize exercise display updates"""
        # Replace sentence label with optimized version if possible
        if hasattr(window, 'sentence_label') and window.sentence_label:
            # Would need careful widget replacement in practice
            pass
        
        # Optimize feedback text updates
        if hasattr(window, 'feedback_text') and window.feedback_text:
            original_set_text = window.feedback_text.setText
            
            @throttle_updates(0.05)  # 50ms throttle for feedback
            def optimized_set_feedback_text(text):
                return original_set_text(text)
            
            window.feedback_text.setText = optimized_set_feedback_text
    
    def _optimize_stats_display(self, window):
        """Optimize statistics display updates"""
        if hasattr(window, 'stats_label') and window.stats_label:
            original_set_text = window.stats_label.setText
            last_stats_text = ""
            
            def optimized_stats_update(text):
                nonlocal last_stats_text
                if text != last_stats_text:
                    last_stats_text = text
                    self.batch_manager.schedule_update(
                        window.stats_label,
                        lambda w: original_set_text(text),
                        priority=3
                    )
            
            # Replace the setText method
            window.stats_label.setText = optimized_stats_update
    
    def _add_performance_monitoring(self, window):
        """Add performance monitoring to the window"""
        # Add performance metrics to status bar
        if hasattr(window, 'status_bar') and window.status_bar:
            # Create a performance info updater
            def update_performance_info():
                try:
                    from .ui_performance import profiler
                    summary = profiler.get_summary()
                    if summary['total_operations'] > 0:
                        perf_text = f"UI Ops: {summary['total_operations']} | Cache: {summary['cache_hit_ratio']:.1%}"
                        # Only update if different to avoid spam
                        current_message = window.status_bar.currentMessage()
                        if not current_message.startswith("UI Ops:"):
                            QTimer.singleShot(100, lambda: window.status_bar.showMessage(perf_text, 2000))
                except Exception as e:
                    pass  # Silently handle errors
            
            # Update performance info periodically
            perf_timer = QTimer()
            perf_timer.timeout.connect(update_performance_info)
            perf_timer.start(5000)  # Every 5 seconds
            
            # Keep reference to prevent garbage collection
            window._performance_timer = perf_timer


class AsyncOperationManager:
    """
    Manages async operations for the Spanish Subjunctive Practice app
    """
    
    def __init__(self, main_window):
        self.main_window = weakref.ref(main_window)
        self.ui_manager = ResponsiveUIManager()
    
    def optimize_gpt_calls(self):
        """Optimize GPT API calls to be non-blocking"""
        window = self.main_window()
        if not window:
            return
        
        # Optimize generateNewExercise method
        if hasattr(window, 'generateNewExercise'):
            original_generate = window.generateNewExercise
            
            def async_generate_exercise():
                # Show loading state immediately
                window.updateStatus("Generating exercises...")
                if hasattr(window, 'submit_button'):
                    window.submit_button.setEnabled(False)
                
                def background_operation():
                    # This would contain the heavy lifting
                    # For now, just call original method
                    try:
                        original_generate()
                    except Exception as e:
                        return f"Error: {e}"
                    return "Success"
                
                def completion_callback(result):
                    # Re-enable UI
                    if hasattr(window, 'submit_button'):
                        window.submit_button.setEnabled(True)
                    
                    if result != "Success":
                        window.updateStatus(f"Generation failed: {result}")
                
                # Run in background
                self.ui_manager.run_async(background_operation, completion_callback)
            
            window.generateNewExercise = async_generate_exercise
    
    def optimize_answer_submission(self):
        """Optimize answer submission to be more responsive"""
        window = self.main_window()
        if not window:
            return
        
        if hasattr(window, 'submitAnswer'):
            original_submit = window.submitAnswer
            
            @measure_performance
            def optimized_submit_answer():
                # Immediate UI feedback
                user_answer = window.getUserAnswer() if hasattr(window, 'getUserAnswer') else ""
                if not user_answer:
                    window.updateStatus("Please provide an answer.")
                    return
                
                # Show processing state
                window.updateStatus("Processing answer...")
                if hasattr(window, 'submit_button'):
                    window.submit_button.setText("Processing...")
                    window.submit_button.setEnabled(False)
                
                def restore_ui():
                    if hasattr(window, 'submit_button'):
                        window.submit_button.setText("Submit")
                        window.submit_button.setEnabled(True)
                
                try:
                    # Call original method
                    original_submit()
                    QTimer.singleShot(100, restore_ui)  # Restore UI after brief delay
                except Exception as e:
                    print(f"Error in submit answer: {e}")
                    restore_ui()
            
            window.submitAnswer = optimized_submit_answer


def integrate_performance_optimizations(main_window: QMainWindow) -> Dict[str, Any]:
    """
    Main integration function to apply all performance optimizations
    
    Args:
        main_window: The main application window
        
    Returns:
        Dictionary with optimization results and managers
    """
    
    print("Integrating UI performance optimizations...")
    
    # Apply global optimizations
    apply_performance_optimizations(main_window)
    
    # Create and apply main window specific optimizations
    window_optimizer = MainWindowOptimizer(main_window)
    window_optimizer.optimize_main_window()
    
    # Setup async operation management
    async_manager = AsyncOperationManager(main_window)
    async_manager.optimize_gpt_calls()
    async_manager.optimize_answer_submission()
    
    # Add cleanup on window close
    original_close = main_window.closeEvent
    
    def optimized_close_event(event):
        # Clean up performance managers
        try:
            from .ui_performance import batch_manager, ui_manager
            ui_manager.wait_for_completion(1000)  # Wait up to 1 second
            batch_manager._update_timer.stop()
        except Exception as e:
            print(f"Cleanup error: {e}")
        
        # Call original close event
        original_close(event)
    
    main_window.closeEvent = optimized_close_event
    
    print("✅ UI performance optimizations integrated successfully!")
    
    return {
        'window_optimizer': window_optimizer,
        'async_manager': async_manager,
        'status': 'success',
        'optimizations_applied': [
            'Batched widget updates',
            'Throttled UI operations', 
            'Async GPT operations',
            'Optimized event handling',
            'Performance monitoring',
            'Memory-efficient caching'
        ]
    }


def get_optimization_recommendations(main_window: QMainWindow) -> Dict[str, Any]:
    """
    Analyze the main window and provide optimization recommendations
    
    Args:
        main_window: The main application window
        
    Returns:
        Dictionary with recommendations and analysis
    """
    
    recommendations = {
        'critical': [],
        'important': [],
        'nice_to_have': [],
        'analysis': {}
    }
    
    # Analyze widget hierarchy
    all_widgets = main_window.findChildren(object)
    widget_counts = {}
    for widget in all_widgets:
        widget_type = type(widget).__name__
        widget_counts[widget_type] = widget_counts.get(widget_type, 0) + 1
    
    recommendations['analysis']['widget_counts'] = widget_counts
    recommendations['analysis']['total_widgets'] = len(all_widgets)
    
    # Check for potential issues
    if widget_counts.get('QLabel', 0) > 20:
        recommendations['important'].append(
            "High number of QLabel widgets - consider using PerformantLabel for frequently updated ones"
        )
    
    if widget_counts.get('QTextEdit', 0) > 5:
        recommendations['critical'].append(
            "Multiple QTextEdit widgets - replace with PerformantTextEdit for better performance"
        )
    
    # Check for threading
    if hasattr(main_window, 'threadpool'):
        recommendations['analysis']['uses_threading'] = True
        recommendations['nice_to_have'].append(
            "Already uses threading - optimize with ResponsiveUIManager"
        )
    else:
        recommendations['critical'].append(
            "No threading detected - implement async operations for GPT calls"
        )
    
    # Check update methods
    update_methods = ['updateExercise', 'updateStats', 'updateStatus']
    for method in update_methods:
        if hasattr(main_window, method):
            recommendations['important'].append(
                f"Optimize {method} with batching and throttling"
            )
    
    return recommendations


# Convenience function for easy integration
def quick_optimize(main_window: QMainWindow) -> bool:
    """
    Quick optimization function that applies the most impactful optimizations
    
    Args:
        main_window: The main application window
        
    Returns:
        True if successful, False otherwise
    """
    try:
        result = integrate_performance_optimizations(main_window)
        return result['status'] == 'success'
    except Exception as e:
        print(f"Quick optimization failed: {e}")
        return False


if __name__ == "__main__":
    print("UI Performance Integration Module")
    print("Usage: from src.ui_integration import integrate_performance_optimizations")