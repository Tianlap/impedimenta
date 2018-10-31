# coding=utf-8
"""Tools for predicting movie ratings with the machine learning algorithm."""
import functools

from movie_recommender import exceptions
from movie_recommender.constants import GENRES
from movie_recommender.graph import Graph, Point
from movie_recommender.db import common, read


def clamp_rating(rating):
    """Clamp the given movie rating to the range [0.5, 5].

    :param rating: A movie rating.
    :return: The given movie rating, but clamped.
    """
    return max(0.5, min(5, rating))


def make_predictor(user_id, predictor_name):
    """Make a univariate predictor for the given user.

    :param user_id: A user ID. The user for which a predictor is being created.
    :param predictor_name: The type of predictor to create. Defines whether the
        predictor will use year, comedy genre, horror genre, etc when making
        predictions.
    :return: A predictor. A function which accepts a movie ID and returns a
        rating.
    """
    predictor_factory = get_predictor_factory(predictor_name)
    return predictor_factory(user_id)


def get_predictor_factory(predictor_name):
    """Find the appropriate predictor factory function.

    :param predictor_name: The desired type of predictor. For example, "year"
        or "genre:Animation."
    :return: A predictor factor function, such as
        :func:`movie_recommender.predict.ml.make_year_predictor`. A predictor
        factory function is one which accepts a ``user_id`` argument and
        returns a predictor function customized for that user.
    :raise movie_recommender.exceptions.NoSuchPredictorError: If the requested
        type of predictor is not yet implemented.
    """
    predictor_factories = {'year': make_year_predictor}
    for genre in GENRES:
        predictor_factories[f'genre:{genre}'] = (
            functools.partial(make_genre_predictor, genre)
        )
    try:
        return predictor_factories[predictor_name]
    except KeyError:
        raise exceptions.NoSuchPredictorError(
            f'A predictor for {predictor_name} is not (yet) implemented.'
        )


def make_year_predictor(user_id, forbidden_movie=None):
    """Make a year-based predictor for the given user.

    If year information can't be extracted from a movie's title, then that
    movie is skipped when generating a predictor. This is done because so few
    movies have this issue. See:
    `class:`movie_recommender.exceptions.NoMovieYearError`.

    :param user_id: A user ID. The user for which a predictor is being created.
    :param forbidden_movie: A movie ID. A movie to ignore when creating the
        predictor.
    :return: A function which accepts a movie ID and returns a predicted
        rating.
    """
    query = """
            SELECT movies.title, ratings.rating
            FROM movies JOIN ratings USING (movieId)
            WHERE ratings.userId == ?
            """
    params = [user_id]
    if forbidden_movie:
        query += 'AND movieId != ?'
        params.append(forbidden_movie)

    # Iterate through movies this user has rated. For each movie, create a
    # Cartesian point, where X is the movie's year, and Y is the rating this
    # user has given to this movie.
    points = []
    with common.get_db_conn() as conn:
        for row in conn.execute(query, params):
            try:
                year = read.year(row[0])
            except exceptions.NoMovieYearError:
                continue
            rating = row[1]
            points.append(Point(year, rating))
    graph = Graph(points)

    def predictor(movie_id):
        """Predict a user's rating for the given movie.

        :param movie_id: A movie ID.
        :return: A predicted rating for the given movie.
        :raise movie_recommender.exceptions.NoMovieYearError: If the given
            movie's title doesn't include a year, and this predictor makes use
            of year data.
        :raise movie_recommender.exceptions.EmptyGraphError: If this predictor
            can't predict movie ratings at all, due to a lack of relevant data.
            For example, this will occur if the given movie's title does
            include a year, but all of the movies this user has rated lack a
            year.
        """
        title = read.title(movie_id)
        year = read.year(title)
        try:
            rating = graph.predict_y(year)
        except exceptions.VerticalLineOfBestFitGraphError:
            rating = graph.avg_point.y
        return clamp_rating(rating)

    return predictor


def make_genre_predictor(genre, user_id, forbidden_movie=None):
    """Make a predictor for the given genre for the given user.

    :param genre: A genre name, as a string.
    :param user_id: A user ID. The user for which a predictor is being created.
    :param forbidden_movie: A movie ID. A movie to ignore when creating the
        predictor.
    :return: A function which accepts a movie ID and returns a predicted
        rating.
    """
    query = """
            SELECT movies.genres, ratings.rating
            FROM movies JOIN ratings USING (movieId)
            WHERE ratings.userId == ?
            """
    params = [user_id]
    if forbidden_movie:
        query += 'AND movieId != ?'
        params.append(forbidden_movie)

    # Iterate through movies this user has rated. For each movie, create a
    # Cartesian point, where X is whether the move has the given genre, and Y
    # is the rating this user has given to this movie.
    points = []
    with common.get_db_conn() as conn:
        for row in conn.execute(query, params):
            genres = row[0].split('|')
            genre_present = 1 if genre in genres else 0
            rating = row[1]
            points.append(Point(genre_present, rating))
    graph = Graph(points)

    def predictor(movie_id):
        """Predict a user's rating for the given movie.

        :param movie_id: A movie ID.
        :return: A predicted rating for the given movie.
        """
        genres = read.genres(movie_id)
        genre_present = 1 if genre in genres else 0
        try:
            rating = graph.predict_y(genre_present)
        except exceptions.VerticalLineOfBestFitGraphError:
            rating = graph.avg_point.y
        return clamp_rating(rating)

    return predictor
