# Focus Management Fix for Detached Windows

## Problem

When using the Image Studio with detached panes, clicking on a detached
window would not bring it to the front. The detached window would stay
behind the main window even when clicked, making it difficult to interact
with.

## Root Cause

The issue was in the `threepanewindows` library's `DetachedWindow` class in
`enhanced_dockable.py`. The `_start_drag` method only handled drag
functionality but did not include focus management when the window was
clicked.

## Solution

Since the `threepanewindows` library is installed in editable mode, we
fixed the issue directly in the library by:

### 1. Enhanced `_start_drag` Method

Modified the `_start_drag` method in `DetachedWindow` class to include
focus management:

```python
def _start_drag(self, event):
    """Start dragging the window and bring it to front."""
    # Bring window to front and give it focus when clicked
    self.lift()
    self.focus_set()

    # Store drag data for dragging functionality
    self._drag_data["x"] = event.x
    self._drag_data["y"] = event.y
```

### 2. Added Comprehensive Focus Management

Added a new `_setup_focus_management` method that:

- Binds click events to bring the window to front
- Recursively applies focus bindings to all child widgets
- Uses `lift()` and `focus_set()` to properly manage window focus
- Temporarily sets `-topmost` attribute to ensure the window comes to
  front

### 3. Integration with Window Setup

Modified the `_setup_ui` method to call the focus management setup during
window initialization.

## Files Modified

- `C:\Users\Admin\Desktop\test\ToolKit\ThreePaneWindows\threepanewindows\enhanced_dockable.py`

## Testing

To test the fix:

1. Run the Image Studio application
2. Detach the left or right panel
3. Click on the main window to bring it to front
4. Click anywhere on the detached panel
5. The detached panel should now come to front and stay there

## Benefits

- Improved user experience with detached windows
- Proper focus management across all UI elements
- Consistent behavior with standard window management expectations
- No changes needed in the main application code

## Technical Details

The fix uses standard Tkinter window management methods:

- `lift()`: Brings the window to the top of the stacking order
- `focus_set()`: Gives keyboard focus to the window
- `-topmost` attribute: Temporarily ensures the window appears above all
  others
- Recursive event binding: Ensures all child widgets can trigger focus
  management
