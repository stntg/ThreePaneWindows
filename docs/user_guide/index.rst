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
   ../logging

Overview
--------

ThreePaneWindows provides professional three-pane window layouts for Tkinter applications. Whether you need a simple fixed layout or an advanced dockable interface, this library has you covered.

Key Features
~~~~~~~~~~~~

**Core Layout Systems**

* **Enhanced Flexible Layout (NEW v1.3.0)**: Modern flexible layout with weight-based distribution
* **Multiple Layout Types**: Choose from fixed-width or fully dockable layouts

**Advanced Theming & UI Components (NEW v1.3.0)**

* **Central Theme Manager**: Unified theming system across all components
* **Custom Scrollbars**: Fully themeable scrollbars with cross-platform support
* **Custom Menu Bars**: Themeable menu bars that work on all platforms
* **Professional Theming**: Light, Dark, Blue, Green, Purple, System, and Native themes

**Professional Features**

* **Cross-Platform Icon Support**: Multiple icon formats (.ico, .png, .gif, .bmp, .xbm) with automatic platform optimization
* **Advanced Docking**: Drag-and-drop pane reordering and window detachment
* **Comprehensive Logging (NEW v1.3.0)**: Silent by default with configurable debug output
* **Responsive Design**: Automatic resizing and intelligent layout management
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
   :widths: 15 20 20 20 25

   * - Feature
     - FixedThreePaneWindow
     - DockableThreePaneWindow
     - EnhancedDockableThreePaneWindow
     - EnhancedFlexibleLayout (NEW v1.3.0)
   * - Weight-based distribution
     - ✗
     - ✗
     - ✗
     - ✓
   * - Nested layouts
     - ✗
     - ✗
     - ✗
     - ✓
   * - Fixed pane sizes
     - ✓
     - ✗
     - ✗
     - ✓ (configurable)
   * - Resizable panes
     - ✗
     - ✓
     - ✓
     - ✓
   * - Drag & drop
     - ✗
     - ✓
     - ✓
     - ✓
   * - Detachable panes
     - ✗
     - ✓
     - ✓
     - ✓
   * - Central theming
     - ✗
     - ✗
     - ✗
     - ✓
   * - Built-in theming
     - Basic
     - ✓
     - ✓
     - ✓
   * - Cross-platform icons
     - ✗
     - ✗
     - ✓
     - ✓
   * - Complexity
     - Low
     - Medium
     - High
     - Medium-High

Choose the layout type that best fits your application's requirements and complexity needs.
