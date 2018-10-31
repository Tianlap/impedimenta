# coding=utf-8
"""Tools for analyzing the database, for the item-item algorithm."""
import itertools
import math
import multiprocessing

from movie_recommender import exceptions
from movie_recommender.constants import (
    JOBS_PER_PROCESS_PER_BATCH,
    MIN_PAIRS_FOR_SIMILARITY,
)
from movie_recommender.db import calc, common, count, read, write


def analyze_users(overwrite, jobs, reporter=None):
    """Compute the average of each user's ratings.

    :meth:`compute_similarity` makes heavy use of users' average ratings. For
    it to work efficiently, these average ratings should be pre-computed. This
    method does just that.

    :param overwrite: Should already-computed values be re-computed?
    :param jobs: The number of processes to spawn. If ``None``, spawn one per
        CPU.
    :param reporter: A function that reports progress to the user. Must accept
        one argument, where that argument is a multiprocessing ``Connection``
        object. Values from 0 to 1, inclusive, will be sent.  If ``None``,
        progress isn't reported.
    :return: Nothing.
    """
    caur_args = gen_caur_args(overwrite, reporter)
    jobs_per_batch = JOBS_PER_PROCESS_PER_BATCH * jobs
    with multiprocessing.Pool(jobs) as pool:
        while True:
            batch = itertools.islice(caur_args, jobs_per_batch)
            try:
                batch_head = next(batch)  # pull val from caur_args
            except StopIteration:
                break
            # chunksize chosen empirically with an R7 1700 CPU and a no-op
            # func. For details, see JOBS_PER_PROCESS_PER_BATCH.
            avg_ratings = tuple(pool.imap_unordered(
                func=call_caur,
                iterable=itertools.chain((batch_head,), batch),
                chunksize=4,
            ))
            write.avg_ratings(avg_ratings)


def call_caur(user_id):
    """Call :meth:`movie_recommender.db.calc.avg_user_rating`."""
    avg_rating = calc.avg_user_rating(user_id)
    return common.AvgRating(user_id, avg_rating)


def gen_caur_args(overwrite, reporter=None):
    """Yield user IDs.

    If ``overwrite`` is true, this function yields every user's ID. Otherwise,
    it yields the ID of every user that isn't yet in the avgRatings database
    table.

    :param overwrite: Should already-computed values be overwritten?
    :param reporter: A function that reports progress to the user. Must accept
        one argument, where that argument is a multiprocessing ``Connection``
        object. Values from 0 to 1, inclusive, will be sent.  If ``None``,
        progress isn't reported.
    :return: A generator that yields user IDs. These values may be passed to
        :meth:`movie_recommender.db.calc.avg_user_rating`.
    """
    users = read.users()
    if not overwrite:
        users.difference_update(read.users_in_avg_ratings())

    if reporter:
        num_users = len(users)
        users_yielded = 0
        conn_out, conn_in = multiprocessing.Pipe(duplex=False)
        proc = multiprocessing.Process(target=reporter, args=(conn_out,))
        proc.start()

    for user in users:
        yield user

        if reporter:
            users_yielded += 1
            if users_yielded % JOBS_PER_PROCESS_PER_BATCH == 0:
                conn_in.send(users_yielded / num_users)

    if reporter:
        conn_in.send(1)
        conn_in.close()
        proc.join()


def analyze_movies(movies, users, overwrite, jobs, reporter=None):
    """Analyze movies.

    The item-item movie prediction algorithm works by comparing a target movie
    to the movies a user has watched. Various types if inferences can then be
    drawn. For example:

    * If the target movie is similar to the movies the user likes, then the
      user will probably like the target movie.
    * If the target movie is similar to the movies the user dislikes, then the
      user will probably dislike the target movie.

    ...and so on. For the algorithm to work efficiently, movie similarity
    should be pre-computed. This function does just that. As pseudo-code, this
    function does the following::

        compute_user_avg_ratings()
        for target_movie in target_movies:
            for movie in all_movies:
                if target_movie == movie:
                    continue
                compute_similarity(target_movie, movie)

    :param movies: Movie IDs. Movies to be analyzed. These movies are merged
        into the ``target_movies`` set.
    :param users: User IDs. The movies these users have rated are merged into
        the ``target_movies`` set.
    :param overwrite: Should already-computed values be re-computed?
    :param jobs: How many processes should be spawned? If none, spawn one per
        CPU.
    :param reporter: A function that reports progress to the user. Must accept
        one argument, where that argument is a multiprocessing ``Connection``
        object. Values from 0 to 1, inclusive, will be sent.  If ``None``,
        progress isn't reported.
    :return: Nothing.
    """
    cs_args = gen_cs_args(movies, users, overwrite, reporter)
    jobs_per_batch = JOBS_PER_PROCESS_PER_BATCH * jobs
    with multiprocessing.Pool(jobs) as pool:
        while True:
            batch = itertools.islice(cs_args, jobs_per_batch)
            try:
                batch_head = next(batch)  # pull val from cs_args
            except StopIteration:
                break
            similarities = tuple(pool.imap_unordered(
                func=call_cs,
                iterable=itertools.chain((batch_head,), batch),
            ))
            write.similarities(similarities)


