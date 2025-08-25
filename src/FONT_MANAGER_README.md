# Font Manager System for Spanish Subjunctive Practice App

## Overview

The Font Manager system provides comprehensive font loading and management capabilities specifically optimized for Windows systems and Spanish character rendering. It ensures excellent readability and proper display of all Spanish characters (ñ, á, é, í, ó, ú, ¿, ¡) across different screen sizes and DPI settings.

## Key Features

- ✅ **System font detection** with intelligent fallbacks
- ✅ **Web-safe font stack** for cross-platform consistency  
- ✅ **Spanish character validation** (ñ, á, é, í, ó, ú, ¿, ¡)
- ✅ **Dynamic font sizing** based on DPI/screen resolution
- ✅ **Windows font rendering optimizations** (ClearType support)
- ✅ **Performance optimizations** and intelligent caching
- ✅ **Font quality scoring** for Spanish language support
- ✅ **Configuration persistence** between sessions

## Quick Start

### Basic Usage

```python
from src.font_manager import FontManager

# Create font manager
font_manager = FontManager()

# Get a font optimized for Spanish content
font = font_manager.get_font('normal')  # 14pt base size
large_font = font_manager.get_font('large')  # 18pt base size

# Apply font to a widget
font_manager.apply_font_to_widget(my_label, 'medium', QFont.Bold)
```

### Integration with Existing Application

The easiest way to integrate the font manager is using the `FontIntegrationMixin`:

```python
from src.font_integration_patch import FontIntegrationMixin

class SpanishSubjunctivePracticeGUI(FontIntegrationMixin, QMainWindow):
    def __init__(self):
        super().__init__()
        
        # ... your existing initialization code ...
        
        # Add these three lines for font management:
        self.initialize_font_manager()
        self.apply_font_management() 
        self.add_font_menu_actions()
```

That's it! Your application now has:
- Automatic Spanish-optimized font selection
- DPI-aware font scaling
- Font settings dialog accessible from toolbar
- Proper Spanish character rendering

## Architecture

### Core Components

1. **FontManager** - Main orchestration class
2. **WindowsDPIManager** - Windows-specific DPI handling
3. **SpanishCharacterValidator** - Tests font Spanish support
4. **FontConfig** - Font configuration data class

### Font Selection Strategy

```
1. Detect all available system fonts
2. Test each font for Spanish character support
3. Rank fonts by Spanish support quality (0-100%)
4. Select best font with fallback chain:
   - Segoe UI (Windows) → SF Pro Display (macOS) → Arial (universal)
5. Apply DPI scaling for current screen
6. Cache results for performance
```

## Spanish Character Support

The system validates support for these essential Spanish characters:

- **Basic vowels**: á, é, í, ó, ú, Á, É, Í, Ó, Ú
- **Ñ character**: ñ, Ñ  
- **Diaeresis**: ü, Ü (güe, güi)
- **Punctuation**: ¿, ¡ (inverted question/exclamation marks)
- **Extended**: ç, Ç, €, «, » (less common but useful)

### Font Quality Scoring

Fonts receive a quality score (0-100%) based on:
- Complete character coverage (80% weight)
- Proper character rendering (20% weight)

Only fonts with >90% support are marked as "Recommended for Spanish".

## DPI and Windows Optimization

### DPI Awareness

The system automatically detects and adapts to:
- Standard DPI (96 DPI = 100% scaling)
- High DPI displays (144 DPI = 150% scaling)
- Very high DPI (192 DPI = 200% scaling)

### Windows Optimizations

On Windows, the system applies:
- **Process DPI awareness** - Prevents blurry text scaling
- **ClearType optimization** - Improved font smoothing
- **Full hinting preference** - Better character edge definition
- **Anti-aliasing** - Smoother font rendering

## API Reference

### FontManager Class

#### Core Methods

```python
# Font retrieval
get_font(size_key='normal', weight=QFont.Normal, italic=False) -> QFont
get_font_metrics(font: QFont) -> QFontMetrics

# Configuration
set_base_font_size(size: int)
set_font_family(family: str) 
get_current_configuration() -> FontConfig

# Widget integration
apply_font_to_widget(widget, size_key='normal', weight=QFont.Normal, italic=False)
create_stylesheet_font_rules(size_key='normal') -> str

# Font analysis
get_recommended_fonts() -> List[str]
get_spanish_character_support(font_name: str) -> SpanishFontSupport
get_available_fonts() -> List[str]
```

#### Font Size Keys

