# coding=utf-8
"""Tools for working with a cartesian graph."""
from collections import namedtuple

from movie_recommender import exceptions


Point = namedtuple('Point', ('x', 'y'))
"""A point on a cartesian graph."""


class Graph():
    """A cartesian graph."""

    def __init__(self, points):
        """Initialize instance attributes.

        :param points: A tuple of :class:`Point` objects. The points on this
            cartesian graph.
        """
        self._points = points
        self._avg_point = None
        self._slope = None
        self._y_intercept = None
        self._sse = None

    @property
    def points(self):
        """Get the points on this graph."""
        return self._points

    @property
    def avg_point(self):
        """Get the average point on this graph.

        :returns: The average of all points on this graph.
        :rtype: Point
        :raise movie_recommender.exceptions.EmptyGraphError: If this graph is
            empty.
        """
        if self._avg_point is None:
            self._avg_point = self._calc_avg_point(self.points)
        return self._avg_point

    @staticmethod
    def _calc_avg_point(points):
        """Calculate the average of the given ``points``."""
        if not points:
            raise exceptions.EmptyGraphError(
                "Can't calculate the average point of an empty graph."
            )
        num_points = 0
        total_x = 0
        total_y = 0
        for point in points:
            num_points += 1
            total_x += point.x
            total_y += point.y
        return Point(total_x / num_points, total_y / num_points)

    @property
    def slope(self):
        """Get the slope of this graph.

        :returns: The "m" term of the following formula: ``y = mx + b``.
        :raise movie_recommender.exceptions.EmptyGraphError: If this graph is
            empty.
        :raise movie_recommender.exceptions.VerticalLineOfBestFitGraphError: If
            this graph's slope is vertical.
        """
        if self._slope is None:
            self._slope = self._calc_clope(self.points, self.avg_point)
        return self._slope

    @staticmethod
    def _calc_clope(points, avg_point):
        """Calculate the slope of an iterable of points."""
        if not points:
            raise exceptions.EmptyGraphError(
                "Can't calculate the average point of an empty graph."
            )

        # m = sumOfAll((Xi - Xavg) * (Yi - Yavg)) / sumOfAll((Xi - Xavg)^2)
        numerator = 0
        denominator = 0
        for point in points:
            xi_minus_xavg = point.x - avg_point.x
            numerator += xi_minus_xavg * (point.y - avg_point.y)
            denominator += xi_minus_xavg ** 2
        try:
            return numerator / denominator
        except ZeroDivisionError as err:
            raise exceptions.VerticalLineOfBestFitGraphError(
                "This graph's line of best fit is vertical. As a result, its "
                "slope can't be calculated."
            ) from err

    @property
    def y_intercept(self):
        """Return the y intercept of this graph.

        :returns: The "b" term of the following formula: ``y = mx + b``.
        """
        if self._y_intercept is None:
            self._y_intercept = self._calc_y_intercept(
                self.avg_point,
                self.slope,
            )
        return self._y_intercept

    @staticmethod
    def _calc_y_intercept(avg_point, slope):
        """Calculate the y intercept of an iterable of points."""
        return avg_point.y - avg_point.x * slope

    def predict_y(self, x):
        """Predict y according to the line of best fit.

        :param x: The x coordinate of a point along the line of best fit.
        :returns: The corresponding y coordinate of a point along the line of
            best fit.
        """
        # y = mx + b
        return self.slope * x + self.y_intercept

    @property
    def sse(self):
        """Get the sum of squared errors for this graph."""
        if self._sse is None:
            self._sse = self._calc_sse()
        return self._sse

    def _calc_sse(self):
        """Calculate the residual sum of squares."""
        sse = 0
        for point in self.points:
            error = point.y - self.predict_y(point.x)
            sse += error ** 2
        return sse