def call_cs(args):
    """Call :meth:`movie_recommender.analyze.ii.compute_similarity`."""
    score = compute_similarity(*args)
    return common.Similarity(*args, score)


def gen_cs_args(movies, users, overwrite, reporter=None):
    """Generate pairs of movies for whom similarity should be computed.

    As pseudo-code, this method does the following::

        target_movies = {2, 4}
        all_movies = {1, 2, 3, 4, 5}
        for movie in all_movies:
            for target_movie in target_movies:
                if problematic(target_movie, movie):
                    continue
                yield (target_movie, movie)

    This function will yield pairs like the following:

    * 1, 2
    * 1, 4
    * 2, 2
    * 2, 4
    * 3, 2
    * 3, 4
    * 4, 2
    * 4, 4
    * 5, 2
    * 5, 4

    These pairs may be passed to
    :meth:`movie_recommender.analyze.ii.compute_similarity`. What constitutes a
    "problematic" pair of movie IDs?

    * Within this application, it's illegal to compute the similarity between a
      movie and itself. As a result, pairs like (2, 2) are problematic.
    * Within this application, similarity is symmetric. It's pointless to
      calculate the similarity between both (2, 4) and (4, 2). One of these
      pairs is problematic.
    * If similarity has already been calculated for a pair of movie IDs, and if
      similarity scores shouldn't be overwritten, then that pair of movie IDs
      is problematic.

    :param movies: Movie IDs. Movies to be analyzed. These movies are merged
        into the ``target_movies`` set.
    :param users: User IDs. The movies these users have rated are merged into
        the ``target_movies`` set.
    :param overwrite: Should already-computed similarities be re-computed?
    :param reporter: A function that reports progress to the user. Must accept
        one argument, where that argument is a multiprocessing ``Connection``
        object. Values from 0 to 1, inclusive, will be sent.  If ``None``,
        progress isn't reported.
    :return: A generator that yields tuples of movie IDs.
    """
    # target_movies can be smaller than all_movies. This code attempts to
    # improve efficiency by making the inner for loop iterate over the smaller
    # set, by performing "x in y" loops on the smaller set, and by keeping a
    # database connection open.
    #
    # Ideally, we would take advantage of the fact that all_movies() is a
    # generator. This would improve streaminess. But this function is called by
    # multiple processes, and SQLite objects can't be shared across threads or
    # processes.
    #
    # In cases where most of the movies returned by this function have already
    # been analyzed, this function is a bottleneck. However, in the presumably
    # more common case where most movies *haven't* been analyzed,
    # compute_similarity() is the bottleneck. Consequently, although there is
    # value in multiprocessing in this function, one should be careful to avoid
    # over-allocating resources here and causing pointless context switches.
    #
    # In addition, using processes has some overhead. Notably, when a master
    # process calls a worker process, arguments are shipped via pickling.
    all_movies = set(read.all_movies())
    target_movies = set(movies).union(set(read.rated_movies(users)))

    if reporter:
        num_pairs = len(all_movies) * len(target_movies)
        pairs_yielded = 0
        conn_out, conn_in = multiprocessing.Pipe(duplex=False)
        proc = multiprocessing.Process(target=reporter, args=(conn_out,))
        proc.start()

    for movie in all_movies:
        for target_movie in target_movies:

            # Skip (2, 2).
            if movie == target_movie:
                continue

            # Skip (4, 2). Process (2, 4).
            if movie in target_movies and movie > target_movie:
                continue

            # Overwrite an already-computed similarity score?
            if not overwrite and similarity_computed(movie, target_movie):
                continue

            yield (movie, target_movie)

            if reporter:
                pairs_yielded += 1
                if pairs_yielded % JOBS_PER_PROCESS_PER_BATCH == 0:
                    conn_in.send(pairs_yielded / num_pairs)

    if reporter:
        conn_in.send(1)
        conn_in.close()
        proc.join()


