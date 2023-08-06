#!/usr/bin/env python3
from setuptools import setup, find_packages

long_description = """
Placeholder for jenni package
"""

setup(
    name="jenni",
    version="0.0.1",
    packages=find_packages(include=("jenni","jenni.*"), exclude=("test", "test.*")),
    install_requires=[],
    python_requires='>=3.6',
    license="Apache 2.0",
    url="https://pypi.org/project/jenni",
    author="Wouter Batelaan",
    author_email="wbjrpub@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        # "Development Status :: 3 - Alpha",
        "Development Status :: 1 - Planning",
    ],
    description="Placeholder for jenni package",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    test_suite="test",
    tests_require=[],
)
