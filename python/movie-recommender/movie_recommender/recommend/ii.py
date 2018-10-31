# coding=utf-8
"""Tools for generating top-n recommendations with item-item."""
import heapq
import multiprocessing

from movie_recommender.constants import JOBS_PER_PROCESS_PER_BATCH
from movie_recommender.db import count as db_count
from movie_recommender.db import read
from movie_recommender.predict.ii import predict_rating_for_recommend


def recommend(user, count, jobs, reporter=None):
    """Recommend several movies for the given user.

    :param user: A user ID. The user for whom recommendations are being
        generated.
    :param count: The number of recommendations to generate for the given user.
    :param jobs: The number of processes to spawn. If ``None``, spawn one per
        CPU.
    :param reporter: A function that reports progress to the user. Must accept
        one argument, where that argument is a multiprocessing ``Connection``
        object. Values from 0 to 1, inclusive, will be sent.  If ``None``,
        progress isn't reported.
    :return: A generator that yields up to ``count``
        :class:`movie_recommender.predict.common.Prediction` objects, in order
        of confidence.
    """
    best_predictions = []
    with multiprocessing.Pool(jobs) as pool:
        prfr_args = _gen_prfr_args(user, reporter)
        predictions = pool.imap_unordered(func=_call_prfr, iterable=prfr_args)
        for prediction in predictions:
            if len(best_predictions) >= count:
                heapq.heappushpop(best_predictions, prediction)
            else:
                heapq.heappush(best_predictions, prediction)

    for prediction in heapq.nlargest(count, best_predictions):
        yield prediction


def _call_prfr(args):
    return predict_rating_for_recommend(*args)


def _gen_prfr_args(user, reporter=None):
    if reporter:
        num_unrated_movies = db_count.unrated_movies(user)
        conn_out, conn_in = multiprocessing.Pipe(duplex=False)
        proc = multiprocessing.Process(target=reporter, args=(conn_out,))
        proc.start()

    for i, movie in enumerate(read.unrated_movies(user)):
        yield (user, movie)

        if reporter:
            yielded = i + 1
            # We're not doing batch processing here, but in practice, this
            # constant also works well in places like this.
            if yielded % JOBS_PER_PROCESS_PER_BATCH == 0:
                conn_in.send(yielded / num_unrated_movies)

    if reporter:
        conn_in.send(1)
        conn_in.close()
        proc.join()
