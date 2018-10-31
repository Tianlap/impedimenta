# coding=utf-8
"""Functions for calculating values with a database query."""
from movie_recommender import exceptions
from movie_recommender.db import common


def avg_movie_rating(movie):
    """Calculate the average of a movie's ratings.

    :param movie: A movie ID. The movie whose average rating is being computed.
    :return: A value such as 3.5.
    :raise movie_recommender.exceptions.NoMovieRatingsError: If an average
        can't be calculated due to a lack of ratings.
    """
    with common.get_db_conn() as conn:
        avg = conn.execute(
            """
            SELECT AVG(rating)
            FROM ratings
            WHERE movieId=?
            """,
            (movie,)
        ).fetchone()[0]
    if avg is None:
        raise exceptions.NoMovieRatingsError(
            f"Can't calculate the average rating for movie {movie}, as no "
            'ratings have been assigned to it.'
        )
    return avg


def avg_user_rating(user):
    """Calculate the average of a user's movie ratings.

    :param user: A user ID. The user whose average ratings are being computed.
    :return: A value such as 3.5.
    """
    with common.get_db_conn() as conn:
        return conn.execute(
            """
            SELECT AVG(rating)
            FROM ratings
            WHERE userId=?
            """,
            (user,)
        ).fetchone()[0]
