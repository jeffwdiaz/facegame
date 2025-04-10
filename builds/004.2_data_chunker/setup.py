"""
Setup configuration for the Data Chunker package.
"""

from setuptools import setup, find_packages

setup(
    name="data_chunker",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.21.0",
    ],
    entry_points={
        "console_scripts": [
            "data-chunker=data_chunker.main:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool for processing large JSON files by splitting them into smaller chunks",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/data_chunker",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 