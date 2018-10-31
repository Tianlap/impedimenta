# coding=utf-8
"""Unit tests for :mod:`movie_recommender.predict.ii`."""
import unittest

from movie_recommender.predict import ii


class NormalizeRatingTestCase(unittest.TestCase):
    """Test :meth:`movie_recommender.predict.ii.normalize_rating`."""

    def test_min(self):
        """Assert a value of ~-1 can be produced."""
        target_val = -1
        actual_val = ii.normalize_rating(0.5)
        self.assertEqual(target_val, actual_val)

    def test_mid(self):
        """Assert a value of ~0 can be produced."""
        target_val = 0
        actual_val = ii.normalize_rating(2.75)
        self.assertEqual(target_val, actual_val)

    def test_max(self):
        """Assert a value of ~1 can be produced."""
        target_val = 1
        actual_val = ii.normalize_rating(5)
        self.assertEqual(target_val, actual_val)


class DenormalizeRatingTestCase(unittest.TestCase):
    """Test :meth:`movie_recommender.predict.ii.denormalize_rating`."""

    def test_min(self):
        """Assert a value of 0.5 can be produced."""
        target_val = 0.5
        actual_val = ii.denormalize_rating(-1)
        self.assertEqual(target_val, actual_val)

    def test_mid(self):
        """Assert a value of 2.75 can be produced."""
        target_val = 2.75
        actual_val = ii.denormalize_rating(0)
        self.assertEqual(target_val, actual_val)

    def test_max(self):
        """Assert a value of 5 can be produced."""
        target_val = 5
        actual_val = ii.denormalize_rating(1)
        self.assertEqual(target_val, actual_val)
