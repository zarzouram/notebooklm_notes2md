#!/usr/bin/env python3
"""
Setup script for notebooklm_notes2md package.
"""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="notebooklm_notes2md",
    version="0.2.0",
    author="zarzouram",
    # author_email="your.email@example.com",
    description="Convert NotebookLM notes to Markdown or PDF",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zarzouram/notebooklm_notes2md",
    packages=find_packages(),
    py_modules=["notebooklm_export"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "beautifulsoup4>=4.13.0",
        "markdown_pdf>=1.7.0",
    ],
    entry_points={
        "console_scripts": [
            "notebooklm-export=notebooklm_notes2md.cli.main:main",
        ],
    },
)
