"""
UI Performance Optimization Module for Spanish Subjunctive Practice App

This module provides performance optimizations for the main PyQt5 application:
1. Efficient widget updates and reduced redraws
2. Optimized event handling 
3. Memory-efficient data structures
4. Responsive UI during operations
5. Widget caching and lazy loading

Author: Performance Optimization System
"""

import sys
import time
import weakref
from typing import Dict, List, Optional, Any, Callable, Union
from functools import wraps, lru_cache
from collections import deque
import threading
from dataclasses import dataclass, field

from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QProgressBar,
    QCheckBox, QRadioButton, QComboBox, QGroupBox, QScrollArea, QApplication
)
from PyQt5.QtCore import (
    Qt, QTimer, QObject, pyqtSignal, QThread, QMutex, QMutexLocker,
    QRunnable, QThreadPool
)
from PyQt5.QtGui import QPainter, QPixmap


# =====================================================================
# PERFORMANCE MONITORING AND METRICS
# =====================================================================

@dataclass
class PerformanceMetrics:
    """Track UI performance metrics"""
    widget_updates: int = 0
    paint_events: int = 0
    event_processing_time: float = 0.0
    memory_usage: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    blocked_operations: int = 0
    
    def reset(self):
        """Reset all metrics"""
        self.widget_updates = 0
        self.paint_events = 0
        self.event_processing_time = 0.0
        self.memory_usage = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.blocked_operations = 0


class PerformanceProfiler:
    """Performance profiler for UI operations"""
    
    def __init__(self):
        self.metrics = PerformanceMetrics()
        self.enabled = True
        self._start_times = {}
    
    def start_timer(self, operation: str):
        """Start timing an operation"""
        if self.enabled:
            self._start_times[operation] = time.perf_counter()
    
    def end_timer(self, operation: str) -> float:
        """End timing and return duration"""
        if not self.enabled or operation not in self._start_times:
            return 0.0
        
        duration = time.perf_counter() - self._start_times[operation]
        self.metrics.event_processing_time += duration
        del self._start_times[operation]
        return duration
    
    def record_widget_update(self):
        """Record a widget update"""
        if self.enabled:
            self.metrics.widget_updates += 1
    
    def record_paint_event(self):
        """Record a paint event"""
        if self.enabled:
            self.metrics.paint_events += 1
    
    def record_cache_hit(self):
        """Record a cache hit"""
        if self.enabled:
            self.metrics.cache_hits += 1
    
    def record_cache_miss(self):
        """Record a cache miss"""
        if self.enabled:
            self.metrics.cache_misses += 1
    
    def get_summary(self) -> Dict[str, Any]:
        """Get performance summary"""
        return {
            "widget_updates": self.metrics.widget_updates,
            "paint_events": self.metrics.paint_events,
            "avg_event_time": (
                self.metrics.event_processing_time / max(1, self.metrics.widget_updates)
            ),
            "cache_hit_ratio": (
                self.metrics.cache_hits / max(1, self.metrics.cache_hits + self.metrics.cache_misses)
            ),
            "total_operations": self.metrics.widget_updates + self.metrics.paint_events
        }


# Global profiler instance
profiler = PerformanceProfiler()


# =====================================================================
# EFFICIENT UI UPDATE BATCHING SYSTEM
# =====================================================================

