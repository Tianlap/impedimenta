# coding=utf-8
"""Predict a user's rating for a movie."""
import argparse
import sys

from movie_recommender import exceptions
from movie_recommender.cli.utils import to_movie_id, to_user_id
from movie_recommender.constants import REASONS
from movie_recommender.db import read
from movie_recommender.predict import ii, ml


def main():
    """Parse arguments and call business logic."""
    # The `dest` argument is a workaround for a bug in argparse. See:
    # https://stackoverflow.com/questions/23349349/argparse-with-required-subparser
    parser = argparse.ArgumentParser(
        description="Predict a user's rating for a movie.",
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
        help=(
            "Predict a user's rating for a movie with the item-item algorithm."
        ),
        description="""\
        Predict a user's rating for a movie with the item-item algorithm. Note
        that prediction quality depends on the completeness of the item-item
        similarity model. The model is filled in by running 'mr-analyze ii
        ...'.
        """,
    )
    add_user_id_arg(parser)
    add_movie_id_arg(parser)
    parser.set_defaults(func=handle_ii)


def add_ml_subcommand(subparsers):
    """Add the ml subcommand to an argparse subparsers object."""
    parser = subparsers.add_parser(
        'ml',
        help="""\
        Predict a user's rating for a movie with the machine learning
        algorithm.
        """,
    )
    parser.add_argument(
        '--predictor',
        help='The type of univariate predictor to use, e.g. "year".',
    )
    add_user_id_arg(parser)
    add_movie_id_arg(parser)
    parser.set_defaults(func=handle_ml)


def add_user_id_arg(parser):
    """Add the positional ``user_id`` parameter to a parser."""
    parser.add_argument(
        'user_id',
        help='The user for which a prediction is being made.',
        type=to_user_id,
    )


def add_movie_id_arg(parser):
    """Add the positional ``movie_id`` parameter to a parser."""
    parser.add_argument(
        'movie_id',
        help='The movie for which a prediction is being made.',
        type=to_movie_id,
    )


def handle_ii(args):
    """Handle the "ii" subcommand."""
    pred = ii.predict_rating_for_predict(args.user_id, args.movie_id)
    movie = read.title(pred.movie)
    pred_rating = f'{pred.pred_rating:.1f}'
    reason = REASONS[pred.reason]
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
        predictor = ml.make_predictor(args.user_id, args.predictor)
    except exceptions.NoSuchPredictorError as err:
        print(err, file=sys.stderr)
        exit(1)

    # Make a prediction.
    try:
        prediction = predictor(args.movie_id)  # movie_id
    except exceptions.NoMovieYearError:
        print(
            "This user's movie preferences are best predicted by movie "
            'release year, but the movie for which a prediction is requested '
            "doesn't have year information in its title. Movie title: "
            f'{read.title(args.movie_id)}',
            file=sys.stderr,
        )
        exit(1)

    print(f'{prediction:.1f}')
