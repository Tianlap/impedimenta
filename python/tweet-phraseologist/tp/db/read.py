# coding=utf-8
"""Functions for reading from the database."""
from typing import Any, Iterator, Iterable, Optional, Set

from tp.db import common


def parties() -> Set[str]:
    """Get the political parties of people who have written tweets."""
    with common.get_db_conn() as conn:
        return {
            row[0] for row in conn.execute('SELECT DISTINCT party FROM handles')
        }


def tweets(party: Optional[str]) -> Iterator[str]:
    """Yield tweet cells from the tweets table.

    :param party: The party whose tweets shall be selected. If ``None``, select
        all tweets.
    :return: An iterator yielding tweets.
    :raise: ``ValueError`` if ``party`` not in :func:`tp.db.read.parties`.
    """
    query: str
    args: Iterable[Any]
    if party:
        _check_party(party)
        query = """
        SELECT tweet
        FROM tweets
        WHERE tweets.party = ?
        """
        args = (party,)
    else:
        query = 'SELECT tweet FROM tweets'
        args = ()
    with common.get_db_conn() as conn:
        for row in conn.execute(query, args):
            yield row[0]


def _check_party(party: str):
    parties_ = parties()
    if party not in parties_:
        raise ValueError(f'{party} not in {parties_}')
