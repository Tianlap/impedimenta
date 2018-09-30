# coding=utf-8
"""Manage Movie Recommender data sets."""
import argparse

from movie_recommender.constants import DATASETS
from movie_recommender.datasets import Dataset, get_installed_datasets


def main():
    """Parse arguments and call business logic."""
    args = parse_args()
    args.func(args)


def parse_args():
    """Parse CLI arguments."""
    # The `dest` argument is a workaround for a bug in argparse. See:
    # https://stackoverflow.com/questions/23349349/argparse-with-required-subparser
    parser = argparse.ArgumentParser(
        description='Manage Movie Recommender data sets.',
    )
    subparsers = parser.add_subparsers(dest='subcommand', required=True)
    _add_absent_subcommand(subparsers)
    _add_install_subcommand(subparsers)
    _add_present_subcommand(subparsers)
    return parser.parse_args()


# The dispatching technique in main() is elegant enough (read: low-maintenance)
# that some wastefulness is OK. See:
# https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_subparsers
def handle_absent(args):  # pylint:disable=unused-argument
    """Handle the "absent" subcommand."""
    datasets = get_installed_datasets()
    absent_dataset_names = set(DATASETS.keys()) - set(datasets.keys())
    for absent_dataset_name in absent_dataset_names:
        print(absent_dataset_name)


def handle_install(args):
    """Handle the "install" subcommand."""
    dataset = Dataset(args.dataset)
    dataset.download()
    dataset.install()


def handle_present(args):
    """Handle the "present" subcommand."""
    datasets = get_installed_datasets()
    if args.paths:
        for dataset_path in datasets.values():
            print(dataset_path)
    else:
        for dataset_name in datasets:
            print(dataset_name)


def _add_absent_subcommand(subparsers):
    """Add the absent subcommand to an argparse subparsers object."""
    helptext = "List datasets which aren't installed."
    parser_absent = subparsers.add_parser(
        'absent',
        help=helptext,
        description=helptext,
    )
    parser_absent.set_defaults(func=handle_absent)


def _add_install_subcommand(subparsers):
    """Add the install subcommand to an argparse subparsers object."""
    parser_install = subparsers.add_parser(
        'install',
        help='Install a dataset.',
        description="""\
        Install a dataset. If the source archive hasn't yet been downloaded
        (with the "download" subcommand), it will automatically be downloaded.
        """,
    )
    parser_install.add_argument(
        'dataset',
        help='The dataset to install.',
        choices=DATASETS.keys(),
    )
    parser_install.set_defaults(func=handle_install)


def _add_present_subcommand(subparsers):
    """Add the present subcommand to an argparse subparsers object."""
    helptext = 'List installed datasets.'
    parser_present = subparsers.add_parser(
        'present',
        help=helptext,
        description=helptext,
    )
    parser_present.add_argument(
        '--paths',
        help='List the paths to the datasets, instead of their names.',
        action='store_true',
    )
    parser_present.set_defaults(func=handle_present)