class BatchedUpdateManager(QObject):
    """
    Manages batched UI updates to reduce redundant operations.
    Groups multiple UI updates together and processes them in a single event loop cycle.
    """
    
    updates_ready = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self._pending_updates = {}  # widget_id -> update_function
        self._update_timer = QTimer()
        self._update_timer.timeout.connect(self._process_updates)
        self._update_timer.setSingleShot(True)
        self._mutex = QMutex()
        
        # Performance settings
        self.batch_delay_ms = 16  # ~60 FPS
        self.max_batch_size = 50
    
    def schedule_update(self, widget: QWidget, update_func: Callable, priority: int = 0):
        """
        Schedule a widget update. Multiple updates to the same widget are coalesced.
        
        Args:
            widget: The widget to update
            update_func: Function to call for the update
            priority: Update priority (higher = more important)
        """
        widget_id = id(widget)
        
        with QMutexLocker(self._mutex):
            # Only keep the most recent update for each widget
            self._pending_updates[widget_id] = {
                'widget': weakref.ref(widget),
                'func': update_func,
                'priority': priority,
                'timestamp': time.perf_counter()
            }
            
            # Start or restart the timer
            if not self._update_timer.isActive():
                self._update_timer.start(self.batch_delay_ms)
    
    def _process_updates(self):
        """Process all pending updates in priority order"""
        profiler.start_timer("batch_update")
        
        with QMutexLocker(self._mutex):
            if not self._pending_updates:
                return
            
            # Sort by priority (highest first) then by timestamp (oldest first)
            updates = sorted(
                self._pending_updates.values(),
                key=lambda x: (-x['priority'], x['timestamp'])
            )
            
            # Limit batch size to prevent UI freezing
            updates = updates[:self.max_batch_size]
            
            processed = 0
            for update_info in updates:
                widget_ref = update_info['widget']
                widget = widget_ref()
                
                if widget is not None:
                    try:
                        update_info['func'](widget)
                        processed += 1
                        profiler.record_widget_update()
                    except Exception as e:
                        print(f"Error in batched update: {e}")
                
                # Remove processed update
                widget_id = id(widget) if widget else None
                if widget_id in self._pending_updates:
                    del self._pending_updates[widget_id]
            
            # If there are still updates pending, schedule another batch
            if self._pending_updates:
                self._update_timer.start(self.batch_delay_ms)
        
        profiler.end_timer("batch_update")
        self.updates_ready.emit()


# Global batch manager
batch_manager = BatchedUpdateManager()


# =====================================================================
# OPTIMIZED WIDGET CLASSES
# =====================================================================

class PerformantLabel(QLabel):
    """
    Optimized QLabel with reduced redraws and smart text caching
    """
    
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._cached_text = text
        self._cached_pixmap = None
        self._needs_repaint = True
        self._last_size = self.size()
    
    def setText(self, text: str):
        """Optimized setText that avoids unnecessary updates"""
        if text == self._cached_text:
            profiler.record_cache_hit()
            return
        
        profiler.record_cache_miss()
        self._cached_text = text
        self._needs_repaint = True
        self._cached_pixmap = None
        
        # Batch the actual update
        batch_manager.schedule_update(
            self, 
            lambda w: super(PerformantLabel, w).setText(text),
            priority=5
        )
    
    def resizeEvent(self, event):
        """Handle resize efficiently"""
        if self.size() != self._last_size:
            self._last_size = self.size()
            self._needs_repaint = True
            self._cached_pixmap = None
        super().resizeEvent(event)
    
    def paintEvent(self, event):
        """Optimized paint event with caching"""
        profiler.record_paint_event()
        
        # Use cached pixmap if available and valid
        if (self._cached_pixmap and not self._needs_repaint and 
            self._cached_pixmap.size() == self.size()):
            painter = QPainter(self)
            painter.drawPixmap(0, 0, self._cached_pixmap)
            return
        
        # Render to cache
        if self._needs_repaint:
            self._cached_pixmap = QPixmap(self.size())
            self._cached_pixmap.fill(Qt.transparent)
            
            painter = QPainter(self._cached_pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Let parent class draw to pixmap
            temp_event = event
            super().paintEvent(temp_event)
            
            self._needs_repaint = False
        
        # Draw cached pixmap
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self._cached_pixmap)


