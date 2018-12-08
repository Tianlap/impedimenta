# coding=utf-8
"""Tests for module ``tp.cli.utils``."""
import unittest

from tp.cli.utils import non_negative_int


class NonNegativeIntTestCase(unittest.TestCase):
    """Tests for :func:`tp.cli.utils.non_negative_int`."""

    def test_negative(self):
        """Pass a negative number.

        Assert a ``ValueError`` is raised.
        """
        with self.assertRaises(ValueError):
            non_negative_int('-1')

    def test_zero(self):
        """Pass zero.

        Assert zero is returned.
        """
        self.assertEqual(0, non_negative_int('0'))

    def test_one(self):
        """Pass one.

        Assert one is returned.
        """
        self.assertEqual(1, non_negative_int('1'))
