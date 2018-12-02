# coding=utf-8
"""Functional tests for :mod:`tp.cli.tp_dataset`."""
import importlib
import unittest

from xdg import BaseDirectory

from .utils import run, temp_xdg_data_home


class GoldenPathTestCase(unittest.TestCase):
    """Test basic usage."""

    # The lack of self.assertX() calls is OK, as run() will raise an exception
    # if any non-zero return codes are discovered.
    def test_help(self):  # pylint:disable=no-self-use
        """Pass ``--help`` to ``tp-dataset`` and its subcommands."""
        commands = (
            ('tp-dataset', '--help'),
            ('tp-dataset', 'install', '--help'),
            ('tp-dataset', 'installable', '--help'),
            ('tp-dataset', 'uninstall', '--help'),
        )
        for command in commands:
            with self.subTest(command=command):
                run(command)

    @temp_xdg_data_home()
    def test_installable(self):
        """Test the "installable" subcommand.

        Assert 'simple-fixture' is one of the lines of output.
        """
        stdout = run(('tp-dataset', 'installable'))
        self.assertIn('simple-fixture', stdout)

    @temp_xdg_data_home()
    def test_install_uninstall(self):
        """Test install, uninstall, and installed subcommands.

        Do the following:

        #. Assert the simple-fixture dataset is not installed.
        #. Install the simple-fixture dataset. Assert the simple-fixture
           dataset is installed, and that it has a sane-looking value.
        #. Uninstall the simple-fixture dataset. Assert the simple-fixture
           dataset is not installed.
        """
        paths = run(('tp-dataset', 'installed', '--path'))
        self.assertEqual(len(paths), 0, paths)

        run(('tp-dataset', 'install', 'simple-fixture'))
        paths = run(('tp-dataset', 'installed', '--path'))
        self.assertEqual(len(paths), 1, paths)
        importlib.reload(BaseDirectory)
        self.assertTrue(
            paths[0].startswith(BaseDirectory.xdg_data_home),
            (paths[0], BaseDirectory.xdg_data_home),
        )

        run(('tp-dataset', 'uninstall', 'simple-fixture'))
        paths = run(('tp-dataset', 'installed', '--path'))
        self.assertEqual(len(paths), 0, paths)
