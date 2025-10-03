# Spanish Typography System Integration Guide

## Overview

The Spanish Typography System (`src/typography_system.py`) is a comprehensive typography solution designed specifically for Spanish language learning applications. It provides optimal font selection, sizing, and spacing for Spanish text with accents and special characters.

## Key Features

### 🎯 Spanish-Optimized Features
- **Accent-friendly fonts**: Prioritizes Windows system fonts with excellent Spanish character support
- **Proper line heights**: 1.4-1.6 line height ratios accommodate Spanish accents and tildes
- **Letter spacing**: Optimized spacing for Spanish character combinations
- **Readability focus**: 14-16px base font sizes for sustained reading

### 📱 Responsive & Accessible
- **High DPI support**: Automatic scaling based on screen resolution and DPI
- **Screen size awareness**: Adjusts font sizes based on screen dimensions
- **Accessibility compliant**: Follows WCAG guidelines for font sizes and contrast
- **System font stack**: Uses native Windows fonts for best performance

### 🎨 Design System Integration
- **Consistent hierarchy**: Clear font weight and size variations
- **Pre-built presets**: Ready-to-use configurations for common UI elements
- **Qt stylesheet generation**: Seamless integration with PyQt5 applications
- **Color-aware**: Supports both light and dark theme text colors

## Basic Usage

### 1. Initialize Typography System

```python
from src.typography_system import create_spanish_typography, apply_spanish_typography_to_app

# Method 1: Apply to entire application
app = QApplication(sys.argv)
typography = apply_spanish_typography_to_app(app)

# Method 2: Create instance for custom usage
typography = create_spanish_typography()
```

### 2. Create Fonts for UI Elements

```python
from src.typography_system import SpanishTypography, TypographyPresets

typography = SpanishTypography()
presets = TypographyPresets(typography)

# Create fonts using presets
exercise_font = presets.create_preset_font('exercise_text')
heading_font = presets.create_preset_font('heading_large')
button_font = presets.create_preset_font('button_text')

# Apply to widgets
exercise_label.setFont(exercise_font)
heading_label.setFont(heading_font)
submit_button.setFont(button_font)
```

### 3. Use Stylesheet Generation

```python
# Generate Qt stylesheets
exercise_style = presets.get_preset_stylesheet('QLabel[role="exercise"]', 'exercise_text')
heading_style = presets.get_preset_stylesheet('QLabel[role="heading"]', 'heading_large')

# Apply styles
exercise_label.setProperty('role', 'exercise')
heading_label.setProperty('role', 'heading')
```

## Integration with Main Application

### Modify main.py

Here's how to integrate the typography system into the existing Spanish Subjunctive Practice app:

```python
# Add import at top of main.py
from src.typography_system import apply_spanish_typography_to_app, TypographyPresets, create_spanish_typography

class SpanishSubjunctivePracticeGUI(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        
        # Initialize typography system
        self.typography = create_spanish_typography()
        self.typography_presets = TypographyPresets(self.typography)
        
        # Existing initialization code...
        self.setWindowTitle("Spanish Subjunctive Practice")
        self.setGeometry(100, 100, 1100, 700)
        
        # Apply typography after UI initialization
        self.initUI()
        self._apply_spanish_typography()
    
    def _apply_spanish_typography(self):
        """Apply Spanish-optimized typography to UI elements"""
        
        # Main sentence display - large, comfortable reading
        self.sentence_label.setProperty('role', 'exercise')
        exercise_font = self.typography_presets.create_preset_font('exercise_text')
        self.sentence_label.setFont(exercise_font)
        
        # Translation text - smaller, italic
        self.translation_label.setProperty('role', 'translation') 
        translation_font = self.typography_presets.create_preset_font('translation_text')
        self.translation_label.setFont(translation_font)
        
        # Stats and status text - monospace for numbers
        stats_font = self.typography_presets.create_preset_font('stats_text')
        self.stats_label.setFont(stats_font)
        
        # Group box titles - medium headings
        heading_font = self.typography_presets.create_preset_font('heading_medium')
        for groupbox in self.findChildren(QGroupBox):
            groupbox.setFont(heading_font)
        
        # Button text - clear and readable
        button_font = self.typography_presets.create_preset_font('button_text')
        for button in self.findChildren(QPushButton):
            button.setFont(button_font)
        
        # Input fields - comfortable typing
        input_font = self.typography_presets.create_preset_font('body_text')
        self.free_response_input.setFont(input_font)
        self.verbs_input.setFont(input_font)
        self.custom_context_input.setFont(input_font)
        
        # Feedback text - comfortable reading with good line height
        feedback_font = self.typography_presets.create_preset_font('feedback_text')
        self.feedback_text.setFont(feedback_font)
        self.feedback_text.setProperty('role', 'feedback')
```

