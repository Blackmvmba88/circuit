#!/usr/bin/env python3
"""Setup script for Circuit CLI."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="circuit-cli",
    version="1.0.0",
    description="CLI tool for working with .circuit.json electronic circuit files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Circuit Project",
    url="https://github.com/Blackmvmba88/circuit",
    license="MIT",
    packages=find_packages(exclude=["tests", "docs", "examples"]),
    include_package_data=True,
    package_data={
        "": ["schema/*.json"],
    },
    python_requires=">=3.7",
    install_requires=[
        "jsonschema>=4.0.0",
    ],
    entry_points={
        "console_scripts": [
            "circuit=cli.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="circuit electronics eda pcb schematic json",
)
