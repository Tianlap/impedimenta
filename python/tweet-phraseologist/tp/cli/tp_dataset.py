# coding=utf-8
"""A CLI tool to manage datasets."""
import argparse
import pathlib
import sys

from tp import datasets, exceptions


def main() -> None:
    """Parse arguments and call business logic."""
    # The `dest` argument is a workaround for a bug in argparse. See:
    # https://stackoverflow.com/questions/23349349/argparse-with-required-subparser
    parser = argparse.ArgumentParser(
        description='Manage datasets.',
        epilog="""\
        A dataset is a corpus of tweets in CSV format, possibly spread across
        multiple CSV files. A dataset is installed if it's in a
        :data:`tp.constants.DATASETS_DIR`.
        """,
    )
    subparsers = parser.add_subparsers(dest='subcommand', required=True)
    add_install_subcommand(subparsers)
    add_installable_subcommand(subparsers)
    add_installed_subcommand(subparsers)
    add_uninstall_subcommand(subparsers)
    args = parser.parse_args()
    args.func(args)


def add_installable_subcommand(subparsers) -> None:
    """Add the installable subcommand to an argparse subparsers object."""
    parser: argparse.ArgumentParser = subparsers.add_parser(
        'installable',
        help='List datasets which may be installed.',
        description="""
        List datasets which may be installed. A dataset is considered
        installable even if that dataset has already been installed (in which
        case nothing should happen) or if the requisite archive is absent. The
        only requirement is that a procedure for installing that dataset
        exists.
        """,
    )
    parser.set_defaults(func=handle_installable)


def add_install_subcommand(subparsers) -> None:
    """Add the install subcommand to an argparse subparsers object."""
    helptext = 'Install a dataset.'
    parser: argparse.ArgumentParser = subparsers.add_parser(
        'install',
        help=helptext,
        description=helptext,
    )
    parser.add_argument(
        'dataset',
        help='The dataset to install.',
        choices=datasets.manageable().keys(),
    )
    parser.add_argument(
        '--archive',
        help='Install from the given archive.',
        type=pathlib.Path,
    )
    parser.set_defaults(func=handle_install)


def add_installed_subcommand(subparsers) -> None:
    """Add the installed subcommand to an argparse subparsers object."""
    helptext = 'List datasets which are installed.'
    parser: argparse.ArgumentParser = subparsers.add_parser(
        'installed',
        help=helptext,
        description=helptext,
    )
    parser.add_argument(
        '--path',
        help='List the path to each dataset.',
        action='store_true',
    )
    parser.set_defaults(func=handle_installed)


def add_uninstall_subcommand(subparsers) -> None:
    """Add the uninstall subcommand to an argparse subparsers object."""
    parser: argparse.ArgumentParser = subparsers.add_parser(
        'uninstall',
        help='Uninstall a dataset.',
        description="""\
        Uninstall a dataset. Return non-zero if the dataset to uninstall is not
        currently installed.
        """,
    )
    parser.add_argument(
        'dataset',
        help='The dataset to uninstall.',
        choices=datasets.manageable().keys(),
    )
    parser.set_defaults(func=handle_uninstall)


def handle_installable(_) -> None:
    """Handle the "installable" subcommand."""
    for name in datasets.manageable():
        print(name)


def handle_install(args: argparse.Namespace) -> None:
    """Handle the "install" subcommand."""
    try:
        datasets.manageable()[args.dataset].install(archive=args.archive)
    except exceptions.DatasetInstallError as err:
        print(err, file=sys.stderr)
        exit(1)


def handle_installed(args: argparse.Namespace) -> None:
    """Handle the "installed" subcommand."""
    installed_datasets = datasets.installed()
    if args.path:
        for dataset_path in installed_datasets.values():
            print(dataset_path)
    else:
        for dataset_name in installed_datasets:
            print(dataset_name)


def handle_uninstall(args: argparse.Namespace) -> None:
    """Handle the "uninstall" subcommand."""
    try:
        datasets.manageable()[args.dataset].uninstall()
    except exceptions.DatasetNotFoundError as err:
        print(err, file=sys.stderr)
        exit(1)
