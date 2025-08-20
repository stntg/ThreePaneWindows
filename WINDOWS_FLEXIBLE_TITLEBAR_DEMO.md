# Windows Flexible Layout + Custom Titlebar Demo

A comprehensive standalone example demonstrating the ThreePaneWindows flexible layout system with custom titlebar functionality and complete theme switching capabilities, optimized for Windows systems.

## Features

### 🎨 **Complete Theme Switching**
- **All Available Themes**: Light, Dark, Blue Professional, Green Nature, Purple Elegance, System, Native
- **Real-time Updates**: All UI elements update instantly when switching themes
- **Detached Window Consistency**: Detached panes maintain theme consistency
- **Titlebar Integration**: Theme switching menu integrated directly into custom titlebar
- **System Theme Integration**: Automatic Windows theme detection and integration

### 📐 **Flexible Layout System**
- **Complex Nested Layout**: 6 panes arranged in a Visual Studio-inspired layout
- **Detachable Panes**: All panes can be detached into separate windows
- **Custom Titlebars**: Both main window and detached panes use custom titlebars
- **Professional Styling**: Windows-optimized fonts, spacing, and visual elements

### 🪟 **Advanced Window Management**
- **Custom Titlebar**: Windows-specific custom titlebar implementation
- **Window Controls**: Minimize, maximize, close buttons (Windows style)
- **Drag & Drop**: Window dragging functionality
- **Focus Management**: Proper window focus and activation
- **Icon Support**: Windows-compatible icon formats (.ico, .png)

### 🪟 **Windows Optimizations**
- **Native Fonts**: Segoe UI, Consolas font families
- **Desktop Integration**: Proper Windows desktop integration
- **DPI Awareness**: High-DPI display support
- **System Theme Detection**: Automatic Windows theme detection

## Layout Structure

```
┌─────────────────────────────────────────────────────────────────┐
│ 🎨 Custom Titlebar with Theme Menu                              │
├─────────────┬─────────────────────────────┬─────────────────────┤
│ 📁 Solution │ 📝 Code Editor              │ 🧰 Toolbox          │
│ Explorer    │                             │                     │
│             │                             │                     │
├─────────────┼─────────────────────────────┼─────────────────────┤
│ 🔧 Properties│ 💻 Command Prompt          │ ❌ Error List       │
│             │                             │                     │
│             │                             ├─────────────────────┤
│             │                             │ 📤 Output           │
└─────────────┴─────────────────────────────┴─────────────────────┘
```

## Panes Description

1. **📁 Solution Explorer**: Visual Studio-style project file tree with toolbar
2. **🔧 Properties**: File and theme information panel with system details
3. **📝 Code Editor**: C# syntax-highlighted code editor with tabs and line numbers
4. **💻 Command Prompt**: Windows command prompt with sample output
5. **🧰 Toolbox**: Visual Studio-style toolbox with common controls
6. **❌ Error List**: Build errors, warnings, and messages
7. **📤 Output**: Build and compilation output with source selection

## Installation & Usage

### Prerequisites
- Python 3.8 or higher
- tkinter (usually included with Python)
- ThreePaneWindows package
- Windows 10/11 (optimized for)

### Quick Start

1. **Clone or download the project**:
   ```cmd
   git clone <repository-url>
   cd ThreePaneWindows
   ```

2. **Install the package**:
   ```cmd
   pip install -e .
   ```

3. **Run the demo**:
   ```cmd
   python run_windows_flexible_titlebar_demo.py
   ```

   Or run directly:
   ```cmd
   python windows_flexible_titlebar_demo.py
   ```

### Alternative Installation

If you prefer to install from PyPI:
```cmd
pip install threepanewindows
python windows_flexible_titlebar_demo.py
```

## Usage Instructions

### Theme Switching
1. Click the **🎨 Themes** button in the custom titlebar
2. Select any theme from the dropdown menu
3. Watch as all UI elements update in real-time
4. Detached windows automatically update to match
5. Use **System Theme** for automatic Windows theme integration

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
| 🖥️ **System** | Follows Windows theme | Automatic adaptation |
| 🏠 **Native** | Windows colors | OS integration |

## Technical Details

### Architecture
- **Flexible Layout Engine**: Dynamic pane arrangement and sizing
- **Theme Management**: Centralized theme system with real-time updates
- **Custom Titlebar**: Windows-specific titlebar implementation
- **Window Management**: Professional detached window handling

### Platform Support
- **Primary**: Windows 10/11 (optimized)
- **Secondary**: Windows 8.1 (basic support)
- **Fallback**: Other platforms (with platform-specific adaptations)

