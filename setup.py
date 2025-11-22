#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
巡检自动化应用安装脚本
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="inspection-automation-app",
    version="1.0.0",
    author="Inspection Team",
    author_email="inspection@example.com",
    description="巡检自动化Android应用",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/inspection-automation-app",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Android",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Topic :: Office/Business",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "inspection-app=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)