### Update Application Initialization

```python
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Apply Spanish typography system to entire app
    typography_system = apply_spanish_typography_to_app(app)
    
    # Initialize visual design system (existing)
    if initialize_modern_ui:
        try:
            style_manager = initialize_modern_ui(app)
            logger.info("Modern UI theme initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to initialize modern UI: {e}")
            style_manager = None
    
    window = SpanishSubjunctivePracticeGUI()
    
    # Assign both style managers
    if style_manager:
        window.style_manager = style_manager
    window.typography_system = typography_system
    
    window.show()
    sys.exit(app.exec_())
```

## Typography Presets Reference

### Available Presets

| Preset Name | Use Case | Size | Weight | Line Height |
|-------------|----------|------|--------|-------------|
| `body_text` | General text content | 14px | Normal | Relaxed (1.5) |
| `exercise_text` | Spanish sentences | 16px | Normal | Loose (1.6) |
| `translation_text` | English translations | 12px | Normal | Normal (1.4) |
| `heading_large` | Main section titles | 22px | Semibold | Tight (1.2) |
| `heading_medium` | Sub-section titles | 18px | Semibold | Snug (1.3) |
| `heading_small` | Minor headings | 16px | Medium | Normal (1.4) |
| `label_text` | UI labels | 12px | Medium | Normal (1.4) |
| `button_text` | Button labels | 14px | Medium | Tight (1.2) |
| `feedback_text` | Explanations | 14px | Normal | Loose (1.6) |
| `stats_text` | Numbers/statistics | 12px | Medium | Normal (1.4) |
| `code_text` | Code/conjugations | 12px | Normal | Relaxed (1.5) |

### Font Families

| Family Key | Fonts | Use Case |
|------------|-------|----------|
| `primary` | Segoe UI, Calibri, Tahoma, Verdana, Arial | Main text content |
| `display` | Segoe UI Light, Segoe UI Semilight | Headlines and titles |
| `monospace` | Consolas, Courier New | Code and statistics |

## Responsive Scaling

The typography system automatically scales fonts based on:

### Screen Characteristics
- **DPI scaling**: Maintains readability on high-DPI displays
- **Resolution scaling**: Adjusts for 4K+ and lower resolution screens  
- **Screen size**: Optimizes for laptop vs desktop screens