### Dependencies
- `tkinter`: GUI framework (included with Python)
- `threepanewindows`: Main package
- `typing`: Type hints (Python 3.8+)

### File Structure
```
windows_flexible_titlebar_demo.py          # Main demo application
run_windows_flexible_titlebar_demo.py      # Launcher script
WINDOWS_FLEXIBLE_TITLEBAR_DEMO.md         # This documentation
```

## Windows-Specific Features

### Visual Studio Integration
- **Solution Explorer**: Familiar project structure
- **Toolbox**: Common Windows Forms controls
- **Error List**: Build errors and warnings
- **Output Window**: Build and debug output
- **Properties Panel**: File and object properties

### Windows Styling
- **Segoe UI Font**: Native Windows font family
- **Consolas Font**: Monospace font for code
- **Windows Colors**: Native color schemes
- **DPI Awareness**: High-resolution display support

### System Integration
- **Windows Theme Detection**: Automatic light/dark mode
- **Taskbar Integration**: Proper window grouping
- **Alt+Tab Support**: Native window switching
- **Windows Snap**: Snap-to-edge functionality

## Customization

### Adding New Themes
```python
# Create custom Windows theme
custom_colors = ColorScheme(
    primary_bg="#f0f0f0",      # Windows light gray
    secondary_bg="#e0e0e0",    # Slightly darker
    accent_bg="#0078d4",       # Windows blue
    # ... other colors
)

custom_theme = Theme(
    name="Windows Custom",
    colors=custom_colors
)

# Register theme
theme_manager.register_theme(custom_theme)
```

### Modifying Layout for Windows
```python
# Customize layout for Windows development
layout_config = FlexContainer(
    direction=LayoutDirection.HORIZONTAL,
    children=[
        # Add Visual Studio-style panes
        FlexPaneConfig(
            name="solution_explorer",
            title="Solution Explorer",
            builder=self._build_solution_explorer,
            custom_titlebar=True,
            detachable=True
        )
    ]
)
```

### Adding Windows-Specific Controls
```python
def _build_windows_pane(self, parent: tk.Frame):
    """Build a Windows-specific pane."""
    theme = self.theme_manager.get_current_theme()

    # Use Windows-style controls
    button = tk.Button(
        parent,
        text="Windows Button",
        bg=theme.button_bg,
        fg=theme.button_text,
        font=('Segoe UI', 9),
        relief="raised",
        borderwidth=1
    )
    button.pack(padx=5, pady=5)
```

## Troubleshooting

### Common Issues

1. **Import Errors**:
   ```cmd
   # Ensure package is installed
   pip install -e .

   # Or install from PyPI
   pip install threepanewindows
   ```

2. **Font Issues**:
   ```cmd
   # Segoe UI should be available on Windows 10/11
   # For older Windows versions, fallback fonts will be used
   ```

3. **DPI Issues**:
   ```cmd
   # Run with DPI awareness
   python -c "import ctypes; ctypes.windll.shcore.SetProcessDpiAwareness(1)" windows_flexible_titlebar_demo.py
   ```

4. **Theme Detection Issues**:
   ```cmd
   # Manually set theme if auto-detection fails
   set THEME=light
   python windows_flexible_titlebar_demo.py
   ```

### Debug Mode
Run with debug output:
```cmd
set PYTHONPATH=.
python -u windows_flexible_titlebar_demo.py
```

### Performance Optimization
For better performance on older Windows systems:
```cmd
# Disable animations
set DISABLE_ANIMATIONS=1
python windows_flexible_titlebar_demo.py
```

## Windows Development Integration

### Visual Studio Code Integration
The demo can be integrated with VS Code:
```json
{
    "name": "Windows Flexible Demo",
    "type": "python",
    "request": "launch",
    "program": "${workspaceFolder}/windows_flexible_titlebar_demo.py",
    "console": "integratedTerminal"
}
```

### PowerShell Integration
Run from PowerShell with enhanced features:
```powershell
# Set execution policy if needed
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Run the demo
python windows_flexible_titlebar_demo.py
```

## Contributing

Feel free to contribute Windows-specific improvements:

1. **Windows-specific Features**: Native Windows integrations
2. **Performance Optimizations**: Windows-specific performance improvements
3. **Visual Enhancements**: Windows 11 styling updates
4. **Accessibility**: Windows accessibility features

## License

This demo is part of the ThreePaneWindows project and follows the same license terms.

## Support

For Windows-specific support:
- Check Windows compatibility requirements
- Verify Python and tkinter installation
- Review Windows-specific troubleshooting steps
- Test with different Windows versions

---

**Enjoy the Windows-optimized flexible layout experience!** 🪟
