Tweet Phraseologist
===================

Discover common phrases in tweets issued by U.S. Representatives.

.. contents::

Concept
-------

Imagine you're writing a tweet, and you want to inject a prototypically
Democratic or Republican phrase. What should you say? Tweet Phraseologist
(hereafter: TP) tackles that made-up problem. Given a `corpus of tweets`_ from
Democrats and Republicans, TP will discover the most common `stemmed`_
`n-grams`_ used by each party. [1]_ [2]_

.. NOTE:: This amateur application exists for educational purposes. Don't take
    it too seriously.

Installation
------------

TP is a pure-Python application. After installing TP itself, `NLTK`_ data must
also be installed, so that textual analyses can be performed. A good way to get
up and running is with a virtualenv:

.. code-block:: sh

    python3 -m venv ~/.venvs/tweet-phraseologist
    source ~/.venvs/tweet-phraseologist/bin/activate
    pip install --upgrade pip
    pip install .
    python -m nltk.downloader all

More advanced Python users can install TP in all the other usual ways too.

TP was designed with Kyle Pastor's `Democrat Vs. Republican Tweets`_ dataset in
mind.

Usage
-----

TP provides several command-line tools, each of which is prefixed with ``tp-``.
Here's an example of how to use them:

.. code-block:: sh

    # A dataset is a corpus of tweets, with some related data such as the party
    # of the representative who sent the tweet. In some cases, you must supply
    # the corpus.
    tp-dataset install democratvsrepublicantweets \
        --archive ~/Downloads/democratvsrepublicantweets.zip

    # Though several corpora may be installed, only one may be loaded into the
    # database at a time. The "cpop" command creates a new database and
    # populates it with the given dataset.
    tp-db cpop democratvsrepublicantweets

    # The tweets can then be analyzed. For example, one can ask for the most
    # common uniquely Democratic or Republican phrases:
    tp-analyze --party Democrat --unique
    tp-analyze --party Republican --unique

    # Or, one could ask for the most popular n-word phrases:
    tp-analyze --count 1 --ngram-length 3
    tp-analyze --count 1 --ngram-length 4

    # Naturally, the commands provide per-subcommand helptext.
    tp-dataset --help
    tp-dataset install --help

Comments
--------

The `Democrat Vs. Republican Tweets`_ dataset has issues. Here's some of the
issues that had to be resolved:

* Some of the tweets in ``ExtractedTweets.csv`` are not associated with a
  representative's individual account.  For example, `@RepublicanStudy`_ is a
  committee, not a representative.
* Tweets above a certain length were truncated to much shorter than what Twitter
  itself enforces. For example, one tweet ended with ``National Teacher
  Apprecia…``.
* Some tweets (but not all tweets!) have URLs appended. For example: ``Deep bow
  from a Cavs fan!  https://t.co/BD0xOh6TB3``.
* Some tweets are both truncated and have URLs appended. For example, one tweet
  ended with ``here in the House… https://t.co/n3tggDLU1L``.
* The tables were not normalized. Party affiliation appeared in both
  ``ExtractedTweets.csv`` and ``TwitterHandles.csv``. This *could* be used to
  great effect: the former file could list party affiliation at the time the
  tweet was sent, and the latter could list current party affiliation. But
  there's no indication that this was so.
* Many of the handles in ``ExtractedTweets.csv`` don't appear in
  ``TwitterHandles.csv``. An inner join on the two tables on the basis of handle
  discards ~90% of tweets.
* ``TwitterHandles.csv`` includes near-duplicate rows that only differ in their
  ``AvatarURL`` column.

.. [1] For an overview of issues related to `stemming`_ and `n-grams`_, see
    Wikipedia's page on `natural language processing`_.

.. [2] If the dataset that TP ingests includes tweets from independents,
    socialists, libertarians, etc, then those parties will also be analyzed.

.. _@RepublicanStudy: https://twitter.com/RepublicanStudy
.. _corpus of tweets: https://www.kaggle.com/kapastor/democratvsrepublicantweets
.. _democrat vs. republican tweets: https://www.kaggle.com/kapastor/democratvsrepublicantweets
.. _n-gram: https://en.wikipedia.org/wiki/N-gram
.. _n-grams: `n-gram`_
.. _natural language processing: https://en.wikipedia.org/wiki/Natural_language_processing
.. _nltk: http://www.nltk.org/
.. _snowball: https://snowballstem.org/
.. _stemmed: `stemming`_
.. _stemming: https://en.wikipedia.org/wiki/Stemming
