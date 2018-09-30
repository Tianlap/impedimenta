# coding=utf-8
"""Recommend movies for a user."""
import argparse

from movie_recommender import predict, db
from movie_recommender.cli.utils import to_user_id


def main():
    """Parse arguments and call business logic."""
    args = parse_args()
    if args.user_ids is None:
        args.user_ids = db.get_user_ids()
    predict.analyze_users(args.user_ids, args.overwrite, args.jobs)


def parse_args():
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description="""\
        Create a personalized predictor for each user. This must be done before
        one can ask for movie predictions or recommendations. At this time,
        only univariate machine learning-based predictors can be created. Other
        types of predictors, such as user-user and user-item, are not
        supported.
        """,
    )
    parser.add_argument(
        '--user-ids',
        help='Create predictors for these users, instead of all users.',
        nargs='+',
        type=to_user_id,
    )
    parser.add_argument(
        '-j',
        '--jobs',
        help='Spawn this many processes, instead of one per CPU.',
        type=int,
    )

    # --{no-,}overwrite
    # See: https://stackoverflow.com/a/15008806
    parser_overwrite = parser.add_mutually_exclusive_group(required=False)
    parser_overwrite.add_argument(
        '--overwrite',
        action='store_true',
        dest='overwrite',
        help="""\
        If a user already has a personalized predictor, create a new one, and
        overwrite the old one.
        """,
    )
    parser_overwrite.add_argument(
        '--no-overwrite',
        action='store_false',
        dest='overwrite',
        help="""\
        If a user already has a personalized predictor, do no analysis for that
        user, and leave the old one in place.
        """,
    )
    parser.set_defaults(overwrite=True)

    return parser.parse_args()
