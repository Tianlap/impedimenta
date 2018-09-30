# coding=utf-8
"""Predict a user's rating for a movie."""
import argparse
import sys

from movie_recommender import predict, db, exceptions
from movie_recommender.cli.utils import to_movie_id, to_user_id


def main():
    """Parse arguments and call business logic."""
    args = parse_args()

    # Retrieve the best type of predictor for this user.
    if args.predictor is None:
        try:
            args.predictor = db.get_predictor_name(args.user_id)
        except exceptions.NoPersonalizedPredictorError as err:
            print(err, file=sys.stderr)
            exit(1)

    # Make a predictor of that type.
    try:
        predictor = predict.make_predictor(args.user_id, args.predictor)
    except exceptions.NoSuchPredictorError as err:
        print(err, file=sys.stderr)
        exit(1)

    # Make a prediction.
    try:
        prediction = predictor(args.movie_id)  # movie_id
    except exceptions.NoMovieYearError as err:
        print(
            "This user's movie preferences are best predicted by movie "
            'release year, but the movie for which a prediction is requested '
            "doesn't have year information in its title. Movie title: "
            f'{db.get_title(args.movie_id)}',
            file=sys.stderr,
        )
        exit(1)

    print(f'{prediction:.1f}')


def parse_args():
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Predict a user's rating for a movie.",
    )
    parser.add_argument(
        'user_id',
        help='The user for which a prediction is being made.',
        type=to_user_id,
    )
    parser.add_argument(
        'movie_id',
        help='The movie for which a prediction is being made.',
        type=to_movie_id,
    )
    parser.add_argument(
        '--predictor',
        help='The type of univariate predictor to use, e.g. "year".',
    )

    return parser.parse_args()
