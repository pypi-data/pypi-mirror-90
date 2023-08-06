#!/usr/bin/env python

"""
Simple setup - should work on most Python versions.
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()  # pylint: disable=invalid-name

setuptools.setup(
    name='mitoc_const',
    version='1.0.1',
    author='David Cain',
    author_email='davidjosephcain@gmail.com',
    url='https://github.com/DavidCain/mitoc-const',
    packages=['mitoc_const'],
    package_data={'mitoc_const': ["py.typed"]},
    description='Constants for use across MIT Outing Club infrastructure',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
    ],
    # Type hints are available in this library. For Python 2 or <3.5, use < 0.5.0
    python_requires='>=3.5',
    # https://mypy.readthedocs.io/en/stable/installed_packages.html#making-pep-561-compatible-packages
    # > If you use setuptools, you must pass the option zip_safe=False to setup(),
    # or mypy will not be able to find the installed package.
    zip_safe=False,
)
