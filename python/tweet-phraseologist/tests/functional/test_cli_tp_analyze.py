# coding=utf-8
"""Functional tests for :mod:`tp.cli.tp_analyze`."""
import unittest

from .utils import run, temp_xdg_data_home


class GoldenPathTestCase(unittest.TestCase):
    """Test basic usage."""

    # The lack of self.assertX() calls is OK, as run() will raise an exception
    # if any non-zero return codes are discovered.
    def test_help(self):  # pylint:disable=no-self-use
        """Pass ``--help`` to ``tp-analyze`` and its subcommands."""
        run(('tp-analyze', '--help'))

    @staticmethod
    def set_up():
        """Create and populate the database with the simple-fixture fixture.

        This is slightly hard to do via ``setUp()``, due to the usage of
        ``@temp_xdg_data_home``. It *can* be done, but only carefully.
        """
        run('tp-dataset install simple-fixture'.split())
        run('tp-db cpop simple-fixture'.split())

    @temp_xdg_data_home()
    def test_default(self):
        """Analyze tweets with the default options.

        Verify the top phrase.
        """
        self.set_up()
        lines = run(('tp-analyze',))
        self.assertGreaterEqual(len(lines), 1, lines)
        self.assertEqual(lines[0], '3,brown fox')

    @temp_xdg_data_home()
    def test_count(self):
        """Test the ``--count`` flag."""
        self.set_up()
        for count in (0, 1, 5):
            lines = run(('tp-analyze', '--count', str(count)))
            self.assertEqual(len(lines), count)

    @temp_xdg_data_home()
    def test_party_democrat(self):
        """Pass ``--party Democrat``.

        Verify the top phrase.
        """
        self.set_up()
        lines = run('tp-analyze --party Democrat'.split())
        self.assertGreaterEqual(len(lines), 1, lines)
        self.assertEqual(lines[0], '2,brown fox')

    @temp_xdg_data_home()
    def test_party_republican(self):
        """Pass ``--party Republican``.

        Verify the top phrase.
        """
        self.set_up()
        lines = run('tp-analyze --party Republican'.split())
        self.assertGreaterEqual(len(lines), 1, lines)
        self.assertEqual(lines[0], '2,is sleep')

    @temp_xdg_data_home()
    def test_party_democrat_unique(self):
        """Pass ``--party Democrat --unique``.

        Verify the top phrase.
        """
        self.set_up()
        lines = run('tp-analyze --party Democrat --unique'.split())
        self.assertGreaterEqual(len(lines), 1, lines)
        self.assertTrue(lines[0].startswith('1,'), lines)

    @temp_xdg_data_home()
    def test_party_republican_unique(self):
        """Pass ``--party Republican --unique``.

        Verify the top phrase.
        """
        self.set_up()
        lines = run('tp-analyze --party Republican --unique'.split())
        self.assertGreaterEqual(len(lines), 1, lines)
        self.assertEqual(lines[0], '2,is sleep')
