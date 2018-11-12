Word Count
==========

Count words in a text file with `Apache Spark`_.

Workflow for lemuria.cis.vtc.edu:

.. code-block:: sh

    source scripts/lemuria-env.sh
    sbt test package
    ./scripts/run-app.sh
    hadoop fs -ls '/user/jaudet/output'
    hadoop fs -rm -r '/user/jaudet/output'

.. _Apache Spark: http://spark.apache.org/
