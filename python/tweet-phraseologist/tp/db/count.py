# coding=utf-8
"""Functions for counting rows in the database."""
from typing import Any, Optional, Tuple

from tp.db import common


def tweets(party: Optional[str] = None) -> int:
    """Count the number of tweets.

    :param party: Count tweets made by the given party, instead of all tweets.
    """
    query: str
    args: Tuple[Any, ...]
    if party:
        query = 'SELECT COUNT(*) FROM tweets WHERE party = ?'
        args = (party,)
    else:
        query = 'SELECT COUNT(*) FROM tweets'
        args = ()
    with common.get_db_conn() as conn:
        return conn.execute(query, args).fetchone()[0]
