User Guide
==========

This comprehensive user guide covers all aspects of using ThreePaneWindows in your applications.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   layouts
   theming
   cross_platform_icons
   customization
   advanced_features
   best_practices
   troubleshooting

Overview
--------

ThreePaneWindows provides professional three-pane window layouts for Tkinter applications. Whether you need a simple fixed layout or an advanced dockable interface, this library has you covered.

Key Features
~~~~~~~~~~~~

* **Multiple Layout Types**: Choose from fixed-width or fully dockable layouts
* **Professional Theming**: Built-in light and dark themes with customization options
* **Cross-Platform Icon Support**: Multiple icon formats (.ico, .png, .gif, .bmp, .xbm) with automatic platform optimization
* **Advanced Docking**: Drag-and-drop pane reordering and window detachment
* **Responsive Design**: Automatic resizing and intelligent layout management
* **Rich Components**: Status bars, toolbars, context menus, and more
* **Easy Integration**: Simple API that works with existing Tkinter code
* **Cross-Platform**: Consistent behavior on Windows, macOS, and Linux

Getting Started
~~~~~~~~~~~~~~~

If you're new to ThreePaneWindows, start with the :doc:`../quickstart` guide for a hands-on introduction. Then explore the specific topics in this user guide based on your needs.

For developers looking to integrate ThreePaneWindows into existing applications, the :doc:`best_practices` section provides valuable guidance on architecture and design patterns.

Layout Types Comparison
~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Layout Comparison
   :header-rows: 1
   :widths: 20 25 25 30

   * - Feature
     - FixedThreePaneWindow
     - DockableThreePaneWindow
     - EnhancedDockableThreePaneWindow
   * - Fixed pane sizes
     - ✓
     - ✗
     - ✗
   * - Resizable panes
     - ✗
     - ✓
     - ✓
   * - Drag & drop
     - ✗
     - ✓
     - ✓
   * - Detachable panes
     - ✗
     - ✓
     - ✓
   * - Built-in theming
     - Basic
     - ✓
     - ✓
   * - Cross-platform icons
     - ✗
     - ✗
     - ✓
   * - Status bars
     - ✗
     - ✗
     - ✓
   * - Toolbars
     - ✗
     - ✗
     - ✓
   * - Context menus
     - ✗
     - ✗
     - ✓
   * - Complexity
     - Low
     - Medium
     - High

Choose the layout type that best fits your application's requirements and complexity needs.
