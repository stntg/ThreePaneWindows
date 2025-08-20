# Linux Comprehensive Demo

This demo showcases the full capabilities of ThreePaneWindows specifically optimized for Linux desktop environments.

## Features Demonstrated

### 🐧 Linux-Specific Optimizations
- **Desktop Environment Detection**: Automatically detects GNOME, KDE, XFCE, and other Linux desktop environments
- **Dark Mode Integration**: Automatically detects system dark mode and applies appropriate themes
- **Native Color Schemes**: Uses desktop environment-specific color schemes (GNOME Adwaita, KDE Breeze, etc.)
- **Window Manager Integration**: Proper window class setting and Linux window manager compatibility

### 🎨 Central Theming System
- **Multiple Theme Support**: Light, Dark, Blue, Green, Purple, and System themes
- **Linux-Native Colors**: Desktop environment-specific color palettes
- **Automatic Theme Switching**: Based on system dark mode detection
- **Accent Color Integration**: Uses system accent colors when available

### 🔤 Typography System
- **Linux-Optimized Fonts**:
  - Primary: Ubuntu font family
  - Fallback: DejaVu Sans
  - Monospace: Ubuntu Mono / DejaVu Sans Mono
- **Scalable Font Sizes**: From tiny (9px) to display (21px) optimized for Linux displays
- **Font Weight Support**: Light, normal, medium, and bold weights
- **Platform Adjustments**: Automatic font size adjustments for different Linux distributions

### 📏 Spacing System
- **Linux-Appropriate Spacing**: Compact spacing optimized for Linux desktop environments
- **Responsive Layout**: Automatic spacing adjustments based on desktop environment
- **Component-Specific Spacing**: Optimized padding and margins for buttons, panels, and inputs
- **Scalable Spacing**: Adjustable spacing system with multiple size options

### 🖼️ Linux-Compatible Icons
- **PNG Format**: Optimized PNG icons for best Linux compatibility
- **High-Quality Icons**: Professional icon set with consistent styling
- **Multiple Categories**: File management, system tools, network utilities, and more
- **Fallback Support**: Text-based emoji fallbacks when icons aren't available

### 🏗️ Flexible Layout System
- **Complex Nested Layouts**: Horizontal and vertical containers with multiple panes
- **Detachable Panels**: Professional detached windows with Linux window manager integration
- **Responsive Design**: Automatic layout adjustments based on window size
- **Theme Preservation**: Detached windows maintain theme consistency

## Demo Components

### 📁 File Explorer Panel
- Linux file system navigation
- Simulated directory structure (`/home`, `/usr`, `/etc`, etc.)
- File operations (open, copy path, search)
- Linux-style file tree with icons

### 📊 Data View Panel
- **System Information Tab**: Comprehensive Linux system details
- **Process Monitor Tab**: Simulated Linux process list
- **Network Tab**: Network configuration and connection details

### ⚙️ Properties Panel
- **Theme Settings**: Live theme switching with preview
- **Font Settings**: Real-time font scaling and preview
- **Linux Settings**: Desktop environment-specific configurations

### 🔧 Tools Panel
- **System Tools**: Process monitor, system monitor, log viewer
- **File Tools**: File manager, disk usage, file search
- **Network Tools**: Network info, port scanner, ping test

## System Requirements

### Minimum Requirements
- **OS**: Linux (any distribution)
- **Python**: 3.8 or higher
- **Desktop Environment**: Any (GNOME, KDE, XFCE, etc.)
- **Display**: Any resolution (optimized for 1920x1080+)

### Recommended Requirements
- **OS**: Ubuntu 20.04+, Fedora 34+, or equivalent
- **Python**: 3.9 or higher
- **Desktop Environment**: GNOME 40+, KDE Plasma 5.20+, or XFCE 4.16+
- **Display**: 1920x1080 or higher
- **Fonts**: Ubuntu fonts installed (usually default on Ubuntu)

### Optional Dependencies
- **darkdetect**: For enhanced dark mode detection
- **Pillow**: For advanced image processing (if needed)

## Running the Demo

### Method 1: Direct Execution
```bash
cd /path/to/ThreePaneWindows
python3 examples/linux_comprehensive_demo.py
```

### Method 2: Using the Launcher
```bash
cd /path/to/ThreePaneWindows
python3 run_linux_demo.py
```

### Method 3: Make Executable
```bash
chmod +x examples/linux_comprehensive_demo.py
./examples/linux_comprehensive_demo.py
```

## Desktop Environment Support

### GNOME
- ✅ Dark mode detection via gsettings
- ✅ Accent color detection
- ✅ Adwaita color scheme
- ✅ Window manager integration

