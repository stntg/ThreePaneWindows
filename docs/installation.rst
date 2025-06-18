Installation
============

Requirements
------------

ThreePaneWindows requires Python 3.8 or later and works with the following operating systems:

* Windows 10/11
* macOS 10.14+
* Linux (Ubuntu 18.04+, CentOS 7+, or equivalent)

Dependencies
~~~~~~~~~~~~

The package has minimal dependencies:

* **tkinter** - Usually included with Python
* **typing-extensions** - For Python < 3.10 compatibility

Install from PyPI
-----------------

The easiest way to install ThreePaneWindows is using pip:

.. code-block:: bash

    pip install threepanewindows

This will install the latest stable version from PyPI.

Install from Source
-------------------

To install the latest development version from GitHub:

.. code-block:: bash

    pip install git+https://github.com/yourusername/threepanewindows.git

Development Installation
------------------------

If you want to contribute to ThreePaneWindows or modify the source code:

.. code-block:: bash

    git clone https://github.com/yourusername/threepanewindows.git
    cd threepanewindows
    pip install -e .[dev]

This installs the package in "editable" mode with development dependencies.

Verify Installation
-------------------

To verify that ThreePaneWindows is installed correctly:

.. code-block:: python

    import threepanewindows
    print(threepanewindows.__version__)

Or run the built-in examples:

.. code-block:: bash

    python -m threepanewindows.examples

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**ImportError: No module named 'tkinter'**

On some Linux distributions, tkinter is not installed by default:

.. code-block:: bash

    # Ubuntu/Debian
    sudo apt-get install python3-tk
    
    # CentOS/RHEL/Fedora
    sudo yum install tkinter
    # or
    sudo dnf install python3-tkinter

**Display Issues on Linux**

If you're running on a headless Linux server or in a container, you may need to set up a virtual display:

.. code-block:: bash

    sudo apt-get install xvfb
    export DISPLAY=:99
    Xvfb :99 -screen 0 1024x768x24 &

**Permission Issues**

If you encounter permission errors during installation:

.. code-block:: bash

    pip install --user threepanewindows

This installs the package for the current user only.

Getting Help
------------

If you encounter issues not covered here:

1. Check the `GitHub Issues <https://github.com/yourusername/threepanewindows/issues>`_
2. Search the documentation
3. Create a new issue with details about your environment and the problem