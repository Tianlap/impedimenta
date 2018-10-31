# coding=utf-8
"""Functions for inserting rows into the database.

Some of the functions in this modules use UPSERT-style statements. SQLite added
support for `UPSERT`_ in version 3.24.0, which was released on 2018-06-24.

.. _UPSERT: https://www.sqlite.org/lang_UPSERT.html
"""
from movie_recommender.db import common


def avg_ratings(avg_ratings_):
    """Write user average ratings to the database.

    :param avg_ratings_: An iterable of
        :class:`movie_recommender.db.common.AvgRating` objects.
    """
    with common.get_db_conn() as conn:
        with conn:
            values = (
                avg_rating + (avg_rating.avg_rating,)
                for avg_rating in avg_ratings_
            )
            conn.executemany(
                """
                INSERT INTO avgRatings VALUES (?, ?)
                ON CONFLICT (userId) DO UPDATE SET avgRating=?
                """,
                values,
            )


def similarities(similarities_):
    """Write movies similarity scores to the database.

    :param similarities_: An iterable of
        :class:`movie_recommender.db.common.Similarity` objects.
    """
    # SQLite added support for UPSERT in version 3.24.0, which was released on
    # 2018-06-24. See: https://www.sqlite.org/lang_UPSERT.html
    with common.get_db_conn() as conn:
        with conn:
            conn.executemany(
                """
                INSERT INTO similarities VALUES (?, ?, ?)
                ON CONFLICT (movieAId, movieBId) DO UPDATE SET similarity=?
                """,
                _similarities_values(similarities_),
            )


def _similarities_values(similarities_):
    """Yield values for ``similarities`` insert statement."""
    for similarity in similarities_:
        row_vars = [similarity.movie_a, similarity.movie_b]
        row_vars.sort()
        row_vars.append(similarity.score)
        row_vars.append(similarity.score)
        yield row_vars
