# coding=utf-8
"""Tests for the item-item recommendation algorithm."""
import unittest

from .utils import backup_db, restore_db, run


def setUpModule():  # pylint:disable=invalid-name
    """Back up the current database if one exists, and create a new one."""
    backup_db()
    run(('mr-dataset', 'install', 'fixture'))
    run(('mr-db', 'create', 'fixture'))


def tearDownModule():  # pylint:disable=invalid-name
    """Delete the current database, and restore the old one."""
    load_path = run(('mr-db', 'load-path'))[0]
    run(('rm', load_path))
    restore_db()


class AnalyzeTestCase(unittest.TestCase):
    """Call ``mr-analyze`` with various arguments."""

    # The lack of self.assertX() calls is OK, as run() will raise an exception
    # if any non-zero return codes are discovered. Furthermore, unittest
    # dictates that tests be written as methods, not functions.
    # pylint:disable=no-self-use

    def test_no_params(self):
        """Don't pass any parameters."""
        run(('mr-analyze', 'ii'))

    def test_overwrite(self):
        """Pass ``--overwrite``."""
        run(('mr-analyze', 'ii', '--overwrite'))

    def test_no_overwrite(self):
        """Pass ``--no-overwrite``."""
        run(('mr-analyze', 'ii', '--no-overwrite'))

    def test_progress(self):
        """Pass ``--progress``."""
        run(('mr-analyze', 'ii', '--overwrite', '--progress'))

    def test_no_progress(self):
        """Pass ``--no-progress``."""
        run(('mr-analyze', 'ii', '--overwrite', '--no-progress'))

    def test_movie_ids(self):
        """Pass ``--movie-ids``."""
        run(('mr-analyze', 'ii', '--movie-ids', '1', '2', '--overwrite'))

    def test_user_ids(self):
        """Pass ``--user-ids``."""
        run(('mr-analyze', 'ii', '--user-ids', '1', '2', '--overwrite'))

    def test_movie_ids_user_ids(self):
        """Pass ``--movie-ids`` and ``--user-ids``."""
        run((
            'mr-analyze', 'ii',
            '--movie-ids', '1', '2',
            '--user-ids', '1', '2',
            '--overwrite'
        ))

    def test_jobs_1(self):
        """Pass ``--jobs 1``."""
        run(('mr-analyze', 'ii', '--overwrite', '--jobs', '1'))

    def test_jobs_2(self):
        """Pass ``--jobs 2``."""
        run(('mr-analyze', 'ii', '--overwrite', '--jobs', '2'))


class RecommendTestCase(unittest.TestCase):
    """Generate recommendations for each user."""

    def test_count_1(self):
        """Generate recommendations with ``--count 1``."""
        lines = run((
            'mr-recommend', 'ii', '1', '--count', '1', '--no-progress'
        ))
        self.assertEqual(len(lines), 1, lines)

    def test_count_2(self):
        """Generate recommendations with ``--count 2``."""
        lines = run((
            'mr-recommend', 'ii', '1', '--count', '2', '--no-progress'
        ))
        self.assertEqual(len(lines), 2, lines)
