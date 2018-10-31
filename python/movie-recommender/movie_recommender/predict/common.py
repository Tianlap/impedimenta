# coding=utf-8
"""Objects used by the other modules in this package."""
from collections import namedtuple


Prediction = namedtuple('Prediction', ('pred_rating', 'movie', 'reason'))
"""A predicted movie rating.

The predicted rating is the first field so that instances may be stored in a
heap queue. See the `heapq`_ documentation for details.

:param pred_rating: A movie rating in the range 0.5 to 5, inclusive.
:param movie: A movie ID.
:param reason: A value from :data:`movie_recommender.constants.REASONS`.

.. _heapq: https://docs.python.org/3.7/library/heapq.html
"""
