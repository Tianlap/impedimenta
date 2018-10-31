# coding=utf-8
"""Utilities for the CLI interfaces."""
import multiprocessing
import sys

from movie_recommender.db import common


def add_jobs_flag(parser):
    """Add the ``--jobs`` flag to a parser."""
    default = multiprocessing.cpu_count()
    parser.add_argument(
        '-j',
        '--jobs',
        default=default,
        help=f'Spawn this many processes, instead of {default}.',
        type=int,
    )


def add_progress_flags(parser):
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
    group.set_defaults(progress=True)


def report_progress(conn_out, prefix=''):
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


def to_movie_id(arg):
    """Cast the given string argument to a movvie ID, if possible.

    An exception of some kind is raised if ``arg`` can't be cast to a movie ID.
    The specific type of exception varies.

    :param arg: A string argument passed on the command line. Semantically, a
        movie ID.
    :return: A movie ID.
    """
    movie_id = int(arg)
    with common.get_db_conn() as conn:
        movie_ids = tuple(
            row[0] for row in conn.execute(
                'SELECT DISTINCT movieId FROM movies WHERE movieId=?',
                (movie_id,)
            )
        )
    if movie_id not in movie_ids:
        raise ValueError(f'Movie ID {movie_id} not in database.')
    return movie_id


def to_user_id(arg):
    """Cast the given string argument to a user ID, if possible.

    An exception of some kind is raised if ``arg`` can't be cast to a user ID.
    The specific type of exception varies.

    :param arg: A string argument passed on the command line. Semantically, a
        user ID.
    :return: A user ID.
    """
    user_id = int(arg)
    with common.get_db_conn() as conn:
        user_ids = tuple(
            row[0] for row in conn.execute(
                'SELECT DISTINCT userId FROM ratings WHERE userId=?',
                (user_id,)
            )
        )
    if user_id not in user_ids:
        raise ValueError(f'User ID {user_id} not in database.')
    return user_id
