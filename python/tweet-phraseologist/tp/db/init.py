# coding=utf-8
"""Functions for initializing the database."""
import sqlite3
from pathlib import Path

from tp import datasets, exceptions
from tp.db import common


def cpop(dataset_name: str) -> None:
    """Create a new database, and populate it.

    :param dataset: The name of a dataset. A key from
        :func:`tp.datasets.installed`.
    :raise DatabaseAlreadyExistsError: If the target database already exists.
    :raise DatasetNotFoundError: If the referenced dataset isn't installed.
    """
    # Check whether a conflicting database exists.
    save_path: Path = common.get_save_path()
    if save_path.exists():
        raise exceptions.DatabaseAlreadyExistsError(
            "Can't create a new database, as a file already exists at: {}"
            .format(save_path),
        )

    # Check whether the dataset to install exists.
    installed_datasets = datasets.installed()
    if dataset_name not in installed_datasets:
        raise exceptions.DatasetNotFoundError(
            f"Can't populate database with dataset {dataset_name}, as it's not "
            'installed'
        )

    # Create and populate a new database.
    dataset_dir = installed_datasets[dataset_name]
    with common.get_db_conn(save_path) as conn:
        cpop_tweets_table(conn, Path(dataset_dir, 'ExtractedTweets.csv'))
        cpop_handles_table(conn, Path(dataset_dir, 'TwitterHandles.csv'))


def cpop_tweets_table(conn: sqlite3.Connection, csv_file: Path) -> None:
    """Create and populate the 'tweets' table.

    :param conn: A connection to the SQLite database.
    :param csv_file: A CSV file containing user account handles, where there is
        one header row, and where each subsequent row consists of ``(party,
        handle, tweet, ...)``.
    """
    with conn:
        conn.execute("""
            CREATE TABLE tweets (
                party TEXT,
                handle TEXT,
                tweet TEXT
            )
        """)

    with open(csv_file) as handle:
        with conn:
            conn.executemany(
                'INSERT INTO tweets VALUES (?, ?, ?)',
                common.parse_csv(handle),
            )


def cpop_handles_table(conn: sqlite3.Connection, csv_file: Path) -> None:
    """Create and populate the 'handles' table.

    :param conn: A connection to the SQLite database.
    :param csv_file: A CSV file containing user account handles, where there is
        one header row, and where each subsequent row consists of ``(party,
        name, handle, ...)``. Handles must be unique.
    """
    with conn:
        conn.execute("""
            CREATE TABLE handles (
                party TEXT,
                name TEXT,
                handle TEXT PRIMARY KEY
            )
        """)

    with open(csv_file) as handle:
        with conn:
            conn.executemany(
                'INSERT INTO handles VALUES (?, ?, ?)',
                common.parse_csv(handle, lambda row: row[:3]),
            )
