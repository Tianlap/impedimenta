# coding=utf-8
"""Unit tests for :mod:`movie_recommender.cli.mr_graph`."""
import unittest

from movie_recommender.cli.mr_graph import Columns, get_points
from movie_recommender.graph import Point
from .utils import get_fixture


class GetPointsTestCase(unittest.TestCase):
    """Test :func:`movie_recommender.cli.mr_graph.get_points`."""

    @classmethod
    def setUpClass(cls):
        """Set class-wide variables."""
        cls.points = (
            Point(0.25, 4.4),
            Point(0.265, 4.62),
            Point(0.25, 3.84),
            Point(0.256, 4.16),
            Point(0.27, 4.28),
            Point(0.25, 4.5),
            Point(0.269, 4.47)
        )

    def test_golden_path(self):
        """Verify the function behaves correctly when given ideal input."""
        with open(get_fixture('xy.csv')) as handle:
            for i, point in enumerate(get_points(handle, Columns(0, 1))):
                self.assertEqual(point, self.points[i])

    def test_header_row(self):
        """Verify the function behaves correctly when asked to skip a header."""
        with open(get_fixture('xy-header.csv')) as handle:
            for i, point in enumerate(
                    get_points(handle, Columns(0, 1), header_rows=1)):
                self.assertEqual(point, self.points[i])
