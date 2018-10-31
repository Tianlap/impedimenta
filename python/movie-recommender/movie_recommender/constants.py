# coding=utf-8
"""Constants for use by the entire application."""
import re


AVG_RATING = 'avg rating'
"""A reason that a movie recommendation might be given, with item-item.

See :data:`movie_recommender.constants.REASONS`.
"""

SIMILAR = 'similar'
"""A reason that a movie recommendation might be given, with item-item.

See :data:`movie_recommender.constants.REASONS`.
"""

REASONS = {
    AVG_RATING: "because of this movie's average rating.",
    None: 'because the other evaluation strategies are failing.',
    SIMILAR: (
        "because of the similarity between this movie and others you've rated."
    ),
}
"""Reasons that a movie recommendation might be given, with item-item."""

DB_NAME = 'db.db'
"""The basename of Movie Recommender's database file."""

DATASETS = {
    'fixture': None,
    'ml-latest-small': (
        'http://files.grouplens.org/datasets/movielens/ml-latest-small.zip'
    ),
    'ml-20m': 'http://files.grouplens.org/datasets/movielens/ml-20m.zip',
}
"""Datasets this application can manage.

The "fixture" dataset can be created on the fly by this application.
"""

GENRES = {
    '(no genres listed)',
    'Action',
    'Adventure',
    'Animation',
    'Children\'s',
    'Comedy',
    'Crime',
    'Documentary',
    'Drama',
    'Fantasy',
    'Film-Noir',
    'Horror',
    'Musical',
    'Mystery',
    'Romance',
    'Sci-Fi',
    'Thriller',
    'War',
    'Western',
}
"""Movie genres, as listed in the MovieLens ml-latest-small readme.

This is primarily useful when generating genre-based predictors. An alternate
approach would be to dynamically extract genre names from the data sets
themselves, but hard-coding names is quicker, and it avoids issues that arise
when not all genres are represented by a dataset.
"""

JOBS_PER_PROCESS_PER_BATCH = 2**8
"""Jobs processed by each process in each batch of work.

Processes can concurrently read a database. But a process which wishes to
write must obtain a lock on the entire database, and if a process holds
the write lock, no other reads or writes can occur. Furthermore, if a
process wishes to write and it fails to obtain the write lock after five
seconds (by default), then it will throw an exception.

The function(s) which perform calculations (like calculating the average
of a user's ratings, or calculating the similarity of two movies) perform
many reads and no writes. Thus, they can be run in parallel. When should
the results be written, though? If each result is written as soon as it's
available, then a write lock timeout is likely.

The solution adopted here is to process arguments in batches. After each
batch of arguments has been processed, the results are written out.
Increasing the batch size improves processing efficiency, as stopping to
write results means letting the CPU idle. But increasing the batch size
also spaces out write checkpoints and increases memory usage. (Each
batch's work queue and results are held in memory.)

The suggested formula for the number of jobs per batch is::

    jobs_per_batch = JOBS_PER_PROCESS_PER_BATCH * allocated_processes

One can also set chunk size when handing work to processes, e.g. when calling
``subprocess.Pool.imap_unordered``. Increasing this value from its default of 1
helps to amortize per-dispatch overhead. But keeping it low better spreads load
across processes and makes the pickled objects sent to each process smaller.
Make sure to perform empirical measurements when setting this value!
"""

MAX_RATING = 5.0
"""The max rating that a user can assign to a movie."""

MIN_RATING = 0.5
"""The min rating that a user can assign to a movie."""

MIN_PAIRS_FOR_SIMILARITY = 1
"""The number of rating pairs that must exist to compute a similarity score.

When computing the similarity score for a pair of movies, one can ask whether
there are are enough rating pairs to confidently compute a similarity score.
Consider the case where only one user has rated a pair of movies, and the
ratings were both :data:`MAX_RATING`. Does this mean that the two movies are
perfectly similar? Based on this, should a user who liked the first movie be
recommended the second movie? The weighted sum algorithm (as implemented by
:meth:`movie_recommender.predict.ii.predict_rating`) is susceptible to exactly
this sort of issue.

Incrementing this value increases confidence in similarity scores. As a bonus,
it makes the model-building process faster. In one informal test, the command
``mr-analyze ii -m {1..10}`` took:

1. 174 seconds when set to 1.
#. 101 seconds when set to 4.
#. 85 seconds when set to 8.
#. 80 seconds when set to 12.
#. 75 seconds when set to 16.
#. 74 seconds when set to 20.
#. 68 seconds when set to 100.

But! Incrementing this value makes it more likely for the weighted sum
prediction algorithm to completely fail to product a prediction, which forces a
real-world prediction engine to fall back to other measures like using a
movie's average rating.

Furthermore, its not clear that using a small number of confident similarity
scores is actually better than using a larger number of unconfident similarity
scores. Answering this question would require a well-designed and controlled
empirical analysis, and ideally peer review.

Sarwar et al use a value of 1, so this seems like a safe value. Incrementing
this value can be useful for development purposes, when quick-and-dirty
analyses are desired.
"""
assert MIN_PAIRS_FOR_SIMILARITY >= 1

XDG_RESOURCE = 'movie-recommender'
"""The basename of the directories this application uses for data.

For more information, see the `XDG Base Directory Specification
<https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html>`_.
"""

YEAR_MATCHER = re.compile(r'\((\d{4})\)')
"""A compiled regular expression for finding the year in a movie title.

Also see :class:`movie_recommender.exceptions.NoMovieYearError`.
"""
