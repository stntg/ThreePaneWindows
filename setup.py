#!/usr/bin/env python3
"""Setup script for threepanewindows package."""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="threepanewindows",
    version="1.3.0",
    author="Stan Griffiths",
    author_email="stantgriffiths@gmail.com",
    description=(
        "Professional three-pane window layouts for Tkinter applications with "
        "flexible layouts, advanced theming, custom UI components, and comprehensive logging"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stntg/threepanewindows",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: User Interfaces",
    ],
    python_requires=">=3.9",
    install_requires=[
        # tkinter is part of Python standard library
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "black",
            "flake8",
        ],
    },
    entry_points={
        "console_scripts": [
            "threepane=threepanewindows.cli:main",
            "threepane-demo=threepanewindows.examples:run_demo",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
