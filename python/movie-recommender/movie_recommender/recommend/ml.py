# coding=utf-8
"""Tools for generating top-n recommendations with machine learning."""
import heapq

from movie_recommender import exceptions
from movie_recommender.db import read
from movie_recommender.predict.common import Prediction


def recommend(user, count, predictor):
    """Yield recommended movies for the given user.

    :param user: A user ID. The user for which recommendations are being
        generated.
    :param count: The number of recommendations to return.
    :param predictor: A predictor function for the given user.
    :return: A generator that yields the top ``count`` recommendations.
    :rtype movie_recommender.recommend.Prediction:
    """
    # Predict a rating for each movie, and track the highest-rated ones.
    predictions = []
    for movie in read.unrated_movies(user):
        try:
            prediction = Prediction(predictor(movie), movie, None)
        except exceptions.NoMovieYearError:
            continue
        if len(predictions) >= count:
            heapq.heappushpop(predictions, prediction)
        else:
            heapq.heappush(predictions, prediction)
    for prediction in heapq.nlargest(count, predictions):
        yield prediction
