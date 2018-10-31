# coding=utf-8
"""Functions for reading rows from the database."""
from movie_recommender import exceptions
from movie_recommender.constants import YEAR_MATCHER
from movie_recommender.db import common


def all_movies():
    """Yield the IDs of every movie.

    :return: A generator that yields movie IDs.
    """
    with common.get_db_conn() as conn:
        for row in conn.execute('SELECT DISTINCT movieId FROM movies'):
            yield row[0]


def avg_rating(user_id):
    """Get the average of a user's ratings, from the avgRatings table.

    :param user_id: A user ID. The user whose average rating is being fetched.
    :return: An average rating, such as 3.5.
    """
    with common.get_db_conn() as conn:
        row = conn.execute(
            """
            SELECT avgRating FROM avgRatings WHERE userId=?
            """,
            (user_id,),
        ).fetchone()
    if not row:
        raise exceptions.MissingAverageRatingError(
            f'No average rating for user {user_id} has been calculated.'
        )
    return row[0]


def genres(movie_id):
    """Get the genres of the given movie.

    :param movie_id: A movie ID.
    :return: An iterable of genres, as strings.
    """
    with common.get_db_conn() as conn:
        genres_strings = tuple(
            row[0] for row in conn.execute(
                'SELECT genres FROM movies WHERE movieId=?',
                (movie_id,)
            )
        )
    assert len(genres_strings) == 1
    return genres_strings[0].split('|')


def predictor_name(user_id):
    """Get the personalized predictor name for the given user.

    :param user_id: A user ID. The user for which the personalized predictor
        name is being fetched.
    :return: The name of the personalized predictor for the given user.
    :raise movie_recommender.exceptions.NoPersonalizedPredictorError: If the
        given user doesn't have a personalized predictor.
    """
    with common.get_db_conn() as conn:
        row = conn.execute(
            'SELECT predictor FROM predictors WHERE userId=?',
            (user_id,)
        ).fetchone()
    if not row:
        raise exceptions.NoPersonalizedPredictorError(
            f'User {user_id} has no personalized predictors. Please generate '
            'one with "mr-analyze".',
        )
    return row[0]


def rated_movies(user_ids):
    """Get the IDs of the movies the given users have rated.

    :param user_ids: An iterable of user IDs.
    :return: A set of movie IDs.
    """
    with common.get_db_conn() as conn:
        return {
            row[0] for row in conn.execute(
                f"""
                SELECT DISTINCT movieId FROM ratings WHERE userId IN ({
                ', '.join('?' for _ in range(len(user_ids)))
                })
                """,
                tuple(user_ids),
            )
        }


def rating(user_id, movie_id):
    """Get the rating that the given user gave to the given movie.

    :param user_id: A user ID.
    :param movie_id: A movie ID.
    :return: A movie rating. (A float.)
    """
    with common.get_db_conn() as conn:
        ratings = tuple(
            row[0] for row in conn.execute(
                'SELECT rating FROM ratings WHERE userId=? and movieId=?',
                (user_id, movie_id)
            )
        )
    assert len(ratings) == 1
    return ratings[0]


def rating_pairs(movie_a, movie_b):
    """Yield pairs of ratings for the given movies.

    Logically, this function generates a table in the following form. Notice
    that the table is perfectly dense.

    ====  =======  =======
    User  Movie A  Movie B
    ====  =======  =======
    1     1.0      0.5
    26    4.0      1.5
    2     5.0      0.5
    ====  =======  =======

    :param movie_a: A movie ID. A movie to get ratings for.
    :param movie_b: A movie ID. A movie to get ratings for.
    :rtype movie_recommender.db.RatingPair:
    :return: A generator that yields every pair of ratings for the two given
        movies.
    :raise: ``ValueError`` if ``movie_a`` and ``movie_b`` are equal.
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
        for row in conn.execute(
                """
                SELECT
                    movieARatings.userId,
                    movieARatings.rating,
                    movieBRatings.rating
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
                movies):
            yield common.RatingPair(row[0], row[1], row[2])


def similar_movies_for_user(movie, user):
    """Yield movies similar to ``movie`` that ``user`` has rated.

    .. NOTE:: A "similar" movie is one with a non-zero similarity score. This
        includes negative similarity scores!

    :param movie: A movie ID.
    :param user: A user ID.
    :return: A generator yielding tuples of the form ``(movie_id,
        similarity)``.
    """
    rated_movies_ = rated_movies((user,))
    with common.get_db_conn() as conn:
        # There's probably some clever technique for expressing the following
        # queries as a single SQL query.
        for row in conn.execute(
                """
                SELECT movieAId, similarity
                FROM similarities
                WHERE movieBId = ? AND similarity != 0
                """,
                (movie,)):
            if row[0] in rated_movies_:
                yield row
        for row in conn.execute(
                """
                SELECT movieBId, similarity
                FROM similarities
                WHERE movieAId = ? AND similarity != 0
                """,
                (movie,)):
            if row[0] in rated_movies_:
                yield row


def similarity(movie_a, movie_b):
    """Return the similarity score for the two given movies.

    :param movie_a: A movie ID.
    :param movie_b: A movie ID.
    :return: The similarity score for the pair of movies.
    :raise movie_recommender.exceptions.MissingSimilarityError: If no
        similarity score has been computed for this pair of movies.
    """
    movies = [movie_a, movie_b]
    movies.sort()
    with common.get_db_conn() as conn:
        row = conn.execute(
            """
            SELECT similarity
            FROM similarities
            WHERE movieAId=? AND movieBId=?
            """,
            movies,
        ).fetchone()
    if not row:
        raise exceptions.MissingSimilarityError(
            f"""
            A similarity score hasn't been computed for movies {movies[0]} and
            {movies[1]}.
            """
        )
    return row[0]


def title(movie_id):
    """Get the title of the given movie.

    :param movie_id: A movie ID.
    :return: The title of the given movie.
    """
    with common.get_db_conn() as conn:
        row = conn.execute(
            'SELECT title FROM movies WHERE movieId=?',
            (movie_id,)
        ).fetchone()
    if not row:
        raise ValueError(f'Movie ID {movie_id} not in database.')
    return row[0]


def users():
    """Get the ID of every user.

    :return: A tuple of user IDs.
    """
    with common.get_db_conn() as conn:
        return {
            row[0]
            for row in conn.execute('SELECT DISTINCT userId FROM ratings')
        }


def users_in_avg_ratings():
    """Get the ID of every user in the avgRatings table.

    :return: A tuple of user IDs.
    """
    with common.get_db_conn() as conn:
        return {
            row[0]
            for row in conn.execute('SELECT DISTINCT userId FROM avgRatings')
        }


def unrated_movies(user_id):
    """Yield the ID of each movie the given user hasn't rated.

    :param user_id: A user ID.
    :return: A generator that yields movie IDs.
    """
    with common.get_db_conn() as conn:
        for row in conn.execute(
                """
                SELECT DISTINCT movieId FROM movies WHERE movieId NOT IN
                (SELECT DISTINCT movieId FROM ratings WHERE userId=?)
                """,
                (user_id,)):
            yield row[0]


def year(movie_title):
    """Extract the year from the given movie title.

    :param movie_title: A movie title.
    :return: The release year of the given movie.
    :raise movie_recommender.exceptions.NoMovieYearError: If the given movie
        doesn't have a release year.
    """
    match = YEAR_MATCHER.search(movie_title)
    if not match:
        raise exceptions.NoMovieYearError(
            f"Can't find year in movie title: {movie_title}"
        )
    return int(match.group(1))
