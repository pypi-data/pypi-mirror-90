#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "click>=7.1.2",
    "ipython>=6.0",
]

setup_requirements = [
    "pytest-runner",
]

test_requirements = [
    "pytest>=3.8",
]

setup(
    author="Matthias Hölzl",
    author_email="tc@xantira.com",
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    description="Support for code that works interactively and in batch mode.",
    entry_points={
        "console_scripts": [
            "nbex=nbex.cli:main",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="nbex",
    name="nbex",
    packages=find_packages(include=["nbex", "nbex.*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/hoelzl/nbex",
    version="0.3.1",
    zip_safe=False,
)
