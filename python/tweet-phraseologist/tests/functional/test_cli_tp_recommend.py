# coding=utf-8
"""Functional tests for :mod:`tp.cli.tp_recommend`."""
import unittest

from .utils import run


class GoldenPathTestCase(unittest.TestCase):
    """Test basic usage."""

    # The lack of self.assertX() calls is OK, as run() will raise an exception
    # if any non-zero return codes are discovered.
    def test_help(self):  # pylint:disable=no-self-use
        """Pass ``--help`` to ``tp-recommend`` and its subcommands."""
        run(('tp-recommend', '--help'))
