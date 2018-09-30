# coding=utf-8
"""Recommend movies for a user."""
import argparse
import sys

from movie_recommender import db, exceptions, predict, recommend
from movie_recommender.cli.utils import to_user_id


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

    # Make recommendations.
    recs = recommend.recommend(args.user_id, args.count, predictor)
    for i, rec in enumerate(recs):
        print(f'{i + 1}. {rec.movie_name} ({rec.pred_rating:.1f})')


def parse_args():
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description='Recommend movies for a user.',
    )
    parser.add_argument(
        'user_id',
        help='The user for which recommendations are being generated.',
        type=to_user_id,
    )
    parser.add_argument(
        '--count',
        help='The number of recommendations to emit.',
        default=5,
        type=int,
    )
    parser.add_argument(
        '--predictor',
        help='The type of univariate predictor to use, e.g. "year".',
    )
    return parser.parse_args()
