#!/usr/bin/env python3
"""
Linux Comprehensive Demo for ThreePaneWindows

This demo is specifically designed for Linux systems and showcases:
- Flexible layout system with complex nested layouts
- Central theming with Linux-native color schemes
- Typography system with Linux-optimized fonts (Ubuntu, DejaVu Sans)
- Spacing system with Linux-appropriate dimensions
- Linux-compatible icons (.png, .xbm format)
- Desktop environment detection and adaptation
- Dark mode detection and automatic theme switching
- Professional UI components optimized for Linux

Features demonstrated:
1. Flexible layout with multiple containers and orientations
2. Linux-native theming with GNOME/KDE color schemes
3. Typography with Ubuntu/DejaVu Sans font families
4. Proper spacing for Linux desktop environments
5. PNG icons optimized for Linux display
6. Desktop environment-specific adaptations
7. Automatic dark mode detection
8. Professional Linux application styling
"""

import os
import platform
import sys
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Dict, List, Optional

# Add the project root to the path so we can import the modules
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    # Import from threepanewindows package
    from threepanewindows.central_theme_manager import (
        ThemeType,
        get_theme_manager,
        set_global_theme,
    )
    from threepanewindows.custom_menubar import CustomMenubar, MenuItem
    from threepanewindows.flexible import (
        EnhancedFlexibleLayout,
        FlexContainer,
        FlexPaneConfig,
        LayoutDirection,
    )
    from threepanewindows.logging_config import get_logger
    from threepanewindows.spacing import COMPACT_SPACING, get_spacing_manager
    from threepanewindows.typography import Typography, get_typography_manager
    from threepanewindows.utils import platform_handler
    from threepanewindows.utils.linux import LinuxPlatformHandler

except ImportError as e:
    print(f"Error importing threepanewindows modules: {e}")
    print("Make sure you're running this from the project root directory")
    sys.exit(1)

# Initialize logger
logger = get_logger(__name__)


