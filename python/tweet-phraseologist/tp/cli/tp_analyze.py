# coding=utf-8
"""A CLI tool to analyze tweets."""
import argparse
import csv
import sys
from typing import Mapping, Tuple

from tp import analyze
from tp.db import read
from tp.cli.utils import add_jobs_flag, non_negative_int


def main() -> None:
    """Parse arguments and call business logic."""
    parser = argparse.ArgumentParser(
        description='Analyze tweets.',
        epilog="""
        Analyze tweets in the database. Analysis is currently limited to
        finding common ngrams.
        """,
    )
    add_jobs_flag(parser)
    default_count = 5
    parser.add_argument(
        '--count',
        help=f'The number of results to return, instead of {default_count}.',
        type=non_negative_int,
        default=default_count,
    )
    default_ngram_length = 2
    parser.add_argument(
        '--ngram-length',
        help=f"""
        Find ngrams of the given length, instead of {default_ngram_length}.
        """,
        type=non_negative_int,
        default=default_ngram_length,
    )
    parser.add_argument(
        '--party',
        help="""
        Analyze tweets written by members of the given party, instead of all
        tweets.
        """,
        type=str,
        choices=read.parties(),
    )
    parser.add_argument(
        '--unique',
        help="""
        Only print ngrams that are unique to the specified party. Only has an
        effect if --party is specified.
        """,
        action='store_true',
    )
    args = parser.parse_args()
    if args.unique:
        handle_root_unique(args)
    else:
        handle_root(args)


def handle_root(args: argparse.Namespace) -> None:
    """Handle the root command."""
    ngrams = analyze.count_ngrams_in_tweets(
        args.jobs,
        ngram_len=args.ngram_length,
        party=args.party,
    )
    print_top_ngrams(ngrams, args.count)


def handle_root_unique(args: argparse.Namespace) -> None:
    """Handle the root command where ``--unique`` was passed."""
    # Calculate ngrams on a per-party basis.
    ngrams_by_party = {}
    for party in read.parties():
        ngrams_by_party[party] = analyze.count_ngrams_in_tweets(
            args.jobs,
            ngram_len=args.ngram_length,
            party=party,
        )

    # Figure out which ngrams are unique to this party.
    target_ngrams = ngrams_by_party.pop(args.party)
    for other_ngrams in ngrams_by_party.values():
        for ngram in other_ngrams:
            target_ngrams.pop(ngram, None)
    print_top_ngrams(target_ngrams, args.count)


def print_top_ngrams(ngrams: Mapping[Tuple[str, ...], int], count: int) -> None:
    """Print the top ``count`` ngrams."""
    sorted_ngrams = sorted(
        ngrams.items(),
        key=lambda pair: pair[1],
        reverse=True
    )
    writer = csv.writer(sys.stdout)
    for top_ngram in sorted_ngrams[:count]:
        writer.writerow((top_ngram[1], ' '.join(top_ngram[0])))
