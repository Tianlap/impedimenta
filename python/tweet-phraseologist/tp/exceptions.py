# coding=utf-8
"""Custom exeptions."""


class DatabaseAlreadyExistsError(Exception):
    """Indicates that a database already exists when it shouldn't.

    For example, this might be raised if this application is asked to create a
    new database and one already exists.
    """


class DatabaseNotFoundError(Exception):
    """Indicates that the database can't be found."""


class DatasetNotFoundError(Exception):
    """Indicates that a requested dataset can't be found."""


class DatasetInstallError(Exception):
    """Indicates that a dataset can't be installed."""