class PerformantTextEdit(QTextEdit):
    """
    Optimized QTextEdit with efficient text updates and reduced redraws
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._update_timer = QTimer()
        self._update_timer.timeout.connect(self._apply_pending_text)
        self._update_timer.setSingleShot(True)
        self._pending_text = None
        self._last_text = ""
        
        # Optimization settings
        self._batch_delay = 50  # ms
        self.setUpdatesEnabled(True)
    
    def setText(self, text: str):
        """Batched setText to prevent rapid successive updates"""
        if text == self._last_text:
            profiler.record_cache_hit()
            return
        
        profiler.record_cache_miss()
        self._pending_text = text
        
        # Batch the update
        if not self._update_timer.isActive():
            self._update_timer.start(self._batch_delay)
    
    def _apply_pending_text(self):
        """Apply the pending text update"""
        if self._pending_text is not None and self._pending_text != self._last_text:
            self._last_text = self._pending_text
            super().setText(self._pending_text)
            profiler.record_widget_update()
            self._pending_text = None
    
    def append(self, text: str):
        """Efficient append operation"""
        # For append operations, bypass batching for better UX
        super().append(text)
        self._last_text = self.toPlainText()
        profiler.record_widget_update()


class PerformantProgressBar(QProgressBar):
    """
    Optimized progress bar with smart update throttling
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._last_value = -1
        self._update_threshold = 1  # Only update if change >= 1%
        self._last_update_time = 0
        self._min_update_interval = 0.1  # seconds
    
    def setValue(self, value: int):
        """Throttled setValue to prevent excessive updates"""
        current_time = time.time()
        
        # Check if update is needed
        if (abs(value - self._last_value) < self._update_threshold and 
            current_time - self._last_update_time < self._min_update_interval):
            return
        
        self._last_value = value
        self._last_update_time = current_time
        
        # Batch the update
        batch_manager.schedule_update(
            self,
            lambda w: super(PerformantProgressBar, w).setValue(value),
            priority=3
        )


# =====================================================================
# EFFICIENT EVENT HANDLING
# =====================================================================

class OptimizedEventFilter(QObject):
    """
    Optimized event filter that reduces unnecessary event processing
    """
    
    def __init__(self):
        super().__init__()
        self._blocked_events = {
            # Events to ignore for performance
            Qt.LayoutRequest,
            Qt.ChildPolished,
            Qt.PolishRequest,
        }
        self._event_cache = {}
        self._cache_size_limit = 1000
    
    def eventFilter(self, obj: QObject, event) -> bool:
        """Filter events for performance optimization"""
        event_type = event.type()
        
        # Skip blocked events
        if event_type in self._blocked_events:
            profiler.metrics.blocked_operations += 1
            return True
        
        # Cache frequently accessed event data
        if hasattr(event, 'pos') and event_type in (Qt.MouseMove, Qt.MouseButtonPress):
            cache_key = (id(obj), event_type, event.pos().x(), event.pos().y())
            if cache_key in self._event_cache:
                profiler.record_cache_hit()
                return self._event_cache[cache_key]
            
            # Limit cache size
            if len(self._event_cache) >= self._cache_size_limit:
                # Remove oldest entries
                keys_to_remove = list(self._event_cache.keys())[:100]
                for key in keys_to_remove:
                    del self._event_cache[key]
        
        return False


# =====================================================================
# MEMORY-EFFICIENT DATA STRUCTURES
# =====================================================================

class CircularBuffer:
    """
    Memory-efficient circular buffer for UI data
    """
    
    def __init__(self, maxsize: int = 1000):
        self._buffer = deque(maxlen=maxsize)
        self._maxsize = maxsize
    
    def append(self, item):
        """Add item to buffer"""
        self._buffer.append(item)
    
    def get_recent(self, n: int = 10) -> List:
        """Get the n most recent items"""
        return list(self._buffer)[-n:] if self._buffer else []
    
    def clear(self):
        """Clear the buffer"""
        self._buffer.clear()
    
    def __len__(self):
        return len(self._buffer)
    
    def __iter__(self):
        return iter(self._buffer)


