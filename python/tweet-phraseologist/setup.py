#!/usr/bin/env python3
# coding=utf-8
"""A setuptools-based script for installing Tweet Phraseologist.

For more information, see:

* https://packaging.python.org/en/latest/index.html
* https://docs.python.org/distutils/sourcedist.html
"""
from setuptools import find_packages, setup


def _get_long_description() -> str:
    """Return the contents of the readme file."""
    with open('README.rst') as handle:
        return handle.read()


def _get_version() -> str:
    """Return the stripped contents of the version file."""
    with open('VERSION') as handle:
        return handle.read().strip()


setup(
    name='tweet-phraseologist',
    version=_get_version(),
    description='Discover common phrases in tweets.',
    long_description=_get_long_description(),
    url='https://github.com/Ichimonji10/impedimenta',
    author='Jeremy Audet',
    author_email='jerebear@protonmail.com',
    license='GPLv3',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Education',
        ('License :: OSI Approved :: GNU General Public License v3 or later '
         '(GPLv3+)'),
        'Programming Language :: Python :: 3.7',
    ],
    packages=find_packages(),
    package_data={
        'tp': ['static/*'],
    },
    install_requires=['pyxdg'],
    extras_require={
        'dev': [
            # For `make lint`
            'flake8',
            'flake8-docstrings',
            'flake8-quotes',
            'pydocstyle',
            'pylint',
        ],
    },
    entry_points={
        'console_scripts': [
            'tp-analyze=tp.cli.tp_analyze:main',
            'tp-dataset=tp.cli.tp_dataset:main',
            'tp-db=tp.cli.tp_db:main',
            'tp-recommend=tp.cli.tp_recommend:main',
        ]
    },
)
