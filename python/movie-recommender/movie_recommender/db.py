# coding=utf-8
"""Tools for workingwith Movie Recommender's database."""
import contextlib
import csv
import re
import sqlite3
from pathlib import Path

from xdg import BaseDirectory

from movie_recommender import datasets, exceptions
from movie_recommender.constants import XDG_RESOURCE

_DB_NAME = 'db.db'
"""The basename of Movie Recommender's database file."""

_YEAR_MATCHER = re.compile(r'\((\d{4})\)')
"""A compiled regular expression for finding the year in a movie title.

Also see :class:`movie_recommender.exceptions.NoMovieYearError`.
"""


def create_populate_db(dataset):
    """Create and populate a new database.

    More specifically:

    * Create database tables for the datasets.
    * Create database tables for calculated data. (i.e. Create a table which
      maps userId → predictorName.)
    * Populate the dataset tables.

    :param dataset: The dataset to populate the new database with. Use one of
        the keys from :data:`movie_recommender.constants.DATASETS`.
    :return: Nothing
    :raises DatabaseAlreadyExistsError: If the target database already exists.
    :raises DatasetAbsentError: If the referenced dataset isn't installed.
    """
    # Check whether a conflicting database exists.
    save_path = Path(get_save_path())
    if save_path.exists():
        raise exceptions.DatasetAbsentError(
            "Can't create a new database, as a file already exists at: {}"
            .format(save_path),
        )

    # Check whether the dataset is installed or not.
    installed_datasets = datasets.get_installed_datasets()
    if dataset not in installed_datasets:
        raise exceptions.DatabaseAlreadyExistsError(
            "Can't create a database from the {} dataset, as it isn't "
            'installed.'.format(dataset)
        )

    # Create and populate a new database.
    with get_db_conn(get_save_path()) as conn:
        _cpop_links_table(
            conn,
            Path(installed_datasets[dataset], 'links.csv'),
        )
        _cpop_movies_table(
            conn,
            Path(installed_datasets[dataset], 'movies.csv'),
        )
        _cpop_ratings_table(
            conn,
            Path(installed_datasets[dataset], 'ratings.csv'),
        )
        _cpop_tags_table(
            conn,
            Path(installed_datasets[dataset], 'tags.csv'),
        )
        _create_predictors_table(conn)


@contextlib.contextmanager
def get_db_conn(db_path):
    """Return a context manager which yields a database connection.

    :param db_path: The path to a SQLite 3 database.
    :return: A sqlite3 `Connection`_ object. It will automatically be closed
        when this context manager exits.

    .. _Connection:
        https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection
    """
    conn = sqlite3.connect(db_path)
    try:
        yield conn
    finally:
        conn.close()


def get_genres(movie_id):
    """Get the genres of the given movie.

    :param movie_id: A movie ID.
    :return: An iterable of genres, as strings.
    """
    with get_db_conn(get_load_path()) as conn:
        genres_strings = tuple(
            row[0] for row in conn.execute(
                'SELECT genres FROM movies WHERE movieId=?',
                (movie_id,)
            )
        )
    assert len(genres_strings) == 1
    return genres_strings[0].split('|')


def get_load_path():
    """Return the path to Movie Recommender's database.

    :return: The path to the database, if it is found.
    :raises movie_recommender.exceptions.DatabaseNotFoundError: If no database
        is found.
    """
    for db_dir in BaseDirectory.load_data_paths(XDG_RESOURCE):
        db_path = Path(db_dir, _DB_NAME)
        if db_path.exists():
            return str(db_path)
    raise exceptions.DatabaseNotFoundError(
        'Movie Recommender is unable to find a database. A database should be '
        'present at one of the following paths: ' + ', '.join((
            Path(db_dir, XDG_RESOURCE, _DB_NAME)
            for db_dir in BaseDirectory.xdg_config_dirs
        ))
    )


def get_rated_movies(user_id):
    """Get movies the given user has rated.

    :param user_id: A user ID.
    :return: A set of movie IDs.
    """
    with get_db_conn(get_load_path()) as conn:
        return {
            row[0] for row in conn.execute(
                'SELECT movieId FROM ratings WHERE userId=?',
                (user_id,)
            )
        }


def get_predictor_name(user_id):
    """Get the personalized predictor name for the given user.

    :param user_id: A user ID. The user for which the personalized predictor
        name is being fetched.
    :return: The name of the personalized predictor for the given user.
    :raise movie_recommender.exceptions.NoPersonalizedPredictorError: If the
        given user doesn't have a personalized predictor.
    """
    with get_db_conn(get_load_path()) as conn:
        predictor_names = tuple(
            row[0] for row in conn.execute(
                'SELECT predictor FROM predictors WHERE userId=?',
                (user_id,)
            )
        )
    if not predictor_names:
        raise exceptions.NoPersonalizedPredictorError(
            f'User {user_id} has no personalized predictors. Please generate '
            'one with "mr-analyze".',
        )
    assert len(predictor_names) == 1
    return predictor_names[0]


def get_rating(user_id, movie_id):
    """Get the rating that the given user gave to the given movie.

    :param user_id: A user ID.
    :param movie_id: A movie ID.
    :return: A movie rating. (A float.)
    """
    with get_db_conn(get_load_path()) as conn:
        ratings = tuple(
            row[0] for row in conn.execute(
                'SELECT rating FROM ratings WHERE userId=? and movieId=?',
                (user_id, movie_id)
            )
        )
    assert len(ratings) == 1
    return ratings[0]


