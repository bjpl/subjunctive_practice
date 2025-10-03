# Qt-Compatible Stylesheet Migration Guide

## Overview

This guide helps developers migrate from CSS stylesheets with unsupported properties to Qt-compatible versions. Qt's stylesheet support is based on CSS2 with extensions but lacks support for modern CSS3 features like transitions, transforms, animations, and box-shadows.

## Key Changes Made

### 1. Removed Unsupported CSS Properties

The following CSS properties are **NOT supported** by Qt and have been removed:

```css
/* REMOVED - Not supported in Qt */
transition: all 0.3s ease;
transform: translateY(-2px);
animation: slideIn 0.5s ease-out;
box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
-webkit-transition: all 0.3s;
-moz-transform: scale(1.05);
```

### 2. Qt-Compatible Replacements

#### Shadow Effects
**Before (CSS box-shadow):**
```css
box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
```

**After (Qt QGraphicsDropShadowEffect):**
```python
from qt_compatible_styles import ShadowUtils
ShadowUtils.apply_button_shadow(button, CleanColors.PRIMARY)
```

#### Animations and Transitions
**Before (CSS transitions):**
```css
transition: all 0.3s ease;
transform: translateY(-2px);
```

**After (Qt Property Animations):**
```python
from qt_compatible_styles import AnimationUtils, QtButtonAnimations

# Setup button animations
button_animations = QtButtonAnimations(button)
button_animations.setup_hover_animation()

# Or create custom animations
shake_animation = AnimationUtils.create_shake_animation(widget)
shake_animation.start()
```

#### Transform Effects
**Before (CSS transforms):**
```css
transform: translateY(-2px) scale(1.05);
```

**After (Qt Property Animations):**
```python
pulse_animation = AnimationUtils.create_pulse_animation(widget)
slide_animation = AnimationUtils.create_slide_animation(widget, "left")
```

## Migration Steps

### Step 1: Import the Qt-Compatible Module

```python
from qt_compatible_styles import (
    QtStyles, 
    ShadowUtils, 
    AnimationUtils, 
    QtButtonAnimations,
    apply_qt_compatible_button_style
)
```

### Step 2: Replace CSS Stylesheets

**Before:**
```python
button.setStyleSheet("""
    QPushButton {
        background: #3B82F6;
        border-radius: 12px;
        padding: 12px 24px;
    }
    QPushButton:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
""")
```

**After:**
```python
# Method 1: Use predefined styles
style = QtStyles.primary_button()
button.setStyleSheet(style)
ShadowUtils.apply_button_shadow(button)

# Method 2: Use helper function
apply_qt_compatible_button_style(button, "primary")
```

### Step 3: Add Qt Animations

**Replace CSS hover effects with Qt event handling:**

```python
class ModernButton(QPushButton):
    def __init__(self, text, button_type="primary"):
        super().__init__(text)
        self.button_animations = QtButtonAnimations(self)
        self.button_animations.setup_hover_animation()
    
    def enterEvent(self, event):
        super().enterEvent(event)
        self.button_animations.animate_hover_enter()
    
    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.button_animations.animate_hover_leave()
```

### Step 4: Update Input Fields

**Before:**
```python
input_field.setStyleSheet("""
    QLineEdit:focus {
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
    }
""")
```

**After:**
```python
class SmartInputField(QLineEdit):
    def apply_correct_style(self):
        style = QtStyles.input_field_correct()
        self.setStyleSheet(style)
        ShadowUtils.apply_focus_shadow(self, CleanColors.SUCCESS)
```

## Available Qt-Compatible Styles

### Button Styles
- `QtStyles.primary_button()`
- `QtStyles.secondary_button()`
- `QtStyles.success_button()`
- `QtStyles.danger_button()`

### Input Field Styles
- `QtStyles.input_field_neutral()`
- `QtStyles.input_field_correct()`
- `QtStyles.input_field_incorrect()`
- `QtStyles.input_field_hint()`

### Card Styles
- `QtStyles.exercise_card()`
- `QtStyles.progress_card()`
- `QtStyles.feedback_card_correct()`
- `QtStyles.feedback_card_incorrect()`
- `QtStyles.feedback_card_hint()`

