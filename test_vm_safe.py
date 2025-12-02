#!/usr/bin/env python3
"""
VM-Safe Test Script

This script tests the VM-safe custom titlebar implementation to ensure
it works without causing segmentation faults in virtual machine environments.
"""

import os
import platform
import sys
import tkinter as tk
from tkinter import messagebox

# Add the project root to the path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


def detect_vm_environment():
    """Detect if running in a virtual machine."""
    try:
        vm_indicators = [
            "VirtualBox", "vboxguest", "vboxsf",
            "VMware", "vmware", "vmxnet",
            "QEMU", "qemu", "virtio",
            "Microsoft Corporation", "Hyper-V",
        ]
        
        # Check DMI information
        try:
            with open("/sys/class/dmi/id/sys_vendor", "r") as f:
                vendor = f.read().strip()
                if any(indicator in vendor for indicator in vm_indicators):
                    return True, vendor
        except:
            pass
            
        try:
            with open("/sys/class/dmi/id/product_name", "r") as f:
                product = f.read().strip()
                if any(indicator in product for indicator in vm_indicators):
                    return True, product
        except:
            pass
        
        return False, "Unknown"
        
    except Exception:
        return True, "Detection failed - assuming VM for safety"


def test_basic_window():
    """Test basic window creation without any custom titlebar."""
    print("🧪 Testing basic window creation...")
    
    root = tk.Tk()
    root.title("VM-Safe Test - Basic Window")
    root.geometry("400x300")
    
    label = tk.Label(
        root,
        text="Basic Window Test\n\nIf you can see this, basic Tkinter works!",
        font=("Arial", 12),
        pady=20
    )
    label.pack(expand=True)
    
    button = tk.Button(
        root,
        text="Close Test",
        command=root.destroy,
        font=("Arial", 10)
    )
    button.pack(pady=10)
    
    print("✓ Basic window created successfully")
    
    # Show for 3 seconds then close automatically
    root.after(3000, root.destroy)
    root.mainloop()
    
    print("✓ Basic window test completed")


def test_vm_safe_titlebar():
    """Test VM-safe custom titlebar."""
    print("🧪 Testing VM-safe custom titlebar...")
    
    try:
        from linux_vm_safe_demo import VMSafeCustomTitleBar
        
        root = tk.Tk()
        root.title("VM-Safe Test - Custom Titlebar")
        root.geometry("500x400")
        
        # Create theme dictionary
        theme_dict = {
            "bg": "#2b2b2b",
            "fg": "#ffffff",
            "btn_bg": "#404040",
            "btn_fg": "#ffffff",
            "btn_active_bg": "#505050",
            "font": ("Ubuntu", 11),
        }
        
        # Create VM-safe titlebar
        titlebar = VMSafeCustomTitleBar(root, theme_dict, "VM-Safe Titlebar Test")
        titlebar_frame = titlebar.create_titlebar()
        
        if titlebar_frame:
            print("✓ VM-safe titlebar created successfully")
            
            # Add content
            content_frame = tk.Frame(root, bg="#333333")
            content_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            label = tk.Label(
                content_frame,
                text="VM-Safe Custom Titlebar Test\n\n" +
                     "✓ No X11 Motif hints\n" +
                     "✓ No low-level X11 calls\n" +
                     "✓ Pure Tkinter implementation\n" +
                     "✓ Safe for virtual machines\n\n" +
                     "Try dragging the titlebar!",
                bg="#333333",
                fg="#ffffff",
                font=("Arial", 11),
                justify="center"
            )
            label.pack(expand=True)
            
            # Auto-close after 5 seconds
            root.after(5000, root.destroy)
            root.mainloop()
            
            print("✓ VM-safe titlebar test completed")
            return True
        else:
            print("⚠ VM-safe titlebar creation failed")
            return False
            
    except Exception as e:
        print(f"✗ VM-safe titlebar test failed: {e}")
        return False


def test_theme_switching():
    """Test theme switching functionality."""
    print("🧪 Testing theme switching...")
    
    try:
        from threepanewindows.central_theme_manager import get_theme_manager, set_global_theme
        
        theme_manager = get_theme_manager()
        available_themes = theme_manager.get_theme_names()
        
        print(f"✓ Found {len(available_themes)} themes: {', '.join(available_themes)}")
        
        # Test switching to a few themes
        test_themes = ["light", "dark", "blue"]
        for theme_name in test_themes:
            if theme_name in available_themes:
                set_global_theme(theme_name)
                current_theme = theme_manager.get_current_theme()
                print(f"✓ Successfully switched to {theme_name} theme")
            else:
                print(f"⚠ Theme {theme_name} not available")
        
        print("✓ Theme switching test completed")
        return True
        
    except Exception as e:
        print(f"✗ Theme switching test failed: {e}")
        return False


def main():
    """Run all VM-safe tests."""
    print("🖥️ VM-Safe Test Suite")
    print("=" * 50)
    
    # Platform detection
    current_os = platform.system()
    print(f"Platform: {current_os}")
    print(f"Python: {platform.python_version()}")
    
    # VM detection
    if current_os == "Linux":
        is_vm, vm_info = detect_vm_environment()
        print(f"Virtual Machine: {'Yes' if is_vm else 'No'} ({vm_info})")
    else:
        print("VM Detection: Skipped (not Linux)")
    
    print()
    
    # Run tests
    tests = [
        ("Basic Window", test_basic_window),
        ("VM-Safe Titlebar", test_vm_safe_titlebar),
        ("Theme Switching", test_theme_switching),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n--- {test_name} Test ---")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nPassed: {passed}/{len(results)} tests")
    
    if passed == len(results):
        print("\n🎉 All tests passed! VM-safe implementation is working correctly.")
        print("You can now safely run the VM-safe demo in your Pop!_OS virtual machine.")
    else:
        print(f"\n⚠️ {len(results) - passed} test(s) failed.")
        print("There may be issues with the VM-safe implementation.")
    
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())