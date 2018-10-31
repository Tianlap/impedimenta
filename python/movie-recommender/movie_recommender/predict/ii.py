# coding=utf-8
"""Tools for predicting movie ratings with the item-item algorithm."""
import math

from movie_recommender import exceptions
from movie_recommender.constants import (
    AVG_RATING,
    MAX_RATING,
    MIN_RATING,
    SIMILAR,
)
from movie_recommender.db import calc, read
from movie_recommender.predict.common import Prediction


def predict_rating_for_predict(user, movie):
    """Predict the given user's rating for the given movie.

    Try the following, in order:

    1. Use :func:`movie_recommender.predict.ii.predict_rating` to predict a
       movie rating.
    2. Calculate the average rating for the given movie. This fallback is
       naive, as it doesn't account for the average of this user's ratings and
       the average for the users who rated the given movie.
    3. Calculate the average of the given user's ratings.

    Given the naive nature of this function, it is best suited for the use case
    of predicting a rating for a single movie.

    :param user: A user ID. The user for whom a predicted rating is generated.
    :param movie: An movie ID. The movie for which a predicted rating is
        generated.
    :return: A predicted rating.
    :rtype movie_recommender.predict.common.Prediction:
    """
    try:
        pred_rating = predict_rating(user, movie)
        reason = SIMILAR
    except exceptions.NoSimilarMoviesError:
        try:
            pred_rating = calc.avg_movie_rating(movie)
            reason = AVG_RATING
        except exceptions.NoMovieRatingsError:
            pred_rating = read.avg_rating(user)
            reason = None
    return Prediction(pred_rating, movie, reason)


def predict_rating_for_recommend(user, movie):
    """Predict the given user's rating for the given movie.

    Try the following, in order:

    1. Use :func:`movie_recommender.predict.ii.predict_rating` to predict a
       movie rating.
    2. Assume a rating of :data:`movie_recommender.constants.MIN_RATING`.

    Given the strict nature of this function, it's best suited for the use case
    of recommending several movies.

    :param user: A user ID. The user for whom a predicted rating is generated.
    :param movie: An movie ID. The movie for which a predicted rating is
        generated.
    :return: A predicted rating.
    :rtype movie_recommender.predict.common.Prediction:
    """
    try:
        pred_rating = predict_rating(user, movie)
        reason = SIMILAR
    except exceptions.NoSimilarMoviesError:
        pred_rating = MIN_RATING
        reason = None
    return Prediction(pred_rating, movie, reason)


def predict_rating(user, movie):
    """Predict the given user's rating for the given movie.

    Use the weighted sum algorithm to predict what rating the given user will
    assign to the given movie. For more on the algorithm, see: "Item-Based
    Collaborative Filtering Recommendation Algorithms," by Sarwar et al. Or,
    for a friendlier introduction, try Head First Data Analysis.

    :param user: A user ID. The user for whom a predicted rating is generated.
    :param movie: An movie ID. The movie for which a predicted rating is
        generated.
    :return: A predicted movie rating, ranging from
        :data:`movie_recommender.constants.MIN_RATING` to
        :data:`movie_recommender.constants.MAX_RATING`.
    :raise movie_recommender.exceptions.NoSimilarMoviesError: If there aren't
        any movies similar to the given movie that the user has seen. (In other
        words, if the algorithm fails to run.)
    """
    numerator = 0
    denominator = 0
    for (similar_movie, similarity) in read.similar_movies_for_user(movie, user):
        numerator += similarity * normalize_rating(
            read.rating(user, similar_movie)
        )
        denominator += math.fabs(similarity)
    try:
        normalized_rating = numerator / denominator
    except ZeroDivisionError as err:
        raise exceptions.NoSimilarMoviesError(
            f"Can't predict a rating for movie {movie}, as there are no "
            'similar movies. Try getting more pairs of ratings for both movie '
            f'{movie} and other movies.'
        ) from err
    return denormalize_rating(normalized_rating)


def normalize_rating(denormalized_rating):
    """Normalize a movie rating.

    :param denormalized_rating: A movie rating in the range 0.5 to 5,
        inclusive.
    :return: A movie rating in the range -1 to 1, inclusive.
    """
    numerator = 2 * (denormalized_rating - MIN_RATING) - (MAX_RATING - MIN_RATING)
    denominator = MAX_RATING - MIN_RATING
    return numerator / denominator


def denormalize_rating(normalized_rating):
    """Denormalize a movie rating.

    :param normalized_rating: A movie rating in the range -1 to 1, inclusive.
    :return: A movie rating in the range 0.5 to 5, inclusive.
    """
    return ((normalized_rating + 1) * (MAX_RATING - MIN_RATING)) / 2 + MIN_RATING