### KDE Plasma
- ✅ Dark mode detection via kreadconfig5
- ✅ Breeze color scheme
- ✅ Window manager integration
- ✅ Transparency support

### XFCE
- ✅ Basic theme detection
- ✅ Window manager integration
- ✅ Standard Linux features

### Other Desktop Environments
- ✅ Generic Linux support
- ✅ Fallback color schemes
- ✅ Basic window management

## Features in Detail

### Automatic Dark Mode Detection
The demo automatically detects if your Linux system is using dark mode through:
1. **darkdetect library** (if installed)
2. **GNOME gsettings** for GNOME desktop
3. **KDE kreadconfig5** for KDE Plasma
4. **Environment variables** (GTK_THEME, etc.)

### Font System
The typography system automatically selects the best fonts for your Linux system:
- **Ubuntu systems**: Uses Ubuntu font family
- **Other distributions**: Falls back to DejaVu Sans
- **Monospace**: Prefers Ubuntu Mono, falls back to DejaVu Sans Mono
- **Font scaling**: Adjustable from 80% to 150% of base size

### Icon System
All icons are provided in PNG format for maximum Linux compatibility:
- **High DPI support**: Icons scale properly on high-resolution displays
- **Theme integration**: Icons adapt to current theme colors
- **Fallback system**: Text-based emoji fallbacks ensure functionality

### Window Management
The demo integrates properly with Linux window managers:
- **Window class setting**: Proper application identification
- **Titlebar customization**: Respects desktop environment preferences
- **Focus management**: Proper window focus and raising behavior
- **Transparency support**: Detects and uses compositor transparency

## Keyboard Shortcuts

### File Operations
- `Ctrl+N`: New Project
- `Ctrl+O`: Open Project
- `Ctrl+S`: Save Project
- `Ctrl+E`: Export Data
- `Ctrl+Q`: Exit Application

### View Controls
- `F5`: Refresh View
- `Ctrl++`: Zoom In
- `Ctrl+-`: Zoom Out
- `F11`: Toggle Fullscreen

### Linux Standard
- `Alt+F4`: Close Window
- `Super+L`: Lock Screen (system shortcut)
- `Ctrl+Alt+T`: Terminal (system shortcut)

## Troubleshooting

### Common Issues

#### Fonts Not Loading
```bash
# Install Ubuntu fonts (on non-Ubuntu systems)
sudo apt install fonts-ubuntu  # Debian/Ubuntu
sudo dnf install ubuntu-family-fonts  # Fedora
sudo pacman -S ttf-ubuntu-font-family  # Arch Linux
```

#### Icons Not Displaying
- Ensure PNG support is available in your Python/Tkinter installation
- Check that icon files exist in `threepanewindows/utils/icons/`
- Verify file permissions allow reading

#### Dark Mode Not Detected
- Install darkdetect: `pip install darkdetect`
- Ensure gsettings is available (GNOME)
- Ensure kreadconfig5 is available (KDE)

#### Window Manager Issues
- Try different desktop environments
- Check compositor settings for transparency
- Verify window manager supports custom window classes

### Performance Tips

#### For Better Performance
- Use a compositor for smooth animations
- Ensure adequate RAM (2GB+ recommended)
- Use SSD storage for faster file operations
- Enable hardware acceleration if available

#### For Lower-End Systems
- Use Light theme instead of Dark theme
- Reduce font scaling to 90% or lower
- Disable transparency effects
- Use smaller window sizes

## Development Notes

### Code Structure
- **Main Demo Class**: `LinuxComprehensiveDemo`
- **Platform Handler**: `LinuxPlatformHandler`
- **Theme Integration**: Central theme manager
- **Layout System**: Enhanced flexible layout
- **Component Builders**: Separate methods for each panel

### Customization Points
- **Themes**: Add new themes in theme manager
- **Fonts**: Modify typography configuration
- **Icons**: Add new PNG icons to utils/icons/
- **Layout**: Modify pane configurations
- **Content**: Customize panel builders

### Testing
The demo has been tested on:
- Ubuntu 20.04, 22.04, 24.04
- Fedora 36, 37, 38
- Arch Linux (current)
- openSUSE Tumbleweed
- Linux Mint 21

## Contributing

To contribute improvements to the Linux demo:

1. **Test on Multiple Distributions**: Ensure compatibility
2. **Follow Linux Standards**: Use appropriate conventions
3. **Optimize for Performance**: Consider lower-end hardware
4. **Document Changes**: Update this README
5. **Test Desktop Environments**: Verify GNOME, KDE, XFCE support

## License

This demo is part of the ThreePaneWindows project and follows the same license terms.

---

**Enjoy exploring ThreePaneWindows on Linux! 🐧**
