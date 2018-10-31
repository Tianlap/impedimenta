# coding=utf-8
"""Functions for counting rows in the database."""
from movie_recommender.db import common


def avg_ratings():
    """Count the number of entries in the "avgRatings" table.

    :return: An integer.
    """
    with common.get_db_conn() as conn:
        return conn.execute(
            'SELECT COUNT(DISTINCT userId) FROM avgRatings'
        ).fetchone()[0]


def rating_pairs(movie_a, movie_b):
    """Count the number of rating pairs for the given movies.

    See :meth:`movie_recommender.db.read.rating_pairs`.

    :param movie_a: A movie ID.
    :param movie_b: A movie ID.
    :return: An integer. The number of movie rating pairs for the given movies.
    """
    if movie_a == movie_b:
        raise ValueError(
            f"""
            Fetching pairs of ratings for a movie and itself is disallowed.
            Movie IDs: {movie_a}, {movie_b}
            """
        )
    movies = [movie_a, movie_b]
    movies.sort()
    with common.get_db_conn() as conn:
        row = conn.execute(
            """
            SELECT COUNT (*)
            FROM (
                SELECT userId, rating
                FROM ratings
                WHERE movieId = ?
            ) movieARatings
            INNER JOIN (
                SELECT userId, rating
                FROM ratings
                WHERE movieId = ?
            ) movieBRatings
            WHERE movieARatings.userId = movieBRatings.userId
            """,
            movies,
        ).fetchone()
    return row[0]


def unrated_movies(user_id):
    """Count the number of movies the given user hasn't rated.

    :param user_id: A user ID.
    :return: An integer.
    """
    with common.get_db_conn() as conn:
        return conn.execute(
            """
            SELECT COUNT(DISTINCT movieId) FROM movies WHERE movieId NOT IN
            (SELECT DISTINCT movieId FROM ratings WHERE userId=?)
            """,
            (user_id,)
        ).fetchone()[0]


def user_ids():
    """Count the number of users in the current dataset.

    :return: An integer.
    """
    with common.get_db_conn() as conn:
        return conn.execute(
            'SELECT COUNT(DISTINCT userId) FROM ratings'
        ).fetchone()[0]
