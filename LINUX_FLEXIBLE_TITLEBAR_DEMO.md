# Linux Flexible Layout + Custom Titlebar Demo

A comprehensive standalone example demonstrating the ThreePaneWindows flexible layout system with custom titlebar functionality and complete theme switching capabilities, optimized for Linux systems.

## Features

### 🎨 **Complete Theme Switching**
- **All Available Themes**: Light, Dark, Blue Professional, Green Nature, Purple Elegance, System, Native
- **Real-time Updates**: All UI elements update instantly when switching themes
- **Detached Window Consistency**: Detached panes maintain theme consistency
- **Titlebar Integration**: Theme switching menu integrated directly into custom titlebar

### 📐 **Flexible Layout System**
- **Complex Nested Layout**: 6 panes arranged in a professional IDE-like layout
- **Detachable Panes**: All panes can be detached into separate windows
- **Custom Titlebars**: Both main window and detached panes use custom titlebars
- **Professional Styling**: Linux-optimized fonts, spacing, and visual elements

### 🪟 **Advanced Window Management**
- **Custom Titlebar**: Cross-platform custom titlebar implementation
- **Window Controls**: Minimize, maximize, close buttons (Linux)
- **Drag & Drop**: Window dragging functionality
- **Focus Management**: Proper window focus and activation
- **Icon Support**: Cross-platform icon loading and display

### 🐧 **Linux Optimizations**
- **Native Fonts**: Ubuntu, DejaVu Sans font families
- **Desktop Integration**: Proper window manager integration
- **Dark Mode Detection**: Automatic system theme detection
- **PNG Icon Support**: Linux-compatible icon formats

## Layout Structure

```
┌─────────────────────────────────────────────────────────────────┐
│ 🎨 Custom Titlebar with Theme Menu                              │
├─────────────┬─────────────────────────────┬─────────────────────┤
│ 📁 Explorer │ 📝 Code Editor              │ 🔧 Properties       │
│             │                             │                     │
│             │                             │                     │
├─────────────┼─────────────────────────────┼─────────────────────┤
│ 📋 Outline  │ 💻 Terminal                 │ 🐛 Debug Console    │
│             │                             │                     │
│             │                             ├─────────────────────┤
│             │                             │ 📤 Output           │
└─────────────┴─────────────────────────────┴─────────────────────┘
```

## Panes Description

1. **📁 File Explorer**: Project file tree with toolbar buttons
2. **📋 Document Outline**: Code structure and navigation
3. **📝 Code Editor**: Syntax-highlighted code editor with tabs and line numbers
4. **💻 Terminal**: Interactive terminal with sample output
5. **🔧 Properties**: File and theme information panel
6. **🐛 Debug Console**: Debug output and controls
7. **📤 Output**: Build and compilation output

## Installation & Usage

### Prerequisites
- Python 3.8 or higher
- tkinter (usually included with Python)
- ThreePaneWindows package

### Quick Start

1. **Clone or download the project**:
   ```bash
   git clone <repository-url>
   cd ThreePaneWindows
   ```

2. **Install the package**:
   ```bash
   pip install -e .
   ```

3. **Run the demo**:
   ```bash
   python3 run_linux_flexible_titlebar_demo.py
   ```

   Or run directly:
   ```bash
   python3 linux_flexible_titlebar_demo.py
   ```

4. **Make executable (optional)**:
   ```bash
   chmod +x run_linux_flexible_titlebar_demo.py
   ./run_linux_flexible_titlebar_demo.py
   ```

### Alternative Installation

If you prefer to install from PyPI:
```bash
pip install threepanewindows
python3 linux_flexible_titlebar_demo.py
```

## Usage Instructions

### Theme Switching
1. Click the **🎨 Themes** button in the custom titlebar
2. Select any theme from the dropdown menu
3. Watch as all UI elements update in real-time
4. Detached windows automatically update to match

### Pane Management
1. **Detach Panes**: Click the detach button (↗️) in any pane header
2. **Reattach Panes**: Click the reattach button (↙️) in detached window
3. **Resize Panes**: Drag the splitter bars between panes
4. **Focus Windows**: Click on any window to bring it to front

