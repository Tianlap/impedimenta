# coding=utf-8
"""Utilities for the CLI interfaces."""
from movie_recommender import db


def to_movie_id(arg):
    """Cast the given string argument to a movvie ID, if possible.

    An exception of some kind is raised if ``arg`` can't be cast to a movie ID.
    The specific type of exception varies.

    :param arg: A string argument passed on the command line. Semantically, a
        movie ID.
    :return: A movie ID.
    """
    movie_id = int(arg)
    with db.get_db_conn(db.get_save_path()) as conn:
        movie_ids = tuple(
            row[0] for row in conn.execute(
                'SELECT DISTINCT movieId FROM movies WHERE movieId=?',
                (movie_id,)
            )
        )
    if movie_id not in movie_ids:
        raise ValueError(
            f'Movie ID {movie_id} not in database.'
        )
    return movie_id


def to_user_id(arg):
    """Cast the given string argument to a user ID, if possible.

    An exception of some kind is raised if ``arg`` can't be cast to a user ID.
    The specific type of exception varies.

    :param arg: A string argument passed on the command line. Semantically, a
        user ID.
    :return: A user ID.
    """
    user_id = int(arg)
    with db.get_db_conn(db.get_save_path()) as conn:
        user_ids = tuple(
            row[0] for row in conn.execute(
                'SELECT DISTINCT userId FROM ratings WHERE userId=?',
                (user_id,)
            )
        )
    if user_id not in user_ids:
        raise ValueError(
            f'User ID {user_id} not in database.'
        )
    return user_id
