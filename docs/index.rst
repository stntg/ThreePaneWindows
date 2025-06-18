ThreePaneWindows Documentation
==============================

.. image:: https://img.shields.io/pypi/v/threepanewindows.svg
    :target: https://pypi.org/project/threepanewindows/
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/threepanewindows.svg
    :target: https://pypi.org/project/threepanewindows/
    :alt: Python versions

.. image:: https://github.com/stntg/threepanewindows/workflows/CI/badge.svg
    :target: https://github.com/stntg/threepanewindows/actions
    :alt: CI Status

.. image:: https://codecov.io/gh/stntg/threepanewindows/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/stntg/threepanewindows
    :alt: Coverage

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code style: black

**ThreePaneWindows** is a professional Python library for creating sophisticated three-pane window layouts in Tkinter applications. It provides ready-to-use, customizable components with advanced features like docking, theming, and modern UI elements.

Features
--------

* **Multiple Layout Types**: Fixed-width and dockable three-pane layouts
* **Professional Theming**: Built-in light and dark themes with customization options
* **Advanced Docking**: Drag-and-drop pane reordering and detachment
* **Responsive Design**: Automatic resizing and layout management
* **Rich Components**: Status bars, toolbars, context menus, and more
* **Easy Integration**: Simple API that works with existing Tkinter applications
* **Cross-Platform**: Works on Windows, macOS, and Linux

Quick Start
-----------

Installation
~~~~~~~~~~~~

.. code-block:: bash

    pip install threepanewindows

Basic Usage
~~~~~~~~~~~

.. code-block:: python

    import tkinter as tk
    from threepanewindows import FixedThreePaneWindow

    root = tk.Tk()
    root.title("My Application")
    root.geometry("1200x800")

    # Create a three-pane window
    three_pane = FixedThreePaneWindow(root)
    three_pane.pack(fill=tk.BOTH, expand=True)

    # Add content to panes
    left_label = tk.Label(three_pane.left_pane, text="Left Pane", bg="lightblue")
    left_label.pack(fill=tk.BOTH, expand=True)

    center_label = tk.Label(three_pane.center_pane, text="Center Pane", bg="lightgreen")
    center_label.pack(fill=tk.BOTH, expand=True)

    right_label = tk.Label(three_pane.right_pane, text="Right Pane", bg="lightcoral")
    right_label.pack(fill=tk.BOTH, expand=True)

    root.mainloop()

Table of Contents
-----------------

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   installation
   quickstart
   user_guide/index
   examples/index

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/index
   api/fixed
   api/dockable
   api/themes
   api/cli

.. toctree::
   :maxdepth: 2
   :caption: Development

   contributing
   changelog
   license

.. toctree::
   :maxdepth: 1
   :caption: Links

   GitHub Repository <https://github.com/stntg/threepanewindows>
   PyPI Package <https://pypi.org/project/threepanewindows/>
   Issue Tracker <https://github.com/stntg/threepanewindows/issues>

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`