### Available Themes

| Theme | Description | Best For |
|-------|-------------|----------|
| ☀️ **Light** | Clean, bright interface | Daytime work, presentations |
| 🌙 **Dark** | Easy on the eyes | Night coding, reduced eye strain |
| 💙 **Blue Professional** | Corporate look | Business applications |
| 💚 **Green Nature** | Calming colors | Long coding sessions |
| 💜 **Purple Elegance** | Modern, sophisticated | Creative work |
| 🖥️ **System** | Follows OS theme | Automatic adaptation |
| 🏠 **Native** | Platform colors | OS integration |

## Technical Details

### Architecture
- **Flexible Layout Engine**: Dynamic pane arrangement and sizing
- **Theme Management**: Centralized theme system with real-time updates
- **Custom Titlebar**: Cross-platform titlebar implementation
- **Window Management**: Professional detached window handling

### Platform Support
- **Primary**: Linux (Ubuntu, Fedora, openSUSE, etc.)
- **Secondary**: Windows (with Windows-specific adaptations)
- **Secondary**: macOS (with macOS-specific adaptations)

### Dependencies
- `tkinter`: GUI framework (included with Python)
- `threepanewindows`: Main package
- `typing`: Type hints (Python 3.8+)

### File Structure
```
linux_flexible_titlebar_demo.py          # Main demo application
run_linux_flexible_titlebar_demo.py      # Launcher script
LINUX_FLEXIBLE_TITLEBAR_DEMO.md         # This documentation
```

## Customization

### Adding New Themes
```python
# Create custom theme
custom_colors = ColorScheme(
    primary_bg="#your_color",
    secondary_bg="#your_color",
    # ... other colors
)

custom_theme = Theme(
    name="Custom",
    colors=custom_colors
)

# Register theme
theme_manager.register_theme(custom_theme)
```

### Modifying Layout
```python
# Customize layout structure in _setup_layout()
layout_config = FlexContainer(
    direction=LayoutDirection.HORIZONTAL,
    children=[
        # Add your panes here
        FlexPaneConfig(
            name="your_pane",
            title="Your Pane",
            builder=self._build_your_pane,
            custom_titlebar=True,
            detachable=True
        )
    ]
)
```

### Adding New Panes
```python
def _build_your_pane(self, parent: tk.Frame):
    """Build your custom pane."""
    theme = self.theme_manager.get_current_theme()

    # Create your pane content here
    label = tk.Label(
        parent,
        text="Your Content",
        bg=theme.colors.primary_bg,
        fg=theme.colors.primary_text
    )
    label.pack(fill="both", expand=True)
```

## Troubleshooting

### Common Issues

1. **Import Errors**:
   ```bash
   # Ensure package is installed
   pip install -e .

   # Or install from PyPI
   pip install threepanewindows
   ```

2. **Display Issues on Linux**:
   ```bash
   # Check DISPLAY variable
   echo $DISPLAY

   # For WSL users
   export DISPLAY=:0
   ```

3. **Font Issues**:
   ```bash
   # Install Ubuntu fonts
   sudo apt install fonts-ubuntu

   # Install DejaVu fonts
   sudo apt install fonts-dejavu
   ```

4. **Permission Issues**:
   ```bash
   # Make script executable
   chmod +x run_linux_flexible_titlebar_demo.py
   ```

### Debug Mode
Run with debug output:
```bash
PYTHONPATH=. python3 -u linux_flexible_titlebar_demo.py
```

### Log Files
Check logs in the `logs/` directory for detailed error information.

## Contributing

Feel free to contribute improvements:

1. **Bug Reports**: Open an issue with detailed reproduction steps
2. **Feature Requests**: Suggest new features or enhancements
3. **Pull Requests**: Submit code improvements or fixes
4. **Documentation**: Help improve this documentation

## License

This demo is part of the ThreePaneWindows project and follows the same license terms.

## Support

For support and questions:
- Check the main ThreePaneWindows documentation
- Open an issue on the project repository
- Review the troubleshooting section above

---

**Enjoy exploring the flexible layout system with custom titlebar functionality!** 🚀
