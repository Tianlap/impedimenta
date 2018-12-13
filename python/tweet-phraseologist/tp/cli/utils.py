# coding=utf-8
"""Utilities for the CLI interfaces."""
import argparse
import multiprocessing
from multiprocessing import connection
import sys


def add_jobs_flag(parser: argparse.ArgumentParser) -> None:
    """Add the ``--jobs`` flag to a parser."""
    default = multiprocessing.cpu_count()
    parser.add_argument(
        '-j',
        '--jobs',
        default=default,
        help=f'Spawn this many processes, instead of {default}.',
        type=int,
    )


def add_progress_flags(parser: argparse.ArgumentParser) -> None:
    """Add the ``--{no-,}progress`` flags to a parser."""
    # See: https://stackoverflow.com/a/15008806
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        '--progress',
        action='store_true',
        dest='progress',
        help='Show progress messages.',
    )
    group.add_argument(
        '--no-progress',
        action='store_false',
        dest='progress',
        help="Don't show progress messages.",
    )
    group.set_defaults(progress=False)


def non_negative_int(arg: str) -> int:
    """Cast the given string argument to a non-negative integer, if possible.

    :param arg: A string argument passed on the command line.
    :return: A positive integer.
    :raise: ``ValueError`` if unable to convert to a non-negative integer.
    """
    int_arg = int(arg)
    if int_arg < 0:
        raise ValueError(f'{int_arg} is less than zero.')
    return int_arg


def report_progress(conn_out: connection.Connection, prefix: str = '') -> None:
    """Tell the user how much work has been done.

    :param prefix: A message to print before the progress prompt, e.g.
        'Progress: '.
    :param conn_out: A multiprocessing ``Connection`` object from which values
        may be read. Each value emitted by the object should be a float between
        0 and 1, inclusive, where 0 indicates 0% complete, and 1 represents
        100% complete. When a value of 1 is received, this function will
        return.
    :return: Nothing.
    """
    while True:
        progress = conn_out.recv()
        # \r is carriage return. The other is an ANSI escape code. See:
        # https://en.wikipedia.org/wiki/ANSI_escape_code
        print(
            '\r\033[K' + prefix + f'{progress * 100:.0f}%',
            end='',
        )
        sys.stdout.flush()
        if progress == 1:
            conn_out.close()
            print()
            break
