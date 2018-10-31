# coding=utf-8
"""Recommend movies for a user."""
import argparse
import functools

from movie_recommender.db import read
from movie_recommender.analyze import ii, ml
from movie_recommender.cli.utils import (
    add_jobs_flag,
    add_progress_flags,
    report_progress,
    to_movie_id,
    to_user_id,
)


def main():
    """Parse arguments and call business logic."""
    # The `dest` argument is a workaround for a bug in argparse. See:
    # https://stackoverflow.com/questions/23349349/argparse-with-required-subparser
    parser = argparse.ArgumentParser(
        description="""\
        Analyze users. This must be done before one can ask for movie
        predictions or recommendations for users.
        """,
    )
    subparsers = parser.add_subparsers(dest='subcommand', required=True)
    add_ii_subcommand(subparsers)
    add_ml_subcommand(subparsers)
    args = parser.parse_args()
    args.func(args)


def add_ii_subcommand(subparsers):
    """Add the ii subcommand to an argparse subparsers object."""
    parser = subparsers.add_parser(
        'ii',
        help='Perform analyses for the item-item recommendation algorithm.',
        description="""\
        Perform analyses for the item-item recommendation algorithm. By
        default, analyze all movies in the database. This can take a long time.
        The scope of analysis can be reduced by passing --movie-ids or
        --user-ids. If both are passed, their effect is cumulative, and the
        union of the movies referenced by the flags are analyzed.
        """,
    )
    parser.add_argument(
        '-m',
        '--movie-ids',
        help='Analyze these movies, instead of all movies.',
        nargs='+',
        type=to_movie_id,
    )
    parser.add_argument(
        '-u',
        '--user-ids',
        help=(
            'Analyze the movies these users have seen, instead of all movies.'
        ),
        nargs='+',
        type=to_user_id,
    )
    add_jobs_flag(parser)
    add_overwrite_flags(parser)
    add_progress_flags(parser)
    parser.set_defaults(func=handle_ii)


def add_ml_subcommand(subparsers):
    """Add the ml subcommand to an argparse subparsers object."""
    helptext = (
        'Perform analyses for the machine learning recommendation algorithm.'
    )
    parser = subparsers.add_parser(
        'ml',
        help=helptext,
        description=helptext,
    )
    parser.add_argument(
        '-u',
        '--user-ids',
        help='Analyze these users, instead of all users.',
        nargs='+',
        type=to_user_id,
    )
    add_jobs_flag(parser)
    add_overwrite_flags(parser)
    parser.set_defaults(func=handle_ml)


def add_overwrite_flags(parser):
    """Add the ``--{no-,}overwrite`` flags to a parser."""
    # See: https://stackoverflow.com/a/15008806
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        '--overwrite',
        action='store_true',
        dest='overwrite',
        help="""\
        If analysis work has already been completed, re-do that work and
        overwrite the old results. The exact effect depends on the analysis
        algorithm in use. Conflicts with --no-overwrite. Default is
        --no-overwrite.
        """,
    )
    group.add_argument(
        '--no-overwrite',
        action='store_false',
        dest='overwrite',
        help='Opposite of --overwrite.',
    )
    group.set_defaults(overwrite=False)


def handle_ii(args):
    """Handle the "ii" subcommand."""
    if args.movie_ids is None and args.user_ids is None:
        movie_ids = set(read.all_movies())
        user_ids = set()
    else:
        movie_ids = set() if args.movie_ids is None else args.movie_ids
        user_ids = set() if args.user_ids is None else args.user_ids
    if args.progress:
        au_reporter = functools.partial(
            report_progress,
            prefix='User analysis progress: ',
        )
        am_reporter = functools.partial(
            report_progress,
            prefix='Movie analysis progress: ',
        )
    else:
        au_reporter = None
        am_reporter = None
    ii.analyze_users(args.overwrite, args.jobs, au_reporter)
    ii.analyze_movies(
        movie_ids,
        user_ids,
        args.overwrite,
        args.jobs,
        am_reporter,
    )


def handle_ml(args):
    """Handle the "ml" subcommand."""
    user_ids = read.users() if args.user_ids is None else args.user_ids
    ml.analyze_users(user_ids, args.overwrite, args.jobs)
