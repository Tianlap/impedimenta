# coding=utf-8
"""Constants for use by the entire application."""
from pathlib import PurePath


XDG_DIR = PurePath('tweet-phraseologist')
"""The basename of this application's directories.

For more information, see the `XDG Base Directory Specification
<https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html>`_.
"""

ARCHIVES_DIR = PurePath(XDG_DIR, 'archives')
"""The basename of an archives directory.

A dataset archive shouldn't be placed directly in an :data:`XDG_DIR`, as doing
so can cause name conflicts. It's better to place such files in a dedicated
directory.
"""

DATASETS_DIR = PurePath(XDG_DIR, 'datasets')
"""The basename of the paths that contain datasets.

A dataset shouldn't be placed directly in an :data:`XDG_DIR`, as doing so can
cause name conflicts. It's better to place such files in a dedicated directory.
"""

DB_FILE = PurePath(XDG_DIR, 'db.db')
"""The path to the database."""