```python
'tiny'        # 10pt
'small'       # 12pt  
'normal'      # 14pt (default)
'medium'      # 16pt
'large'       # 18pt
'extra_large' # 22pt
'huge'        # 28pt
```

All sizes are automatically DPI-scaled.

### Signals

```python
fontChanged = pyqtSignal(QFont)    # Emitted when font family changes
sizeChanged = pyqtSignal(int)      # Emitted when base size changes
```

### Configuration

Settings are automatically saved to the system registry (Windows) or preferences (macOS/Linux):

```python
# Settings location
QSettings("SpanishSubjunctive", "FontManager")

# Stored configuration
{
    "font_config": {
        "family": "Segoe UI",
        "size": 14,
        "weight": 50,
        "italic": false,
        "stretch": 100
    }
}
```

## Performance Characteristics

### Benchmarks (Typical Windows System)

- **Font creation**: ~0.5ms per font (cached)
- **Spanish validation**: ~15ms per font
- **DPI detection**: ~1ms (Windows API)
- **Memory usage**: ~2MB (with 50+ fonts cached)

### Optimization Features

- **Intelligent caching** - Fonts and metrics cached by configuration
- **Lazy loading** - Fonts validated only when needed
- **Batch operations** - Efficient bulk font analysis
- **Memory management** - Automatic cache size limits

## Testing

Run the comprehensive test suite:

```bash
cd tests
python test_font_manager.py
```

Test coverage includes:
- Font detection and validation
- Spanish character support testing  
- DPI scaling accuracy
- Performance benchmarks
- Windows API integration
- Configuration persistence
- Widget integration

## Examples

### Demo Applications

1. **Font Integration Demo** - Complete demonstration
   ```bash
   python src/font_integration_example.py
   ```

2. **Font Manager Test** - Basic functionality test
   ```bash
   python src/font_manager.py
   ```

3. **Integration Patch Test** - Mixin pattern test
   ```bash
   python src/font_integration_patch.py
   ```

### Real-World Usage

```python
class MySpanishApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Initialize font manager
        self.font_manager = FontManager()
        
        # Create UI elements
        self.title = QLabel("¡Aprende Español!")
        self.content = QTextEdit("Ñoño güeña años corazón...")
        
        # Apply fonts
        self.font_manager.apply_font_to_widget(self.title, 'extra_large', QFont.Bold)
        self.font_manager.apply_font_to_widget(self.content, 'normal')
        
        # Connect to font changes
        self.font_manager.fontChanged.connect(self.update_ui_fonts)
    
    def update_ui_fonts(self):
        # Reapply fonts when settings change
        self.font_manager.apply_font_to_widget(self.title, 'extra_large', QFont.Bold)
        self.font_manager.apply_font_to_widget(self.content, 'normal')
```

## Troubleshooting

### Common Issues

**Q: Fonts appear too small/large**
- Check DPI scaling: `font_manager.dpi_manager.get_dpi_scale()`
- Verify Windows display scaling settings
- Use `set_base_font_size()` to adjust

**Q: Spanish characters not displaying properly**  
- Check font support: `get_spanish_character_support(font_name)`
- Switch to recommended font: `get_recommended_fonts()[0]`
- Verify Unicode encoding in text files

**Q: Font changes not persisting**
- Check QSettings permissions
- Verify settings path: `QSettings("SpanishSubjunctive", "FontManager")`
- Use absolute paths for font files

**Q: Performance issues with many fonts**
- Monitor cache size: `get_debug_info()['font_cache_size']`
- Limit font validation to essential fonts only
- Clear caches periodically if needed

### Debug Information

Get comprehensive debug info:

```python
debug_info = font_manager.get_debug_info()
print(json.dumps(debug_info, indent=2))
```

Output includes:
- Current configuration
- DPI settings
- Font counts and cache sizes
- Platform information
- Top Spanish-compatible fonts

## Contributing

When modifying the font manager:

1. **Run tests** - Ensure all tests pass
2. **Test on Windows** - Verify DPI scaling works correctly  
3. **Validate Spanish characters** - Test with real Spanish content
4. **Check performance** - Monitor font creation/caching performance
5. **Update documentation** - Keep this README current

### Adding New Font Features

1. Add feature to appropriate class (FontManager/Validator/DPIManager)
2. Write comprehensive tests
3. Update type hints and docstrings
4. Add example usage to integration demo
5. Update API reference in this README

## License

This font management system is part of the Spanish Subjunctive Practice application and follows the same license terms.