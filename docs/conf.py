"""Configuration file for the Sphinx documentation builder.

For the full list of built-in configuration values, see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

import os
import sys
from typing import Any, Dict

sys.path.insert(0, os.path.abspath(".."))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "ThreePaneWindows"
copyright = "2025, Stan Griffiths"
author = "Stan Griffiths"

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# Import version from the package
try:
    from threepanewindows._version import FULL_VERSION, __version__

    # The short X.Y version.
    version = ".".join(__version__.split(".")[:2])  # e.g., "1.2" from "1.2.0"
    # The full version, including alpha/beta/rc tags.
    release = FULL_VERSION
except ImportError:
    # Fallback if import fails
    version = "1.2.0"
    release = "1.2.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.ifconfig",
    "sphinx.ext.githubpages",
]

# Add myst_parser if available
try:
    import myst_parser

    extensions.append("myst_parser")
    myst_parser_available = True
    print(f"MyST Parser {myst_parser.__version__} loaded successfully")
except ImportError as e:
    myst_parser_available = False
    print(f"Warning: myst_parser not available ({e}), .md files will not be processed")
except Exception as e:
    myst_parser_available = False
    print(f"Error loading myst_parser ({e}), .md files will not be processed")

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Exclude .md files if MyST parser is not available
if not myst_parser_available:
    exclude_patterns.extend(["*.md", "**/*.md"])

# The suffix(es) of source filenames.
if myst_parser_available:
    source_suffix = {
        ".rst": None,
        ".md": None,
    }
else:
    source_suffix = {
        ".rst": None,
    }

# MyST parser configuration is handled above in extensions

# MyST parser configuration
if myst_parser_available:
    # Check which extensions are available
    available_extensions = []

    # Always available extensions
    basic_extensions = [
        "colon_fence",
        "deflist",
        "replacements",
        "smartquotes",
        "tasklist",
    ]
    available_extensions.extend(basic_extensions)

    # Check if linkify is available
    try:
        from linkify_it import LinkifyIt  # noqa: F401

        available_extensions.append("linkify")
        print("Linkify extension available")
    except ImportError:
        print("Linkify extension not available - skipping")

    try:
        myst_enable_extensions = available_extensions

        # MyST parser options
        myst_heading_anchors = 3
        myst_html_meta = {
            "description lang=en": "Documentation for ThreePaneWindows",
            "keywords": "tkinter, gui, layout, three-pane, dockable, ui",
        }
        print(f"MyST parser configured with extensions: {myst_enable_extensions}")
    except Exception as e:
        # Fallback to minimal configuration
        myst_enable_extensions = basic_extensions
        print(f"Using basic MyST configuration due to: {e}")
else:
    # Fallback: basic MyST configuration
    myst_enable_extensions = []

# The master toctree document.
master_doc = "index"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    "canonical_url": "",
    "analytics_id": "",
    "logo_only": False,
    "display_version": True,
    "prev_next_buttons_location": "bottom",
    "style_external_links": False,
    "vcs_pageview_mode": "",
    "style_nav_header_background": "#2980B9",
    # Toc options
    "collapse_navigation": True,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path is already defined above

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
html_sidebars = {
    "**": [
        "relations.html",  # needs 'show_related': True theme option to display
        "searchbox.html",
    ]
}

# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "ThreePaneWindowsdoc"

# -- Options for LaTeX output ---------------------------------------------

latex_elements: Dict[str, Any] = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',
    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (
        master_doc,
        "ThreePaneWindows.tex",
        "ThreePaneWindows Documentation",
        "ThreePaneWindows Contributors",
        "manual",
    ),
]

# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, "threepanewindows", "ThreePaneWindows Documentation", [author], 1)
]

# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "ThreePaneWindows",
        "ThreePaneWindows Documentation",
        author,
        "ThreePaneWindows",
        "Professional three-pane window layouts for Tkinter.",
        "Miscellaneous",
    ),
]

# -- Extension configuration -------------------------------------------------

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
}

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# -- Options for autodoc extension -------------------------------------------

# This value selects what content will be inserted into the main body of an
# autoclass directive.
autoclass_content = "both"

# This value is a list of autodoc directive flags that should be automatically
# applied to all autodoc directives.
autodoc_default_flags = ["members", "undoc-members", "show-inheritance"]

# This value controls how to represent typehints.
autodoc_typehints = "description"

# -- Options for autosummary extension ---------------------------------------

autosummary_generate = True

# -- Setup function for additional configuration ---------------------------


def setup(app: Any) -> Dict[str, Any]:
    """Sphinx setup function for additional configuration."""
    # Add any custom setup here
    if myst_parser_available:
        print("MyST parser is configured and ready")
    else:
        print("MyST parser is not available - only .rst files will be processed")

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
