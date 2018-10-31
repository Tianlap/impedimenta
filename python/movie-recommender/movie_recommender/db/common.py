# coding=utf-8
"""Objects used by the other database management modules."""
import contextlib
import csv
import sqlite3
from collections import namedtuple
from pathlib import Path

from xdg import BaseDirectory

from movie_recommender import exceptions
from movie_recommender.constants import DB_NAME, XDG_RESOURCE


AvgRating = namedtuple('AvgRating', ('user_id', 'avg_rating'))
"""The average of a user's movie ratings."""


RatingPair = namedtuple('RatingPair', ('user_id', 'rating_a', 'rating_b'))
"""A pair of ratings that a user has given to a pair of movies."""


Similarity = namedtuple('Similarity', ('movie_a', 'movie_b', 'score'))
"""A pair of movies and their similarity score."""


@contextlib.contextmanager
def get_db_conn(db_path=None):
    """Return a context manager which yields a database connection.

    :param db_path: The path to a SQLite 3 database.
    :return: A sqlite3 `Connection`_ object. It will automatically be closed
        when this context manager exits.

    .. _Connection:
        https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection
    """
    if db_path is None:
        db_path = get_load_path()
    conn = sqlite3.connect(db_path)
    try:
        yield conn
    finally:
        conn.close()


def get_load_path():
    """Return the path to Movie Recommender's database.

    :return: The path to the database, if it is found.
    :raises movie_recommender.exceptions.DatabaseNotFoundError: If no database
        is found.
    """
    for db_dir in BaseDirectory.load_data_paths(XDG_RESOURCE):
        db_path = Path(db_dir, DB_NAME)
        if db_path.exists():
            return str(db_path)
    raise exceptions.DatabaseNotFoundError(
        'Movie Recommender is unable to find a database. A database should be '
        'present at one of the following paths: ' + ', '.join((
            str(Path(db_dir, XDG_RESOURCE, DB_NAME))
            for db_dir in BaseDirectory.xdg_config_dirs
        ))
    )


def get_save_path():
    """Return a path to where a database may be created.

    Create directories as needed.
    """
    return str(Path(BaseDirectory.save_data_path(XDG_RESOURCE), DB_NAME))


def parse_csv(handle, caster=lambda fields: fields, header_rows=1):
    """Read a CSV file and yield a parsed tuple per consumed row.

    :param handle: The handle to an input stream.
    :param caster: A callback which accepts a tuple of strings, and returns a
        tuple of munged strings. For example:

        .. code-block:: python

            def caster(fields):
                return (int(fields[0]), fields[1], fields[2])

        The default returns input as-is.
    :param header_rows: The number of header rows in the input file. Header
        rows are ignored.
    :return: A generator yielding tuples of strings, where each tuple of
        strings represents a row in the input file.
    """
    current_line = 0
    reader = csv.reader(handle)
    for row in reader:
        current_line += 1
        if current_line <= header_rows:
            continue
        yield caster(tuple(row))
