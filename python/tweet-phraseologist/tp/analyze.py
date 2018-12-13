# coding=utf-8
"""Tools to analyze tweets."""
import itertools
import multiprocessing
import unicodedata
from typing import Callable, Dict, Iterable, Iterator, List, Optional, Tuple

from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import sent_tokenize
from nltk.tokenize.casual import TweetTokenizer
from nltk.util import ngrams

from tp.db import count, read


def count_ngrams_in_tweets(
        jobs: Optional[int],
        *,
        ngram_len: int,
        party: Optional[str],
        reporter: Optional[Callable] = None) -> Dict[Tuple[str, ...], int]:
    """Find the top ngrams in the corpus of tweets.

    :param jobs: The number of processes to spawn. If ``None``, spawn one per
        CPU.
    :param ngram_len: The length of ngrams.
    :param party: The party whose tweets should be analyze. If ``None``, all
        tweets are analyzed.
    :param reporter: A function that reports progress to the user. Must accept
        one argument, where that argument is a multiprocessing ``Connection``
        object. Values from 0 to 1, inclusive, will be sent through the
        connection.
    :return: A dict mapping each ngram to the number of times it appears within
        the corpus of tweets currently in the database.
    """
    totals: Dict[Tuple[str, ...], int] = {}
    with multiprocessing.Pool(jobs) as pool:
        # chunksize chosen empirically with an R7 1700 CPU
        for ngram_counts in pool.imap_unordered(
                func=call_cnit,
                iterable=gen_cnit_args(ngram_len, party, reporter),
                chunksize=2**5):
            for ngram, ncount in ngram_counts.items():
                totals.setdefault(ngram, 0)
                totals[ngram] += ncount
    return totals


def call_cnit(args):
    """Call :meth:`tp.analyze.count_ngrams_in_tweet`."""
    return count_ngrams_in_tweet(*args)


def gen_cnit_args(
        ngram_len: int,
        party: Optional[str],
        reporter: Optional[Callable] = None) -> Iterator[Tuple[str, int]]:
    """Generate arguments for :meth:`tp.analyze.count_ngrams_in_tweet`.

    :param ngram_len: Passed through to
        :meth:`tp.analyze.count_ngrams_in_tweet`.
    :param party: If specified, only yield tweets from the given party, instead
        of all tweets.
    :param reporter: A function that reports progress to the user. Must accept
        one argument, where that argument is a multiprocessing ``Connection``
        object. Values from 0 to 1, inclusive, will be sent through the
        connection.
    :return: A generator that yields tuples of arguments.
    """
    if reporter:
        num_tweets: int = count.tweets(party)
        tweets_yielded: int = 0

        conn_out: multiprocessing.connection.Connection
        conn_in: multiprocessing.connection.Connection
        conn_out, conn_in = multiprocessing.Pipe(duplex=False)
        proc: multiprocessing.Process = (
            multiprocessing.Process(target=reporter, args=(conn_out,))
        )
        proc.start()

    for tweet in read.tweets(party):
        yield (tweet, ngram_len)

        if reporter:
            tweets_yielded += 1
            if tweets_yielded % 2**8 == 0:
                conn_in.send(tweets_yielded / num_tweets)

    if reporter:
        conn_in.send(1)
        conn_in.close()
        proc.join()


def count_ngrams_in_tweet(
        tweet: str,
        ngram_len: int) -> Dict[Tuple[str, ...], int]:
    """Find ngrams within a tweet.

    :param tweet: The tweet to analyze.
    :return: A dict mapping each ngram to the number of times it appears within
        the given tweet.
    """
    stemmer = SnowballStemmer('english')
    tweet_tokenizer = TweetTokenizer()
    ngram_counts: Dict[Tuple[str, ...], int] = {}
    for sentence in sent_tokenize(tweet):
        words: Iterable[str] = tweet_tokenizer.tokenize(sentence)
        no_punct = itertools.filterfalse(punctuation, words)
        # The stemmer lower-cases words.
        normalized_words: Iterator[str] = (stemmer.stem(word) for word in no_punct)
        ngram: List[str]
        for ngram in ngrams(normalized_words, n=ngram_len):
            immutable_ngram: Tuple[str, ...] = tuple(ngram)
            ngram_counts.setdefault(immutable_ngram, 0)
            ngram_counts[immutable_ngram] += 1
    return ngram_counts


def punctuation(string: str) -> bool:
    """Tell whether the given string consists entirely of punctuation."""
    # If this function is too slow, consider switching to the third-party regex
    # module and using its ability to match strings based on unicde attributes.
    for char in string:
        if not unicodedata.category(char).startswith('P'):
            return False
    return True
