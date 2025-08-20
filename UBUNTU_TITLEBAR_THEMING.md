# Linux Titlebar Theming Guide

## The Challenge

On Linux desktop environments (Ubuntu, WSL, etc.), the window manager controls the titlebar appearance, making it difficult to theme the titlebar to match your application's theme. The system titlebar will always use the system theme colors.

## WSL Special Considerations

When running on Windows Subsystem for Linux (WSL), there are additional considerations:
- WSL uses an X server running on Windows (VcXsrv, Xming, X410)
- Window management behavior differs from native Linux
- Custom titlebars often work better than system integration
- The demo automatically detects WSL and optimizes accordingly

## Solutions Provided

### 1. Enhanced System Integration (Default)

The demo automatically applies enhanced system integration:

- ✅ **Window Background Theming** - Main window background matches the selected theme
- ✅ **Window Class Setting** - Proper window class for better window manager integration
- ✅ **Desktop Environment Detection** - Automatic detection of GNOME, KDE, XFCE, etc.
- ✅ **System Theme Influence** - Attempts to influence system theme when possible
- ✅ **Window Title Updates** - Window title reflects current theme

### 2. Custom Titlebar (Optional)

For complete titlebar theme control, you can enable a custom titlebar:

#### How to Enable Custom Titlebar

**For Native Linux:**
```bash
# Set environment variable before running
export THREEPANE_CUSTOM_TITLEBAR=1
python3 examples/linux_comprehensive_demo.py

# Or run directly with the variable
THREEPANE_CUSTOM_TITLEBAR=1 python3 examples/linux_comprehensive_demo.py
```

**For WSL (Windows Subsystem for Linux):**
```bash
# WSL-optimized launcher (enables custom titlebar by default)
python3 run_wsl_demo.py

# Or manually with environment setup
export DISPLAY=:0  # Adjust for your X server
export THREEPANE_CUSTOM_TITLEBAR=1
python3 examples/linux_comprehensive_demo.py
```

#### Custom Titlebar Features

- ✅ **Full Theme Control** - Titlebar colors match your selected theme perfectly
- ✅ **Custom Window Controls** - Themed minimize and close buttons
- ✅ **Draggable Window** - Click and drag the titlebar to move the window
- ✅ **Theme Responsive** - Titlebar updates when you change themes
- ✅ **Linux-Optimized** - Uses Ubuntu fonts and Linux-appropriate styling
- ✅ **WSL Enhanced** - Double-click to maximize, right-click context menu
- ✅ **Auto-Detection** - Automatically enabled on WSL for better experience

#### Custom Titlebar Trade-offs

**Advantages:**
- Perfect theme matching
- Complete visual control
- Professional appearance
- Consistent with application theme

**Disadvantages:**
- Removes native window manager integration
- No native window controls (maximize, window menu)
- May not integrate with some desktop environment features
- Requires manual window dragging implementation

## Recommendations

### For Most Users (Default Behavior)
Use the default enhanced system integration. This provides:
- Good theme integration where possible
- Full native window manager features
- Better desktop environment integration
- Standard Linux user experience

### For Theme Purists
Enable the custom titlebar when you need:
- Perfect visual consistency
- Complete theme control
- Professional application appearance
- Custom branding requirements

## Implementation Details

### System Integration Approach
```python
# Automatic window background theming
window.configure(bg=theme.primary_bg)

# Window class for better integration
window.wm_class("ThreePaneWindows", "ThreePaneWindows")

# Desktop environment specific optimizations
if desktop_env == "gnome":
    apply_gnome_titlebar_theme(window, theme)
elif desktop_env == "kde":
    apply_kde_titlebar_theme(window, theme)
```

### Custom Titlebar Approach
```python
# Remove window decorations
window.overrideredirect(True)

# Create custom titlebar with theme colors
titlebar = tk.Frame(window, bg=theme.panel_header_bg)

# Add window controls and dragging functionality
add_window_controls(titlebar, theme)
make_draggable(titlebar)
```

## Testing Both Approaches

### Test Default Integration
**Native Linux:**
```bash
python3 examples/linux_comprehensive_demo.py
# Try changing themes and observe window background changes
```

**WSL:**
```bash
python3 run_wsl_demo.py
# WSL launcher automatically configures optimal settings
```

### Test Custom Titlebar
**Native Linux:**
```bash
THREEPANE_CUSTOM_TITLEBAR=1 python3 examples/linux_comprehensive_demo.py
# Try changing themes and observe complete titlebar theming
```

**WSL:**
```bash
python3 run_wsl_demo.py
# Custom titlebar is enabled by default on WSL
# Try changing themes and observe complete titlebar theming
```

## Desktop Environment Specific Notes

### Ubuntu/GNOME
- System titlebar uses Adwaita theme colors
- Window background theming works well
- Custom titlebar provides complete control

### KDE Plasma
- System titlebar uses Breeze theme colors
- Better native theme integration than GNOME
- Custom titlebar still provides more control

### XFCE
- Lightweight window manager
- Basic theme integration
- Custom titlebar works well

### WSL (Windows Subsystem for Linux)
- Automatic WSL detection and optimization
- Custom titlebar enabled by default for better theming
- Enhanced window controls (double-click maximize, right-click menu)
- Optimized for X servers running on Windows

### Other Desktop Environments
- Generic Linux integration provided
- Custom titlebar recommended for consistent theming

## Troubleshooting

### Window Background Not Theming
```bash
# Check if theme manager is working
python3 -c "
from threepanewindows.central_theme_manager import get_theme_manager
tm = get_theme_manager()
print(f'Current theme: {tm.current_theme}')
print(f'Background color: {tm.get_current_theme().primary_bg}')
"
```

### Custom Titlebar Not Appearing
```bash
# Verify environment variable is set
echo $THREEPANE_CUSTOM_TITLEBAR

# Check for errors in the log
python3 examples/linux_comprehensive_demo.py 2>&1 | grep -i titlebar
```

### Theme Changes Not Applying
- Ensure you're using the theme buttons in the Properties panel
- Check that the theme manager is properly initialized
- Try restarting the application

## Conclusion

The Linux demo provides both approaches to titlebar theming:

1. **Default**: Enhanced system integration with good compatibility
2. **Custom**: Complete theme control with custom titlebar

Choose the approach that best fits your needs:
- Use **default** for standard Linux applications
- Use **custom** for branded or theme-critical applications

Both approaches demonstrate the flexibility of the ThreePaneWindows system and provide excellent Linux desktop integration.
