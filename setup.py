#!/usr/bin/env python3
"""
Circuit - Universal Electronic Circuit Format
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="circuit-cli",
    version="0.2.0",
    description="Universal format for describing electronic circuits and logic designs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Circuit Project",
    author_email="contact@circuit-project.org",
    url="https://github.com/Blackmvmba88/circuit",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "jsonschema>=4.0.0",
        "click>=8.0.0",
        "colorama>=0.4.0",
        "rich>=10.0.0",
    ],
    entry_points={
        "console_scripts": [
            "circuit=circuit.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
    ],
    keywords="electronics circuit eda schematic pcb design",
)
