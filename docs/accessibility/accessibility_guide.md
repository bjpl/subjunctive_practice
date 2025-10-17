# Accessibility Guide for Spanish Subjunctive Practice App

## Overview

The Spanish Subjunctive Practice app includes comprehensive accessibility features designed to make Spanish learning accessible to users with diverse needs and abilities. This guide covers all accessibility features and how to use them effectively.

## Features Summary

### 🔧 Core Accessibility Features
- **Enhanced Keyboard Navigation**: Full keyboard control with logical tab order
- **Visual Focus Indicators**: High-visibility focus rings with customizable colors and sizes
- **High Contrast Modes**: Multiple color themes for better visibility
- **Screen Reader Support**: ARIA labels and announcements for assistive technologies
- **Customizable Text Scaling**: Font size adjustment from 50% to 200%
- **Reduced Motion Options**: Minimize animations for users with vestibular disorders
- **Comprehensive Keyboard Shortcuts**: Quick access to all features

### 🎯 Learning-Focused Enhancements
- **Audio Announcements**: Exercise content and feedback read aloud
- **Focus Management**: Automatic focus handling for dynamic content
- **Context-Aware Navigation**: Smart navigation between related elements
- **Enhanced Tooltips**: Detailed descriptions and usage hints

## Quick Start

### Initial Setup
1. **Launch the application** - accessibility features are enabled by default
2. **First-time users** see an introduction to accessibility features
3. **Press F1** anytime to see keyboard shortcuts
4. **Press Ctrl+Alt+A** to open accessibility settings

### Essential Keyboard Shortcuts

| Action | Shortcut | Description |
|--------|----------|-------------|
| Submit Answer | **Return** | Submit your current conjugation answer |
| Next Exercise | **Right Arrow** | Move to the next exercise |
| Previous Exercise | **Left Arrow** | Go back to previous exercise |
| Show Hint | **H** | Get a helpful hint for current exercise |
| Conjugation Reference | **Ctrl+R** | Open quick reference guide |
| Toggle Translation | **Ctrl+T** | Show/hide English translations |
| High Contrast | **Ctrl+Alt+H** | Toggle high contrast mode |
| Accessibility Settings | **Ctrl+Alt+A** | Open accessibility preferences |
| Keyboard Help | **F1** | Show complete shortcut list |
| Skip to Content | **Ctrl+K** | Jump to main exercise area |
| Skip to Navigation | **Ctrl+N** | Jump to navigation buttons |
| Focus Answer Field | **Ctrl+I** | Jump to answer input |
| Read Exercise Aloud | **Ctrl+Space** | Announce current exercise |

## Detailed Feature Guide

### 1. Keyboard Navigation

#### Basic Navigation
- **Tab / Shift+Tab**: Navigate between interface elements
- **Arrow Keys**: Navigate within groups (checkboxes, radio buttons)
- **Space**: Activate buttons and toggle checkboxes
- **Enter**: Submit forms and activate default buttons

#### Advanced Navigation
- **Focus Groups**: Related elements are grouped for efficient navigation
  - Trigger checkboxes: Navigate with Up/Down arrows
  - Tense selection: Navigate with Up/Down arrows
  - Person selection: Navigate with Up/Down arrows
  - Navigation buttons: Navigate with Tab

#### Skip Links
Quick navigation shortcuts help users bypass repetitive content:
- **Ctrl+K**: Skip directly to exercise content
- **Ctrl+N**: Skip to navigation buttons
- **Ctrl+I**: Jump to answer input field

### 2. Visual Accessibility

#### High Contrast Modes
Four color themes optimized for different visual needs:

