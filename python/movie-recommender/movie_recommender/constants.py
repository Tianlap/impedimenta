# coding=utf-8
"""Constants for use by the entire application."""

DATASETS = {
    'fixture': None,
    'ml-latest-small': (
        'http://files.grouplens.org/datasets/movielens/ml-latest-small.zip'
    ),
    'ml-20m': 'http://files.grouplens.org/datasets/movielens/ml-20m.zip',
}
"""Datasets this application can manage.

The "fixture" dataset can be created on the fly by this application.
"""

GENRES = {
    '(no genres listed)',
    'Action',
    'Adventure',
    'Animation',
    'Children\'s',
    'Comedy',
    'Crime',
    'Documentary',
    'Drama',
    'Fantasy',
    'Film-Noir',
    'Horror',
    'Musical',
    'Mystery',
    'Romance',
    'Sci-Fi',
    'Thriller',
    'War',
    'Western',
}
"""Movie genres, as listed in the MovieLens ml-latest-small readme.

This is primarily useful when generating genre-based predictors. An alternate
approach would be to dynamically extract genre names from the data sets
themselves, but hard-coding names is quicker, and it avoids issues that arise
when not all genres are represented by a dataset.
"""

XDG_RESOURCE = 'movie-recommender'
"""The basename of the directories this application uses for data.

For more information, see the `XDG Base Directory Specification
<https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html>`_.
"""
