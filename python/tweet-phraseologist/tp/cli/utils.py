# coding=utf-8
"""Utilities for the CLI interfaces."""
import argparse
import multiprocessing


def add_jobs_flag(parser: argparse.ArgumentParser):
    """Add the ``--jobs`` flag to a parser."""
    default = multiprocessing.cpu_count()
    parser.add_argument(
        '-j',
        '--jobs',
        default=default,
        help=f'Spawn this many processes, instead of {default}.',
        type=int,
    )


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
