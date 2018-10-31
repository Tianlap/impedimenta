# coding=utf-8
"""Unit tests for :mod:`movie_recommender.graph`."""
import unittest

from movie_recommender import exceptions
from movie_recommender.graph import Graph, Point


class GraphPointsTestCase(unittest.TestCase):
    """Test :meth:`movie_recommender.graph.Graph.points`."""

    def test_zero_points(self):
        """Create a graph with no points."""
        points = ()
        graph = Graph(points)
        self.assertEqual(graph.points, points)

    def test_one_point(self):
        """Create a graph with one point."""
        points = (Point(-1, 1),)
        graph = Graph(points)
        self.assertEqual(graph.points, points)

    def test_two_points(self):
        """Create a graph with two points."""
        points = (Point(1.2, 3.4), Point(5.6, 7.8))
        graph = Graph(points)
        self.assertEqual(graph.points, points)


class GraphAvgPointTestCase(unittest.TestCase):
    """Test :meth:`movie_recommender.graph.Graph.avg_point`."""

    def test_zero_points(self):
        """Attempt to calculate the average point of an empty graph.

        Assert :class:`movie_recommender.exceptions.EmptyGraphError` is raised.
        """
        graph = Graph(())
        with self.assertRaises(exceptions.EmptyGraphError):
            graph.avg_point  # pylint:disable=pointless-statement

    def test_one_point(self):
        """Assert the method behaves correctly when given one point."""
        graph = Graph((Point(25, -1.5),))
        self.assertEqual(graph.avg_point, graph.points[0])

    def test_two_points(self):
        """Assert the method behaves correctly when given two points."""
        graph = Graph((Point(10, -1), Point(20, -2)))
        self.assertEqual(graph.avg_point, Point(15, -1.5))


class GraphSlopeTestCase(unittest.TestCase):
    """Test :meth:`movie_recommender.graph.Graph.slope`."""

    def test_positive_slope(self):
        """Verify the method can calculate a positive slope."""
        graph = Graph((Point(1, 1), Point(2, 2)))
        self.assertEqual(graph.slope, 1)

    def test_negative_slope(self):
        """Verify the method can calculate a negative slope."""
        graph = Graph((Point(1, 2), Point(2, 1)))
        self.assertEqual(graph.slope, -1)

    def test_flat_slope(self):
        """Verify the method can calculate a flat slope."""
        graph = Graph((Point(1, 1), Point(2, 1)))
        self.assertEqual(graph.slope, 0)

    def test_vertical_slope(self):
        """Attempt to calculate a vertical slope.

        Assert
        :class:`movie_recommender.exceptions.VerticalLineOfBestFitGraphError`
        is raised.
        """
        graph = Graph((Point(1, 1), Point(1, 2)))
        with self.assertRaises(exceptions.VerticalLineOfBestFitGraphError):
            graph.slope  # pylint:disable=pointless-statement


class GraphYInterceptTestCase(unittest.TestCase):
    """Test :meth:`movie_recommender.graph.Graph.y_intercept`."""

    def test_positive_intercept(self):
        """Verify the method can calculate a positive y-intercept."""
        graph = Graph((Point(1, 11), Point(2, 12)))
        self.assertEqual(graph.y_intercept, 10)

    def test_negative_intercept(self):
        """Verify the method can calculate a positive y-intercept."""
        graph = Graph((Point(1, -9), Point(2, -8)))
        self.assertEqual(graph.y_intercept, -10)

    def test_zero_intercept(self):
        """Verify the method can calculate a zero y-intercept."""
        graph = Graph((Point(1, 0.5), Point(2, 1)))
        self.assertEqual(graph.y_intercept, 0)


class TrivialGraphTestCase(unittest.TestCase):
    """Call several high-level methods on a trivial graph.

    In this context, a "trivial" graph is one for which the line of best fit
    can pass through all points.
    """

    @classmethod
    def setUpClass(cls):
        """Define a trivial graph."""
        # y = 0.5x + 1
        cls.graph = Graph((Point(0, 1), Point(2, 2)))

    def test_slope(self):
        """Test :meth:`movie_recommender.graph.Graph.slope`."""
        self.assertEqual(self.graph.slope, 0.5)

    def test_y_intercept(self):
        """Test :meth:`movie_recommender.graph.Graph.y_intercept`."""
        self.assertEqual(self.graph.y_intercept, 1)

    def test_predict_y(self):
        """Test :meth:`movie_recommender.graph.Graph.predict_y`."""
        self.assertEqual(self.graph.predict_y(1), 1.5)

    def test_sse(self):
        """Test :meth:`movie_recommender.graph.Graph.sse`."""
        self.assertEqual(self.graph.sse, 0)


class NonTrivialGraphTestCase(unittest.TestCase):
    """Call several high-level methods on a trivial graph.

    In this context, a "non-trivial" graph is one for which the line of best
    fit can't pass through all points.
    """

    @classmethod
    def setUpClass(cls):
        """Define a non-trivial graph."""
        # The line of best fit is `y = -1x + 10`.
        cls.graph = Graph((
            # Define a line 2 above the line of best fit.
            Point(-2, 14),
            Point(2, 10),
            # Define a line 2 below the line of best fit.
            Point(-2, 10),
            Point(2, 6),
        ))

    def test_slope(self):
        """Test :meth:`movie_recommender.graph.Graph.slope`."""
        self.assertEqual(self.graph.slope, -1)

    def test_y_intercept(self):
        """Test :meth:`movie_recommender.graph.Graph.y_intercept`."""
        self.assertEqual(self.graph.y_intercept, 10)

    def test_predict_y(self):
        """Test :meth:`movie_recommender.graph.Graph.predict_y`."""
        self.assertEqual(self.graph.predict_y(0), 10)

    def test_sse(self):
        """Test :meth:`movie_recommender.graph.Graph.sse`."""
        # 2^2 + 2^2 + 2^2 + 2^2
        # 4 + 4 + 4 + 4
        # 16
        self.assertEqual(self.graph.sse, 16)
