# Smart Layout System (v1.2.0)

This document explains the new Smart Layout System introduced in
ThreePaneWindows v1.2.0, which automatically optimizes sash behavior based
on pane configuration.

## Requirements

- **Python**: 3.9 to 3.13
- **ThreePaneWindows**: v1.2.0 or later

## Overview

The Smart Layout System automatically detects the optimal layout approach
based on your pane configuration:

- **Custom Layout**: Used for windows with fixed panes (no interactive
  sash handles)
- **TTK PanedWindow**: Used for fully resizable windows (standard sash
  handles)

This ensures that fixed panes truly behave as fixed, while resizable
panes maintain full TTK PanedWindow functionality.

## How It Works

### Automatic Detection

The system analyzes your pane configuration during window initialization:

```python
# This triggers Custom Layout (fixed panes)
left_config = PaneConfig(fixed_width=200)

# This triggers Custom Layout (non-resizable panes)
right_config = PaneConfig(resizable=False, default_width=150)

# This uses TTK PanedWindow (all resizable)
left_config = PaneConfig(resizable=True)
center_config = PaneConfig(resizable=True)
right_config = PaneConfig(resizable=True)
```

### Custom Layout (Fixed Panes)

**When Used:**

- Any pane has `fixed_width` set
- Any pane has `resizable=False`

**Features:**

- Visual sash separators without interactive resize handles
- Fixed panes maintain their specified widths
- Center pane automatically expands to fill remaining space
- Proper handling when panes are detached (center expands)
- No resize cursors or drag functionality on sashes

**Example:**

```python
from threepanewindows.enhanced_dockable import (
    EnhancedDockableThreePaneWindow, PaneConfig
)

# Fixed width left pane - triggers custom layout
left_config = PaneConfig(
    title="Fixed Left",
    fixed_width=200,  # This triggers custom layout
    resizable=False
)

center_config = PaneConfig(
    title="Expandable Center",
    resizable=True  # Will expand to fill remaining space
)

right_config = PaneConfig(
    title="Fixed Right",
    resizable=False,  # This also triggers custom layout
    default_width=150  # Used as fixed width
)

window = EnhancedDockableThreePaneWindow(
    master=root,
    left_config=left_config,
    center_config=center_config,
    right_config=right_config
)
```

### TTK PanedWindow Layout (Resizable Panes)

**When Used:**

- All panes have `resizable=True`
- No panes have `fixed_width` set

**Features:**

- Standard TTK PanedWindow with interactive sash handles
- All panes can be resized by dragging sash handles
- Standard TTK behavior for detaching/reattaching
- Resize cursors appear when hovering over sashes

**Example:**

```python
# All resizable - uses TTK PanedWindow
left_config = PaneConfig(
    title="Resizable Left",
    resizable=True,
    default_width=200
)

center_config = PaneConfig(
    title="Resizable Center",
    resizable=True
)

right_config = PaneConfig(
    title="Resizable Right",
    resizable=True,
    default_width=150
)

window = EnhancedDockableThreePaneWindow(
    master=root,
    left_config=left_config,
    center_config=center_config,
    right_config=right_config
)
```

## Configuration Options

### PaneConfig Parameters

The following parameters affect layout detection:

```python
@dataclass
class PaneConfig:
    fixed_width: Optional[int] = None  # Forces custom layout if set
    resizable: bool = True             # Forces custom layout if False
    default_width: int = 200           # Used as fixed width when
                                       # resizable=False
    min_width: int = 100               # Minimum width constraint
    max_width: int = 0                 # Maximum width constraint
                                       # (0 = no limit)
```

### Layout Decision Matrix

| Left Pane | Center Pane | Right Pane | Layout Used |
|-----------|-------------|------------|-------------|
| `fixed_width=200` | `resizable=True` | `resizable=True` | Custom Layout |
| `resizable=False` | `resizable=True` | `resizable=True` | Custom Layout |
| `resizable=True` | `resizable=True` | `fixed_width=150` | Custom Layout |
| `resizable=True` | `resizable=True` | `resizable=True` | TTK PanedWindow |

## Detach/Reattach Behavior

### Custom Layout

- When panes are detached, center pane expands to fill the space
- Reattaching restores panes to their original fixed positions
- Fixed panes maintain their widths throughout the process

### TTK PanedWindow

- Standard TTK PanedWindow detach/reattach behavior
- Sash positions are preserved and restored
- All panes can be resized after reattaching

## Migration from v1.1.x

### No Breaking Changes

Existing code continues to work without modifications. The system
automatically detects the appropriate layout.

### Behavior Changes

- **Fixed panes now truly fixed**: Panes with `fixed_width` or
  `resizable=False` no longer show interactive sash handles
- **Better visual feedback**: Clear distinction between fixed and
  resizable layouts
- **Improved detach behavior**: Center pane properly expands when other
  panes are detached

### Recommended Updates

While not required, you may want to review your configurations:

```python
# Old approach (still works)
config = PaneConfig(default_width=200)

# New explicit approach (recommended)
config = PaneConfig(
    fixed_width=200,    # For truly fixed panes
    resizable=False     # Alternative for fixed panes
)
# OR
config = PaneConfig(
    resizable=True,     # For resizable panes
    default_width=200   # Initial width, but resizable
)
```

## Troubleshooting

### Issue: Panes are not resizable when expected

**Solution**: Ensure all panes have `resizable=True` and no `fixed_width`
set.

### Issue: Fixed panes still show sash handles

**Solution**: Verify that at least one pane has `fixed_width` set or
`resizable=False`.

### Issue: Center pane doesn't expand when panes are detached

**Solution**: This is expected behavior in TTK PanedWindow mode. Use custom
layout for automatic expansion.

## Performance Considerations

- **Custom Layout**: Slightly more overhead for layout calculations, but
  negligible in practice
- **TTK PanedWindow**: Standard TTK performance characteristics
- **Detection**: Layout detection happens once during initialization

## Examples

See the following files for complete examples:

- `examples/smart_layout_demo.py` - Demonstrates both layout types
- `test_comprehensive_behavior.py` - Test cases for both layouts
- `test_sash_fixed.py` - Verification of sash behavior

## API Reference

### Internal Methods (Advanced Users)

The following methods are used internally but may be useful for advanced
customization:

```python
# Check if custom layout is being used
window._has_fixed_panes  # Boolean indicating layout type

# Layout creation methods
window._create_custom_layout()     # Creates custom layout
window._create_visual_sashes()     # Creates visual sash separators
window._handle_custom_resize()     # Handles window resize events
```

**Note**: These are internal methods and may change in future versions.
Use at your own risk.
