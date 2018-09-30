# coding=utf-8
"""Custom exeptions for :mod:`movie_recommender`."""


class DatabaseAlreadyExistsError(Exception):
    """Indicates that a database already exists when it shouldn't.

    For example, this might be raised if this application is asked to create a
    new database and one already exists.
    """


class DatabaseNotFoundError(Exception):
    """Indicates that no database can be found."""


class DatasetAbsentError(Exception):
    """Indicates that a requested data set is absent.

    "Absent" means one of the following:

    * A dataset isn't downloaded.
    * A dataset isn't installed.
    """


class EmptyGraphError(Exception):
    """Indicates that a graph is empty."""


class NoMovieYearError(Exception):
    r"""Indicates that a movie doesn't have a release year.

    See for yourself:

    .. code-block:: bash

        grep -Pv '\(\d{4}\)' …/movies.csv | wc -l  # 14

    """


class NoSuchPredictorError(Exception):
    """Indicates that the requested type of predictor isn't (yet) implemented.

    A predictor is a function of the form ``predict(userId, movieId) →
    rating``.
    """


class NoPersonalizedPredictorError(Exception):
    """Indicates that the named user doesn't have a personalized predictor."""


class VerticalLineOfBestFitGraphError(Exception):
    """Indicates that a graph's line of best fit is vertical."""
