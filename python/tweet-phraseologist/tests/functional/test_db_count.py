# coding=utf-8
"""Functional tests for :mod:`tp.db.count`."""
import unittest

from tp.db import count

from .utils import run, temp_xdg_data_home


class TweetsTestCase(unittest.TestCase):
    """Test :func:`tp.db.count.tweets`."""

    @temp_xdg_data_home()
    def test_all(self):
        """Count all tweets."""
        run('tp-dataset install simple-fixture'.split())
        run('tp-db cpop simple-fixture'.split())
        self.assertEqual(count.tweets(), 4)

    @temp_xdg_data_home()
    def test_per_party(self):
        """Count specific parties' tweets."""
        run('tp-dataset install simple-fixture'.split())
        run('tp-db cpop simple-fixture'.split())
        for party, num_tweets in (('Democrat', 2), ('Republican', 2)):
            with self.subTest(args=(party, num_tweets)):
                self.assertEqual(count.tweets(party), num_tweets)
