# coding=utf-8
"""Tests for the machine learning recommendation algorithm."""
import unittest

from .utils import backup_db, restore_db, run


def setUpModule():  # pylint:disable=invalid-name
    """Back up the current database if one exists, and create a new one."""
    backup_db()
    run(('mr-dataset', 'install', 'fixture'))
    run(('mr-db', 'create', 'fixture'))
    run(('mr-analyze', 'ml'))


def tearDownModule():  # pylint:disable=invalid-name
    """Delete the current database, and restore the old one."""
    load_path = run(('mr-db', 'load-path'))[0]
    run(('rm', load_path))
    restore_db()


class PredictTestCase(unittest.TestCase):
    """Generate predictions for each user."""

    def test_user_1(self):
        """Verify user 1's predictions.

        The best predictor for this user is "genre:Animation."
        """
        for movie, target_rating in (
                ('10', '1.0'),
                ('11', '4.5'),
                ('12', '1.0'),
                ('13', '1.0')):
            with self.subTest(movie=movie, target_rating=target_rating):
                actual_rating = run(('mr-predict', 'ml', '1', movie))[0]
                self.assertEqual(target_rating, actual_rating)

    def test_user_2(self):
        """Verify user 1's predictions.

        The best predictor for this user is "year." This dataset has an inverse
        linear relationship between year and rating. We can't get predictions
        for movies that lack year data.
        """
        for movie, target_rating in (('10', '4.0'), ('11', '2.0')):
            with self.subTest(movie=movie, target_rating=target_rating):
                actual_rating = run(('mr-predict', 'ml', '2', movie))[0]
                self.assertEqual(target_rating, actual_rating)

    def test_user_3(self):
        """Verify user 3's predictions.

        The best predictor this user is "(no genres listed)." All of the movies
        this user has rated have the "(no genres listed)" genre. As a result,
        the scatter plot is a vertical line, and the recommendation is the
        average of ratings: 3.5.
        """
        for movie, target_rating in (
                ('10', '3.5'),
                ('11', '3.5'),
                ('12', '3.5'),
                ('13', '3.5')):
            with self.subTest(movie=movie, target_rating=target_rating):
                actual_rating = run(('mr-predict', 'ml', '3', movie))[0]
                self.assertEqual(target_rating, actual_rating)

    def test_user_4(self):
        """Verify user 3's predictions.

        The best predictor for this user is "(no genres listed)." The user
        hasn't rated any movies with year data, so the SSE for a year-based
        predictor is infinite.
        """
        for movie, target_rating in (
                ('10', '4.5'),
                ('11', '4.5'),
                ('12', '4.5'),
                ('13', '4.5')):
            with self.subTest(movie=movie, target_rating=target_rating):
                actual_rating = run(('mr-predict', 'ml', '4', movie))[0]
                self.assertEqual(target_rating, actual_rating)


class RecommendTestCase(unittest.TestCase):
    """Generate recommendations for each user."""

    def test_format_csv(self):
        """Generate recommendations with ``--format csv``."""
        lines = run((
            'mr-recommend', 'ml', '1', '--count', '1', '--format', 'csv',
        ))
        # The three lines are a header row, a data row, and a blank line.
        self.assertEqual(len(lines), 3, lines)

    def test_format_pretty(self):
        """Generate recommendations with ``--format pretty``."""
        lines = run((
            'mr-recommend', 'ml', '1', '--count', '1', '--format', 'pretty',
        ))
        self.assertEqual(len(lines), 1, lines)

    def test_user_1(self):
        """Verify user 1's recommendations."""
        lines = run((
            'mr-recommend', 'ml', '1', '--count', '1', '--format', 'csv',
        ))
        self.assertEqual(len(lines), 3, lines)
        self.assertEqual(lines[1], '11,4.5')

    def test_user_2(self):
        """Verify user 2's recommendations."""
        lines = run((
            'mr-recommend', 'ml', '2', '--count', '1', '--format', 'csv',
        ))
        self.assertEqual(len(lines), 3, lines)
        self.assertEqual(lines[1], '10,4.0')
