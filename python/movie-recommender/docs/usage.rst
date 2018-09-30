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
    mr-dataset install fixture
    mr-db create fixture

    # A user must be analyzed before predictions or recommendations may be made
    # for that user.
    mr-analyze

    # mr-predict predicts a user's rating for a single movie. mr-recommend
    # generates a top-n list of recommendations for a user.
    mr-predict 1 1
    mr-recommend 1

    # Once you're comfortable with basic usage, load a more formidable dataset
    # into the database.
    mr-dataset install ml-latest-small
    mr-db create ml-latest-small --overwrite
    mr-analyze --user-ids {1..20}
    mr-recommend 1
