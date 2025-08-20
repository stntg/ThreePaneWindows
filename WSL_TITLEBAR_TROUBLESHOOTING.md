# WSL Custom Titlebar Troubleshooting Guide

## Problem: Custom Titlebar Not Appearing on WSL

If you're running the Linux demo on WSL and the custom titlebar is not appearing, leaving you with an unmovable window, follow this troubleshooting guide.

## Quick Emergency Exit

If you're stuck with an unmovable window:

**Emergency Exit Keys:**
- `Ctrl+Q` - Quit application
- `Alt+F4` - Close window (Windows-style)
- `Escape` - Emergency exit

**Terminal Method:**
```bash
# Find and kill the process
ps aux | grep python
kill -9 <process_id>

# Or kill all Python processes (be careful!)
pkill -f python
```

## Diagnostic Steps

### Step 1: Test Basic X Server Connection

```bash
# Check if DISPLAY is set
echo $DISPLAY

# Test X server connection
xset q

# Test basic GUI
python3 -c "import tkinter as tk; root = tk.Tk(); root.title('Test'); tk.Label(root, text='X Server Works!').pack(); root.mainloop()"
```

### Step 2: Run Debug Scripts

```bash
# Test custom titlebar functionality
python3 debug_titlebar.py

# Test simple titlebar
python3 test_custom_titlebar.py

# Test WSL launcher with debug
python3 run_wsl_demo.py --test-titlebar
```

### Step 3: Check WSL Environment

```bash
# Verify WSL detection
python3 -c "
import os
print('WSL_DISTRO_NAME:', os.environ.get('WSL_DISTRO_NAME', 'Not set'))
if os.path.exists('/proc/version'):
    with open('/proc/version') as f:
        print('Kernel:', f.read().strip())
"

# Check for Windows interop
ls -la /mnt/c 2>/dev/null && echo 'Windows mount found' || echo 'Windows mount not found'
```

## Common Issues and Solutions

### Issue 1: X Server Not Running

**Symptoms:**
- `DISPLAY` variable not set
- `xset q` fails
- No GUI windows appear

**Solutions:**
```bash
# Install and start VcXsrv on Windows
# Download from: https://sourceforge.net/projects/vcxsrv/

# Set DISPLAY variable
export DISPLAY=:0

# Or for VcXsrv with different settings
export DISPLAY=localhost:0.0

# Add to ~/.bashrc for persistence
echo 'export DISPLAY=:0' >> ~/.bashrc
```

### Issue 2: Custom Titlebar Creation Fails

**Symptoms:**
- Window appears but no titlebar
- Window cannot be moved or closed
- Console shows titlebar creation errors

**Solutions:**
```bash
# Disable custom titlebar
export THREEPANE_CUSTOM_TITLEBAR=0
python3 examples/linux_comprehensive_demo.py

# Or use system titlebar mode
unset THREEPANE_CUSTOM_TITLEBAR
python3 examples/linux_comprehensive_demo.py
```

### Issue 3: Font Issues

**Symptoms:**
- Titlebar appears but text is missing
- Font-related errors in console

**Solutions:**
```bash
# Install common fonts
sudo apt-get update
sudo apt-get install fonts-dejavu-core fonts-liberation

# Or use basic fonts
export THREEPANE_USE_BASIC_FONTS=1
python3 examples/linux_comprehensive_demo.py
```

### Issue 4: Theme Manager Issues

**Symptoms:**
- Titlebar creation fails with theme errors
- Color-related exceptions

**Solutions:**
```bash
# Use safe theme mode
export THREEPANE_SAFE_THEME=1
python3 examples/linux_comprehensive_demo.py

# Or disable theming
export THREEPANE_NO_THEME=1
python3 examples/linux_comprehensive_demo.py
```

## Debug Mode

Enable detailed logging to see what's happening:

```bash
# Enable debug logging
export PYTHONPATH=.
python3 -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from examples.linux_comprehensive_demo import LinuxComprehensiveDemo
demo = LinuxComprehensiveDemo()
demo.run()
"
```

## Manual Testing

### Test 1: Basic Window
```bash
python3 -c "
import tkinter as tk
root = tk.Tk()
root.title('Basic Test')
root.geometry('300x200')
tk.Label(root, text='Basic window works!').pack(expand=True)
root.mainloop()
"
```

### Test 2: Frame Creation
```bash
python3 -c "
import tkinter as tk
root = tk.Tk()
root.title('Frame Test')
frame = tk.Frame(root, bg='blue', height=30)
frame.pack(fill='x')
frame.pack_propagate(False)
tk.Label(frame, text='Frame works!', bg='blue', fg='white').pack()
tk.Label(root, text='Click to close').pack(expand=True)
root.bind('<Button-1>', lambda e: root.quit())
root.mainloop()
"
```

