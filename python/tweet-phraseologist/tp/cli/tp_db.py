# coding=utf-8
"""A CLI tool to manage Tweet Phraseologist's database."""
import argparse
import sys
from pathlib import Path
from typing import Callable

from tp import datasets, exceptions
from tp.db import common, init


def main() -> None:
    """Parse arguments and call business logic."""
    # The `dest` argument is a workaround for a bug in argparse. See:
    # https://stackoverflow.com/questions/23349349/argparse-with-required-subparser
    parser = argparse.ArgumentParser(description='Manage database.')
    subparsers = parser.add_subparsers(dest='subcommand', required=True)
    add_cpop_subcommand(subparsers)
    add_load_path_subcommand(subparsers)
    add_save_path_subcommand(subparsers)
    args = parser.parse_args()
    args.func(args)


def add_cpop_subcommand(subparsers) -> None:
    """Add the cpop subcommand to an argparse subparser."""
    msg = 'Create and populate a database.'
    parser: argparse.ArgumentParser = subparsers.add_parser(
        'cpop',
        help=msg,
        description=msg,
    )
    parser.add_argument(
        'dataset',
        help='The dataset to use when populating the database.',
        choices=datasets.installed().keys(),
    )
    parser.add_argument(
        '--overwrite',
        help='Overwrite an existing database if one exists.',
        action='store_true',
    )
    func: Callable[[argparse.Namespace], None] = handle_cpop
    parser.set_defaults(func=func)


def add_load_path_subcommand(subparsers) -> None:
    """Add the load-path subcommand to an argparse subparser."""
    parser: argparse.ArgumentParser = subparsers.add_parser(
        'load-path',
        help='Search for a database file.',
        description="""\
        Search several paths for a database file, in order of preference. If a
        file is found, print its path. Otherwise, return a non-zero exit code.
        """,
    )
    func: Callable[[argparse.Namespace], None] = handle_load_path
    parser.set_defaults(func=func)


def add_save_path_subcommand(subparsers) -> None:
    """Add the save-path subcommand to an argparse subparser."""
    parser: argparse.ArgumentParser = subparsers.add_parser(
        'save-path',
        help='Print the path to where a new database will be created.',
        description="""\
        Print the path to where a new database will be created when the 'cpop'
        subcommand is executed. As a side effect, create all directories in the
        path that don't yet exist.
        """,
    )
    func: Callable[[argparse.Namespace], None] = handle_save_path
    parser.set_defaults(func=func)


def handle_cpop(args: argparse.Namespace) -> None:
    """Handle the 'cpop' subcommand."""
    if args.overwrite:
        path = Path(common.get_save_path())
        try:
            path.unlink()
        except FileNotFoundError:
            pass
    try:
        init.cpop(args.dataset)
    except exceptions.DatabaseAlreadyExistsError as err:
        print(err, file=sys.stderr)
        exit(1)


def handle_load_path(_) -> None:
    """Handle the "load-path" subcommand."""
    try:
        print(common.get_load_path())
    except exceptions.DatabaseNotFoundError:
        exit(1)


def handle_save_path(_) -> None:
    """Handle the 'save-path' subcommand."""
    print(common.get_save_path())
