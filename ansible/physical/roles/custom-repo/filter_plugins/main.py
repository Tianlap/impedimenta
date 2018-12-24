# coding=utf-8
"""Custom filters."""
from pathlib import PurePath

from typing import Callable, Mapping


class FilterModule():  # pylint:disable=too-few-public-methods
    """Turn functions into filters."""

    @staticmethod
    def filters() -> Mapping[str, Callable]:
        """Return custom filters."""
        return {
            'custom_repo_db': custom_repo_db,
            'custom_repo_path': custom_repo_path,
        }


def custom_repo_db(custom_repo: Mapping[str, str]) -> str:
    """Generate the path to a custom repository's database.

    :param custom_repo: A dict containing at least the keys ``path_prefix`` and
        ``name``.
    :return: The path to the given custom repository's database.
    """
    repo_path = custom_repo_path(custom_repo)
    db_path = PurePath(repo_path, custom_repo['name'] + '.db.tar.xz')
    return str(db_path)


def custom_repo_path(custom_repo: Mapping[str, str]) -> str:
    """Generate the path to a custom repository.

    :param custom_repo: A dict containing at least the keys ``path_prefix`` and
        ``name``.
    :return: The path to the given custom repository.
    """
    repo_path = PurePath(custom_repo['path_prefix'], custom_repo['name'])
    return str(repo_path)
