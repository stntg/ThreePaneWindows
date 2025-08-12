# Typography and Spacing Modules

The ThreePaneWindows package includes comprehensive typography and spacing modules
that provide professional text styling and layout management capabilities.

## Typography Module

The typography module (`threepanewindows.typography`) provides comprehensive
font and text styling management.

### Key Classes

#### Typography

A dataclass that defines font families, sizes, weights, and other typography properties.

```python
from threepanewindows import Typography

# Create custom typography
typography = Typography(
    font_family="Arial",
    font_size_normal=12,
    font_size_title=16,
    font_weight_bold="bold"
)

# Get font configuration for widgets
font_config = typography.get_font_config("large", "bold")
label.configure(**font_config)
```

#### TypographyManager

Manages font caching, text metrics, and provides utilities for working with fonts.

```python
from threepanewindows import TypographyManager, get_typography_manager

# Use global manager
manager = get_typography_manager()

# Get cached font object
font = manager.get_font("title", "bold")

# Get text measurements
metrics = manager.get_text_metrics("Sample Text", "normal", "normal")
print(f"Text width: {metrics['width']}, height: {metrics['height']}")

# Scale all fonts
manager.scale_fonts(1.2)  # 20% larger
```

### Predefined Typography Configurations

- **DEFAULT_TYPOGRAPHY**: Standard typography settings
- **COMPACT_TYPOGRAPHY**: Smaller fonts for compact layouts
- **LARGE_TYPOGRAPHY**: Larger fonts for better readability
- **ACCESSIBILITY_TYPOGRAPHY**: High-contrast, large fonts for accessibility

```python
from threepanewindows import LARGE_TYPOGRAPHY, set_global_typography

# Use predefined configuration
set_global_typography(LARGE_TYPOGRAPHY)
```

### Font Sizes

Available font size names:

- `tiny`: 8px (default)
- `small`: 9px (default)
- `normal`: 10px (default)
- `medium`: 11px (default)
- `large`: 12px (default)
- `title`: 14px (default)
- `heading`: 16px (default)
- `display`: 20px (default)

### Font Weights

Available font weight names:

- `light`: Normal weight
- `normal`: Normal weight
- `medium`: Bold weight
- `bold`: Bold weight

### Platform Support

The typography module automatically adjusts fonts for different platforms:

- **Windows**: Uses Segoe UI font family
- **macOS**: Uses SF Pro Display font family with slightly larger sizes
- **Linux**: Uses Ubuntu font family

## Spacing Module

The spacing module (`threepanewindows.spacing`) provides comprehensive layout
spacing and padding management.

### Key Classes

#### Spacing

A dataclass that defines padding, margins, borders, and layout spacing values.

```python
from threepanewindows import Spacing

# Create custom spacing
spacing = Spacing(
    padding_normal=12,
    margin_normal=6,
    border_normal=2
)

# Get spacing values
padding = spacing.get_padding("large")  # 16px
margin = spacing.get_margin("small")    # 2px
border = spacing.get_border_width("thick")  # 3px
```

#### SpacingManager

Provides utilities for applying spacing to widgets and creating layout helpers.

```python
from threepanewindows import SpacingManager, get_spacing_manager

# Use global manager
manager = get_spacing_manager()

# Apply spacing to widgets
manager.apply_padding_to_widget(button, "large")
manager.apply_margin_to_widget(label, "medium")

# Create spacer widgets
spacer = manager.create_spacer(parent, "large", "horizontal")
spacer.pack()

# Create grid layout with consistent spacing
grid = manager.create_layout_grid(parent, rows=3, cols=2, gap_size="normal")
```

### Predefined Spacing Configurations

- **DEFAULT_SPACING**: Standard spacing settings
- **COMPACT_SPACING**: Tighter spacing for compact layouts
- **GENEROUS_SPACING**: More generous spacing for spacious layouts
- **ACCESSIBILITY_SPACING**: Larger spacing for better accessibility

