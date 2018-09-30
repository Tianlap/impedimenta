# coding=utf-8
"""Sphinx documentation generator configuration file.

The full set of configuration options is listed on the Sphinx website:
http://sphinx-doc.org/config.html
"""
import os
import sys


# Add the Movie Recommender root directory to the system path. This allows
# references such as :mod:`movie_recommender.…` to be processed correctly.
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.path.pardir
))
sys.path.insert(0, ROOT_DIR)


def _get_version():
    """Return the stripped contents of the version file.

    We could parse this version string with packaging.version.Version if we
    wished to verify that the version string in the VERSION file was valid.
    (The act of generating documentation would serve as a unit test for the
    contents of the version file.)
    """
    with open(os.path.join(ROOT_DIR, 'VERSION')) as handle:
        return handle.read().strip()


# Project Information ---------------------------------------------------------
# pylint:disable=invalid-name
author = 'Jeremy Audet'
copyright = '2018, Jeremy Audet'  # pylint:disable=redefined-builtin
project = 'Movie Recommender'
version = release = _get_version()


# General Configuration -------------------------------------------------------
extensions = ['sphinx.ext.autodoc']
source_suffix = '.rst'
master_doc = 'index'
exclude_patterns = ['_build']
nitpicky = True
autodoc_default_flags = ['members']
# Format-Specific Options -----------------------------------------------------
htmlhelp_basename = 'MovieRecommenderdoc'
latex_documents = [(
    master_doc,
    project + '.tex',
    project + ' Documentation',
    author,
    'manual',
)]
man_pages = [(
    master_doc,
    'movie-recommender',
    project + ' Documentation',
    [author],
    1,  # man pages section
)]
texinfo_documents = [(
    master_doc,
    'MovieRecommender',
    project + ' Documentation',
    author,
    'MovieRecommender',
    ('Movie Recommender is an application for generating movie '
     'recommendations.'),
    'Miscellaneous'
)]
