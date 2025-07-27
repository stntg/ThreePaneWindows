"""Setup script for threepanewindows type stubs."""

from setuptools import find_packages, setup

setup(
    name="threepanewindows-stubs",
    version="1.0.4",
    description="Type stubs for threepanewindows",
    long_description=(
        "Type stubs for the threepanewindows library - "
        "Professional three-pane window layouts for Tkinter applications."
    ),
    author="Generated Stubs",
    packages=find_packages(),
    package_data={
        "threepanewindows-stubs": ["py.typed", "*.pyi", "*/*.pyi"],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: User Interfaces",
        "Typing :: Stubs Only",
    ],
)
