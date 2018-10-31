# coding=utf-8
"""Recommend movies for a user."""
import argparse
import csv
import io
import sys

from movie_recommender import exceptions
from movie_recommender.cli.utils import (
    add_jobs_flag,
    add_progress_flags,
    report_progress,
)
from movie_recommender.cli.utils import to_user_id
from movie_recommender.constants import REASONS
from movie_recommender.db import read
from movie_recommender.predict.ml import make_predictor
from movie_recommender.recommend import ii, ml


def main():
    """Parse arguments and call business logic."""
    # The `dest` argument is a workaround for a bug in argparse. See:
    # https://stackoverflow.com/questions/23349349/argparse-with-required-subparser
    parser = argparse.ArgumentParser(
        description='Recommend movies to a user.',
    )
    subparsers = parser.add_subparsers(dest='subcommand', required=True)
    add_ii_subcommand(subparsers)
    add_ml_subcommand(subparsers)
    args = parser.parse_args()
    args.func(args)


def add_ii_subcommand(subparsers):
    """Add the ii subcommand to an argparse subparsers object."""
    helptext = 'Recommend movies using the item-item algorithm.'
    parser = subparsers.add_parser(
        'ii',
        help=helptext,
        description=helptext,
    )
    add_jobs_flag(parser)
    add_user_id_flag(parser)
    add_count_flag(parser)
    add_progress_flags(parser)
    parser.set_defaults(func=handle_ii)


def add_ml_subcommand(subparsers):
    """Add the ml subcommand to an argparse subparsers object."""
    helptext = 'Recommend movies using the item-item algorithm.'
    parser = subparsers.add_parser(
        'ml',
        help=helptext,
        description=helptext,
    )
    parser.add_argument(
        '--predictor',
        help='The type of univariate predictor to use, e.g. "year".',
    )
    add_user_id_flag(parser)
    add_count_flag(parser)
    add_format_flag(parser)
    parser.set_defaults(func=handle_ml)


def add_count_flag(parser):
    """Add the ``--count`` parameter to a parser."""
    default = 5
    parser.add_argument(
        '--count',
        help=f'The number of recommendations to emit, instead of {default}.',
        default=default,
        type=int,
    )


def add_format_flag(parser):
    """Add the ``--format`` parameter to a parser."""
    parser.add_argument(
        '--format',
        help=(
            f"""
            Print output in the chosen format, instead of {_DEFAULT_FORMATTER}.
            """
        ),
        default=_DEFAULT_FORMATTER,
        choices=_FORMATTERS,
    )


def add_user_id_flag(parser):
    """Add the positional ``user_id`` parameter to a parser."""
    parser.add_argument(
        'user_id',
        help='The user for which recommendations are being generated.',
        type=to_user_id,
    )


def handle_ii(args):
    """Handle the "ii" subcommand."""
    reporter = report_progress if args.progress else None
    recommendations = ii.recommend(
        args.user_id,
        args.count,
        args.jobs,
        reporter,
    )
    for rec in recommendations:
        movie = read.title(rec.movie)
        pred_rating = f'{rec.pred_rating:.1f}'
        reason = REASONS[rec.reason]
        print(f'{movie} ({pred_rating}), {reason}')


def handle_ml(args):
    """Handle the "ml" subcommand."""
    # Retrieve the best type of predictor for this user.
    if args.predictor is None:
        try:
            args.predictor = read.predictor_name(args.user_id)
        except exceptions.NoPersonalizedPredictorError as err:
            print(err, file=sys.stderr)
            exit(1)

    # Make a predictor of that type.
    try:
        predictor = make_predictor(args.user_id, args.predictor)
    except exceptions.NoSuchPredictorError as err:
        print(err, file=sys.stderr)
        exit(1)

    # Make recommendations.
    formatter = _FORMATTERS[args.format]
    recommendations = ml.recommend(args.user_id, args.count, predictor)
    for line in formatter(recommendations):
        print(line)


def _format_csv(recommendations):
    """Yield recommendations, formatted as CSV."""
    output = io.StringIO()
    writer = csv.DictWriter(output, ('movie_id', 'pred_rating'))
    writer.writeheader()
    for rec in recommendations:
        writer.writerow({
            'movie_id': rec.movie,
            'pred_rating': f'{rec.pred_rating:.1f}',
        })
    yield output.getvalue()


def _format_pretty(recommendations):
    """Yield recommendations, formatted prettily."""
    for i, recommendation in enumerate(recommendations):
        movie_name = read.title(recommendation.movie)
        yield f'{i + 1}. {movie_name} ({recommendation.pred_rating:.1f})'


_DEFAULT_FORMATTER = 'pretty'
_FORMATTERS = {
    'csv': _format_csv,
    _DEFAULT_FORMATTER: _format_pretty,
}