### Test 3: Override Redirect
```bash
python3 -c "
import tkinter as tk
root = tk.Tk()
root.geometry('400x300')
frame = tk.Frame(root, bg='red', height=30)
frame.pack(fill='x')
tk.Label(frame, text='Before override', bg='red', fg='white').pack()
root.update_idletasks()
print('Frame height before:', frame.winfo_height())
root.overrideredirect(True)
root.update_idletasks()
print('Frame height after:', frame.winfo_height())
tk.Label(root, text='Override test - Ctrl+Q to quit').pack(expand=True)
root.bind('<Control-q>', lambda e: root.quit())
root.mainloop()
"
```

## X Server Configuration

### VcXsrv Settings (Recommended)

1. **Display number**: 0
2. **Start no client**: ✓ Checked
3. **Clipboard**: ✓ Primary selection
4. **Native opengl**: ✓ Checked
5. **Disable access control**: ✓ Checked

### Alternative X Servers

**Xming:**
```bash
export DISPLAY=:0
# Or
export DISPLAY=localhost:0.0
```

**X410:**
```bash
export DISPLAY=:0
# X410 usually works with default settings
```

## WSL-Specific Workarounds

### Workaround 1: Force System Titlebar
```bash
# Completely disable custom titlebar
export THREEPANE_CUSTOM_TITLEBAR=0
export THREEPANE_FORCE_SYSTEM_TITLEBAR=1
python3 examples/linux_comprehensive_demo.py
```

### Workaround 2: Minimal Custom Titlebar
```bash
# Use minimal titlebar implementation
export THREEPANE_MINIMAL_TITLEBAR=1
python3 examples/linux_comprehensive_demo.py
```

### Workaround 3: Safe Mode
```bash
# Run in safe mode with all custom features disabled
export THREEPANE_SAFE_MODE=1
python3 examples/linux_comprehensive_demo.py
```

## Creating Your Own Test

Create a minimal test file:

```python
#!/usr/bin/env python3
import tkinter as tk
import os

def test_custom_titlebar():
    root = tk.Tk()
    root.geometry("400x300+200+200")

    # Create titlebar BEFORE overrideredirect
    titlebar = tk.Frame(root, bg="#333", height=30)
    titlebar.pack(fill="x")
    titlebar.pack_propagate(False)

    tk.Label(titlebar, text="Test Titlebar", bg="#333", fg="white").pack(side="left", padx=10)
    tk.Button(titlebar, text="×", command=root.quit, bg="#333", fg="white").pack(side="right")

    tk.Label(root, text="Content Area\nCtrl+Q to quit").pack(expand=True)

    # Force update
    root.update_idletasks()
    print(f"Titlebar height: {titlebar.winfo_height()}")

    # Remove decorations
    root.overrideredirect(True)
    root.update_idletasks()
    print(f"Titlebar height after override: {titlebar.winfo_height()}")

    # Emergency exit
    root.bind('<Control-q>', lambda e: root.quit())

    root.mainloop()

if __name__ == "__main__":
    test_custom_titlebar()
```

## Getting Help

If none of these solutions work:

1. **Check the console output** for specific error messages
2. **Run the debug scripts** to isolate the issue
3. **Try different X server configurations**
4. **Use system titlebar mode** as a fallback
5. **Report the issue** with full debug output

## Environment Variables Reference

```bash
# Custom titlebar control
export THREEPANE_CUSTOM_TITLEBAR=1          # Enable custom titlebar
export THREEPANE_CUSTOM_TITLEBAR=0          # Disable custom titlebar

# Debug and safe modes
export THREEPANE_SAFE_MODE=1                # Enable safe mode
export THREEPANE_SAFE_THEME=1               # Use safe theme colors
export THREEPANE_NO_THEME=1                 # Disable theming
export THREEPANE_USE_BASIC_FONTS=1          # Use basic fonts only
export THREEPANE_MINIMAL_TITLEBAR=1         # Use minimal titlebar

# WSL specific
export THREEPANE_WSL_MODE=1                 # Force WSL mode
export THREEPANE_FORCE_SYSTEM_TITLEBAR=1    # Force system titlebar

# X Server
export DISPLAY=:0                           # Set display
export LIBGL_ALWAYS_INDIRECT=1              # OpenGL compatibility
```

## Success Indicators

When custom titlebar works correctly, you should see:

1. ✅ **Custom titlebar appears** at the top of the window
2. ✅ **Window can be dragged** by clicking and dragging the titlebar
3. ✅ **Minimize button works** (− button)
4. ✅ **Close button works** (× button)
5. ✅ **Theme changes** update the titlebar colors
6. ✅ **No console errors** related to titlebar creation

If any of these fail, use the troubleshooting steps above to identify and fix the issue.