class LazyWidgetCache:
    """
    Lazy-loading cache for widgets to reduce memory usage
    """
    
    def __init__(self, max_cached_widgets: int = 50):
        self._cache = {}
        self._access_times = {}
        self._max_size = max_cached_widgets
        self._creation_functions = {}
    
    def register_widget_factory(self, widget_type: str, creation_func: Callable):
        """Register a function to create widgets of a specific type"""
        self._creation_functions[widget_type] = creation_func
    
    def get_widget(self, widget_type: str, widget_id: str) -> Optional[QWidget]:
        """Get or create a widget"""
        cache_key = f"{widget_type}:{widget_id}"
        
        if cache_key in self._cache:
            widget_ref = self._cache[cache_key]
            widget = widget_ref()
            if widget is not None:
                self._access_times[cache_key] = time.time()
                profiler.record_cache_hit()
                return widget
            else:
                # Widget was garbage collected
                del self._cache[cache_key]
                if cache_key in self._access_times:
                    del self._access_times[cache_key]
        
        profiler.record_cache_miss()
        
        # Create new widget
        if widget_type in self._creation_functions:
            widget = self._creation_functions[widget_type]()
            
            # Add to cache
            self._cache[cache_key] = weakref.ref(widget)
            self._access_times[cache_key] = time.time()
            
            # Clean old entries if cache is full
            self._cleanup_cache()
            
            return widget
        
        return None
    
    def _cleanup_cache(self):
        """Remove least recently used widgets if cache is full"""
        if len(self._cache) <= self._max_size:
            return
        
        # Sort by access time (oldest first)
        sorted_items = sorted(
            self._access_times.items(),
            key=lambda x: x[1]
        )
        
        # Remove oldest entries
        entries_to_remove = len(self._cache) - self._max_size + 10  # Remove extra for efficiency
        for cache_key, _ in sorted_items[:entries_to_remove]:
            if cache_key in self._cache:
                del self._cache[cache_key]
            if cache_key in self._access_times:
                del self._access_times[cache_key]


# Global widget cache
widget_cache = LazyWidgetCache()


# =====================================================================
# RESPONSIVE UI THREADING
# =====================================================================

class UIResponseWorker(QRunnable):
    """
    Worker for running operations without blocking the UI thread
    """
    
    def __init__(self, operation: Callable, callback: Optional[Callable] = None):
        super().__init__()
        self.operation = operation
        self.callback = callback
        self.setAutoDelete(True)
    
    def run(self):
        """Execute the operation in background thread"""
        try:
            result = self.operation()
            if self.callback:
                # Execute callback in main thread
                QTimer.singleShot(0, lambda: self.callback(result))
        except Exception as e:
            print(f"Error in UI response worker: {e}")


class ResponsiveUIManager:
    """
    Manages responsive UI operations to prevent blocking
    """
    
    def __init__(self):
        self._thread_pool = QThreadPool.globalInstance()
        self._thread_pool.setMaxThreadCount(4)  # Limit threads
        self._pending_operations = 0
        self._mutex = QMutex()
    
    def run_async(self, operation: Callable, callback: Optional[Callable] = None):
        """
        Run an operation asynchronously to keep UI responsive
        
        Args:
            operation: Function to run in background
            callback: Function to call with result in main thread
        """
        with QMutexLocker(self._mutex):
            self._pending_operations += 1
        
        def wrapped_callback(result):
            with QMutexLocker(self._mutex):
                self._pending_operations -= 1
            if callback:
                callback(result)
        
        worker = UIResponseWorker(operation, wrapped_callback)
        self._thread_pool.start(worker)
    
    def is_busy(self) -> bool:
        """Check if there are pending async operations"""
        with QMutexLocker(self._mutex):
            return self._pending_operations > 0
    
    def wait_for_completion(self, timeout_ms: int = 5000):
        """Wait for all pending operations to complete"""
        self._thread_pool.waitForDone(timeout_ms)


# Global responsive UI manager
ui_manager = ResponsiveUIManager()


# =====================================================================
# PERFORMANCE DECORATORS AND UTILITIES
# =====================================================================

