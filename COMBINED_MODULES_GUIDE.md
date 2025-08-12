# Combined Modules Guide: Typography + Spacing + Central Theme Manager

## Overview

The ThreePaneWindows library provides three independent but complementary modules
for UI styling:

- **Typography Module**: Font management and text styling
- **Spacing Module**: Layout, padding, margins, and spacing
- **Central Theme Manager**: Color theming and comprehensive widget styling

## Key Principle: Independence Through Composition

✅ **What makes this powerful:**

- Each module works independently
- No module imports or depends on the others
- They can be used individually or together
- They complement each other through composition, not inheritance
- No conflicts or duplicate functionality

## Module Responsibilities

### Typography Module (`typography.py`)

- **Purpose**: Font families, sizes, weights, and text styling
- **Independence**: Works without any other modules
- **Key Classes**: `Typography`, `TypographyManager`
- **Global Access**: `get_typography_manager()`

### Spacing Module (`spacing.py`)

- **Purpose**: Padding, margins, borders, layout gaps, and spacing
- **Independence**: Works without any other modules
- **Key Classes**: `Spacing`, `SpacingManager`
- **Global Access**: `get_spacing_manager()`

### Central Theme Manager (`central_theme_manager.py`)

- **Purpose**: Colors, comprehensive widget theming, theme switching
- **Independence**: Works without any other modules
- **Key Classes**: `CentralThemeManager`, `ThemeColors`, `ThemeType`
- **Global Access**: Create instance as needed

## Usage Patterns

### Pattern 1: Individual Module Usage

```python
# Use only Typography
from threepanewindows.typography import Typography, TypographyManager

typography = Typography(font_size_normal=12, font_family="Arial")
typo_manager = TypographyManager(typography)
typo_manager.typography.apply_to_widget(label, size="large", weight="bold")
```

```python
# Use only Spacing
from threepanewindows.spacing import Spacing, SpacingManager

spacing = Spacing(padding_normal=15, margin_normal=10)
spacing_manager = SpacingManager(spacing)
spacing_manager.apply_padding_to_widget(button, size="large")
```

```python
# Use only Central Theme Manager
from threepanewindows.central_theme_manager import CentralThemeManager

theme_manager = CentralThemeManager()
theme_manager.set_theme("dark")
theme_manager.apply_comprehensive_theme(root)
```

### Pattern 2: Combined Usage (Recommended)

```python
import tkinter as tk
from threepanewindows.typography import Typography, TypographyManager
from threepanewindows.spacing import Spacing, SpacingManager
from threepanewindows.central_theme_manager import CentralThemeManager

# Initialize all three modules independently
typography = Typography(font_size_normal=12, font_family="Segoe UI")
typo_manager = TypographyManager(typography)

spacing = Spacing(padding_normal=15, margin_normal=10)
spacing_manager = SpacingManager(spacing)

theme_manager = CentralThemeManager()
theme_manager.set_theme("dark")

# Create UI using all three
root = tk.Tk()

# Typography handles fonts
title = tk.Label(root, text="My Application")
typo_manager.typography.apply_to_widget(title, size="title", weight="bold")

# Spacing handles layout
title.pack(pady=spacing.get_margin("large"))

# Theme Manager handles colors
theme_manager.apply_comprehensive_theme(root)
```

### Pattern 3: Global Managers

```python
from threepanewindows.typography import get_typography_manager
from threepanewindows.spacing import get_spacing_manager
from threepanewindows.central_theme_manager import CentralThemeManager

# Use global instances for convenience
typo_manager = get_typography_manager()
spacing_manager = get_spacing_manager()
theme_manager = CentralThemeManager()

# Apply to widgets
typo_manager.typography.apply_to_widget(widget, size="normal")
spacing_manager.apply_padding_to_widget(widget, size="medium")
theme_manager.apply_theme_to_widget(widget)
```

## Complete Example