def get_save_path():
    """Return a path to where a database may be created.

    Create directories as needed.
    """
    return str(Path(BaseDirectory.save_data_path(XDG_RESOURCE), _DB_NAME))


def get_title(movie_id):
    """Get the title of the given movie.

    :param movie_id: A movie ID.
    :return: The title of the given movie.
    """
    with get_db_conn(get_load_path()) as conn:
        titles = tuple(
            row[0] for row in conn.execute(
                'SELECT title FROM movies WHERE movieId=?',
                (movie_id,)
            )
        )
    assert len(titles) == 1
    return titles[0]


def get_user_ids():
    """Get all user IDs.

    :return: A tuple of user IDs.
    """
    with get_db_conn(get_load_path()) as conn:
        return tuple(
            row[0]
            for row in conn.execute('SELECT DISTINCT userId FROM ratings')
        )


def get_year(movie_title):
    """Extract the year from the given movie title.

    :param movie_title: A movie title.
    :return: The release year of the given movie.
    :raise movie_recommender.exceptions.NoMovieYearError: If the given movie
        doesn't have a release year.
    """
    match = _YEAR_MATCHER.search(movie_title)
    if not match:
        raise exceptions.NoMovieYearError(
            f"Can't find year in movie title: {movie_title}"
        )
    return int(match.group(1))


def get_unrated_movies(user_id):
    """Get movies a user hasn't rated.

    :param user_id: A user ID.
    :return: A tuple of unique movie IDs.
    """
    with get_db_conn(get_load_path()) as conn:
        all_movie_ids = set(
            row[0] for row in conn.execute(
                'SELECT DISTINCT movies.movieId FROM movies'
            )
        )
    rated_movie_ids = get_rated_movies(user_id)
    return tuple(all_movie_ids - rated_movie_ids)


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


def _cpop_links_table(connection, csv_path):
    """Create and populate the "links" table.

    :param connection: A sqlite3 `Connection`_ object.
    :param csv_path: The path to a ``links.csv`` file.
    :return: Nothing.

    .. _Connection:
        https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection
    """
    with open(csv_path) as handle:
        with connection:
            connection.execute("""\
                CREATE TABLE links (
                    movieId integer primary key,
                    imdbId text,
                    tmdbId text
                )
            """)
        with connection:
            connection.executemany(
                'INSERT INTO links VALUES (?, ?, ?)',
                parse_csv(
                    handle,
                    lambda fields: (int(fields[0]), fields[1], fields[2]),
                )
            )


def _cpop_movies_table(connection, csv_path):
    """Create and populate the "movies" table.

    :param connection: A sqlite3 `Connection`_ object.
    :param csv_path: The path to a ``movies.csv`` file.
    :return: Nothing.

    .. _Connection:
        https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection
    """
    with open(csv_path) as handle:
        with connection:
            connection.execute("""\
                CREATE TABLE movies (
                    movieId integer primary key,
                    title text,
                    genres text
                )
            """)
        with connection:
            connection.executemany(
                'INSERT INTO movies VALUES (?, ?, ?)',
                parse_csv(
                    handle,
                    lambda fields: (int(fields[0]), fields[1], fields[2]),
                )
            )


def _cpop_ratings_table(connection, csv_path):
    """Create and populate the "ratings" table.

    :param connection: A sqlite3 `Connection`_ object.
    :param csv_path: The path to a ``ratings.csv`` file.
    :return: Nothing.

    .. _Connection:
        https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection
    """
    with open(csv_path) as handle:
        with connection:
            connection.execute("""\
                CREATE TABLE ratings (
                    userId integer,
                    movieId integer,
                    rating real,
                    timestamp integer,
                    PRIMARY KEY (userId, movieId)
                )
            """)
        with connection:
            connection.executemany(
                'INSERT INTO ratings VALUES (?, ?, ?, ?)',
                parse_csv(
                    handle,
                    lambda fields: (
                        int(fields[0]),
                        int(fields[1]),
                        float(fields[2]),
                        int(fields[3]),
                    )
                )
            )


def _cpop_tags_table(connection, csv_path):
    """Create and populate the "tags" table.

    :param connection: A sqlite3 `Connection`_ object.
    :param csv_path: The path to a ``tags.csv`` file.
    :return: Nothing.

    .. _Connection:
        https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection
    """
    with open(csv_path) as handle:
        with connection:
            connection.execute("""\
                CREATE TABLE tags (
                    userId integer,
                    movieId integer,
                    tag text,
                    timestamp integer,
                    PRIMARY KEY (userId, movieId, tag)
                )
            """)
        with connection:
            connection.executemany(
                'INSERT INTO tags VALUES (?, ?, ?, ?)',
                parse_csv(
                    handle,
                    lambda fields: (
                        int(fields[0]),
                        int(fields[1]),
                        fields[2],
                        int(fields[3]),
                    )
                )
            )


def _create_predictors_table(connection):
    """Create the "predictors" table.

    :param connection: A sqlite3 `Connection`_ object.
    :return: Nothing.

    .. _Connection:
        https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection
    """
    with connection:
        connection.execute("""\
        CREATE TABLE predictors (
            userId integer primary key,
            predictor text
        )
        """)
