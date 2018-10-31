# coding=utf-8
"""Utilities for functional tests."""
import subprocess

_BACKUP_PATH = None
"""The path to the backed-up database, if any."""


def backup_db():
    """Back up the current database if one exists.

    .. WARNING:: Not thread-safe!
    """
    try:
        load_path = run(('mr-db', 'load-path'))[0]
    except subprocess.CalledProcessError:
        return
    # It's OK to use a global here, so long as the same process and thread
    # runs both this and restore_db().
    global _BACKUP_PATH  # pylint:disable=global-statement
    _BACKUP_PATH = run(('mktemp',))[0]
    run(('mv', load_path, _BACKUP_PATH))


def restore_db():
    """Restore the backed-up database.

    .. WARNING:: Not thread-safe!
    """
    # It's OK to use a global here, so long as the same process and thread
    # runs both this and restore_db().
    global _BACKUP_PATH  # pylint:disable=global-statement
    if not _BACKUP_PATH:
        return
    save_path = run(('mr-db', 'save-path'))[0]
    run(('mv', _BACKUP_PATH, save_path))
    _BACKUP_PATH = None


def run(args):
    """Call ``subprocess.run`` with several common arguments set.

    :param args: For details, see the parameter by the same name provided by
        ``subprocess.run``. A command, e.g. ``('echo', 'foo')``.
    :return: The contents of stdout, split on newlines.
    :raise: ``CalledProcessError`` if the called process returns a non-zero
        return code.
    """
    return subprocess.run(
        args,
        check=True,
        stdout=subprocess.PIPE,
        universal_newlines=True,  # convert this OSs newline sequence to \n
    ).stdout.splitlines()
