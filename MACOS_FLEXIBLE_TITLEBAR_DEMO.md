# macOS Flexible Layout + Custom Titlebar Demo

A comprehensive standalone example demonstrating the ThreePaneWindows flexible layout system with custom titlebar functionality and complete theme switching capabilities, optimized for macOS systems.

## Features

### 🎨 **Complete Theme Switching**
- **All Available Themes**: Light, Dark, Blue Professional, Green Nature, Purple Elegance, System, Native
- **Real-time Updates**: All UI elements update instantly when switching themes
- **Detached Window Consistency**: Detached panes maintain theme consistency
- **Titlebar Integration**: Theme switching menu integrated directly into custom titlebar
- **System Theme Integration**: Automatic macOS theme detection and integration

### 📐 **Flexible Layout System**
- **Complex Nested Layout**: 6 panes arranged in an Xcode-inspired layout
- **Detachable Panes**: All panes can be detached into separate windows
- **Custom Titlebars**: Both main window and detached panes use custom titlebars
- **Professional Styling**: macOS-optimized fonts, spacing, and visual elements

### 🍎 **Advanced Window Management**
- **Custom Titlebar**: macOS-specific custom titlebar implementation
- **Window Controls**: Traffic light buttons (red, yellow, green)
- **Drag & Drop**: Window dragging functionality
- **Focus Management**: Proper window focus and activation
- **Icon Support**: macOS-compatible icon formats (.icns, .png)

### 🍎 **macOS Optimizations**
- **Native Fonts**: SF Pro Display, Menlo font families
- **Desktop Integration**: Proper macOS desktop integration
- **Retina Display**: High-resolution display optimization
- **System Theme Detection**: Automatic light/dark mode detection
- **Mission Control**: Proper window grouping and spaces support

## Layout Structure

```
┌─────────────────────────────────────────────────────────────────┐
│ 🎨 Custom Titlebar with Theme Menu                              │
├─────────────┬─────────────────────────────┬─────────────────────┤
│ 📁 Project  │ 📝 Source Editor            │ 🛠️ Utilities        │
│ Navigator   │                             │                     │
│             │                             │                     │
├─────────────┼─────────────────────────────┼─────────────────────┤
│ 🔍 Inspector│ 💻 Terminal                 │ 🐛 Debug Area       │
│             │                             │                     │
│             │                             ├─────────────────────┤
│             │                             │ 📊 Report Navigator │
└─────────────┴─────────────────────────────┴─────────────────────┘
```

## Panes Description

1. **📁 Project Navigator**: Xcode-style project file tree with search and options
2. **🔍 Inspector**: File and theme information panel with system details
3. **📝 Source Editor**: Swift syntax-highlighted code editor with tabs and line numbers
4. **💻 Terminal**: macOS terminal with sample command output
5. **🛠️ Utilities**: Xcode-style utilities with object library and code snippets
6. **🐛 Debug Area**: Debug console with controls and output
7. **📊 Report Navigator**: Build reports and analysis results

## Installation & Usage

### Prerequisites
- Python 3.8 or higher
- tkinter (usually included with Python)
- ThreePaneWindows package
- macOS 10.14+ (optimized for macOS 11+)

### Quick Start

1. **Clone or download the project**:
   ```bash
   git clone <repository-url>
   cd ThreePaneWindows
   ```

2. **Install the package**:
   ```bash
   pip3 install -e .
   ```

3. **Run the demo**:
   ```bash
   python3 run_macos_flexible_titlebar_demo.py
   ```

   Or run directly:
   ```bash
   python3 macos_flexible_titlebar_demo.py
   ```

4. **Make executable (optional)**:
   ```bash
   chmod +x run_macos_flexible_titlebar_demo.py
   ./run_macos_flexible_titlebar_demo.py
   ```

### Alternative Installation

If you prefer to install from PyPI:
```bash
pip3 install threepanewindows
python3 macos_flexible_titlebar_demo.py
```

## Usage Instructions

### Theme Switching
1. Click the **🎨 Themes** button in the custom titlebar
2. Select any theme from the dropdown menu
3. Watch as all UI elements update in real-time
4. Detached windows automatically update to match
5. Use **System Theme** for automatic macOS theme integration

### Pane Management
1. **Detach Panes**: Click the detach button (↗️) in any pane header
2. **Reattach Panes**: Click the reattach button (↙️) in detached window
3. **Resize Panes**: Drag the splitter bars between panes
4. **Focus Windows**: Click on any window to bring it to front
5. **Mission Control**: Use Mission Control to manage detached windows

### Available Themes

| Theme | Description | Best For |
|-------|-------------|----------|
| ☀️ **Light** | Clean, bright interface | Daytime work, presentations |
| 🌙 **Dark** | Easy on the eyes | Night coding, reduced eye strain |
| 💙 **Blue Professional** | Corporate look | Business applications |
| 💚 **Green Nature** | Calming colors | Long coding sessions |
| 💜 **Purple Elegance** | Modern, sophisticated | Creative work |
| 🖥️ **System** | Follows macOS theme | Automatic adaptation |
| 🏠 **Native** | macOS colors | OS integration |

## Technical Details

### Architecture
- **Flexible Layout Engine**: Dynamic pane arrangement and sizing
- **Theme Management**: Centralized theme system with real-time updates
- **Custom Titlebar**: macOS-specific titlebar implementation
- **Window Management**: Professional detached window handling

### Platform Support
- **Primary**: macOS 11+ (Big Sur and later, optimized)
- **Secondary**: macOS 10.14+ (Mojave and later, basic support)
- **Architecture**: Both Intel and Apple Silicon Macs

