# Release v1.0.4: Center Panel Expansion Fix

## 🚀 What's New

### 🔧 Critical Bug Fix
- **Fixed center panel expansion**: When side panels are detached in `DockableThreePaneWindow`, the center panel now properly expands to fill the available space
- **Removed placeholder frames**: Eliminated empty placeholder frames that were preventing proper layout expansion
- **Improved space utilization**: No more empty gaps when panels are detached

### 🧪 Enhanced Testing
- **New test suite**: Added comprehensive tests for `DockableThreePaneWindow` functionality
- **Detach/reattach testing**: New test cases covering panel detachment and reattachment behavior
- **Layout validation**: Tests ensure center panel expansion works correctly

### 📚 Documentation Updates
- **API documentation**: Updated to highlight center panel expansion feature
- **README improvements**: Enhanced feature descriptions
- **Changelog**: Complete documentation of all changes

## 🐛 Bug Fixes

### DockableThreePaneWindow Layout Issue
**Problem**: When detaching left or right panels, placeholder frames with fixed widths were created, preventing the center panel from expanding to fill the available space.

**Solution**: Removed placeholder frame creation entirely, allowing the center panel to automatically expand when side panels are detached.

**Impact**:
- ✅ Center panel now fills entire available space when panels are detached
- ✅ No more empty gaps in the layout
- ✅ Better user experience with proper space utilization
- ✅ Consistent behavior across all panel configurations

## 🔄 Technical Changes

### Modified Files
- `threepanewindows/dockable.py`: Updated `_detach()` and `_reattach()` methods
- `tests/test_dockable.py`: New comprehensive test suite
- Documentation files: Updated API docs, README, and changelog
- Version files: Incremented to v1.0.4

### Backward Compatibility
- ✅ **Fully backward compatible**: All existing code continues to work
- ✅ **No API changes**: Same methods and parameters
- ✅ **Enhanced behavior**: Existing functionality now works better

## 📦 Installation

```bash
pip install threepanewindows==1.0.4
```sql

Or upgrade from previous version:
```bash
pip install --upgrade threepanewindows
```

## 🧪 Testing the Fix

To verify the fix works:

```python
import tkinter as tk
from threepanewindows import DockableThreePaneWindow

def build_panel(frame, text, color):
    tk.Label(frame, text=text, bg=color).pack(fill=tk.BOTH, expand=True)

root = tk.Tk()
root.title("Test Center Panel Expansion")
root.geometry("800x500")

window = DockableThreePaneWindow(
    root,
    side_width=150,
    left_builder=lambda f: build_panel(f, "Left Panel", "lightblue"),
    center_builder=lambda f: build_panel(f, "Center - Watch me expand!", "lightgreen"),
    right_builder=lambda f: build_panel(f, "Right Panel", "lightcoral"),
)
window.pack(fill=tk.BOTH, expand=True)

root.mainloop()
```

**Expected behavior**: Click "Detach Left" or "Detach Right" buttons and observe the center panel expanding to fill the space.

## 🙏 Acknowledgments

Thanks to all users who reported the layout issue and provided feedback on the expected behavior.

---

**Full Changelog**: https://github.com/stntg/ThreePaneWindows/blob/main/CHANGELOG.md