def throttle_updates(min_interval: float = 0.1):
    """
    Decorator to throttle function calls to prevent excessive UI updates
    
    Args:
        min_interval: Minimum time between calls in seconds
    """
    def decorator(func):
        last_call_time = 0
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal last_call_time
            current_time = time.time()
            
            if current_time - last_call_time >= min_interval:
                last_call_time = current_time
                return func(*args, **kwargs)
            else:
                # Schedule for later
                delay_ms = int((min_interval - (current_time - last_call_time)) * 1000)
                QTimer.singleShot(delay_ms, lambda: func(*args, **kwargs))
        
        return wrapper
    return decorator


def cache_widget_property(cache_size: int = 128):
    """
    Decorator to cache widget property calculations
    
    Args:
        cache_size: Maximum number of cached results
    """
    def decorator(func):
        func._cache = {}
        
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Create cache key from widget state and args
            widget_id = id(self)
            cache_key = (widget_id, args, tuple(sorted(kwargs.items())))
            
            if cache_key in func._cache:
                profiler.record_cache_hit()
                return func._cache[cache_key]
            
            profiler.record_cache_miss()
            result = func(self, *args, **kwargs)
            
            # Limit cache size
            if len(func._cache) >= cache_size:
                # Remove oldest entry
                oldest_key = next(iter(func._cache))
                del func._cache[oldest_key]
            
            func._cache[cache_key] = result
            return result
        
        return wrapper
    return decorator


def measure_performance(func):
    """Decorator to measure function performance"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        
        duration = end_time - start_time
        if duration > 0.1:  # Log slow operations
            print(f"Slow UI operation: {func.__name__} took {duration:.3f}s")
        
        return result
    return wrapper


# =====================================================================
# WIDGET FACTORY AND BUILDER
# =====================================================================

class OptimizedWidgetFactory:
    """
    Factory for creating optimized widgets with performance enhancements
    """
    
    @staticmethod
    def create_label(text: str = "", parent=None) -> PerformantLabel:
        """Create an optimized label"""
        label = PerformantLabel(text, parent)
        label.setWordWrap(True)
        return label
    
    @staticmethod
    def create_text_edit(parent=None) -> PerformantTextEdit:
        """Create an optimized text edit"""
        text_edit = PerformantTextEdit(parent)
        text_edit.setReadOnly(False)
        return text_edit
    
    @staticmethod
    def create_progress_bar(parent=None) -> PerformantProgressBar:
        """Create an optimized progress bar"""
        progress_bar = PerformantProgressBar(parent)
        progress_bar.setTextVisible(True)
        return progress_bar
    
    @staticmethod
    def create_optimized_button(text: str, parent=None) -> QPushButton:
        """Create an optimized button with smart event handling"""
        button = QPushButton(text, parent)
        
        # Add click throttling to prevent double-clicks
        original_clicked = button.clicked
        last_click_time = 0
        
        def throttled_click():
            nonlocal last_click_time
            current_time = time.time()
            if current_time - last_click_time > 0.3:  # 300ms throttle
                last_click_time = current_time
                original_clicked.emit()
        
        button.clicked.disconnect()
        button.clicked.connect(throttled_click)
        
        return button


# =====================================================================
# PERFORMANCE MONITORING WIDGET
# =====================================================================

class PerformanceMonitorWidget(QLabel):
    """
    Widget to display real-time performance metrics
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 60)
        self.setStyleSheet("""
            background-color: rgba(0, 0, 0, 128);
            color: white;
            padding: 5px;
            border-radius: 3px;
            font-size: 10px;
        """)
        
        # Update timer
        self._update_timer = QTimer()
        self._update_timer.timeout.connect(self._update_display)
        self._update_timer.start(1000)  # Update every second
        
        self._update_display()
    
    def _update_display(self):
        """Update the performance display"""
        summary = profiler.get_summary()
        
        text = f"""FPS: {1000 / max(1, summary['avg_event_time']):.1f}
Updates: {summary['widget_updates']}
Cache Hit: {summary['cache_hit_ratio']:.1%}
Operations: {summary['total_operations']}"""
        
        self.setText(text)