```python
#!/usr/bin/env python3
import tkinter as tk
from threepanewindows.typography import Typography, TypographyManager
from threepanewindows.spacing import Spacing, SpacingManager
from threepanewindows.central_theme_manager import CentralThemeManager

def create_styled_application():
    # Initialize modules independently
    typography = Typography(
        font_family="Segoe UI",
        font_size_normal=11,
        font_size_large=14,
        font_size_title=18
    )
    typo_manager = TypographyManager(typography)

    spacing = Spacing(
        padding_normal=12,
        margin_normal=8,
        button_padding_x=16,
        button_padding_y=6
    )
    spacing_manager = SpacingManager(spacing)

    theme_manager = CentralThemeManager()
    theme_manager.set_theme("blue")

    # Create UI
    root = tk.Tk()
    root.title("Combined Modules Example")
    root.geometry("500x300")

    # Main container with spacing
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True,
                   padx=spacing.get_padding("large"),
                   pady=spacing.get_padding("large"))

    # Title with typography
    title = tk.Label(main_frame, text="Styled Application")
    typo_manager.typography.apply_to_widget(title, size="title", weight="bold")
    title.pack(pady=spacing.get_margin("large"))

    # Content with all three modules
    content = tk.Label(main_frame,
                      text="Typography + Spacing + Theme Manager working together!")
    typo_manager.typography.apply_to_widget(content, size="normal")
    content.pack(pady=spacing.get_margin("medium"))

    # Button with custom spacing
    button = tk.Button(main_frame, text="Styled Button")
    button.configure(padx=spacing.button_padding_x, pady=spacing.button_padding_y)
    button.pack(pady=spacing.get_margin("large"))

    # Apply theme colors to everything
    theme_manager.apply_comprehensive_theme(root)

    return root

if __name__ == "__main__":
    app = create_styled_application()
    app.mainloop()
```

## Benefits of This Approach

### 1. **Modularity**

- Use only what you need
- No unnecessary dependencies
- Easy to understand and maintain

### 2. **Flexibility**

- Mix and match modules
- Override specific aspects
- Gradual adoption possible

### 3. **No Conflicts**

- Each module has clear responsibilities
- No overlapping functionality
- No import cycles or dependencies

### 4. **Consistency**

- Unified API patterns across modules
- Consistent naming conventions
- Similar usage patterns

### 5. **Extensibility**

- Easy to add new modules
- Easy to customize existing modules
- Easy to integrate with existing code

## Advanced Usage

### Custom Configurations

```python
# Create custom configurations for each module
custom_typography = Typography(
    font_family="JetBrains Mono",  # Custom font
    font_size_normal=10,
    font_size_large=13
)

custom_spacing = Spacing(
    padding_normal=20,  # More generous padding
    margin_normal=15,
    button_padding_x=25
)

# Use them together
typo_manager = TypographyManager(custom_typography)
spacing_manager = SpacingManager(custom_spacing)
theme_manager = CentralThemeManager()
theme_manager.set_theme("dark")
```

### Dynamic Theme Switching

```python
def switch_theme(theme_name):
    """Switch theme while keeping typography and spacing unchanged."""
    theme_manager.set_theme(theme_name)
    theme_manager.apply_comprehensive_theme(root)
    # Typography and spacing remain unchanged!

# Theme switching buttons
for theme in ["light", "dark", "blue"]:
    btn = tk.Button(root, text=theme.title(),
                   command=lambda t=theme: switch_theme(t))
```

### Responsive Scaling

```python
def scale_ui(scale_factor):
    """Scale fonts and spacing together."""
    # Scale typography
    typo_manager.scale_fonts(scale_factor)

    # Scale spacing
    spacing_manager.scale_spacing(scale_factor)

    # Theme colors remain unchanged
```

## Best Practices

1. **Initialize Early**: Set up all modules at application startup
2. **Use Composition**: Combine modules through composition, not inheritance
3. **Consistent Patterns**: Use similar patterns across your application
4. **Global vs Local**: Use global managers for convenience, local for customization
5. **Theme Last**: Apply themes after setting up typography and spacing
6. **Test Independence**: Ensure each module works independently

## Troubleshooting

### Common Issues

1. **Font Creation Errors**: Ensure Tkinter root window exists before creating fonts
2. **Theme Not Applied**: Call `apply_comprehensive_theme()` after setting theme
3. **Spacing Not Visible**: Check that widgets are packed/gridded properly
4. **Module Not Found**: Ensure proper imports from `threepanewindows` package

### Debug Tips

```python
# Enable logging to see what each module is doing
import logging
logging.basicConfig(level=logging.DEBUG)

# Check module states
print(f"Current theme: {theme_manager.get_current_theme()}")
print(f"Font cache size: {len(typo_manager._font_cache)}")
print(f"Spacing values: {spacing.get_padding('normal')}")
```

## Conclusion

The combination of Typography, Spacing, and Central Theme Manager modules
provides a powerful, flexible, and maintainable approach to UI styling. Each
module maintains its independence while working harmoniously with the others,
giving you the best of both worlds: modularity and integration.