### Dependencies
- `tkinter`: GUI framework (included with Python)
- `threepanewindows`: Main package
- `typing`: Type hints (Python 3.8+)

### File Structure
```
macos_flexible_titlebar_demo.py          # Main demo application
run_macos_flexible_titlebar_demo.py      # Launcher script
MACOS_FLEXIBLE_TITLEBAR_DEMO.md         # This documentation
```

## macOS-Specific Features

### Xcode Integration
- **Project Navigator**: Familiar Xcode project structure
- **Utilities**: Object library and code snippets
- **Debug Area**: Debug console and controls
- **Report Navigator**: Build reports and analysis
- **Inspector**: File and object properties

### macOS Styling
- **SF Pro Display**: Native macOS font family
- **Menlo Font**: Monospace font for code
- **macOS Colors**: Native color schemes
- **Retina Support**: High-resolution display optimization
- **Dark Mode**: Automatic dark mode detection

### System Integration
- **macOS Theme Detection**: Automatic light/dark mode
- **Dock Integration**: Proper dock icon and behavior
- **Mission Control**: Native window management
- **Spaces Support**: Multiple desktop spaces
- **Full Screen**: Native full-screen mode support

## Customization

### Adding New Themes
```python
# Create custom macOS theme
custom_colors = ColorScheme(
    primary_bg="#f5f5f7",      # macOS light gray
    secondary_bg="#e5e5e7",    # Slightly darker
    accent_bg="#007aff",       # macOS blue
    # ... other colors
)

custom_theme = Theme(
    name="macOS Custom",
    colors=custom_colors
)

# Register theme
theme_manager.register_theme(custom_theme)
```

### Modifying Layout for Xcode Style
```python
# Customize layout for iOS/macOS development
layout_config = FlexContainer(
    direction=LayoutDirection.HORIZONTAL,
    children=[
        # Add Xcode-style panes
        FlexPaneConfig(
            name="project_navigator",
            title="Project Navigator",
            builder=self._build_project_navigator,
            custom_titlebar=True,
            detachable=True
        )
    ]
)
```

### Adding macOS-Specific Controls
```python
def _build_macos_pane(self, parent: tk.Frame):
    """Build a macOS-specific pane."""
    theme = self.theme_manager.get_current_theme()

    # Use macOS-style controls
    button = tk.Button(
        parent,
        text="macOS Button",
        bg=theme.button_bg,
        fg=theme.button_text,
        font=('.AppleSystemUIFont', 13),
        relief="flat",
        borderwidth=0
    )
    button.pack(padx=10, pady=5)
```

## Troubleshooting

### Common Issues

1. **Import Errors**:
   ```bash
   # Ensure package is installed
   pip3 install -e .

   # Or install from PyPI
   pip3 install threepanewindows
   ```

2. **Font Issues**:
   ```bash
   # SF Pro should be available on macOS 10.11+
   # For older macOS versions, fallback fonts will be used
   ```

3. **Retina Display Issues**:
   ```bash
   # Run with Retina optimization
   python3 -c "import tkinter as tk; root = tk.Tk(); root.tk.call('tk', 'scaling', 2.0)" macos_flexible_titlebar_demo.py
   ```

4. **Permission Issues**:
   ```bash
   # Make script executable
   chmod +x run_macos_flexible_titlebar_demo.py

   # Check Python installation
   which python3
   ```

### Debug Mode
Run with debug output:
```bash
PYTHONPATH=. python3 -u macos_flexible_titlebar_demo.py
```

### Performance Optimization
For better performance:
```bash
# Disable animations if needed
export DISABLE_ANIMATIONS=1
python3 macos_flexible_titlebar_demo.py
```

## macOS Development Integration

### Xcode Integration
The demo can be integrated with Xcode projects:
```xml
<!-- Add to Info.plist for app integration -->
<key>CFBundleExecutable</key>
<string>macos_flexible_titlebar_demo</string>
<key>CFBundleIdentifier</key>
<string>com.example.flexible-titlebar-demo</string>
```

### Terminal Integration
Run from Terminal with enhanced features:
```bash
# Add to .zshrc or .bash_profile
alias flexible-demo="python3 ~/path/to/macos_flexible_titlebar_demo.py"

# Run the demo
flexible-demo
```

### Homebrew Integration
For easy installation via Homebrew:
```bash
# If available via Homebrew
brew install threepanewindows
python3 macos_flexible_titlebar_demo.py
```

## Apple Silicon Support

### Native Performance
- **M1/M2/M3 Optimization**: Native Apple Silicon performance
- **Rosetta 2 Compatibility**: Works on Intel Macs via Rosetta 2
- **Universal Binary**: Supports both architectures

### Memory Efficiency
- **Unified Memory**: Optimized for Apple Silicon unified memory
- **Energy Efficiency**: Low power consumption on Apple Silicon

## Accessibility

### macOS Accessibility Features
- **VoiceOver Support**: Screen reader compatibility
- **High Contrast**: Support for high contrast themes
- **Reduced Motion**: Respects reduced motion preferences
- **Keyboard Navigation**: Full keyboard accessibility

## Contributing

Feel free to contribute macOS-specific improvements:

1. **macOS-specific Features**: Native macOS integrations
2. **Performance Optimizations**: Apple Silicon optimizations
3. **Visual Enhancements**: macOS Big Sur/Monterey/Ventura styling
4. **Accessibility**: macOS accessibility features

## License

This demo is part of the ThreePaneWindows project and follows the same license terms.

## Support

For macOS-specific support:
- Check macOS compatibility requirements (10.14+)
- Verify Python and tkinter installation
- Review macOS-specific troubleshooting steps
- Test with different macOS versions and architectures

---

**Enjoy the macOS-optimized flexible layout experience!** 🍎
