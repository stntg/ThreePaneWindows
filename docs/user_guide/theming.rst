Theming System
==============

ThreePaneWindows includes a comprehensive theming system that provides professional appearance and consistent styling across all components.

Overview
--------

The theming system supports:

* **Built-in Themes**: Professional light, dark, and blue themes
* **Custom Themes**: Create your own themes with custom colors and styles
* **Dynamic Theme Switching**: Change themes at runtime
* **Component-Specific Styling**: Fine-tune individual components
* **Cross-Platform Consistency**: Themes work consistently across all platforms

Built-in Themes
----------------

Light Theme
~~~~~~~~~~~

Clean, modern light theme suitable for most applications.

.. code-block:: python

    from threepanewindows import EnhancedDockableThreePaneWindow

    window = EnhancedDockableThreePaneWindow(
        root,
        # ... other parameters ...
        theme_name="light"
    )

**Characteristics:**
- Light backgrounds with dark text
- Subtle borders and separators
- Professional appearance
- Good readability in bright environments

Dark Theme
~~~~~~~~~~

Professional dark theme for reduced eye strain and modern appearance.

.. code-block:: python

    window = EnhancedDockableThreePaneWindow(
        root,
        # ... other parameters ...
        theme_name="dark"
    )

**Characteristics:**
- Dark backgrounds with light text
- Reduced eye strain in low-light environments
- Modern, professional appearance
- Popular with developers and power users

Blue Theme
~~~~~~~~~~

Professional blue theme combining the best of light and dark themes.

.. code-block:: python

    window = EnhancedDockableThreePaneWindow(
        root,
        # ... other parameters ...
        theme_name="blue"
    )

**Characteristics:**
- Blue accent colors
- Professional corporate appearance
- Good contrast and readability
- Suitable for business applications

Using the Theme Manager
-----------------------

The ThemeManager provides advanced theme control:

.. code-block:: python

    from threepanewindows import get_theme_manager, ThemeType

    # Get the global theme manager
    theme_manager = get_theme_manager()

    # Apply a theme
    theme_manager.apply_theme(window, ThemeType.DARK)

    # Get current theme
    current_theme = theme_manager.get_current_theme()
    print(f"Current theme: {current_theme}")

**Available Theme Types:**

.. code-block:: python

    from threepanewindows import ThemeType

    # Enum values for type safety
    ThemeType.LIGHT    # Light theme
    ThemeType.DARK     # Dark theme
    ThemeType.BLUE     # Blue professional theme

Dynamic Theme Switching
-----------------------

Change themes at runtime for better user experience:

.. code-block:: python

    import tkinter as tk
    from threepanewindows import EnhancedDockableThreePaneWindow, get_theme_manager

    def create_themed_application():
        root = tk.Tk()
        root.title("Themed Application")
        
        # Create window with initial theme
        window = EnhancedDockableThreePaneWindow(
            root,
            # ... configuration ...
            theme_name="light"
        )
        
        # Theme switching function
        def switch_theme(theme_name):
            theme_manager = get_theme_manager()
            theme_manager.apply_theme(window, theme_name)
            root.update()  # Refresh the display
        
        # Add theme selection menu
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        
        theme_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Theme", menu=theme_menu)
        
        theme_menu.add_command(label="Light", command=lambda: switch_theme("light"))
        theme_menu.add_command(label="Dark", command=lambda: switch_theme("dark"))
        theme_menu.add_command(label="Blue", command=lambda: switch_theme("blue"))
        
        return root

**Theme Persistence:**

.. code-block:: python

    import json
    import os

    def save_theme_preference(theme_name):
        """Save user's theme preference."""
        config = {"theme": theme_name}
        with open("app_config.json", "w") as f:
            json.dump(config, f)

    def load_theme_preference():
        """Load user's theme preference."""
        try:
            with open("app_config.json", "r") as f:
                config = json.load(f)
                return config.get("theme", "light")
        except FileNotFoundError:
            return "light"  # Default theme

    # Use saved theme
    preferred_theme = load_theme_preference()
    window = EnhancedDockableThreePaneWindow(
        root,
        # ... other parameters ...
        theme_name=preferred_theme
    )

Custom Themes
-------------

