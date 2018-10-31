Usage
=====

Location: :doc:`/index` → :doc:`/usage`

Movie Recommender ships with several command-line tools, each of which begins
with the prefix ``mr-``. To produce recommendations, you need to use several of
them. Here's an example:

.. code-block:: sh

    # A "dataset" is a set of movie ratings, links, etc. When executed, this
    # will install a dataset to the application's data directory. It can then be
    # used to populate the application's database.
    mr-dataset install ml-latest-small
    mr-db create ml-latest-small

    # It's advisable to analyze users and items before asking for predictions.
    # The exact requirements vary depending on the algorithm. For example, the
    # item-item algorithm will return results right away...
    mr-predict ii 49 1

    # ...but it will produce better results after a relevant analysis has been
    # performed.
    mr-analyze ii --user-ids 49 --item-ids 1
    mr-predict ii 49 1