```python
from threepanewindows import GENEROUS_SPACING, set_global_spacing

# Use predefined configuration
set_global_spacing(GENEROUS_SPACING)
```

### Spacing Sizes

Available spacing size names:

**Padding/Margin:**

- `none`: 0px
- `tiny`: 2px (default)
- `small`: 4px (default)
- `normal`: 8px (default)
- `medium`: 12px (default)
- `large`: 16px (default)
- `xl`: 24px (default)
- `xxl`: 32px (default)

**Borders:**

- `none`: 0px
- `thin`: 1px
- `normal`: 2px
- `thick`: 3px
- `heavy`: 4px

**Corner Radius:**

- `none`: 0px
- `small`: 2px
- `normal`: 4px
- `medium`: 6px
- `large`: 8px
- `xl`: 12px
- `round`: 999px (fully rounded)

### Component-Specific Spacing

The spacing module includes predefined spacing for common UI components:

```python
# Get standard button padding
button_padding = manager.get_button_padding()  # (12, 6)

# Get standard input padding
input_padding = manager.get_input_padding()    # (8, 4)

# Get panel spacing configuration
panel_config = manager.get_panel_spacing()
# Returns: {'padding': 16, 'margin': 8, 'header_padding': 12,
#           'content_padding': 16}
```

## Integration with Themes

Both typography and spacing integrate seamlessly with the existing theme system:

```python
from threepanewindows import Theme, ColorScheme, LARGE_TYPOGRAPHY, GENEROUS_SPACING

# Create theme with custom typography and spacing
theme = Theme(
    name="accessible_theme",
    colors=ColorScheme(),
    typography=LARGE_TYPOGRAPHY,
    spacing=GENEROUS_SPACING
)

# Use with theme manager
theme_manager = ThemeManager()
theme_manager.register_theme(theme)
theme_manager.set_theme("accessible_theme")
```

## Advanced Usage

### Custom Font Loading

```python
from threepanewindows import Typography, TypographyManager

# Create typography with custom fonts
typography = Typography(
    font_family="Custom Font",
    font_family_fallback="Arial",
    font_family_monospace="Fira Code",
    font_family_monospace_fallback="Courier New"
)

manager = TypographyManager(typography)

# Apply to widgets
manager.typography.apply_to_widget(code_label, "normal", "normal", "monospace")
```

### Dynamic Scaling

```python
from threepanewindows import get_typography_manager, get_spacing_manager

# Scale typography and spacing together
typography_manager = get_typography_manager()
spacing_manager = get_spacing_manager()

# Scale for high DPI displays
scale_factor = 1.25
typography_manager.scale_fonts(scale_factor)
spacing_manager.scale_spacing(scale_factor)
```

### Layout Utilities

```python
from threepanewindows import get_spacing_manager

manager = get_spacing_manager()

# Create responsive grid
grid_frame = manager.create_layout_grid(parent, rows=2, cols=3, gap_size="medium")

# Add widgets to grid with consistent spacing
for i in range(2):
    for j in range(3):
        widget = tk.Button(grid_frame, text=f"Button {i},{j}")
        widget.grid(row=i, column=j, sticky="nsew")
```

## Best Practices

1. **Use predefined configurations** when possible for consistency
2. **Scale typography and spacing together** for proportional layouts
3. **Test on different platforms** to ensure proper font rendering
4. **Use semantic size names** (e.g., "title", "normal") rather than pixel values
5. **Apply spacing consistently** throughout your application
6. **Consider accessibility** when choosing typography and spacing configurations

## Migration from Legacy Themes

If you're migrating from the legacy theme system:

```python
# Old way (still works)
from threepanewindows.themes import Typography, Spacing

# New way (recommended)
from threepanewindows import Typography, Spacing, get_typography_manager, get_spacing_manager
```

The new modules are fully backward compatible with existing code while providing
enhanced functionality and better organization.
