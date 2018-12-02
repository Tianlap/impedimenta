# coding=utf-8
"""Functional tests for :mod:`tp.cli.tp_dataset`."""
import importlib
import subprocess
import unittest

from xdg import BaseDirectory

from .utils import run, temp_xdg_data_home


class GoldenPathTestCase(unittest.TestCase):
    """Test basic usage."""

    # The lack of self.assertX() calls is OK, as run() will raise an exception
    # if any non-zero return codes are discovered.
    def test_help(self):  # pylint:disable=no-self-use
        """Pass ``--help`` to ``tp-db`` and its subcommands."""
        commands = (
            ('tp-db', '--help'),
            ('tp-db', 'cpop', '--help'),
            ('tp-db', 'load-path', '--help'),
            ('tp-db', 'save-path', '--help'),
        )
        for command in commands:
            with self.subTest(command=command):
                run(command)

    @temp_xdg_data_home()
    def test_save_path(self):
        """Test the "save-path" subcommand."""
        paths = run(('tp-db', 'save-path'))
        self.assertEqual(len(paths), 1, paths)
        importlib.reload(BaseDirectory)
        self.assertTrue(
            paths[0].startswith(BaseDirectory.xdg_data_home),
            (paths[0], BaseDirectory.xdg_data_home),
        )

    @temp_xdg_data_home()
    def test_load_path(self):
        """Don't create a database, and run the load-path subcommand.

        Assert it returns non-zero, because no database can be found.
        """
        with self.assertRaises(subprocess.CalledProcessError):
            run(('tp-db', 'load-path'))

    @temp_xdg_data_home()
    def test_cpop_load_path(self):
        """Do create a database, and run the load-path subcommand.

        Assert it returns zero, because a database is found.
        """
        run(('tp-dataset', 'install', 'simple-fixture'))
        run(('tp-db', 'cpop', 'simple-fixture'))
        paths = run(('tp-db', 'load-path'))
        self.assertEqual(len(paths), 1, paths)
        importlib.reload(BaseDirectory)
        self.assertTrue(
            paths[0].startswith(BaseDirectory.xdg_data_home),
            (paths[0], BaseDirectory.xdg_data_home),
        )

    @temp_xdg_data_home()
    def test_cpop_v1(self):
        """Call ``cpop`` twice.

        Assert the second call fails, because a database is already present.
        """
        run(('tp-dataset', 'install', 'simple-fixture'))
        run(('tp-db', 'cpop', 'simple-fixture'))
        with self.assertRaises(subprocess.CalledProcessError):
            run(('tp-db', 'cpop', 'simple-fixture'))

    @temp_xdg_data_home()
    def test_cpop_v2(self):  # pylint:disable=no-self-use
        """Call ``cpop``, ``cpop --overwrite``.

        Assert both commands succeed.
        """
        run(('tp-dataset', 'install', 'simple-fixture'))
        run(('tp-db', 'cpop', 'simple-fixture'))
        run(('tp-db', 'cpop', '--overwrite', 'simple-fixture'))

    @temp_xdg_data_home()
    def test_cpop_v3(self):  # pylint:disable=no-self-use
        """Call ``cpop --overwrite``, ``cpop --overwrite``.

        Assert both commands succeed.
        """
        run(('tp-dataset', 'install', 'simple-fixture'))
        run(('tp-db', 'cpop', '--overwrite', 'simple-fixture'))
        run(('tp-db', 'cpop', '--overwrite', 'simple-fixture'))

    @temp_xdg_data_home()
    def test_cpop_v4(self):  # pylint:disable=no-self-use
        """Call ``cpop --overwrite``, ``cpop``.

        Assert the second call fails, because a database is already present.
        """
        run(('tp-dataset', 'install', 'simple-fixture'))
        run(('tp-db', 'cpop', '--overwrite', 'simple-fixture'))
        with self.assertRaises(subprocess.CalledProcessError):
            run(('tp-db', 'cpop', 'simple-fixture'))