Create custom themes for unique branding:

.. code-block:: python

    from threepanewindows.themes import ThemeManager, Theme

    def create_custom_theme():
        """Create a custom corporate theme."""
        
        # Define custom colors
        custom_theme = Theme(
            name="corporate",
            background="#f8f9fa",
            foreground="#212529",
            accent="#007bff",
            border="#dee2e6",
            hover="#e9ecef",
            active="#0056b3",
            text="#495057",
            text_secondary="#6c757d"
        )
        
        # Register the theme
        theme_manager = ThemeManager()
        theme_manager.register_theme(custom_theme)
        
        return custom_theme

    # Use custom theme
    custom_theme = create_custom_theme()
    window = EnhancedDockableThreePaneWindow(
        root,
        # ... other parameters ...
        theme_name="corporate"
    )

**Theme Properties:**

.. code-block:: python

    class Theme:
        def __init__(self,
                     name: str,
                     background: str = "#ffffff",      # Main background color
                     foreground: str = "#000000",      # Main text color
                     accent: str = "#0078d4",          # Accent/highlight color
                     border: str = "#cccccc",          # Border color
                     hover: str = "#f0f0f0",           # Hover state color
                     active: str = "#005a9e",          # Active state color
                     text: str = "#333333",            # Primary text color
                     text_secondary: str = "#666666"   # Secondary text color
                     ):
            # Theme implementation

Component-Specific Styling
---------------------------

Fine-tune individual components:

.. code-block:: python

    from threepanewindows.themes import get_theme_manager

    def customize_component_styling():
        theme_manager = get_theme_manager()
        
        # Get current theme
        theme = theme_manager.get_current_theme()
        
        # Customize specific components
        theme.pane_header_bg = "#2c3e50"      # Pane header background
        theme.pane_header_fg = "#ecf0f1"      # Pane header text
        theme.separator_color = "#34495e"      # Separator color
        theme.detached_window_bg = "#ffffff"   # Detached window background
        
        # Apply customizations
        theme_manager.apply_theme(window, theme)

**Styling Detached Windows:**

.. code-block:: python

    def on_pane_detached(pane_side, detached_window):
        """Customize detached window appearance."""
        theme_manager = get_theme_manager()
        current_theme = theme_manager.get_current_theme()
        
        # Apply theme to detached window
        detached_window.configure(bg=current_theme.background)
        
        # Customize title bar (platform-dependent)
        if hasattr(detached_window, 'wm_attributes'):
            # Windows-specific customizations
            detached_window.wm_attributes('-alpha', 0.95)  # Slight transparency

    window = EnhancedDockableThreePaneWindow(
        root,
        # ... other parameters ...
        on_detach=on_pane_detached
    )

System Theme Integration
------------------------

Integrate with system theme preferences:

.. code-block:: python

    import platform
    import subprocess

    def detect_system_theme():
        """Detect system theme preference."""
        system = platform.system()
        
        if system == "Windows":
            try:
                # Windows 10/11 theme detection
                import winreg
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                   r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize")
                value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
                return "light" if value else "dark"
            except:
                return "light"
        
        elif system == "Darwin":  # macOS
            try:
                result = subprocess.run(['defaults', 'read', '-g', 'AppleInterfaceStyle'], 
                                      capture_output=True, text=True)
                return "dark" if "Dark" in result.stdout else "light"
            except:
                return "light"
        
        else:  # Linux and others
            # Check common environment variables
            desktop = os.environ.get('XDG_CURRENT_DESKTOP', '').lower()
            if 'gnome' in desktop:
                try:
                    result = subprocess.run(['gsettings', 'get', 'org.gnome.desktop.interface', 'gtk-theme'], 
                                          capture_output=True, text=True)
                    return "dark" if "dark" in result.stdout.lower() else "light"
                except:
                    pass
            
            return "light"  # Default fallback

    # Use system theme
    system_theme = detect_system_theme()
    window = EnhancedDockableThreePaneWindow(
        root,
        # ... other parameters ...
        theme_name=system_theme
    )

Theme Validation and Testing
----------------------------

Ensure themes work correctly:

.. code-block:: python

    def validate_theme(theme):
        """Validate theme colors and properties."""
        required_properties = [
            'background', 'foreground', 'accent', 'border',
            'hover', 'active', 'text', 'text_secondary'
        ]
        
        for prop in required_properties:
            if not hasattr(theme, prop):
                raise ValueError(f"Theme missing required property: {prop}")
            
            color = getattr(theme, prop)
            if not color.startswith('#') or len(color) != 7:
                raise ValueError(f"Invalid color format for {prop}: {color}")
        
        return True

    def test_theme_contrast(theme):
        """Test theme for sufficient contrast."""
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        def calculate_contrast(color1, color2):
            # Simplified contrast calculation
            rgb1 = hex_to_rgb(color1)
            rgb2 = hex_to_rgb(color2)
            
            # Calculate relative luminance (simplified)
            lum1 = sum(rgb1) / 3
            lum2 = sum(rgb2) / 3
            
            return abs(lum1 - lum2) / 255
        
        # Test key color combinations
        bg_fg_contrast = calculate_contrast(theme.background, theme.foreground)
        if bg_fg_contrast < 0.5:  # Minimum contrast threshold
            print("Warning: Low contrast between background and foreground")
        
        return bg_fg_contrast

**Theme Testing Example:**

.. code-block:: python

    def create_theme_test_window():
        """Create a window for testing themes."""
        root = tk.Tk()
        root.title("Theme Testing")
        
        def build_test_panel(frame):
            # Test various UI elements
            tk.Label(frame, text="Sample Text", font=("Arial", 12)).pack(pady=5)
            tk.Button(frame, text="Sample Button").pack(pady=5)
            tk.Entry(frame).pack(pady=5, fill=tk.X, padx=10)
            
            # Test listbox
            listbox = tk.Listbox(frame, height=4)
            listbox.pack(pady=5, fill=tk.X, padx=10)
            for i in range(5):
                listbox.insert(tk.END, f"Item {i+1}")
        
        # Create test window with all themes
        themes = ["light", "dark", "blue"]
        for i, theme in enumerate(themes):
            test_window = tk.Toplevel(root)
            test_window.title(f"Theme Test: {theme.title()}")
            test_window.geometry(f"{300}x{400}+{100 + i*320}+{100}")
            
            window = EnhancedDockableThreePaneWindow(
                test_window,
                left_config=PaneConfig(title=f"{theme.title()} Theme"),
                center_config=PaneConfig(title="Test Panel"),
                right_config=PaneConfig(title="Controls"),
                left_builder=build_test_panel,
                center_builder=build_test_panel,
                right_builder=build_test_panel,
                theme_name=theme
            )
            window.pack(fill=tk.BOTH, expand=True)
        
        return root

Best Practices
--------------

**Theme Selection:**
1. Choose themes appropriate for your application's context
2. Consider your target audience (developers prefer dark themes)
3. Test themes in different lighting conditions
4. Provide theme options for user preference

**Custom Themes:**
1. Maintain sufficient contrast for accessibility
2. Test on different screen types and resolutions
3. Use consistent color schemes throughout
4. Consider color blindness when choosing colors

**Performance:**
1. Avoid frequent theme switching during runtime
2. Cache theme resources when possible
3. Use efficient color representations
4. Minimize theme-related computations

**Accessibility:**
1. Ensure sufficient contrast ratios (WCAG guidelines)
2. Test with screen readers
3. Provide high-contrast theme options
4. Support system accessibility settings

**Cross-Platform:**
1. Test themes on all target platforms
2. Account for platform-specific rendering differences
3. Use system fonts when appropriate
4. Respect platform conventions

Troubleshooting
---------------

**Common Issues:**

*Theme not applying:*
- Ensure theme name is correct
- Check if theme is registered with ThemeManager
- Verify theme properties are valid

*Colors not displaying correctly:*
- Check color format (must be hex: #RRGGBB)
- Verify platform-specific color support
- Test on different displays

*Performance issues:*
- Avoid complex theme switching logic
- Cache theme objects
- Minimize theme-related calculations

*Accessibility problems:*
- Test contrast ratios
- Verify with accessibility tools
- Get feedback from users with disabilities

The theming system provides powerful tools for creating professional, accessible, and visually appealing applications that work consistently across all platforms.