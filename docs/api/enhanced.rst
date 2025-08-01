Enhanced Dockable API
=====================

The enhanced dockable module provides professional-grade three-pane windows with advanced features including cross-platform icon support, professional theming, and sophisticated user interactions.

.. automodule:: threepanewindows.enhanced_dockable
   :members:
   :undoc-members:
   :show-inheritance:

EnhancedDockableThreePaneWindow
-------------------------------

.. autoclass:: threepanewindows.EnhancedDockableThreePaneWindow
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

PaneConfig
----------

.. autoclass:: threepanewindows.PaneConfig
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

Cross-Platform Icon Support
----------------------------

The enhanced dockable window supports cross-platform icon display for detached windows with automatic format detection and fallback mechanisms.

Supported Icon Formats
~~~~~~~~~~~~~~~~~~~~~~~

* **Windows**: ``.ico`` (primary), ``.png``, ``.bmp``, ``.gif`` (secondary)
* **macOS**: ``.png`` (primary), ``.gif``, ``.bmp`` (secondary), ``.ico`` (limited)
* **Linux**: ``.png``, ``.xbm`` (primary), ``.gif``, ``.bmp`` (secondary), ``.ico`` (limited)

Icon Resolution Strategy
~~~~~~~~~~~~~~~~~~~~~~~~

1. Check file existence
2. Detect format from extension
3. Use best method for format (``iconbitmap`` for .ico, ``iconphoto`` for others)
4. Fallback to alternative methods if primary fails
5. Continue without icon if all methods fail

Example Usage
~~~~~~~~~~~~~

.. code-block:: python

    from threepanewindows.enhanced_dockable import (
        PaneConfig,
        get_recommended_icon_formats,
        validate_icon_path
    )

    # Check recommended formats for current platform
    formats = get_recommended_icon_formats()
    print(f"Recommended formats: {formats}")

    # Validate icon before use
    is_valid, message = validate_icon_path("icons/app.png")
    if is_valid:
        config = PaneConfig(
            title="My Panel",
            icon="🔧",                    # Unicode icon for header
            window_icon="icons/app.png"   # File icon for detached window
        )

Icon Utility Functions
~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: threepanewindows.enhanced_dockable.get_recommended_icon_formats
   :no-index:

.. autofunction:: threepanewindows.enhanced_dockable.validate_icon_path
   :no-index:
