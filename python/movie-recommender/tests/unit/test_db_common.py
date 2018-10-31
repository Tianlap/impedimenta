# coding=utf-8
"""Unit tests for :mod:`movie_recommender.db.common`."""
import unittest

from movie_recommender.db import common

from .utils import get_fixture


class ParseCSVTestCase(unittest.TestCase):
    """Tests for :func:`movie_recommender.db.common.parse_csv`."""

    def test_identity(self):
        """Verify the function can return all fields without altering them."""
        with open(get_fixture('xy-header.csv')) as handle:
            rows = tuple(common.parse_csv(handle, header_rows=0))
            self.assertEqual(
                rows,
                (
                    ('batting average', 'runs per game'),
                    ('0.250', '4.40'),
                    ('0.265', '4.62'),
                    ('0.250', '3.84'),
                    ('0.256', '4.16'),
                    ('0.270', '4.28'),
                    ('0.250', '4.50'),
                    ('0.269', '4.47'),
                ),
            )

    def test_transform(self):
        """Verify the function can transform rows and skip headers."""
        with open(get_fixture('xy-header.csv')) as handle:
            rows = tuple(common.parse_csv(
                handle,
                lambda fields: (float(fields[0]), float(fields[1])),
                2
            ))
            self.assertEqual(
                rows,
                (
                    (0.265, 4.62),
                    (0.250, 3.84),
                    (0.256, 4.16),
                    (0.270, 4.28),
                    (0.250, 4.50),
                    (0.269, 4.47),
                ),
            )