### Scaling Factors
- **Small screens (<13")**: 1.05x scaling
- **Standard screens (13-27")**: 1.0x scaling  
- **Large screens (>27")**: 1.1x scaling
- **High DPI (>96 DPI)**: Proportional scaling
- **4K+ displays**: Additional 1.1x scaling

## Advanced Usage

### Custom Font Creation

```python
# Create custom fonts with specific parameters
typography = create_spanish_typography()

# Large exercise text with extra spacing
exercise_font = typography.create_font(
    size='xl',              # 18px base
    weight='normal',        # Regular weight
    family='primary',       # Segoe UI family
    line_height='loose',    # 1.6 line height
    letter_spacing='wide'   # Extra letter spacing
)

# Compact button text
button_font = typography.create_font(
    size='sm',              # 12px base  
    weight='semibold',      # Bold weight
    family='primary',       # Segoe UI family
    line_height='tight',    # 1.2 line height
    letter_spacing='wider'  # Wide letter spacing for buttons
)
```

### Stylesheet Generation

```python
# Generate complete Qt stylesheets
typography = create_spanish_typography()

# Exercise text styling
exercise_style = typography.get_qt_stylesheet_rules(
    selector='QLabel[role="exercise"]',
    size='lg',
    weight='normal', 
    line_height='loose',
    letter_spacing='wide',
    color='primary_light'
)

# Apply to application
app.setStyleSheet(exercise_style)
```

### Text Measurement

```python
from src.typography_system import SpanishTextMetrics

typography = create_spanish_typography()
metrics = SpanishTextMetrics(typography)

# Measure Spanish text with accents
spanish_text = "Espero que tengas éxito en el aprendizaje del subjuntivo"
dimensions = metrics.measure_text(
    text=spanish_text,
    font_size='lg',
    max_width=400
)

print(f"Text dimensions: {dimensions['width']}x{dimensions['height']}")
print(f"Line count: {dimensions['line_count']}")

# Get optimal width for readability
optimal_width = metrics.get_optimal_width(spanish_text, 'lg')
print(f"Optimal width: {optimal_width}px")
```

## Dark Theme Support

The typography system includes dark theme color variants:

```python
# Light theme colors
light_colors = {
    'primary_light': '#1a202c',    # Dark text on light background
    'secondary_light': '#4a5568',  # Secondary text
    'muted_light': '#718096'       # Muted text
}

# Dark theme colors  
dark_colors = {
    'primary_dark': '#f7fafc',     # Light text on dark background
    'secondary_dark': '#e2e8f0',   # Secondary text
    'muted_dark': '#a0aec0'        # Muted text
}

# Use appropriate colors based on theme
def get_text_color(theme: str, level: str = 'primary') -> str:
    color_key = f"{level}_{theme}"
    return SpanishTypographyConfig.TEXT_COLORS.get(color_key, '#1a202c')
```

## Performance Considerations

### Font Caching
The typography system includes built-in font caching to improve performance:

```python
# Fonts are automatically cached by configuration
typography = create_spanish_typography()

# First call creates and caches the font
font1 = typography.create_font('base', 'normal', 'primary')

# Second call returns cached font
font2 = typography.create_font('base', 'normal', 'primary')  # From cache

# Cache key format: "{size}_{weight}_{family}_{line_height}_{letter_spacing}"
```

### Memory Usage
- Font objects are cached to reduce memory allocation
- Screen metrics are calculated once and reused
- Stylesheet generation is optimized for performance

## Testing and Validation

### Typography Demo

Run the built-in demo to test typography:

```bash
cd src/
python typography_system.py
```

This will show:
- Spanish text samples with proper accent rendering
- Font scaling at current screen resolution
- Typography system information and metrics
- Real-time demonstration of different text styles

### Integration Testing

```python
# Test typography integration
def test_typography_integration():
    app = QApplication([])
    typography = apply_spanish_typography_to_app(app)
    
    # Test font creation
    font = typography.create_font('base', 'normal', 'primary')
    assert font.family() in ['Segoe UI', 'Calibri', 'Tahoma']
    
    # Test scaling
    scaler = typography.scaler
    scale_factor = scaler.calculate_font_scale_factor()
    assert 0.8 <= scale_factor <= 2.0
    
    print("Typography system integration successful!")
```

## Troubleshooting

### Common Issues

1. **Fonts not applying properly**
   - Ensure `setProperty('role', 'preset_name')` is called before applying fonts
   - Check that font files are available on the system
   - Verify Qt stylesheet syntax is correct

2. **Scaling issues on high DPI displays**
   - Ensure `QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)` is set
   - Check that DPI detection is working correctly
   - Verify scale factors are within expected ranges (0.8-2.0)

3. **Spanish characters not rendering correctly**
   - Confirm system fonts support Spanish characters
   - Check text encoding is UTF-8
   - Verify font fallback chain includes proper fonts

### Debug Information

```python
# Get comprehensive typography information
from src.typography_system import get_typography_info

info = get_typography_info()
print(f"Typography System v{info['version']}")
print(f"Current scale factor: {info['current_scale_factor']}")
print(f"Screen DPI: {info['screen_info']['dpi']}")
print(f"Available fonts: {info['primary_fonts']}")
```

## Best Practices

### 1. Consistent Usage
- Use typography presets consistently across the application
- Apply role-based styling with `setProperty('role', 'preset_name')`
- Test typography on different screen sizes and resolutions

### 2. Spanish Text Optimization
- Use `exercise_text` preset for main Spanish content
- Apply `translation_text` preset for English translations
- Ensure adequate line height (1.5+) for text with accents

### 3. Performance
- Cache font objects when possible
- Use presets instead of creating custom fonts repeatedly
- Apply typography system once during application initialization

### 4. Accessibility
- Test font sizes at different system scaling levels
- Ensure sufficient color contrast for all text
- Provide options for users to adjust font sizes if needed

## Migration from Existing System

If migrating from the existing UI system:

1. **Keep existing visual theme**: The typography system works alongside `src/ui_visual.py`
2. **Apply typography selectively**: Start with main content areas first
3. **Test thoroughly**: Verify all text elements render correctly
4. **Maintain compatibility**: Existing stylesheets should continue working

## Conclusion

The Spanish Typography System provides a robust foundation for optimal Spanish text rendering in PyQt5 applications. It combines responsive design principles, accessibility best practices, and Spanish-specific optimizations to create the best possible reading and learning experience.

For questions or contributions, refer to the main application documentation or create an issue in the project repository.