### Layout Styles
- `QtStyles.main_window()`
- `QtStyles.progress_bar()`
- `QtStyles.context_label()`

## Shadow Effects Utilities

### Button Shadows
```python
# Primary button shadow
ShadowUtils.apply_button_shadow(button, CleanColors.PRIMARY)

# Card shadow
ShadowUtils.apply_card_shadow(card)

# Focus ring shadow
ShadowUtils.apply_focus_shadow(input_field, CleanColors.SUCCESS)

# Remove shadow
ShadowUtils.remove_shadow(widget)
```

## Animation Utilities

### Feedback Animations
```python
# Shake animation for errors
shake = AnimationUtils.create_shake_animation(input_field)
shake.start()

# Pulse animation for success
pulse = AnimationUtils.create_pulse_animation(button)
pulse.start()

# Slide transition
slide = AnimationUtils.create_slide_animation(widget, "left")
slide.start()

# Fade in/out
fade = AnimationUtils.create_fade_animation(widget, fade_out=False)
fade.start()
```

## Best Practices

### 1. Use Semantic Styles
```python
# Good: Use semantic button types
apply_qt_compatible_button_style(submit_button, "primary")
apply_qt_compatible_button_style(cancel_button, "secondary")

# Avoid: Creating custom styles for each button
```

### 2. Consistent Shadow Application
```python
# Apply shadows consistently
for card in cards:
    ShadowUtils.apply_card_shadow(card)

for button in primary_buttons:
    ShadowUtils.apply_button_shadow(button, CleanColors.PRIMARY)
```

### 3. Animation Management
```python
# Store animations as instance variables for cleanup
self.shake_animation = AnimationUtils.create_shake_animation(self.input_field)

# Clean up animations when widget is destroyed
def closeEvent(self, event):
    if hasattr(self, 'shake_animation'):
        self.shake_animation.stop()
    super().closeEvent(event)
```

### 4. Performance Considerations
- Use `ShadowUtils.remove_shadow()` to remove effects when not needed
- Stop animations before creating new ones to avoid memory leaks
- Apply shadows after widget sizing is complete

## Migration Checklist

- [ ] Replace all CSS `transition` properties with Qt animations
- [ ] Replace all CSS `transform` properties with Qt property animations  
- [ ] Replace all CSS `box-shadow` with `QGraphicsDropShadowEffect`
- [ ] Remove all vendor prefixes (`-webkit-`, `-moz-`, etc.)
- [ ] Replace CSS `animation` with Qt `QPropertyAnimation`
- [ ] Update hover effects to use Qt event handling
- [ ] Test animations work correctly across different Qt versions
- [ ] Verify shadows display properly on different platforms
- [ ] Check performance impact of shadow effects
- [ ] Ensure proper animation cleanup

## Testing Different Qt Versions

The Qt-compatible styles have been designed to work across Qt versions:

### Qt 5.12+
- Full support for all stylesheet properties used
- `QGraphicsDropShadowEffect` fully supported
- Property animations work correctly

### Qt 5.9+  
- Basic stylesheet support
- Limited shadow effect support
- Property animations supported

### Qt 6.x
- Enhanced stylesheet support
- Better graphics effects performance
- Improved animation handling

## Troubleshooting

### Common Issues

1. **Shadows not appearing**: Ensure widget is visible and sized before applying shadows
2. **Animations not smooth**: Check Qt version and graphics driver support
3. **Styles not applying**: Verify import paths and module availability
4. **Memory leaks**: Always stop animations before widget destruction

### Performance Tips

1. Limit number of simultaneous shadow effects
2. Use shorter animation durations for better perceived performance  
3. Apply shadows to container widgets rather than individual elements
4. Cache frequently used stylesheet strings

## Examples

See the following files for complete implementation examples:
- `src/qt_compatible_styles.py` - Core implementation
- `ui_enhancements.py` - Updated UI components
- `examples/qt_compatibility_demo.py` - Usage examples

This migration ensures your Qt application maintains modern visual appeal while being compatible across different Qt versions and platforms.