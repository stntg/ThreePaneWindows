API Reference
=============

Complete API documentation for all ThreePaneWindows classes and functions.

.. toctree::
   :maxdepth: 2
   :caption: API Modules:

   fixed
   dockable
   enhanced
   themes
   cli
   utilities

Overview
--------

The ThreePaneWindows API is organized into several modules:

Core Layout Classes
~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: _autosummary

   threepanewindows.FixedThreePaneWindow
   threepanewindows.DockableThreePaneWindow
   threepanewindows.EnhancedDockableThreePaneWindow

Configuration Classes
~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: _autosummary

   threepanewindows.PaneConfig

Theming System
~~~~~~~~~~~~~~

.. autosummary::
   :toctree: _autosummary

   threepanewindows.ThemeManager
   threepanewindows.get_theme_manager
   threepanewindows.set_global_theme
   threepanewindows.ThemeType

Quick Reference
---------------

Most Common Classes
~~~~~~~~~~~~~~~~~~~

For most applications, you'll primarily use these classes:

.. code-block:: python

   from threepanewindows import (
       FixedThreePaneWindow,        # Simple fixed layout
       DockableThreePaneWindow,     # Resizable/dockable layout
       EnhancedDockableThreePaneWindow,  # Full-featured layout
   )

Basic Usage Pattern
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tkinter as tk
   from threepanewindows import FixedThreePaneWindow

   root = tk.Tk()
   window = FixedThreePaneWindow(root)
   window.pack(fill=tk.BOTH, expand=True)

   # Access panes
   left_pane = window.left_pane
   center_pane = window.center_pane  
   right_pane = window.right_pane

Common Parameters
~~~~~~~~~~~~~~~~~

Most layout classes accept these common parameters:

* ``parent`` - The parent Tkinter widget
* ``left_width`` - Initial width of left pane (pixels)
* ``right_width`` - Initial width of right pane (pixels)
* ``min_pane_size`` - Minimum size for any pane (pixels)
* ``theme`` - Theme name or ThemeType enum value

Error Handling
~~~~~~~~~~~~~~

All classes raise appropriate exceptions for invalid parameters:

* ``ValueError`` - Invalid parameter values
* ``TypeError`` - Wrong parameter types
* ``RuntimeError`` - Runtime configuration errors

Type Hints
~~~~~~~~~~

All public APIs include comprehensive type hints for better IDE support and static analysis.