# coding=utf-8
"""Unit tests for :mod:`movie_recommender.db`."""
import unittest

from movie_recommender import db, exceptions

from .utils import get_fixture


class GetYearTestCase(unittest.TestCase):
    """Test :func:`movie_recommender.db.get_year`."""

    def test_parseable(self):
        """Pass a parseable movie title to the function."""
        title = '"White Balloon, The (Badkonake sefid) (1995)"'
        year = db.get_year(title)
        self.assertEqual(year, 1995)

    def test_unparseable(self):
        """Pass an un-parseable movie title to the function."""
        title = 'Babylon 5'
        with self.assertRaises(exceptions.NoMovieYearError):
            db.get_year(title)


class ParseCSVTestCase(unittest.TestCase):
    """Tests for :func:`movie_recommender.db.parse_csv`."""

    def test_identity(self):
        """Verify the function can return all fields without altering them."""
        with open(get_fixture('xy-header.csv')) as handle:
            rows = tuple(db.parse_csv(handle, header_rows=0))
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
            rows = tuple(db.parse_csv(
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
