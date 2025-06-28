#!/usr/bin/env python3
"""Setup script for threepanewindows package."""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="threepanewindows",
    version="1.0.4",
    author="ThreePaneWindows Team",
    author_email="contact@example.com",
    description="A Python library for creating dockable and fixed three-pane window layouts in Tkinter with cross-platform icon support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/threepanewindows",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: User Interfaces",
    ],
    python_requires=">=3.7",
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
