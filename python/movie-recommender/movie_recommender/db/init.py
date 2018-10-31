# coding=utf-8
"""Functions for initializing the database."""
from pathlib import Path

from movie_recommender import datasets, exceptions
from movie_recommender.db import common


def cpop_db(dataset):
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
    save_path = Path(common.get_save_path())
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
    with common.get_db_conn(save_path) as conn:
        cpop_links_table(
            conn,
            Path(installed_datasets[dataset], 'links.csv'),
        )
        cpop_movies_table(
            conn,
            Path(installed_datasets[dataset], 'movies.csv'),
        )
        cpop_ratings_table(
            conn,
            Path(installed_datasets[dataset], 'ratings.csv'),
        )
        cpop_tags_table(
            conn,
            Path(installed_datasets[dataset], 'tags.csv'),
        )
        c_predictors_table(conn)
        c_similarities_table(conn)
        c_avg_ratings_table(conn)


def cpop_links_table(connection, csv_path):
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
                common.parse_csv(
                    handle,
                    lambda fields: (int(fields[0]), fields[1], fields[2]),
                )
            )


def cpop_movies_table(connection, csv_path):
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
                common.parse_csv(
                    handle,
                    lambda fields: (int(fields[0]), fields[1], fields[2]),
                )
            )


def cpop_ratings_table(connection, csv_path):
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
                common.parse_csv(
                    handle,
                    lambda fields: (
                        int(fields[0]),
                        int(fields[1]),
                        float(fields[2]),
                        int(fields[3]),
                    )
                )
            )


def cpop_tags_table(connection, csv_path):
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
                common.parse_csv(
                    handle,
                    lambda fields: (
                        int(fields[0]),
                        int(fields[1]),
                        fields[2],
                        int(fields[3]),
                    )
                )
            )


def c_avg_ratings_table(connection):
    """Create the "avgRatings" table.

    :param connection: A sqlite3 `Connection`_ object.
    :return: Nothing.

    .. _Connection:
        https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection
    """
    with connection:
        connection.execute(
            """
            CREATE TABLE avgRatings (
                userId INTEGER PRIMARY KEY,
                avgRating REAL
            )
            """
        )


def c_predictors_table(connection):
    """Create the "predictors" table.

    :param connection: A sqlite3 `Connection`_ object.
    :return: Nothing.

    .. _Connection:
        https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection
    """
    with connection:
        connection.execute(
            """
            CREATE TABLE predictors (
                userId integer primary key,
                predictor text
            )
            """
        )


def c_similarities_table(connection):
    """Create the "similarities" table.

    This table is logically an m×m table, where "m" is the number of movies.
    This table tells how similar pairs of movies are. For example, if movies 0
    and 1 are perfectly similar, then cells 0,1 and 1,0 will hold the value 1.
    If they're perfectly dissimilar, then the cells will hold the value -1. And
    if they're unrelated, then the cells will hold the value 0.

    Movie relationships are symmetric. Cells 0,1 and 1,0 hold identical values.
    The same is true for every movie pair. The relationship between movie 5 and
    8 is described by 5,8 and 8,5, and the two cells have identical values. In
    addition, each movie is perfectly related to itself. Cells 0,0, 1,1, 2,2,
    and so on all contain the value 1.

    In practice, this symmetric table design is problematic:

    1. The diagonal (0,0, 1,1, 2,2, etc) consists of ones, and these values
       aren't used by the model-based recommendation algorithm. Storing these
       values is a waste of space.
    2. Of the remaining cells, half are duplicates. If cells 0,1 and 1,0 store
       identical values, why bother having two cells?
    3. It's difficult to work with tables where the number of columns isn't
       known until runtime. Even worse is the case where the number of columns
       changes *at* runtime.

    This "similarities" table is logically one half of the m×m table. Values
    0,1, 0,2, 1,2, and so on are stored. Values 1,0, 2,0, 2,1, and so on aren't
    stored. Neither are 0,0, 1,1, 2,2, and so on.

    :param connection: A sqlite3 `Connection`_ object.
    :return: Nothing.

    .. _Connection:
        https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection
    """
    with connection:
        connection.execute(
            """
            CREATE TABLE similarities (
                movieAId INTEGER,
                movieBId INTEGER CHECK(movieAId < movieBId),
                similarity REAL,
                PRIMARY KEY (movieAId, movieBId)
            )
            """
        )
