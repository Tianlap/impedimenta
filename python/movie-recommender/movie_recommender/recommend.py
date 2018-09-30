# coding=utf-8
"""Tools for generating top-n recommendations for users."""
import heapq
from collections import namedtuple

from movie_recommender import db, exceptions


Recommendation = namedtuple('Recommendation', (
    'movie_name',
    'pred_rating',
))
"""A movie recommendation."""

Candidate = namedtuple('Candidate', ('pred_rating', 'movie_id'))
"""A possible movie recommendation.

The predicted rating is the first field so that instances may be stored in a
heap queue. See the `heapq`_ documentation for details.

.. _heapq: https://docs.python.org/3.7/library/heapq.html
"""


def recommend(user_id, count, predictor):
    """Recommend movies to the given user.

    :param user_id: A user ID. The user for which recommendations are being
        generated.
    :param count: The number of recommendations to return.
    :param predictor: A predictor function for the given user.
    """
    movie_ids = db.get_unrated_movies(user_id)

    # Predict a rating for each movie, and track the highest-rated ones.
    candidates = []
    for movie_id in movie_ids:
        try:
            candidate = Candidate(predictor(movie_id), movie_id)
        except exceptions.NoMovieYearError:
            continue
        if len(candidates) >= count:
            heapq.heappushpop(candidates, candidate)
        else:
            heapq.heappush(candidates, candidate)

    # Munge and return the best candidates.
    return tuple(
        Recommendation(db.get_title(candidate.movie_id), candidate.pred_rating)
        for candidate in heapq.nlargest(5, candidates)
    )