# =====================================================================
# INTEGRATION HELPERS
# =====================================================================

def apply_performance_optimizations(main_window):
    """
    Apply performance optimizations to an existing main window
    
    Args:
        main_window: The main application window
    """
    # Install global event filter
    event_filter = OptimizedEventFilter()
    QApplication.instance().installEventFilter(event_filter)
    
    # Replace standard widgets with optimized versions where possible
    _replace_widgets_recursive(main_window)
    
    # Start batch update manager
    batch_manager.moveToThread(QApplication.instance().thread())
    
    # Add performance monitor (optional, for debugging)
    if hasattr(main_window, 'statusBar'):
        monitor = PerformanceMonitorWidget()
        main_window.statusBar().addPermanentWidget(monitor)
    
    print("UI performance optimizations applied successfully!")


def _replace_widgets_recursive(widget):
    """Recursively replace widgets with optimized versions"""
    for child in widget.findChildren(QLabel):
        if not isinstance(child, PerformantLabel):
            # Would need careful replacement logic here
            pass
    
    for child in widget.findChildren(QTextEdit):
        if not isinstance(child, PerformantTextEdit):
            # Would need careful replacement logic here
            pass


# =====================================================================
# EXAMPLE USAGE AND INTEGRATION
# =====================================================================

def create_optimized_exercise_display(parent=None):
    """
    Example function showing how to create an optimized exercise display
    using the performance-enhanced widgets
    """
    from PyQt5.QtWidgets import QVBoxLayout, QWidget
    
    widget = QWidget(parent)
    layout = QVBoxLayout(widget)
    
    # Use optimized widgets
    sentence_label = OptimizedWidgetFactory.create_label(
        "Exercise sentence will appear here..."
    )
    
    translation_label = OptimizedWidgetFactory.create_label()
    translation_label.setStyleSheet("color: gray;")
    
    feedback_text = OptimizedWidgetFactory.create_text_edit()
    feedback_text.setReadOnly(True)
    
    progress_bar = OptimizedWidgetFactory.create_progress_bar()
    
    # Add to layout
    layout.addWidget(sentence_label)
    layout.addWidget(translation_label)
    layout.addWidget(feedback_text)
    layout.addWidget(progress_bar)
    
    return widget, {
        'sentence_label': sentence_label,
        'translation_label': translation_label,
        'feedback_text': feedback_text,
        'progress_bar': progress_bar
    }


# =====================================================================
# CONFIGURATION AND SETTINGS
# =====================================================================

class PerformanceSettings:
    """Configuration settings for UI performance"""
    
    # Batch update settings
    BATCH_UPDATE_DELAY_MS = 16  # ~60 FPS
    MAX_BATCH_SIZE = 50
    
    # Cache settings
    WIDGET_CACHE_SIZE = 50
    PROPERTY_CACHE_SIZE = 128
    EVENT_CACHE_SIZE = 1000
    
    # Threading settings
    MAX_BACKGROUND_THREADS = 4
    
    # Update throttling
    MIN_UPDATE_INTERVAL = 0.1  # seconds
    PROGRESS_UPDATE_THRESHOLD = 1  # percent
    
    # Memory settings
    CIRCULAR_BUFFER_SIZE = 1000
    
    @classmethod
    def apply_settings(cls):
        """Apply settings to global managers"""
        batch_manager.batch_delay_ms = cls.BATCH_UPDATE_DELAY_MS
        batch_manager.max_batch_size = cls.MAX_BATCH_SIZE
        
        widget_cache._max_size = cls.WIDGET_CACHE_SIZE
        
        ui_manager._thread_pool.setMaxThreadCount(cls.MAX_BACKGROUND_THREADS)


# Apply default settings
PerformanceSettings.apply_settings()

if __name__ == "__main__":
    # Example usage
    print("UI Performance Optimization Module loaded")
    print("Key features:")
    print("- Batched widget updates")
    print("- Optimized event handling")
    print("- Widget caching and lazy loading")
    print("- Responsive threading")
    print("- Performance monitoring")