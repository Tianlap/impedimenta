# coding=utf-8
"""Unit tests for :mod:`movie_recommender.db`."""
import unittest

from movie_recommender import exceptions
from movie_recommender.db import read


class GetYearTestCase(unittest.TestCase):
    """Test :func:`movie_recommender.db.read.year`."""

    def test_parseable(self):
        """Pass a parseable movie title to the function."""
        title = '"White Balloon, The (Badkonake sefid) (1995)"'
        year = read.year(title)
        self.assertEqual(year, 1995)

    def test_unparseable(self):
        """Pass an un-parseable movie title to the function."""
        title = 'Babylon 5'
        with self.assertRaises(exceptions.NoMovieYearError):
            read.year(title)
