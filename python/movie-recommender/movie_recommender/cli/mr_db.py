# coding=utf-8
"""Manage Movie Recommender's database."""
import argparse
import sys
from pathlib import Path

from movie_recommender import exceptions
from movie_recommender.constants import DATASETS
from movie_recommender.db import common, init


def main():
    """Parse arguments and call business logic."""
    args = parse_args()
    args.func(args)


def parse_args():
    """Parse CLI arguments."""
    # The `dest` argument is a workaround for a bug in argparse. See:
    # https://stackoverflow.com/questions/23349349/argparse-with-required-subparser
    parser = argparse.ArgumentParser(
        description="Manage Movie Recommender's database.",
    )
    subparsers = parser.add_subparsers(dest='subcommand', required=True)
    _add_create_subcommand(subparsers)
    _add_load_path_subcommand(subparsers)
    _add_save_path_subcommand(subparsers)
    return parser.parse_args()


def handle_create(args):
    """Handle the "create" subcommand."""
    if args.overwrite:
        path = Path(common.get_save_path())
        if path.exists():
            path.unlink()
    try:
        init.cpop_db(args.dataset)
    except (
            exceptions.DatabaseAlreadyExistsError,
            exceptions.DatasetAbsentError) as err:
        print(err, file=sys.stderr)
        exit(1)


def handle_load_path(args):  # pylint:disable=unused-argument
    """Handle the "load-path" subcommand."""
    try:
        print(common.get_load_path())
    except exceptions.DatabaseNotFoundError:
        exit(1)


def handle_save_path(args):  # pylint:disable=unused-argument
    """Handle the "save-path" subcommand."""
    print(common.get_save_path())


def _add_create_subcommand(subparsers):
    """Add the create subcommand to an argparse subparsers object."""
    helptext = 'Create and populate a database.'
    parser_create = subparsers.add_parser(
        'create',
        help=helptext,
        description=helptext,
    )
    parser_create.add_argument(
        'dataset',
        help='The dataset to use when populating the database.',
        choices=DATASETS.keys(),
    )
    parser_create.add_argument(
        '--overwrite',
        help='Overwrite an existing database if one exists.',
        action='store_true',
    )
    parser_create.set_defaults(func=handle_create)


def _add_load_path_subcommand(subparsers):
    """Add the load-path subcommand to an argparse subparsers object."""
    parser_load_path = subparsers.add_parser(
        'load-path',
        help='Search several paths for a database file.',
        description="""\
        Search several paths for a database file, in order of preference. If a
        file is found, print its path. Otherwise, return a non-zero exit code.
        This path is used when performing analyses and generating movie
        recommendations.
        """
    )
    parser_load_path.set_defaults(func=handle_load_path)


def _add_save_path_subcommand(subparsers):
    """Add the save-path subcommand to an argparse subparsers object."""
    parser_save_path = subparsers.add_parser(
        'save-path',
        help='Print the path to where a new database might be created.',
        description="""\
        Print the path to where a new database might be created. As a
        side-effect, create all directories in the path that don't yet exist.
        This save path is used by sibling commands such as "create."
        """
    )
    parser_save_path.set_defaults(func=handle_save_path)