**Default Theme**: Standard colors with good contrast
- Background: White (#ffffff)
- Text: Black (#000000)
- Accent: Blue (#007ACC)

**High Contrast Theme**: Maximum contrast for low vision
- Background: Black (#000000)
- Text: White (#ffffff)
- Focus: Yellow (#ffff00)
- Accent: Yellow (#ffff00)

**Dark High Contrast**: Dark background with high contrast
- Background: Dark gray (#1a1a1a)
- Text: White (#ffffff)
- Focus: Yellow (#ffff00)
- Accent: Cyan (#00ffff)

**Low Vision Theme**: Enhanced contrast with comfortable colors
- Background: Cream (#fffbf0)
- Text: Black (#000000)
- Focus: Dark red (#cc0000)

#### Font Scaling
- **Range**: 50% to 200% of base size
- **Base Font Size**: 18px (scales proportionally)
- **UI Elements**: All text scales together for consistency

#### Focus Indicators
- **Default Width**: 3px border
- **High Contrast**: Minimum 4px width
- **Customizable Color**: User-selectable focus ring color
- **Enhanced Visibility**: Includes background highlight and outline

### 3. Screen Reader Support

#### ARIA Labels
Every interactive element includes appropriate ARIA labels:
- **Buttons**: Clear action descriptions
- **Input Fields**: Context and expected format
- **Checkboxes**: Purpose and current state
- **Progress Indicators**: Current position and total

#### Live Regions
Dynamic content updates are announced:
- **Exercise Changes**: New exercise number and content
- **Answer Feedback**: Results and explanations
- **Status Updates**: System messages and errors
- **Progress Updates**: Completion status

#### Structured Navigation
- **Headings**: Proper heading hierarchy for screen readers
- **Landmarks**: Main content areas clearly marked
- **Tab Order**: Logical sequence through interface

### 4. Audio Announcements

#### Automatic Announcements
When enabled, the system announces:
- **Focus Changes**: Current element and its purpose
- **Exercise Transitions**: New exercise loaded
- **Answer Submission**: Confirmation of submitted answer
- **Mode Changes**: Interface mode switches
- **System Status**: Important updates and errors

#### Manual Announcements
- **Ctrl+Space**: Read current exercise aloud
- **Exercise Content**: Sentence and translation if visible
- **Context Information**: Relevant hints and guidance

### 5. Customization Options

#### Accessibility Settings Dialog (Ctrl+Alt+A)

**Visual Settings**
- High Contrast Mode toggle
- Font size slider (50%-200%)
- Color theme selection
- Reduce motion/animations

**Navigation Settings**
- Enhanced keyboard navigation toggle
- Focus ring width (1-10 pixels)
- Focus ring color picker
- Focus ring animation preferences

**Screen Reader Settings**
- Screen reader support toggle
- Automatic announcements
- Enhanced tooltips
- Live region updates

**Keyboard Shortcuts**
- Show shortcuts in interface
- Customize shortcut keys (future feature)
- Reset to defaults option

## Learning-Specific Accessibility Features

### 1. Exercise Navigation
- **Smart Focus**: Automatically focuses relevant elements
- **Context Preservation**: Maintains position when switching exercises
- **Progress Announcements**: Clear indication of position in set

### 2. Answer Input
- **Format Guidance**: Clear instructions for expected input
- **Error Prevention**: Input validation with helpful messages
- **Multiple Formats**: Support for various input methods

### 3. Feedback Delivery
- **Multi-Modal**: Visual, auditory, and text feedback
- **Progressive Disclosure**: Information presented in digestible chunks
- **Contextual Help**: Relevant assistance based on user errors

### 4. Reference Materials
- **Quick Access**: Instant access to conjugation tables
- **Searchable Content**: Find specific information quickly
- **Multiple Views**: Tabbed organization for different topics

## Troubleshooting

### Common Issues and Solutions

#### Focus Not Visible
- **Check high contrast mode**: Ctrl+Alt+H to toggle
- **Adjust focus ring width**: Use accessibility settings
- **Update graphics drivers**: Ensure proper rendering support

#### Screen Reader Not Announcing
- **Enable screen reader support**: Check accessibility settings
- **Turn on auto-announcements**: Enable in settings dialog
- **Check screen reader settings**: Ensure application focus is detected

#### Keyboard Shortcuts Not Working
- **Check keyboard navigation**: Enable in accessibility settings
- **Verify shortcuts**: Press F1 to see current mappings
- **Clear conflicts**: Other applications might override shortcuts

#### Text Too Small/Large
- **Adjust font scaling**: Use slider in accessibility settings
- **Check system scaling**: Verify OS-level display settings
- **Reset to defaults**: Use reset button if needed

#### High Contrast Issues
- **Try different themes**: Switch between available options
- **Custom colors**: Adjust focus ring and accent colors
- **System compatibility**: Check OS high contrast settings

## Best Practices for Accessible Learning

### 1. Setup Recommendations
- **Start with accessibility check**: Review settings on first use
- **Customize to your needs**: Adjust colors, fonts, and navigation
- **Practice navigation**: Familiarize yourself with keyboard shortcuts
- **Test announcements**: Ensure audio feedback is working

### 2. Efficient Learning Workflow
- **Use skip links**: Navigate quickly to content areas
- **Enable translations initially**: Build confidence with context
- **Leverage hints effectively**: Use H key for guidance
- **Review with keyboard**: Navigate through previous exercises

### 3. Progress Tracking
- **Monitor accessibility**: Settings persist across sessions
- **Export sessions**: Accessible CSV format for review
- **Use reference frequently**: Ctrl+R for quick lookup
- **Track improvements**: Built-in statistics with accessibility

## Integration with Assistive Technologies

### Screen Readers
**Tested with**:
- NVDA (Windows)
- JAWS (Windows)  
- VoiceOver (macOS)
- Orca (Linux)

**Features**:
- Complete keyboard navigation
- Live region announcements
- Structured content navigation
- Form field descriptions

### Voice Control Software
- **Dragon NaturallySpeaking**: Full command support
- **Windows Voice Recognition**: Compatible with standard commands
- **macOS Voice Control**: Works with accessibility features

### Switch Navigation
- **Switch Access**: Compatible with external switches
- **Scan Mode**: Sequential navigation through elements
- **Timing Adjustments**: Customizable scan rates

### Magnification Software
- **ZoomText**: Compatible with high contrast modes
- **Windows Magnifier**: Proper focus tracking
- **macOS Zoom**: Maintains focus indicators

## Developer Notes

### Implementation Details
- **PyQt5 Accessibility**: Full QAccessible implementation
- **Cross-Platform**: Windows, macOS, Linux support
- **Performance**: Minimal impact on application performance
- **Extensible**: Modular architecture for feature additions

### Testing Coverage
- **Automated Tests**: Comprehensive test suite
- **Manual Testing**: Regular accessibility audits
- **User Testing**: Feedback from diverse user groups
- **Standards Compliance**: WCAG 2.1 AA guidelines

## Support and Feedback

### Getting Help
- **F1 Key**: In-application help
- **Documentation**: Complete feature documentation
- **Community**: User forums and discussion groups

### Reporting Issues
- **Accessibility Bugs**: Specific accessibility problems
- **Feature Requests**: Suggested improvements
- **Compatibility Issues**: Problems with assistive technologies

### Contributing
- **Testing**: Help test new accessibility features
- **Feedback**: Share your accessibility experiences
- **Translation**: Accessibility content localization

## Conclusion

The Spanish Subjunctive Practice app's accessibility features are designed to provide an inclusive learning experience for all users. Whether you use assistive technologies, prefer keyboard navigation, need high contrast visuals, or have other accessibility needs, these features work together to create an effective and enjoyable Spanish learning environment.

Remember: Accessibility benefits everyone, not just users with disabilities. Features like keyboard shortcuts, clear navigation, and customizable displays enhance the learning experience for all users.

For the most current accessibility information and updates, please refer to the application's built-in help system (F1) and settings dialog (Ctrl+Alt+A).