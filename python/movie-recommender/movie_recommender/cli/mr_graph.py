# coding=utf-8
"""Make a graph from a pair of columns in a CSV file, and analyze it."""
import argparse
import csv
from collections import namedtuple

from movie_recommender.graph import Graph, Point


def main():
    """Parse arguments and call business logic."""
    args = parse_args()
    graph = Graph(tuple(get_points(
        args.input,
        Columns(args.x_column, args.y_column),
        header_rows=args.header_rows,
    )))
    print(f'y = {graph.slope:g} × x + {graph.y_intercept:g}')
    print(f'sse = {graph.sse:g}')


def parse_args():
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description="""\
        Make a graph from a pair of columns in a CSV file, and analyze it.
        """,
    )
    parser.add_argument(
        'input',
        type=argparse.FileType('r'),
        help="""\
        A CSV file describing a scatter plot, where each row describes one
        point. Each row must be in "X,Y" format, e.g. "2,3.5". If "-" is
        passed, values are read from stdin.
        """,
    )
    parser.add_argument(
        'x_column',
        type=int,
        help='The index of the column to read in as the "x" value.',
    )
    parser.add_argument(
        'y_column',
        type=int,
        help='The index of the column to read in as the "y" value.',
    )
    parser.add_argument(
        '--header-rows',
        type=int,
        default=0,
        help="""\
        The number of header rows in the input file. Header rows are ignored.
        Defaults to "0".
        """,
    )
    return parser.parse_args()


Columns = namedtuple('Columns', ('x', 'y'))
"""A pair of columns in a CSV file.

Indices are zero-based. Given this CSV file::

    0,1,2,3
    10,11,12,13

Then this object::

    Columns(x=0, y=3)

References the values 0, 10, 3, and 13.
"""


def get_points(input_stream, columns, *, header_rows=0):
    """Consume an input stream, yielding an x,y point for each line.

    :param input_stream: A `text I/O`_ stream, where eacah line is CSV data in
        "x,y" format.
    :param Columns columns: The columns to read from the CSV file.
    :param header_rows: The number of header rows in the input file. Header
        rows are ignored.
    :returns: A generator yielding :class:`movie_recommender.graph.Point`
        instances.
    :raises: A ``TypeError`` if an input line doesn't have exactly two fields.

    .. _text I/O: https://docs.python.org/3/library/io.html#text-i-o
    """
    current_line = 0
    reader = csv.reader(input_stream)
    for row in reader:
        current_line += 1
        if current_line <= header_rows:
            continue
        x = float(row[columns.x])
        y = float(row[columns.y])
        yield Point(x, y)
