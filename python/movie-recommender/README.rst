Movie Recommender
=================

Movie Recommender is an application for generating movie recommendations.

To install with a virtualenv:

.. code-block:: sh

    python3 -m venv ~/.venvs/movie-recommender
    source ~/.venvs/movie-recommender/bin/activate
    pip install --upgrade pip
    pip install .

You can now use the ``mr-*`` CLI applications. To deactivate the virtualenv,
execute ``deactivate``. To do development work such as generating documentation,
do the above, then:

.. code-block:: sh

    pip install .[dev]

You can now execute commands such as ``make docs-html`` or ``make lint``.

.. Everything above this comment should also be in docs/index.rst.
