Tweet Phraseologist
===================

Discover common phrases in tweets issued by U.S. Representatives.

.. contents::

Concept
-------

Imagine you're writing a tweet, and you want to inject a prototypically
Democratic or Republican phrase. What should you say? Tweet Phraseologist
(hereafter: TP) tackles that made-up problem. Given a `corpus of tweets`_ from
Democratic and Republican U.S. Representatives, TP will discover the most common
`stemmed`_ `n-grams`_ used by each party. [1]_ [2]_

.. NOTE:: This amateur application exists for educational purposes. Don't take
    it too seriously.

Installation
------------

TP can function as a standalone pure-Python application. However, if `snowball`_
is installed, the application will be faster. The quickest way to get up and
running is with a virtualenv:

.. code-block:: sh

    python3 -m venv ~/.venvs/tweet-phraseologist
    source ~/.venvs/tweet-phraseologist/bin/activate
    pip install --upgrade pip
    pip install .

Expert Python users can install TP in all the other usual ways too.

Usage
-----

TP provides several command-line tools, each of which is prefixed with ``tp-``.
Here's an example of how to use them:

.. code-block:: sh

    # A dataset is a corpus of tweets, with some related data such as the party
    # of the representative who sent the tweet. TP can't download tweets by
    # itself. You must supply them. Use this command to get instructions for
    # installing.
    tp-dataset install democratvsrepublicantweets \
        --archive ~/Downloads/democratvsrepublicantweets.zip

    # Though many corpora of tweets may be installed, only one may be loaded
    # into the database. The "cpop" command creates a new database and populates
    # it with the given dataset.
    tp-db cpop democratvsrepublicantweets

    # The tweets must be analyzed before predictions can be made. The analyses
    # can be customized.
    tp-analyze
    tp-analyze --word-reduction none
    tp-analyze --word-reduction stemming
    tp-analyze --word-reduction lemmatisation

    # TP can then provide recommendations such as the most common phrases
    # overall, or the most common uniquely democratic phrase.
    tp-recommend
    tp-recommend --count 1 --party democrat --unique

.. [1] For an overview of issues related to `stemming`_ and `n-grams`_, see
    Wikipedia's page on `natural language processing`_.

.. [2] If the dataset that TP ingests includes tweets from independents,
    socialists, libertarians, etc, then those parties will also be analyzed.

.. _corpus of tweets: https://www.kaggle.com/kapastor/democratvsrepublicantweets
.. _n-gram: https://en.wikipedia.org/wiki/N-gram
.. _n-grams: `n-gram`_
.. _natural language processing: https://en.wikipedia.org/wiki/Natural_language_processing
.. _snowball: https://snowballstem.org/
.. _stemmed: `stemming`_
.. _stemming: https://en.wikipedia.org/wiki/Stemming
