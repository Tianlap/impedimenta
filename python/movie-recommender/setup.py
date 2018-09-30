#!/usr/bin/env python3
# coding=utf-8
"""A setuptools-based script for installing Movie Recommender.

For more information, see:

* https://packaging.python.org/en/latest/index.html
* https://docs.python.org/distutils/sourcedist.html
"""
from setuptools import find_packages, setup  # prefer setuptools over distutils


def _get_long_description():
    """Return the contents of the readme file."""
    with open('README.rst') as handle:
        return handle.read()


def _get_version():
    """Return the stripped contents of the version file."""
    with open('VERSION') as handle:
        return handle.read().strip()


setup(
    name='movie-recommender',
    version=_get_version(),
    description='An application for generating movie recommendations.',
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
    install_requires=['pyxdg', 'requests'],
    extras_require={
        'dev': [
            # For `make docs-{clean,html}`
            'sphinx',
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
            'mr-analyze=movie_recommender.cli.mr_analyze:main',
            'mr-dataset=movie_recommender.cli.mr_dataset:main',
            'mr-db=movie_recommender.cli.mr_db:main',
            'mr-graph=movie_recommender.cli.mr_graph:main',
            'mr-predict=movie_recommender.cli.mr_predict:main',
            'mr-recommend=movie_recommender.cli.mr_recommend:main',
        ]
    },
    test_suite='tests',
)