class LinuxComprehensiveDemo:
    """
    Comprehensive Linux demo showcasing all ThreePaneWindows features
    optimized for Linux desktop environments.
    """

    def __init__(self):
        """Initialize the Linux demo application."""
        self.root = tk.Tk()
        self.root.title("ThreePaneWindows - Linux Comprehensive Demo")
        self.root.geometry("1200x800")

        # CRITICAL: Hide window initially to prevent dual-window issue on WSL
        # We'll show it after custom titlebar is properly set up
        self.root.withdraw()
        print("[DEBUG] Window withdrawn initially to prevent dual-window issue")

        # Initialize Linux platform handler
        self.linux_handler = LinuxPlatformHandler()

        # Detect desktop environment and dark mode
        self.desktop_env = self.linux_handler.get_desktop_environment()
        self.is_dark_mode = self.linux_handler.is_dark_mode()

        # Initialize managers
        self.theme_manager = get_theme_manager()
        self.typography_manager = get_typography_manager()
        self.spacing_manager = get_spacing_manager()

        # Setup Linux-optimized typography
        self._setup_linux_typography()

        # Setup Linux-optimized spacing
        self._setup_linux_spacing()

        # Set initial theme based on system dark mode
        initial_theme = ThemeType.DARK if self.is_dark_mode else ThemeType.LIGHT
        set_global_theme(initial_theme)

        # Get icon paths
        self.icon_paths = self._get_linux_icon_paths()

        # IMPORTANT: Setup custom titlebar BEFORE creating layout and showing window
        # This prevents the dual-window issue on WSL X servers
        self._setup_custom_titlebar()

        # Setup the flexible layout
        self._setup_flexible_layout()

        # Setup window icon
        self._setup_window_icon()

        # Setup window properties for Linux
        self._setup_linux_window_properties()

        logger.info(
            f"Linux demo initialized for {self.desktop_env} desktop environment"
        )

    def _setup_linux_typography(self):
        """Setup Linux-optimized typography with Ubuntu/DejaVu Sans fonts."""
        # Create Linux-optimized typography
        linux_typography = Typography(
            font_family="Ubuntu",
            font_family_fallback="DejaVu Sans",
            font_family_monospace="Ubuntu Mono",
            font_family_monospace_fallback="DejaVu Sans Mono",
            # Slightly larger fonts for better Linux readability
            font_size_tiny=9,
            font_size_small=10,
            font_size_normal=11,
            font_size_medium=12,
            font_size_large=13,
            font_size_title=15,
            font_size_heading=17,
            font_size_display=21,
        )

        # Apply Linux-specific adjustments
        linux_typography._apply_platform_adjustments()

        # Update the global typography manager
        self.typography_manager.typography = linux_typography
        logger.info("Applied Linux-optimized typography")

    def _setup_linux_spacing(self):
        """Setup Linux-optimized spacing."""
        # Linux typically uses slightly more compact spacing
        self.spacing_manager.spacing._scale_spacing(0.9)
        logger.info("Applied Linux-optimized spacing")

    def _get_linux_icon_paths(self) -> Dict[str, str]:
        """Get paths to Linux-compatible PNG icons."""
        icon_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "threepanewindows",
            "utils",
            "icons",
        )

        # Select PNG icons that work well on Linux
        icons = {
            "folder": os.path.join(icon_dir, "folder-1449.png"),
            "database": os.path.join(icon_dir, "database-db-icon.png"),
            "chart": os.path.join(icon_dir, "column-chart-icon.png"),
            "settings": os.path.join(icon_dir, "setting-line-icon.png"),
            "edit": os.path.join(icon_dir, "edit-pen-icon.png"),
            "info": os.path.join(icon_dir, "info-circle-line-icon.png"),
            "search": os.path.join(icon_dir, "search-icon.png"),
            "save": os.path.join(icon_dir, "save-icon.png"),
            "copy": os.path.join(icon_dir, "copy-icon.png"),
            "paint": os.path.join(icon_dir, "paint-palette-icon.png"),
            "image": os.path.join(icon_dir, "pictures-icon.png"),
            "control": os.path.join(icon_dir, "control-panel-icon.png"),
        }

        # Verify icons exist and are PNG format
        verified_icons = {}
        for name, path in icons.items():
            if os.path.exists(path) and path.lower().endswith(".png"):
                verified_icons[name] = path
                logger.debug(f"Verified Linux icon: {name} -> {path}")
            else:
                logger.warning(f"Linux icon not found or not PNG: {name} -> {path}")

        return verified_icons

    def _setup_window_icon(self):
        """Setup window icon using Linux-compatible method."""
        if "folder" in self.icon_paths:
            success = self.linux_handler.set_window_icon(
                self.root, self.icon_paths["folder"]
            )
            if success:
                logger.info("Set window icon successfully")
            else:
                logger.warning("Failed to set window icon")

    def _setup_linux_window_properties(self):
        """Setup Linux-specific window properties."""
        try:
            # Set window class for better integration with Linux window managers
            self.root.wm_class("ThreePaneWindows", "ThreePaneWindows")

            # Set window manager hints
            self.root.wm_attributes("-type", "normal")

            # Apply Linux titlebar customization
            theme = self.theme_manager.get_current_theme()
            self.linux_handler.apply_custom_titlebar(self.root, theme)

            # For Ubuntu/GNOME, try additional integration
            if self.desktop_env == "ubuntu" or self.desktop_env == "gnome":
                self._setup_ubuntu_integration(theme)
            elif self.desktop_env == "wsl":
                self._setup_wsl_integration(theme)

            logger.info(f"Applied Linux window properties for {self.desktop_env}")

        except Exception as e:
            logger.warning(f"Could not apply all Linux window properties: {e}")

    def _setup_ubuntu_integration(self, theme):
        """Setup Ubuntu/GNOME specific integration."""
        try:
            # Set window background to match theme immediately
            self.root.configure(bg=theme.primary_bg)

            # Try to set window properties that Ubuntu's window manager respects
            try:
                # Set window role for better GNOME integration
                self.root.wm_command("threepane-linux-demo")

                # Set window title with theme indicator
                theme_name = self.theme_manager.current_theme.value.title()
                self.root.title(f"ThreePaneWindows Linux Demo - {theme_name} Theme")

                # Try to influence window decorations through properties
                if hasattr(self.root, "tk"):
                    try:
                        # Set window properties that might influence decoration
                        self.root.tk.call(
                            "wm", "attributes", self.root, "-type", "normal"
                        )
                    except tk.TclError:
                        pass

            except (tk.TclError, AttributeError) as e:
                logger.debug(f"Ubuntu integration property setting failed: {e}")

            # Schedule a delayed theme refresh to ensure proper application
            self.root.after(100, lambda: self._refresh_ubuntu_theming(theme))

        except Exception as e:
            logger.debug(f"Ubuntu integration setup failed: {e}")

    def _refresh_ubuntu_theming(self, theme):
        """Refresh Ubuntu-specific theming."""
        try:
            # Ensure window background matches theme
            self.root.configure(bg=theme.primary_bg)

            # Update window title to reflect current theme
            theme_name = self.theme_manager.current_theme.value.title()
            self.root.title(f"ThreePaneWindows Linux Demo - {theme_name} Theme")

            # Force a window update
            self.root.update_idletasks()

        except Exception as e:
            logger.debug(f"Ubuntu theming refresh failed: {e}")

    def _setup_wsl_integration(self, theme):
        """Setup WSL-specific integration."""
        try:
            # Set window background to match theme immediately
            self.root.configure(bg=theme.primary_bg)

            # WSL-specific window properties
            try:
                # Set window role for better X server integration
                self.root.wm_command("threepane-wsl-demo")

                # Set window title with WSL indicator
                theme_name = self.theme_manager.current_theme.value.title()
                self.root.title(f"ThreePaneWindows WSL Demo - {theme_name} Theme")

                # WSL X servers often work better with explicit geometry
                self.root.geometry("1000x700+100+100")

                # Set window properties that work well with WSL X servers
                self.root.wm_attributes("-type", "normal")
                self.root.wm_resizable(True, True)

                # Enable better window manager integration
                self.root.wm_protocol("WM_DELETE_WINDOW", self.root.quit)

            except (tk.TclError, AttributeError) as e:
                logger.debug(f"WSL integration property setting failed: {e}")

            # Schedule a delayed theme refresh for WSL
            self.root.after(200, lambda: self._refresh_wsl_theming(theme))

        except Exception as e:
            logger.debug(f"WSL integration setup failed: {e}")

    def _refresh_wsl_theming(self, theme):
        """Refresh WSL-specific theming."""
        try:
            # Ensure window background matches theme
            self.root.configure(bg=theme.primary_bg)

            # Update window title to reflect current theme
            theme_name = self.theme_manager.current_theme.value.title()
            self.root.title(f"ThreePaneWindows WSL Demo - {theme_name} Theme")

            # Force a window update for WSL X servers
            self.root.update_idletasks()
            self.root.update()

        except Exception as e:
            logger.debug(f"WSL theming refresh failed: {e}")

    def _setup_custom_titlebar(self):
        """Setup custom titlebar for better theme control on Linux."""
        print("\n" + "=" * 60)
        print("CUSTOM TITLEBAR SETUP - DEBUG OUTPUT")
        print("=" * 60)

        try:
            # Debug environment variables
            env_var = os.environ.get("THREEPANE_CUSTOM_TITLEBAR", "")
            print(f"[DEBUG] THREEPANE_CUSTOM_TITLEBAR = '{env_var}'")
            print(f"[DEBUG] Desktop environment = '{self.desktop_env}'")

            # Check if we should use custom titlebar
            use_custom = os.environ.get("THREEPANE_CUSTOM_TITLEBAR", "").lower() in (
                "1",
                "true",
                "yes",
            )
            print(f"[DEBUG] Initial use_custom decision = {use_custom}")

            # On WSL, enable custom titlebar by default for better theming
            # But only if not explicitly disabled and if basic GUI works
            if self.desktop_env == "wsl" and not use_custom:
                print(
                    "[DEBUG] WSL detected and use_custom is False, checking auto-enable..."
                )
                # Check if user explicitly disabled it
                env_check = os.environ.get(
                    "THREEPANE_CUSTOM_TITLEBAR", ""
                ).lower() not in ("0", "false", "no")
                print(
                    f"[DEBUG] Environment variable not explicitly disabled = {env_check}"
                )

                if env_check:
                    print("[DEBUG] Testing basic GUI functionality...")
                    gui_test_result = self._test_gui_functionality()
                    print(f"[DEBUG] GUI functionality test result = {gui_test_result}")

                    if gui_test_result:
                        use_custom = True
                        print("[DEBUG] ✓ Enabling custom titlebar by default for WSL")
                        logger.info("Enabling custom titlebar by default for WSL")
                    else:
                        print(
                            "[DEBUG] ✗ Basic GUI test failed - disabling custom titlebar"
                        )
                        logger.warning(
                            "Basic GUI test failed - disabling custom titlebar"
                        )
                        use_custom = False
                else:
                    print(
                        "[DEBUG] Custom titlebar explicitly disabled by environment variable"
                    )

            print(f"[DEBUG] Final use_custom decision = {use_custom}")

            if not use_custom:
                print("[DEBUG] ✗ Custom titlebar disabled")
                logger.debug(
                    "Custom titlebar disabled (set THREEPANE_CUSTOM_TITLEBAR=1 to enable)"
                )

                # Show window normally since no custom titlebar
                print("[DEBUG] Showing window with system titlebar...")
                self.root.deiconify()
                print("[DEBUG] ✓ Window displayed with system titlebar")
                print("=" * 60)
                return

            print("[DEBUG] ✓ Proceeding with custom titlebar creation...")

            # CRITICAL: Apply overrideredirect FIRST, before creating any content
            # This prevents the dual-window issue on WSL X servers
            print("[DEBUG] Applying overrideredirect BEFORE creating titlebar...")

            # Check if we should try alternative approach for problematic WSL X servers
            wsl_alternative = os.environ.get(
                "THREEPANE_WSL_ALTERNATIVE", ""
            ).lower() in ("1", "true", "yes")

            if wsl_alternative and self.desktop_env == "wsl":
                print("[DEBUG] Using WSL alternative approach (no overrideredirect)")
                print(
                    "[DEBUG] This will keep system titlebar but add custom titlebar below it"
                )
                # Don't apply overrideredirect - let system titlebar remain
                self.use_system_titlebar = True
            else:
                try:
                    # Check current window state
                    current_override = self.root.overrideredirect()
                    print(f"[DEBUG] Current overrideredirect state: {current_override}")

                    if not current_override:
                        print("[DEBUG] Applying overrideredirect(True) early...")
                        self.root.overrideredirect(True)
                        self.root.update_idletasks()

                        # Verify it was applied
                        new_override = self.root.overrideredirect()
                        print(f"[DEBUG] New overrideredirect state: {new_override}")

                        if new_override:
                            print("[DEBUG] ✓ Early overrideredirect successful")
                            self.use_system_titlebar = False
                        else:
                            print("[DEBUG] ⚠ Early overrideredirect may have failed")
                            self.use_system_titlebar = True
                    else:
                        print("[DEBUG] Window already has overrideredirect=True")
                        self.use_system_titlebar = False

                except Exception as e:
                    print(f"[DEBUG] ✗ Early overrideredirect failed: {e}")
                    print("[DEBUG] Falling back to system titlebar approach")
                    self.use_system_titlebar = True

            # Now create the custom titlebar
            print("[DEBUG] Creating custom titlebar...")
            logger.info("Creating custom titlebar...")

            try:
                # Test basic tkinter functionality first
                print("[DEBUG] Testing basic tkinter frame creation...")
                test_frame = tk.Frame(self.root, bg="red", height=5)
                test_frame.pack(fill="x")
                test_frame.destroy()
                print("[DEBUG] ✓ Basic tkinter frame test passed")
                logger.info("Basic tkinter frame test passed")

                # Create custom titlebar frame
                print("[DEBUG] Calling _create_custom_titlebar()...")
                self.custom_titlebar = self._create_custom_titlebar()
                print("[DEBUG] ✓ Custom titlebar created successfully")
                logger.info("Custom titlebar created successfully")

                # Force update to ensure titlebar is rendered
                print("[DEBUG] Forcing GUI updates...")
                self.root.update_idletasks()
                self.root.update()

                # Verify titlebar exists and is visible
                print("[DEBUG] Verifying titlebar exists...")
                if not self.custom_titlebar.winfo_exists():
                    print("[DEBUG] ✗ Custom titlebar widget does not exist!")
                    raise Exception(
                        "Custom titlebar widget does not exist after creation"
                    )

                titlebar_height = self.custom_titlebar.winfo_height()
                print(f"[DEBUG] Titlebar height = {titlebar_height}")
                logger.info(f"Custom titlebar verified: height={titlebar_height}")

                # More lenient validation for WSL
                if self.desktop_env == "wsl":
                    print("[DEBUG] Using WSL-specific height validation...")
                    if titlebar_height <= 0:
                        print(
                            f"[DEBUG] ✗ Invalid height: {titlebar_height} (0 or negative)"
                        )
                        raise Exception(
                            "Custom titlebar has invalid height (0 or negative)"
                        )
                    elif titlebar_height == 1:
                        print(
                            "[DEBUG] ⚠ Height is 1 - common on WSL, continuing anyway"
                        )
                        logger.warning(
                            "Titlebar height is 1 - common on WSL, but should still work"
                        )
                    else:
                        print(f"[DEBUG] ✓ Height validation passed: {titlebar_height}")
                else:
                    print("[DEBUG] Using standard height validation...")
                    if titlebar_height <= 1:
                        print(f"[DEBUG] ✗ Invalid height: {titlebar_height}")
                        raise Exception("Custom titlebar has invalid height")
                    else:
                        print(f"[DEBUG] ✓ Height validation passed: {titlebar_height}")

                # Verify window decorations are removed (should already be done)
                print("[DEBUG] Verifying window decorations are removed...")
                logger.info("Verifying window decorations are removed...")

                current_override = self.root.overrideredirect()
                print(f"[DEBUG] Current overrideredirect state: {current_override}")

                if not current_override:
                    print("[DEBUG] ⚠ Overrideredirect not active, applying now...")
                    # WSL-specific overrideredirect handling as fallback
                    if self.desktop_env == "wsl":
                        print(
                            "[DEBUG] Applying WSL-specific overrideredirect sequence..."
                        )
                        logger.info(
                            "Applying WSL-specific overrideredirect sequence..."
                        )

                        # Method 1: Try standard overrideredirect
                        print("[DEBUG] Step 1: Applying overrideredirect(True)...")
                        self.root.overrideredirect(True)
                        self.root.update_idletasks()
                        self.root.update()

                        # Check if decorations were removed
                        print("[DEBUG] Step 2: Waiting for X server to process...")
                        import time

                        time.sleep(0.1)  # Give X server time to process

                        # WSL X servers sometimes need explicit geometry after overrideredirect
                        self.root.geometry("1000x700+100+100")
                        self.root.update_idletasks()
                        self.root.update()

                    else:
                        # Standard Linux overrideredirect
                        self.root.overrideredirect(True)
                        self.root.update_idletasks()
                        self.root.update()
                else:
                    print("[DEBUG] ✓ Overrideredirect already active")

                # Make window draggable
                self._make_window_draggable()

                # WSL-specific post-setup
                if self.desktop_env == "wsl":
                    self._setup_wsl_custom_titlebar()

                # Add emergency exit keybinding
                self._setup_emergency_exit()

                # Final verification
                if not self.custom_titlebar.winfo_exists():
                    raise Exception(
                        "Custom titlebar was destroyed after overrideredirect"
                    )

                # Check if overrideredirect actually worked
                try:
                    override_status = self.root.overrideredirect()
                    logger.info(f"Override redirect status: {override_status}")

                    if not override_status:
                        logger.warning(
                            "Override redirect appears to have failed - system decorations may still be visible"
                        )
                        logger.info("This is a known issue with some WSL X servers")
                        logger.info(
                            "The custom titlebar will still work, but system decorations may also be visible"
                        )
                    else:
                        logger.info(
                            "Override redirect successful - system decorations should be hidden"
                        )

                except Exception as e:
                    logger.debug(f"Could not check override redirect status: {e}")

                logger.info(f"Custom titlebar enabled for {self.desktop_env}")

                # Show success message with override redirect status
                def show_status_message():
                    try:
                        override_status = self.root.overrideredirect()
                        if override_status:
                            logger.info(
                                "Custom titlebar is active - try dragging the window"
                            )
                        else:
                            logger.info(
                                "Custom titlebar is active but system decorations may also be visible"
                            )
                            logger.info("This is a known WSL X server limitation")
                    except:
                        logger.info(
                            "Custom titlebar is active - try dragging the window"
                        )

                self.root.after(1000, show_status_message)

                print("\n[DEBUG] ✓ CUSTOM TITLEBAR SETUP COMPLETED SUCCESSFULLY!")

                # Check if we have the dual window issue
                print("[DEBUG] Checking for dual window issue...")

                # Force updates before showing
                self.root.update_idletasks()
                self.root.update()

                # Check window geometry and properties
                try:
                    geometry = self.root.geometry()
                    override_status = self.root.overrideredirect()
                    print(f"[DEBUG] Window geometry: {geometry}")
                    print(f"[DEBUG] Override redirect status: {override_status}")

                    # Check if there are multiple windows
                    all_windows = self.root.tk.call("wm", "stackorder", self.root)
                    print(f"[DEBUG] Window stack order: {all_windows}")

                except Exception as e:
                    print(f"[DEBUG] Could not check window properties: {e}")

                # Now show the window with custom titlebar
                print("[DEBUG] Showing window with custom titlebar...")

                # Force window to a visible position
                print("[DEBUG] Setting window position to ensure visibility...")
                self.root.geometry("1200x800+100+100")  # Explicit position
                self.root.update_idletasks()

                # Show the window
                self.root.deiconify()
                self.root.update_idletasks()
                self.root.update()

                # Force window to front
                print("[DEBUG] Bringing window to front...")
                self.root.lift()
                self.root.attributes("-topmost", True)  # Temporarily on top
                self.root.update()
                self.root.attributes("-topmost", False)  # Remove topmost
                self.root.focus_force()

                # Additional visibility checks
                print("[DEBUG] Checking window visibility...")
                try:
                    is_visible = self.root.winfo_viewable()
                    is_mapped = self.root.winfo_ismapped()
                    print(f"[DEBUG] Window viewable: {is_visible}")
                    print(f"[DEBUG] Window mapped: {is_mapped}")

                    if not is_visible or not is_mapped:
                        print(
                            "[DEBUG] ⚠ Window may not be visible, trying additional methods..."
                        )
                        # Try alternative show methods
                        self.root.wm_deiconify()
                        self.root.tkraise()
                        self.root.update()

                except Exception as e:
                    print(f"[DEBUG] Visibility check failed: {e}")

                # Additional check after showing
                self.root.after(500, self._check_window_state)

                print("[DEBUG] ✓ Window display sequence completed")

                print("=" * 60)

            except Exception as titlebar_error:
                print(f"\n[DEBUG] ✗ CUSTOM TITLEBAR SETUP FAILED: {titlebar_error}")
                print("[DEBUG] Full error details:")
                import traceback

                traceback.print_exc()

                logger.error(f"Failed to create custom titlebar: {titlebar_error}")
                logger.error(f"Full traceback: {traceback.format_exc()}")

                # Capture error message for lambda closure
                error_message = str(titlebar_error)
                print(f"[DEBUG] Error message captured: {error_message}")

                # If titlebar creation failed, restore window decorations
                try:
                    self.root.overrideredirect(False)
                    logger.info("Restored window decorations")
                except Exception as restore_error:
                    logger.error(f"Failed to restore decorations: {restore_error}")

                # Clean up failed titlebar
                if hasattr(self, "custom_titlebar"):
                    try:
                        self.custom_titlebar.destroy()
                    except:
                        pass
                    delattr(self, "custom_titlebar")

                # Show error message to user
                try:
                    import tkinter.messagebox as messagebox

                    self.root.after(
                        100,
                        lambda: messagebox.showerror(
                            "Custom Titlebar Error",
                            f"Failed to create custom titlebar: {error_message}\n\n"
                            "Using system titlebar instead.\n"
                            "Check console for detailed error information.",
                        ),
                    )
                except Exception as msg_error:
                    logger.error(f"Could not show error message: {msg_error}")

                print("[DEBUG] Falling back to system titlebar")
                logger.info("Falling back to system titlebar")

                # Show window with system titlebar since custom failed
                print("[DEBUG] Showing window with system titlebar (fallback)...")
                self.root.deiconify()
                print("[DEBUG] ✓ Window displayed with system titlebar")
                print("=" * 60)
                return

        except Exception as e:
            print(f"\n[DEBUG] ✗ OUTER EXCEPTION in _setup_custom_titlebar: {e}")
            logger.warning(f"Could not setup custom titlebar: {e}")
            # Ensure we don't leave the window in a bad state
            try:
                self.root.overrideredirect(False)
                print("[DEBUG] Restored overrideredirect(False)")
            except:
                print("[DEBUG] Failed to restore overrideredirect(False)")
                pass

            # Show window with system titlebar since custom failed
            print("[DEBUG] Showing window with system titlebar (outer exception)...")
            self.root.deiconify()
            print("[DEBUG] ✓ Window displayed with system titlebar")
            print("=" * 60)

    def _create_custom_titlebar(self):
        """Create a custom titlebar with theme support."""
        print("\n[DEBUG] === _create_custom_titlebar() START ===")
        try:
            print("[DEBUG] Getting theme for titlebar...")
            logger.info("Getting theme for titlebar...")
            theme = self.theme_manager.get_current_theme()
            print(
                f"[DEBUG] Theme colors: bg={theme.panel_header_bg}, fg={theme.panel_header_text}"
            )
            logger.info(
                f"Theme colors: bg={theme.panel_header_bg}, fg={theme.panel_header_text}"
            )

            # Create titlebar frame
            print("[DEBUG] Creating titlebar frame...")
            logger.info("Creating titlebar frame...")

            # Set root window background to match theme to avoid white bars
            self.root.configure(bg=theme.panel_header_bg)
            print(f"[DEBUG] Set root window background to {theme.panel_header_bg}")

            titlebar = tk.Frame(
                self.root, bg=theme.panel_header_bg, height=32, relief="flat", bd=0
            )
            print("[DEBUG] Packing titlebar frame...")
            logger.info("Packing titlebar frame...")
            titlebar.pack(fill="x", side="top")
            titlebar.pack_propagate(False)

            # WSL-specific: Force geometry and multiple updates
            if hasattr(self, "desktop_env") and self.desktop_env == "wsl":
                print("[DEBUG] WSL detected - applying special frame rendering...")
                # Force the frame to have minimum dimensions
                titlebar.configure(height=32)
                titlebar.update_idletasks()

                # Try to force the frame to actually render
                self.root.geometry()  # This can trigger a layout recalculation
                self.root.update_idletasks()
                self.root.update()

                # Additional WSL-specific rendering attempts
                titlebar.configure(height=32)  # Set height again
                titlebar.update()
                self.root.update()

            # Force update to ensure frame is created
            print("[DEBUG] Forcing update after frame creation...")
            self.root.update_idletasks()
            self.root.update()

            frame_width = titlebar.winfo_width()
            frame_height = titlebar.winfo_height()
            print(
                f"[DEBUG] Titlebar frame dimensions after updates: {frame_width}x{frame_height}"
            )
            logger.info(f"Titlebar frame created: {frame_width}x{frame_height}")

            # If height is still 1, try alternative approaches
            if (
                frame_height <= 1
                and hasattr(self, "desktop_env")
                and self.desktop_env == "wsl"
            ):
                print("[DEBUG] Height still 1, trying alternative WSL approaches...")

                # Method 1: Try using minsize
                try:
                    titlebar.configure(height=32)
                    titlebar.pack_configure(ipady=16)  # Internal padding
                    self.root.update_idletasks()
                    frame_height = titlebar.winfo_height()
                    print(f"[DEBUG] After ipady: height={frame_height}")
                except Exception as e:
                    print(f"[DEBUG] ipady method failed: {e}")

                # Method 2: Try using a spacer frame to force height
                if frame_height <= 1:
                    try:
                        print("[DEBUG] Trying spacer frame approach...")
                        # Create an invisible spacer frame to force height
                        spacer = tk.Frame(
                            titlebar, bg=theme.panel_header_bg, height=32, width=1
                        )
                        spacer.pack(side="left", fill="y")
                        spacer.pack_propagate(False)
                        self.root.update_idletasks()
                        frame_height = titlebar.winfo_height()
                        print(f"[DEBUG] After spacer frame: height={frame_height}")
                    except Exception as e:
                        print(f"[DEBUG] Spacer frame method failed: {e}")

                # Method 3: Try using a nested frame
                if frame_height <= 1:
                    try:
                        print("[DEBUG] Trying nested frame approach...")
                        inner_frame = tk.Frame(
                            titlebar, bg=theme.panel_header_bg, height=30
                        )
                        inner_frame.pack(fill="both", expand=True, padx=1, pady=1)
                        inner_frame.pack_propagate(False)
                        self.root.update_idletasks()
                        frame_height = titlebar.winfo_height()
                        print(f"[DEBUG] After nested frame: height={frame_height}")
                    except Exception as e:
                        print(f"[DEBUG] Nested frame method failed: {e}")

            # Window title - adjust based on whether we're using system titlebar too
            if hasattr(self, "use_system_titlebar") and self.use_system_titlebar:
                title_text = (
                    f"Custom Controls"  # Shorter since system titlebar has main title
                )
            elif self.desktop_env == "wsl":
                title_text = f"ThreePaneWindows WSL Demo"
            else:
                title_text = f"ThreePaneWindows {self.desktop_env.upper()} Demo"
            print(f"[DEBUG] Creating title label: '{title_text}'")
            logger.info(f"Creating title label: '{title_text}'")

            # Use a larger font and more padding to force height on WSL
            title_label = tk.Label(
                titlebar,
                text=title_text,
                bg=theme.panel_header_bg,
                fg=theme.panel_header_text,
                font=("Arial", 11, "bold"),  # Slightly larger font
                anchor="w",
                height=2,  # Force label height
            )

            # Use more padding to force the titlebar height
            if hasattr(self, "desktop_env") and self.desktop_env == "wsl":
                # WSL needs more aggressive padding
                title_label.pack(
                    side="left", fill="both", expand=True, padx=10, pady=8, ipady=4
                )
                print("[DEBUG] Applied WSL-specific title label padding")
            else:
                title_label.pack(side="left", fill="both", expand=True, padx=10, pady=6)

            print("[DEBUG] Title label created and packed")
            logger.info("Title label created and packed")

            # Window controls
            print("[DEBUG] Creating controls frame...")
            logger.info("Creating controls frame...")
            controls_frame = tk.Frame(titlebar, bg=theme.panel_header_bg)

            # Use more padding for WSL to force height
            if hasattr(self, "desktop_env") and self.desktop_env == "wsl":
                controls_frame.pack(side="right", pady=8, padx=4, ipady=4)
                print("[DEBUG] Applied WSL-specific controls frame padding")
            else:
                controls_frame.pack(side="right", pady=4, padx=4)

            # Minimize button
            print("[DEBUG] Creating minimize button...")
            logger.info("Creating minimize button...")
            min_btn = tk.Button(
                controls_frame,
                text="−",
                command=self._minimize_window,
                bg=theme.panel_header_bg,
                fg=theme.panel_header_text,
                activebackground=theme.accent_bg,
                activeforeground=theme.accent_text,
                relief="flat",
                width=3,
                height=2,  # Increased height
                font=("Arial", 10, "bold"),  # Slightly smaller font
                bd=0,
                highlightthickness=0,
            )
            min_btn.pack(side="left", padx=1, pady=2)  # Added vertical padding
            print("[DEBUG] Minimize button created")
            logger.info("Minimize button created")

            # Close button
            print("[DEBUG] Creating close button...")
            logger.info("Creating close button...")
            close_btn = tk.Button(
                controls_frame,
                text="×",
                command=self._safe_quit,
                bg=theme.panel_header_bg,
                fg=theme.panel_header_text,
                activebackground="#e74c3c",
                activeforeground="white",
                relief="flat",
                width=3,
                height=2,  # Increased height to match minimize button
                font=("Arial", 10, "bold"),  # Slightly smaller font
                bd=0,
                highlightthickness=0,
            )
            close_btn.pack(side="left", padx=1, pady=2)  # Added vertical padding
            print("[DEBUG] Close button created")
            logger.info("Close button created")

            # Store references to buttons for theme updates
            titlebar.title_label = title_label
            titlebar.min_btn = min_btn
            titlebar.close_btn = close_btn
            titlebar.controls_frame = controls_frame

            # Force final update and wait for proper rendering
            print("[DEBUG] Final update and rendering...")
            self.root.update_idletasks()
            self.root.update()

            # WSL-specific: Give extra time for frame rendering
            if hasattr(self, "desktop_env") and self.desktop_env == "wsl":
                print("[DEBUG] WSL detected - adding extra rendering delay...")
                import time

                time.sleep(0.05)  # 50ms delay for WSL X server
                self.root.update_idletasks()

            final_height = titlebar.winfo_height()
            print(f"[DEBUG] Final titlebar height: {final_height}")
            logger.info(f"Custom titlebar created successfully: height={final_height}")

            # More lenient height validation for WSL
            if hasattr(self, "desktop_env") and self.desktop_env == "wsl":
                print("[DEBUG] Using WSL-specific final validation...")
                # WSL X servers sometimes report height as 1 initially, but the frame is actually there
                if final_height <= 0:
                    print(
                        f"[DEBUG] ✗ VALIDATION FAILED: height={final_height} (0 or negative)"
                    )
                    raise Exception(f"Titlebar height is invalid: {final_height}")
                elif final_height == 1:
                    print(f"[DEBUG] ⚠ Height is 1 - common on WSL, allowing it")
                    logger.warning(
                        f"Titlebar height reported as 1 - this is common on WSL but titlebar should still work"
                    )
                else:
                    print(f"[DEBUG] ✓ VALIDATION PASSED: height={final_height}")
            else:
                print("[DEBUG] Using standard final validation...")
                # Standard validation for other platforms
                if final_height <= 1:
                    print(f"[DEBUG] ✗ VALIDATION FAILED: height={final_height}")
                    raise Exception(f"Titlebar height is invalid: {final_height}")
                else:
                    print(f"[DEBUG] ✓ VALIDATION PASSED: height={final_height}")

            print("[DEBUG] === _create_custom_titlebar() SUCCESS ===")
            return titlebar

        except Exception as e:
            print(f"[DEBUG] ✗ _create_custom_titlebar() FAILED: {e}")
            logger.error(f"Failed to create custom titlebar: {e}")
            import traceback

            print(f"[DEBUG] Full traceback:")
            traceback.print_exc()
            logger.error(f"Titlebar creation traceback: {traceback.format_exc()}")
            raise

    def _safe_quit(self):
        """Safely quit the application."""
        try:
            logger.info("Quitting application...")
            self.root.quit()
        except Exception as e:
            logger.error(f"Error during quit: {e}")
            # Force exit if normal quit fails
            import sys

            sys.exit(0)

    def _make_window_draggable(self):
        """Make the window draggable by the custom titlebar."""
        if not hasattr(self, "custom_titlebar"):
            return

        def start_drag(event):
            try:
                self.root.x = event.x
                self.root.y = event.y
            except Exception as e:
                logger.debug(f"Start drag failed: {e}")

        def drag_window(event):
            try:
                x = self.root.winfo_pointerx() - self.root.x
                y = self.root.winfo_pointery() - self.root.y
                self.root.geometry(f"+{x}+{y}")
            except Exception as e:
                logger.debug(f"Drag window failed: {e}")

        try:
            # Bind to titlebar and title label for dragging
            self.custom_titlebar.bind("<Button-1>", start_drag)
            self.custom_titlebar.bind("<B1-Motion>", drag_window)

            # Also bind to title label for better dragging area
            if hasattr(self.custom_titlebar, "title_label"):
                self.custom_titlebar.title_label.bind("<Button-1>", start_drag)
                self.custom_titlebar.title_label.bind("<B1-Motion>", drag_window)

            logger.info("Window dragging enabled")

        except Exception as e:
            logger.warning(f"Failed to make window draggable: {e}")

    def _minimize_window(self):
        """Minimize the window."""
        try:
            self.root.iconify()
        except Exception as e:
            logger.debug(f"Window minimize failed: {e}")

    def _refresh_custom_titlebar(self):
        """Refresh custom titlebar with current theme."""
        print("\n[DEBUG] === _refresh_custom_titlebar() START ===")

        if not hasattr(self, "custom_titlebar"):
            print("[DEBUG] ✗ No custom titlebar to refresh")
            return

        try:
            theme = self.theme_manager.get_current_theme()
            print(
                f"[DEBUG] Refreshing titlebar with theme: bg={theme.panel_header_bg}, fg={theme.panel_header_text}"
            )

            # Update titlebar background
            self.custom_titlebar.configure(bg=theme.panel_header_bg)
            print("[DEBUG] ✓ Updated titlebar background")

            # Update title label
            if hasattr(self.custom_titlebar, "title_label"):
                self.custom_titlebar.title_label.configure(
                    bg=theme.panel_header_bg, fg=theme.panel_header_text
                )
                print("[DEBUG] ✓ Updated title label colors")
            else:
                print("[DEBUG] ⚠ No title_label found")

            # Update controls frame
            if hasattr(self.custom_titlebar, "controls_frame"):
                self.custom_titlebar.controls_frame.configure(bg=theme.panel_header_bg)
                print("[DEBUG] ✓ Updated controls frame background")
            else:
                print("[DEBUG] ⚠ No controls_frame found")

            # Update minimize button
            if hasattr(self.custom_titlebar, "min_btn"):
                self.custom_titlebar.min_btn.configure(
                    bg=theme.panel_header_bg,
                    fg=theme.panel_header_text,
                    activebackground=theme.accent_bg,
                    activeforeground=theme.accent_text,
                )
                print("[DEBUG] ✓ Updated minimize button colors")
            else:
                print("[DEBUG] ⚠ No min_btn found")

            # Update close button (keep red hover)
            if hasattr(self.custom_titlebar, "close_btn"):
                self.custom_titlebar.close_btn.configure(
                    bg=theme.panel_header_bg,
                    fg=theme.panel_header_text,
                    activebackground="#e74c3c",
                    activeforeground="white",
                )
                print("[DEBUG] ✓ Updated close button colors")
            else:
                print("[DEBUG] ⚠ No close_btn found")

            # Force update to apply changes
            self.custom_titlebar.update_idletasks()
            self.root.update_idletasks()
            print("[DEBUG] ✓ Forced GUI updates")

            print("[DEBUG] === _refresh_custom_titlebar() SUCCESS ===")
            logger.debug("Custom titlebar refreshed with new theme")

        except Exception as e:
            print(f"[DEBUG] ✗ _refresh_custom_titlebar() FAILED: {e}")
            logger.debug(f"Custom titlebar refresh failed: {e}")
            import traceback

            traceback.print_exc()

    def _check_window_state(self):
        """Check window state after display to diagnose issues."""
        print("\n[DEBUG] === POST-DISPLAY WINDOW STATE CHECK ===")
        try:
            geometry = self.root.geometry()
            override_status = self.root.overrideredirect()
            print(f"[DEBUG] Final window geometry: {geometry}")
            print(f"[DEBUG] Final override redirect status: {override_status}")

            # Check if titlebar is visible and has correct height
            if hasattr(self, "custom_titlebar"):
                titlebar_height = self.custom_titlebar.winfo_height()
                titlebar_width = self.custom_titlebar.winfo_width()
                print(
                    f"[DEBUG] Custom titlebar dimensions: {titlebar_width}x{titlebar_height}"
                )

                if titlebar_height <= 1:
                    print("[DEBUG] ⚠ WARNING: Custom titlebar height is still 1 pixel!")
                    print(
                        "[DEBUG] This explains the blank bar - titlebar is not rendering properly"
                    )
                else:
                    print(
                        f"[DEBUG] ✓ Custom titlebar height looks good: {titlebar_height}px"
                    )

            # Check for multiple windows
            try:
                all_windows = self.root.tk.call("wm", "stackorder", self.root)
                window_count = len(str(all_windows).split()) if all_windows else 1
                print(f"[DEBUG] Number of windows detected: {window_count}")

                if window_count > 1:
                    print("[DEBUG] ⚠ WARNING: Multiple windows detected!")
                    print("[DEBUG] This explains why you see the window twice")
                else:
                    print("[DEBUG] ✓ Only one window detected")

            except Exception as e:
                print(f"[DEBUG] Could not check window count: {e}")

            # Provide user guidance
            if override_status and hasattr(self, "custom_titlebar"):
                titlebar_height = self.custom_titlebar.winfo_height()
                if titlebar_height <= 1:
                    print(
                        "\n[DEBUG] DIAGNOSIS: Custom titlebar created but not rendering properly"
                    )
                    print(
                        "[DEBUG] ISSUE: The blank bar is the space where titlebar should be"
                    )
                    print(
                        "[DEBUG] CAUSE: WSL X server issue - titlebar frame height not being respected"
                    )
                    print(
                        "[DEBUG] WORKAROUND: Set environment variable THREEPANE_WSL_ALTERNATIVE=1"
                    )
                    print(
                        "[DEBUG] This will keep the system titlebar and add custom controls below it"
                    )
                else:
                    print(
                        "\n[DEBUG] DIAGNOSIS: Custom titlebar appears to be working correctly"
                    )
            else:
                print(
                    "\n[DEBUG] DIAGNOSIS: Override redirect may not be working properly"
                )
                print(
                    "[DEBUG] WORKAROUND: Set environment variable THREEPANE_WSL_ALTERNATIVE=1"
                )

            # Show current environment variable status
            wsl_alt = os.environ.get("THREEPANE_WSL_ALTERNATIVE", "not set")
            print(f"[DEBUG] Current THREEPANE_WSL_ALTERNATIVE = '{wsl_alt}'")

            # Additional visibility diagnostics
            try:
                is_visible = self.root.winfo_viewable()
                is_mapped = self.root.winfo_ismapped()
                window_state = self.root.state()
                print(f"[DEBUG] Window viewable: {is_visible}")
                print(f"[DEBUG] Window mapped: {is_mapped}")
                print(f"[DEBUG] Window state: {window_state}")

                # Check window position
                x = self.root.winfo_x()
                y = self.root.winfo_y()
                width = self.root.winfo_width()
                height = self.root.winfo_height()
                print(f"[DEBUG] Window position: ({x}, {y})")
                print(f"[DEBUG] Window size: {width}x{height}")

                # Check if window might be off-screen
                if x < -width or y < -height or x > 2000 or y > 2000:
                    print("[DEBUG] ⚠ WARNING: Window may be positioned off-screen!")
                    print(
                        "[DEBUG] SOLUTION: Try moving your mouse around the screen edges"
                    )
                    print(
                        "[DEBUG] Or try setting DISPLAY variable if using remote X server"
                    )

                if not is_visible:
                    print("[DEBUG] ⚠ WARNING: Window is not viewable!")
                    print("[DEBUG] This could be a WSL X server issue")
                    print("[DEBUG] Try: export DISPLAY=:0 or check your X server")

            except Exception as e:
                print(f"[DEBUG] Extended visibility check failed: {e}")

        except Exception as e:
            print(f"[DEBUG] Window state check failed: {e}")

        print("[DEBUG] === END WINDOW STATE CHECK ===\n")

        # If window is not visible, offer to create a test window
        try:
            is_visible = self.root.winfo_viewable()
            if not is_visible:
                print(
                    "[DEBUG] Since main window is not visible, creating test window..."
                )
                self._create_test_window()
        except:
            pass

    def _create_test_window(self):
        """Create a simple test window to verify X server connectivity."""
        try:
            print("[DEBUG] Creating simple test window...")
            test_window = tk.Toplevel()
            test_window.title("WSL X Server Test")
            test_window.geometry("300x200+200+200")
            test_window.configure(bg="lightblue")

            label = tk.Label(
                test_window,
                text="If you can see this,\nX server is working!",
                bg="lightblue",
                font=("Arial", 12),
            )
            label.pack(expand=True)

            button = tk.Button(
                test_window, text="Close Test", command=test_window.destroy
            )
            button.pack(pady=10)

            test_window.lift()
            test_window.focus_force()
            print("[DEBUG] Test window created - check if you can see it")

        except Exception as e:
            print(f"[DEBUG] Test window creation failed: {e}")

    def _setup_wsl_custom_titlebar(self):
        """Setup WSL-specific custom titlebar enhancements."""
        try:
            if not hasattr(self, "custom_titlebar"):
                return

            # WSL X servers sometimes need additional setup for custom titlebars
            # Add double-click to maximize functionality (common on Windows)
            def on_titlebar_double_click(event):
                try:
                    # Toggle between normal and maximized state
                    if hasattr(self, "_is_maximized") and self._is_maximized:
                        # Restore to normal size
                        self.root.geometry("1000x700+100+100")
                        self._is_maximized = False
                    else:
                        # Maximize window (simulate)
                        self.root.state("zoomed")
                        self._is_maximized = True
                except Exception as e:
                    logger.debug(f"WSL titlebar double-click failed: {e}")

            self.custom_titlebar.bind("<Double-Button-1>", on_titlebar_double_click)
            self._is_maximized = False

            # Add right-click context menu for WSL
            def show_titlebar_menu(event):
                try:
                    menu = tk.Menu(self.root, tearoff=0)
                    menu.add_command(label="Minimize", command=self._minimize_window)
                    menu.add_separator()
                    menu.add_command(label="Close", command=self.root.quit)
                    menu.tk_popup(event.x_root, event.y_root)
                except Exception as e:
                    logger.debug(f"WSL titlebar menu failed: {e}")

            self.custom_titlebar.bind("<Button-3>", show_titlebar_menu)

            # Force window focus for WSL
            self.root.focus_force()

        except Exception as e:
            logger.debug(f"WSL custom titlebar setup failed: {e}")

    def _setup_emergency_exit(self):
        """Setup emergency exit keybindings for custom titlebar mode."""
        try:
            # Bind Ctrl+Q to quit
            self.root.bind("<Control-q>", lambda e: self.root.quit())
            # Bind Alt+F4 to quit (Windows-like)
            self.root.bind("<Alt-F4>", lambda e: self.root.quit())
            # Bind Escape to quit (emergency)
            self.root.bind("<Escape>", lambda e: self.root.quit())

            logger.info("Emergency exit keybindings set up: Ctrl+Q, Alt+F4, Escape")

        except Exception as e:
            logger.debug(f"Emergency exit setup failed: {e}")

    def _test_gui_functionality(self):
        """Test basic GUI functionality before enabling custom titlebar."""
        try:
            logger.info("Testing basic GUI functionality...")

            # Test 1: Create a simple frame
            test_frame = tk.Frame(self.root, bg="red", height=5)
            test_frame.pack(fill="x")

            # Test 2: Force update
            self.root.update_idletasks()

            # Test 3: Check frame properties
            if not test_frame.winfo_exists():
                raise Exception("Test frame does not exist")

            frame_height = test_frame.winfo_height()
            if frame_height <= 0:
                raise Exception(f"Test frame has invalid height: {frame_height}")

            # Test 4: Create a label in the frame
            test_label = tk.Label(test_frame, text="Test", bg="red", fg="white")
            test_label.pack()

            # Test 5: Force another update
            self.root.update_idletasks()

            # Clean up test widgets
            test_frame.destroy()

            logger.info("Basic GUI functionality test passed")
            return True

        except Exception as e:
            logger.warning(f"Basic GUI functionality test failed: {e}")
            return False

    def _setup_flexible_layout(self):
        """Setup the flexible layout with Linux-optimized configuration."""
        # Create pane configurations with Linux-compatible icons
        pane_configs = [
            FlexPaneConfig(
                name="file_explorer",
                title="📁 File Explorer",
                weight=0.25,
                min_size=200,
                icon=self.icon_paths.get("folder", "📁"),
                builder=self._build_file_explorer_content,
                detached_height=500,
                default_width=400,
            ),
            FlexPaneConfig(
                name="data_view",
                title="📊 Data View",
                weight=0.5,
                min_size=300,
                icon=self.icon_paths.get("database", "📊"),
                builder=self._build_data_view_content,
                detached_height=600,
                default_width=600,
            ),
            FlexPaneConfig(
                name="properties",
                title="⚙️ Properties",
                weight=0.25,
                min_size=200,
                icon=self.icon_paths.get("settings", "⚙️"),
                builder=self._build_properties_content,
                detached_height=400,
                default_width=350,
            ),
        ]

        # Create nested layout structure
        main_container = FlexContainer(
            direction=LayoutDirection.HORIZONTAL,
            children=[
                pane_configs[0],  # File Explorer (left)
                FlexContainer(
                    direction=LayoutDirection.VERTICAL,
                    children=[
                        pane_configs[1],  # Data View (center-top)
                        FlexContainer(
                            direction=LayoutDirection.HORIZONTAL,
                            children=[
                                FlexPaneConfig(
                                    name="tools",
                                    title="🔧 Tools",
                                    weight=0.6,
                                    min_size=200,
                                    icon=self.icon_paths.get("control", "🔧"),
                                    builder=self._build_tools_content,
                                    detached_height=300,
                                    default_width=400,
                                ),
                                pane_configs[2],  # Properties (bottom-right)
                            ],
                            weight=0.4,
                        ),
                    ],
                    weight=0.75,
                ),
            ],
        )

        # Setup menu bar with Linux-appropriate styling first
        self._setup_linux_menubar()

        # Create the flexible layout
        current_theme = self.theme_manager.current_theme.value
        self.layout = EnhancedFlexibleLayout(
            self.root,
            main_container,
            theme_name=current_theme,
        )

        # Pack the layout to fill the remaining space
        self.layout.pack(fill="both", expand=True)

    def _setup_linux_menubar(self):
        """Setup menu bar with Linux-appropriate styling."""
        menu_items = [
            MenuItem(
                "File",
                [
                    MenuItem("New Project", self._new_project, "Ctrl+N"),
                    MenuItem("Open Project", self._open_project, "Ctrl+O"),
                    MenuItem("Save Project", self._save_project, "Ctrl+S"),
                    MenuItem("separator"),
                    MenuItem("Export Data", self._export_data, "Ctrl+E"),
                    MenuItem("separator"),
                    MenuItem("Exit", self._exit_app, "Ctrl+Q"),
                ],
            ),
            MenuItem(
                "View",
                [
                    MenuItem("Refresh", self._refresh_view, "F5"),
                    MenuItem("Zoom In", self._zoom_in, "Ctrl+Plus"),
                    MenuItem("Zoom Out", self._zoom_out, "Ctrl+Minus"),
                    MenuItem("separator"),
                    MenuItem("Full Screen", self._toggle_fullscreen, "F11"),
                ],
            ),
            MenuItem(
                "Theme",
                [
                    MenuItem(
                        "Light Theme", lambda: self._change_theme(ThemeType.LIGHT)
                    ),
                    MenuItem("Dark Theme", lambda: self._change_theme(ThemeType.DARK)),
                    MenuItem("Blue Theme", lambda: self._change_theme(ThemeType.BLUE)),
                    MenuItem(
                        "Green Theme", lambda: self._change_theme(ThemeType.GREEN)
                    ),
                    MenuItem(
                        "Purple Theme", lambda: self._change_theme(ThemeType.PURPLE)
                    ),
                    MenuItem("separator"),
                    MenuItem(
                        "System Theme", lambda: self._change_theme(ThemeType.SYSTEM)
                    ),
                ],
            ),
            MenuItem(
                "Linux",
                [
                    MenuItem("Desktop Info", self._show_desktop_info),
                    MenuItem("Font Info", self._show_font_info),
                    MenuItem("Icon Info", self._show_icon_info),
                    MenuItem("separator"),
                    MenuItem("Detect Dark Mode", self._detect_dark_mode),
                    MenuItem("Test Transparency", self._test_transparency),
                ],
            ),
            MenuItem(
                "Help",
                [
                    MenuItem("About", self._show_about),
                    MenuItem("Linux Features", self._show_linux_features),
                    MenuItem("Keyboard Shortcuts", self._show_shortcuts),
                ],
            ),
        ]

        self.menubar = CustomMenubar(self.root)
        self.menubar.pack(fill="x", side="top")

        # Add menus to the menubar
        for menu_item in menu_items:
            self.menubar.add_menu(menu_item.label, menu_item.submenu or [])

        # Apply theme to menubar
        theme = self.theme_manager.get_current_theme()
        self.menubar.configure(bg=theme.menu_bg)

    def _build_file_explorer_content(self, parent: tk.Frame):
        """Build file explorer content with Linux-style file tree."""
        # Title with Linux styling
        title_frame = tk.Frame(parent)
        title_frame.pack(
            fill="x",
            padx=self.spacing_manager.spacing.padding_normal,
            pady=self.spacing_manager.spacing.padding_small,
        )

        title_label = tk.Label(
            title_frame,
            text="Linux File System",
            font=self.typography_manager.get_font("title", "bold"),
        )
        title_label.pack(side="left")

        # File tree with Linux paths
        tree_frame = tk.Frame(parent)
        tree_frame.pack(
            fill="both",
            expand=True,
            padx=self.spacing_manager.spacing.padding_normal,
            pady=self.spacing_manager.spacing.padding_small,
        )

        # Create treeview with scrollbar
        tree = ttk.Treeview(
            tree_frame, columns=("size", "modified"), show="tree headings"
        )
        tree.heading("#0", text="Name")
        tree.heading("size", text="Size")
        tree.heading("modified", text="Modified")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Add Linux-specific directories
        linux_dirs = [
            ("🏠 /home", "Home Directory", "4.0 KB", "Today"),
            ("📁 /usr", "User Programs", "2.1 GB", "Yesterday"),
            ("⚙️ /etc", "Configuration", "12.5 MB", "Last week"),
            ("📚 /var", "Variable Data", "856 MB", "2 days ago"),
            ("🔧 /bin", "System Binaries", "45.2 MB", "Last month"),
            ("📦 /opt", "Optional Software", "1.2 GB", "3 days ago"),
            ("💾 /tmp", "Temporary Files", "128 MB", "1 hour ago"),
        ]

        for i, (name, desc, size, modified) in enumerate(linux_dirs):
            item_id = tree.insert("", "end", text=name, values=(size, modified))

            # Add some subdirectories for demonstration
            if i < 3:
                tree.insert(
                    item_id,
                    "end",
                    text=f"  📄 {desc} file 1",
                    values=("1.2 KB", "Today"),
                )
                tree.insert(
                    item_id,
                    "end",
                    text=f"  📄 {desc} file 2",
                    values=("3.4 KB", "Yesterday"),
                )

        # Expand first few items
        for item in tree.get_children()[:3]:
            tree.item(item, open=True)

        # Action buttons with Linux styling
        button_frame = tk.Frame(parent)
        button_frame.pack(
            fill="x",
            padx=self.spacing_manager.spacing.padding_normal,
            pady=self.spacing_manager.spacing.padding_small,
        )

        buttons = [
            ("📂 Open", self._open_file),
            ("📋 Copy Path", self._copy_path),
            ("🔍 Search", self._search_files),
        ]

        for text, command in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                command=command,
                font=self.typography_manager.get_font("normal"),
                padx=self.spacing_manager.spacing.button_padding_x,
                pady=self.spacing_manager.spacing.button_padding_y,
            )
            btn.pack(side="left", padx=self.spacing_manager.spacing.margin_small)

    def _build_data_view_content(self, parent: tk.Frame):
        """Build data view content with Linux system information."""
        # Create notebook for tabbed interface
        notebook = ttk.Notebook(parent)
        notebook.pack(
            fill="both",
            expand=True,
            padx=self.spacing_manager.spacing.padding_normal,
            pady=self.spacing_manager.spacing.padding_small,
        )

        # System Info Tab
        sys_frame = tk.Frame(notebook)
        notebook.add(sys_frame, text="🖥️ System Info")

        self._build_system_info_tab(sys_frame)

        # Process Monitor Tab
        proc_frame = tk.Frame(notebook)
        notebook.add(proc_frame, text="⚡ Processes")

        self._build_process_monitor_tab(proc_frame)

        # Network Tab
        net_frame = tk.Frame(notebook)
        notebook.add(net_frame, text="🌐 Network")

        self._build_network_tab(net_frame)

    def _build_system_info_tab(self, parent: tk.Frame):
        """Build system information tab."""
        # System info with Linux details
        info_text = tk.Text(
            parent,
            wrap="word",
            font=self.typography_manager.get_font("normal", family="monospace"),
            height=20,
        )
        info_text.pack(
            fill="both",
            expand=True,
            padx=self.spacing_manager.spacing.padding_normal,
            pady=self.spacing_manager.spacing.padding_small,
        )

        # Get system information
        system_info = f"""Linux System Information
{'=' * 50}

Desktop Environment: {self.desktop_env.title()}
Dark Mode Detected: {self.is_dark_mode}
Platform: {platform.platform()}
Architecture: {platform.architecture()[0]}
Processor: {platform.processor() or 'Unknown'}
Python Version: {platform.python_version()}

Font Configuration:
- Primary Font: {self.typography_manager.typography.font_family}
- Fallback Font: {self.typography_manager.typography.font_family_fallback}
- Monospace Font: {self.typography_manager.typography.font_family_monospace}

Theme Information:
- Current Theme: {self.theme_manager.current_theme.value}
- Supports Transparency: {self.linux_handler.supports_transparency()}
- System Accent Color: {self.linux_handler.get_system_accent_color()}

Icon Support:
- Recommended Formats: {', '.join(self.linux_handler.get_recommended_icon_formats())}
- Icons Loaded: {len(self.icon_paths)} PNG icons

Spacing Configuration:
- Button Padding: {self.spacing_manager.spacing.button_padding_x}x{self.spacing_manager.spacing.button_padding_y}
- Panel Padding: {self.spacing_manager.spacing.panel_padding}
- Layout Gap: {self.spacing_manager.spacing.layout_gap_normal}
"""

        info_text.insert("1.0", system_info)
        info_text.configure(state="disabled")

    def _build_process_monitor_tab(self, parent: tk.Frame):
        """Build process monitor tab."""
        # Process list simulation
        process_frame = tk.Frame(parent)
        process_frame.pack(
            fill="both",
            expand=True,
            padx=self.spacing_manager.spacing.padding_normal,
            pady=self.spacing_manager.spacing.padding_small,
        )

        # Process tree
        proc_tree = ttk.Treeview(
            process_frame,
            columns=("pid", "cpu", "memory", "status"),
            show="tree headings",
        )
        proc_tree.heading("#0", text="Process")
        proc_tree.heading("pid", text="PID")
        proc_tree.heading("cpu", text="CPU %")
        proc_tree.heading("memory", text="Memory")
        proc_tree.heading("status", text="Status")

        # Add sample Linux processes
        linux_processes = [
            ("systemd", "1", "0.1", "8.2 MB", "Running"),
            ("gnome-shell", "1234", "2.3", "156 MB", "Running"),
            ("firefox", "2345", "15.7", "512 MB", "Running"),
            ("python3", "3456", "5.2", "45 MB", "Running"),
            ("code", "4567", "8.1", "234 MB", "Running"),
            ("nautilus", "5678", "1.2", "67 MB", "Running"),
        ]

        for name, pid, cpu, memory, status in linux_processes:
            proc_tree.insert("", "end", text=name, values=(pid, cpu, memory, status))

        proc_tree.pack(fill="both", expand=True)

    def _build_network_tab(self, parent: tk.Frame):
        """Build network information tab."""
        net_info = tk.Text(
            parent,
            wrap="word",
            font=self.typography_manager.get_font("normal", family="monospace"),
        )
        net_info.pack(
            fill="both",
            expand=True,
            padx=self.spacing_manager.spacing.padding_normal,
            pady=self.spacing_manager.spacing.padding_small,
        )

        network_info = """Network Configuration (Simulated)
========================================

Interface: eth0
  Status: Up
  IP Address: 192.168.1.100
  Netmask: 255.255.255.0
  Gateway: 192.168.1.1

Interface: wlan0
  Status: Up
  IP Address: 192.168.1.101
  SSID: MyLinuxNetwork
  Signal: -45 dBm (Excellent)

Interface: lo
  Status: Up
  IP Address: 127.0.0.1
  Description: Loopback

DNS Servers:
  Primary: 8.8.8.8
  Secondary: 8.8.4.4

Active Connections:
  TCP 192.168.1.100:22 -> 192.168.1.50:54321 (SSH)
  TCP 192.168.1.100:80 -> 0.0.0.0:* (HTTP Server)
  UDP 192.168.1.100:53 -> 8.8.8.8:53 (DNS)
"""

        net_info.insert("1.0", network_info)
        net_info.configure(state="disabled")

    def _build_properties_content(self, parent: tk.Frame):
        """Build properties panel with Linux-specific settings."""
        # Properties notebook
        prop_notebook = ttk.Notebook(parent)
        prop_notebook.pack(
            fill="both",
            expand=True,
            padx=self.spacing_manager.spacing.padding_normal,
            pady=self.spacing_manager.spacing.padding_small,
        )

        # Theme Settings Tab
        theme_frame = tk.Frame(prop_notebook)
        prop_notebook.add(theme_frame, text="🎨 Theme")
        self._build_theme_settings(theme_frame)

        # Font Settings Tab
        font_frame = tk.Frame(prop_notebook)
        prop_notebook.add(font_frame, text="🔤 Fonts")
        self._build_font_settings(font_frame)

        # Linux Settings Tab
        linux_frame = tk.Frame(prop_notebook)
        prop_notebook.add(linux_frame, text="🐧 Linux")
        self._build_linux_settings(linux_frame)

    def _build_theme_settings(self, parent: tk.Frame):
        """Build theme settings panel."""
        # Theme selection
        theme_label = tk.Label(
            parent,
            text="Theme Selection:",
            font=self.typography_manager.get_font("medium", "bold"),
        )
        theme_label.pack(
            anchor="w",
            padx=self.spacing_manager.spacing.padding_normal,
            pady=self.spacing_manager.spacing.padding_small,
        )

        # Theme buttons
        themes = [
            (ThemeType.LIGHT, "☀️ Light"),
            (ThemeType.DARK, "🌙 Dark"),
            (ThemeType.BLUE, "💙 Blue"),
            (ThemeType.GREEN, "💚 Green"),
            (ThemeType.PURPLE, "💜 Purple"),
            (ThemeType.SYSTEM, "🖥️ System"),
        ]

        for theme_type, label in themes:
            btn = tk.Button(
                parent,
                text=label,
                command=lambda t=theme_type: self._change_theme(t),
                font=self.typography_manager.get_font("normal"),
                padx=self.spacing_manager.spacing.button_padding_x,
                pady=self.spacing_manager.spacing.button_padding_y,
            )
            btn.pack(
                fill="x",
                padx=self.spacing_manager.spacing.padding_normal,
                pady=self.spacing_manager.spacing.margin_tiny,
            )

    def _build_font_settings(self, parent: tk.Frame):
        """Build font settings panel."""
        # Font size controls
        size_label = tk.Label(
            parent,
            text="Font Size:",
            font=self.typography_manager.get_font("medium", "bold"),
        )
        size_label.pack(
            anchor="w",
            padx=self.spacing_manager.spacing.padding_normal,
            pady=self.spacing_manager.spacing.padding_small,
        )

        size_frame = tk.Frame(parent)
        size_frame.pack(fill="x", padx=self.spacing_manager.spacing.padding_normal)

        # Font size scale
        self.font_scale = tk.Scale(
            size_frame,
            from_=0.8,
            to=1.5,
            resolution=0.1,
            orient="horizontal",
            command=self._on_font_scale_change,
        )
        self.font_scale.set(1.0)
        self.font_scale.pack(fill="x")

        # Font samples
        sample_frame = tk.Frame(parent)
        sample_frame.pack(
            fill="x",
            padx=self.spacing_manager.spacing.padding_normal,
            pady=self.spacing_manager.spacing.padding_normal,
        )

        samples = [
            ("Display", "display", "bold"),
            ("Heading", "heading", "bold"),
            ("Title", "title", "medium"),
            ("Normal", "normal", "normal"),
            ("Small", "small", "normal"),
            ("Monospace", "normal", "normal", "monospace"),
        ]

        for text, size, weight, *family in samples:
            font_family = family[0] if family else "default"
            sample = tk.Label(
                sample_frame,
                text=f"{text}: The quick brown fox jumps over the lazy dog",
                font=self.typography_manager.get_font(size, weight, font_family),
            )
            sample.pack(anchor="w", pady=self.spacing_manager.spacing.margin_tiny)

    def _build_linux_settings(self, parent: tk.Frame):
        """Build Linux-specific settings panel."""
        # Desktop environment info
        de_label = tk.Label(
            parent,
            text=f"Desktop Environment: {self.desktop_env.title()}",
            font=self.typography_manager.get_font("medium", "bold"),
        )
        de_label.pack(
            anchor="w",
            padx=self.spacing_manager.spacing.padding_normal,
            pady=self.spacing_manager.spacing.padding_small,
        )

        # Dark mode detection
        dark_mode_var = tk.BooleanVar(value=self.is_dark_mode)
        dark_mode_check = tk.Checkbutton(
            parent,
            text="Dark Mode Detected",
            variable=dark_mode_var,
            state="disabled",
            font=self.typography_manager.get_font("normal"),
        )
        dark_mode_check.pack(
            anchor="w", padx=self.spacing_manager.spacing.padding_normal
        )

        # Transparency support
        transparency_var = tk.BooleanVar(
            value=self.linux_handler.supports_transparency()
        )
        transparency_check = tk.Checkbutton(
            parent,
            text="Transparency Supported",
            variable=transparency_var,
            state="disabled",
            font=self.typography_manager.get_font("normal"),
        )
        transparency_check.pack(
            anchor="w", padx=self.spacing_manager.spacing.padding_normal
        )

        # Linux-specific actions
        action_frame = tk.Frame(parent)
        action_frame.pack(
            fill="x",
            padx=self.spacing_manager.spacing.padding_normal,
            pady=self.spacing_manager.spacing.padding_normal,
        )

        actions = [
            ("🔄 Refresh System Info", self._refresh_system_info),
            ("🎨 Detect System Colors", self._detect_system_colors),
            ("📋 Copy System Info", self._copy_system_info),
        ]

        for text, command in actions:
            btn = tk.Button(
                action_frame,
                text=text,
                command=command,
                font=self.typography_manager.get_font("normal"),
                padx=self.spacing_manager.spacing.button_padding_x,
                pady=self.spacing_manager.spacing.button_padding_y,
            )
            btn.pack(fill="x", pady=self.spacing_manager.spacing.margin_tiny)

    def _build_tools_content(self, parent: tk.Frame):
        """Build tools panel with Linux utilities."""
        # Tools title
        title_label = tk.Label(
            parent,
            text="Linux Tools & Utilities",
            font=self.typography_manager.get_font("title", "bold"),
        )
        title_label.pack(
            padx=self.spacing_manager.spacing.padding_normal,
            pady=self.spacing_manager.spacing.padding_small,
        )

        # Tool categories
        categories = [
            (
                "🔧 System Tools",
                [
                    ("Process Monitor", self._open_process_monitor),
                    ("System Monitor", self._open_system_monitor),
                    ("Log Viewer", self._open_log_viewer),
                ],
            ),
            (
                "📁 File Tools",
                [
                    ("File Manager", self._open_file_manager),
                    ("Disk Usage", self._show_disk_usage),
                    ("Find Files", self._find_files),
                ],
            ),
            (
                "🌐 Network Tools",
                [
                    ("Network Info", self._show_network_info),
                    ("Port Scanner", self._port_scanner),
                    ("Ping Test", self._ping_test),
                ],
            ),
        ]

        for category_name, tools in categories:
            # Category header
            cat_frame = tk.LabelFrame(
                parent,
                text=category_name,
                font=self.typography_manager.get_font("medium", "bold"),
            )
            cat_frame.pack(
                fill="x",
                padx=self.spacing_manager.spacing.padding_normal,
                pady=self.spacing_manager.spacing.padding_small,
            )

            # Tool buttons
            for tool_name, command in tools:
                btn = tk.Button(
                    cat_frame,
                    text=tool_name,
                    command=command,
                    font=self.typography_manager.get_font("normal"),
                    padx=self.spacing_manager.spacing.button_padding_x,
                    pady=self.spacing_manager.spacing.button_padding_y,
                )
                btn.pack(
                    fill="x",
                    padx=self.spacing_manager.spacing.padding_small,
                    pady=self.spacing_manager.spacing.margin_tiny,
                )

    # Event handlers and utility methods
    def _change_theme(self, theme_type: ThemeType):
        """Change the application theme."""
        try:
            set_global_theme(theme_type)
            # Update the layout's theme manager
            self.layout.theme_manager.set_theme(theme_type.value)
            self.layout.refresh_theme()

            # Refresh the main window theming
            theme = self.theme_manager.get_current_theme()
            self.root.configure(bg=theme.primary_bg)

            # Apply Linux titlebar theming
            self.linux_handler.apply_custom_titlebar(self.root, theme)

            # For Ubuntu/GNOME, apply additional integration
            if self.desktop_env == "ubuntu" or self.desktop_env == "gnome":
                self._refresh_ubuntu_theming(theme)
            elif self.desktop_env == "wsl":
                self._refresh_wsl_theming(theme)

            # Refresh custom titlebar if it exists
            self._refresh_custom_titlebar()

            # Also refresh the menubar if it exists
            if hasattr(self, "menubar"):
                self.menubar.configure(bg=theme.menu_bg)
                # Update menubar button colors
                for button in self.menubar.menu_buttons.values():
                    button.configure(
                        bg=theme.menu_bg,
                        fg=theme.menu_text,
                        activebackground=theme.menu_hover,
                        activeforeground=theme.menu_text,
                    )

            logger.info(f"Changed theme to {theme_type.value}")
        except Exception as e:
            logger.error(f"Error changing theme: {e}")
            messagebox.showerror("Theme Error", f"Failed to change theme: {e}")

    def _on_font_scale_change(self, value):
        """Handle font scale change."""
        try:
            scale_factor = float(value)
            self.typography_manager.scale_fonts(scale_factor)
            # Refresh the layout to apply new font sizes
            self.layout.refresh_theme()

            # Refresh the main window theming
            theme = self.theme_manager.get_current_theme()
            self.root.configure(bg=theme.primary_bg)

            # Also refresh the menubar if it exists
            if hasattr(self, "menubar"):
                self.menubar.configure(bg=theme.menu_bg)
                # Update menubar button colors
                for button in self.menubar.menu_buttons.values():
                    button.configure(
                        bg=theme.menu_bg,
                        fg=theme.menu_text,
                        activebackground=theme.menu_hover,
                        activeforeground=theme.menu_text,
                    )

            logger.info(f"Scaled fonts by factor {scale_factor}")
        except Exception as e:
            logger.error(f"Error scaling fonts: {e}")

    # Menu handlers
    def _new_project(self):
        messagebox.showinfo("New Project", "Creating new Linux project...")

    def _open_project(self):
        messagebox.showinfo("Open Project", "Opening Linux project...")

    def _save_project(self):
        messagebox.showinfo("Save Project", "Saving Linux project...")

    def _export_data(self):
        messagebox.showinfo("Export Data", "Exporting data in Linux format...")

    def _exit_app(self):
        self.root.quit()

    def _refresh_view(self):
        messagebox.showinfo("Refresh", "Refreshing Linux view...")

    def _zoom_in(self):
        current_scale = self.font_scale.get()
        new_scale = min(1.5, current_scale + 0.1)
        self.font_scale.set(new_scale)
        self._on_font_scale_change(new_scale)

    def _zoom_out(self):
        current_scale = self.font_scale.get()
        new_scale = max(0.8, current_scale - 0.1)
        self.font_scale.set(new_scale)
        self._on_font_scale_change(new_scale)

    def _toggle_fullscreen(self):
        current_state = self.root.attributes("-fullscreen")
        self.root.attributes("-fullscreen", not current_state)

    def _show_desktop_info(self):
        info = f"""Linux Desktop Information

Desktop Environment: {self.desktop_env.title()}
Dark Mode: {self.is_dark_mode}
Transparency Support: {self.linux_handler.supports_transparency()}
System Accent Color: {self.linux_handler.get_system_accent_color()}

Platform Details:
{platform.platform()}
Architecture: {platform.architecture()[0]}
"""
        messagebox.showinfo("Desktop Information", info)

    def _show_font_info(self):
        typo = self.typography_manager.typography
        info = f"""Linux Font Configuration

Primary Font: {typo.font_family}
Fallback Font: {typo.font_family_fallback}
Monospace Font: {typo.font_family_monospace}
Monospace Fallback: {typo.font_family_monospace_fallback}

Font Sizes:
Normal: {typo.font_size_normal}
Title: {typo.font_size_title}
Heading: {typo.font_size_heading}
Display: {typo.font_size_display}
"""
        messagebox.showinfo("Font Information", info)

    def _show_icon_info(self):
        info = f"""Linux Icon Configuration

Icon Format: PNG (Linux optimized)
Icons Loaded: {len(self.icon_paths)}
Recommended Formats: {', '.join(self.linux_handler.get_recommended_icon_formats())}

Available Icons:
{chr(10).join(f"• {name}: {os.path.basename(path)}" for name, path in self.icon_paths.items())}
"""
        messagebox.showinfo("Icon Information", info)

    def _detect_dark_mode(self):
        is_dark = self.linux_handler.is_dark_mode()
        messagebox.showinfo(
            "Dark Mode Detection",
            f"Dark mode detected: {is_dark}\n\n"
            f"Current theme will be updated automatically.",
        )
        if is_dark != self.is_dark_mode:
            self.is_dark_mode = is_dark
            theme = ThemeType.DARK if is_dark else ThemeType.LIGHT
            self._change_theme(theme)

    def _test_transparency(self):
        supports = self.linux_handler.supports_transparency()
        messagebox.showinfo(
            "Transparency Test",
            f"Transparency supported: {supports}\n\n"
            f"Desktop Environment: {self.desktop_env}",
        )

    def _show_about(self):
        about_text = f"""ThreePaneWindows - Linux Comprehensive Demo

Version: 1.0.0
Platform: Linux ({self.desktop_env})
Python: {platform.python_version()}

This demo showcases the full capabilities of ThreePaneWindows
optimized for Linux desktop environments including:

• Flexible layout system
• Linux-native theming
• Ubuntu/DejaVu Sans typography
• PNG icon support
• Desktop environment detection
• Dark mode integration
• Professional Linux styling

Developed with ❤️ for the Linux community
"""
        messagebox.showinfo("About", about_text)

    def _show_linux_features(self):
        features_text = """Linux-Specific Features

🐧 Desktop Environment Detection
   • Automatic detection of GNOME, KDE, XFCE, etc.
   • Environment-specific optimizations

🎨 Native Theming
   • System dark mode detection
   • Desktop-specific color schemes
   • Accent color integration

🔤 Linux Typography
   • Ubuntu font family (primary)
   • DejaVu Sans fallback fonts
   • Optimized font sizes for Linux displays

🖼️ Icon Support
   • PNG format optimization
   • XBM format support
   • Linux-compatible icon paths

⚙️ Window Management
   • Proper window class setting
   • Linux window manager integration
   • Transparency detection and support

🔧 System Integration
   • Process monitoring capabilities
   • Network information display
   • File system navigation
"""
        messagebox.showinfo("Linux Features", features_text)

    def _show_shortcuts(self):
        shortcuts_text = """Keyboard Shortcuts

File Operations:
Ctrl+N    New Project
Ctrl+O    Open Project
Ctrl+S    Save Project
Ctrl+E    Export Data
Ctrl+Q    Exit Application

View Controls:
F5        Refresh View
Ctrl++    Zoom In
Ctrl+-    Zoom Out
F11       Toggle Fullscreen

Linux Specific:
Alt+F4    Close Window (Linux standard)
Super+L   Lock Screen (if supported)
Ctrl+Alt+T Terminal (system shortcut)

Navigation:
Tab       Navigate between panes
Shift+Tab Navigate backwards
Enter     Activate selected item
Escape    Cancel current operation
"""
        messagebox.showinfo("Keyboard Shortcuts", shortcuts_text)

    # Tool handlers
    def _open_file(self):
        messagebox.showinfo("Open File", "Opening selected Linux file...")

    def _copy_path(self):
        messagebox.showinfo("Copy Path", "Linux file path copied to clipboard")

    def _search_files(self):
        messagebox.showinfo("Search Files", "Searching Linux file system...")

    def _refresh_system_info(self):
        messagebox.showinfo("Refresh", "System information refreshed")

    def _detect_system_colors(self):
        colors = self.linux_handler.get_platform_native_colors()
        color_info = "\n".join(f"{k}: {v}" for k, v in colors.items())
        messagebox.showinfo("System Colors", f"Detected Linux colors:\n\n{color_info}")

    def _copy_system_info(self):
        messagebox.showinfo("Copy", "System information copied to clipboard")

    def _open_process_monitor(self):
        messagebox.showinfo("Process Monitor", "Opening Linux process monitor...")

    def _open_system_monitor(self):
        messagebox.showinfo("System Monitor", "Opening Linux system monitor...")

    def _open_log_viewer(self):
        messagebox.showinfo("Log Viewer", "Opening Linux log viewer...")

    def _open_file_manager(self):
        messagebox.showinfo("File Manager", "Opening Linux file manager...")

    def _show_disk_usage(self):
        messagebox.showinfo("Disk Usage", "Showing Linux disk usage...")

    def _find_files(self):
        messagebox.showinfo("Find Files", "Linux file search utility...")

    def _show_network_info(self):
        messagebox.showinfo("Network Info", "Displaying Linux network information...")

    def _port_scanner(self):
        messagebox.showinfo("Port Scanner", "Linux port scanning tool...")

    def _ping_test(self):
        messagebox.showinfo("Ping Test", "Linux network ping test...")

    def run(self):
        """Run the Linux demo application."""
        logger.info("Starting Linux comprehensive demo")
        self.root.mainloop()


def main():
    """Main entry point for the Linux demo."""
    # Check if running on Linux
    if platform.system() != "Linux":
        print("Warning: This demo is optimized for Linux systems.")
        print(f"Current system: {platform.system()}")
        print("Some features may not work as expected on non-Linux systems.")

        response = input("Continue anyway? (y/N): ")
        if response.lower() != "y":
            print("Exiting...")
            return

    try:
        # Create and run the demo
        demo = LinuxComprehensiveDemo()
        demo.run()
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"Error running Linux demo: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