def compute_similarity(movie_a, movie_b):
    """Compute the similarity between two movies.

    Use the "adjusted cosine similarity" formula to compute similarity.

    :param movie_a: A movie ID. A movie to compare.
    :param movie_b: A movie ID. A movie to compare.
    :return: A value between -1 and 1, inclusive. If there are too few pairs of
        ratings for both of the given movies, then return 0. For more on this,
        see :data:`movie_recommender.constants.MIN_PAIRS_FOR_SIMILARITY`.
    :raise: ``ValueError`` if ``movie_a`` and ``movie_b`` are equal.
    :raise movie_recommender.exceptions.MissingAverageRatingError: If the
        average of a user's ratings hasn't been pre-computed.
    """
    # Are we computing the similarity between a movie and itself?
    if movie_a == movie_b:
        raise ValueError(
            f"""
            Computing the similarity between a movie and itself is disallowed.
            Movie IDs: {movie_a}, {movie_b}
            """
        )

    # Are there enough rating pairs to confidently compute a similarity score?
    if count.rating_pairs(movie_a, movie_b) < MIN_PAIRS_FOR_SIMILARITY:
        return 0

    # This formula makes heavy use of users' average ratings. For efficiency
    # reasons, they must be precomputed. Are they?
    num_avg_ratings = count.avg_ratings()
    num_user_ids = count.user_ids()
    if num_avg_ratings < num_user_ids:
        raise exceptions.MissingAverageRatingError(
            f"""
            The adjusted cosine similarity algorithm requires that the average
            ratings given by each user be precomputed. However, there are
            {num_avg_ratings} precomputed average ratings, and {num_user_ids}
            users.
            """
        )

    # All pre-flight checks have passed. The exception handling is stupid. See
    # the comments in the called function.
    try:
        return compute_similarity_unsafe(movie_a, movie_b)
    except ZeroDivisionError:
        return 0


def compute_similarity_unsafe(movie_a, movie_b):
    """Compute the similarity between two movies.

    Use the "adjusted cosine similarity" formula to compute similarity.
    Consider using :meth:`movie_recommender.analyze.ii.compute_similarity`
    instead.

    Certain pathological data sets will cause this function to throw an
    exception. As an example, consider the following scenario, where only one
    user has rated both ``movie_a`` and ``movie_b``:

    =======  ==============  ==============
    User ID  Movie A rating  Movie B rating
    =======  ==============  ==============
    554      5.0             4.0
    =======  ==============  ==============

    If the average of user 554's ratings is 4.0, then division by zero will
    occur. In this case, one can't reasonably assume that the similarity is 0,
    or 1, or anything else. Instead, the ideal solution is to re-compute the
    similarity between these two movies with a different formula, such as
    cosine-based similarity or correlation-based similarity.

    Also see: https://stackoverflow.com/a/40651746

    :param movie_a: A movie ID. A movie to compare.
    :param movie_b: A movie ID. A movie to compare.
    :return: A value between -1 and 1, inclusive.
    :raise: ``ZeroDivisionError`` for certain pathological datasets.
    """
    numerator = 0
    denominator_left = 0
    denominator_right = 0
    for rating_pair in read.rating_pairs(movie_a, movie_b):
        avg_rating = read.avg_rating(rating_pair.user_id)
        numerator += (
            (rating_pair.rating_a - avg_rating) * (rating_pair.rating_b - avg_rating)
        )
        denominator_left += (rating_pair.rating_a - avg_rating)**2
        denominator_right += (rating_pair.rating_b - avg_rating)**2
    denominator = math.sqrt(denominator_left) * math.sqrt(denominator_right)
    return numerator / denominator


def similarity_computed(movie_a, movie_b):
    """Tell whether a similarity score has been computed for the given movies.

    :param movie_a: A movie ID.
    :param movie_b: A movie ID.
    :return: True if a score exists, false otherwise.
    """
    try:
        read.similarity(movie_a, movie_b)
    except exceptions.MissingSimilarityError:
        return False
    return True
