Star Distance
=============

Calculate the distance from the sun to other stars with `Apache Spark`_.

Workflow for lemuria.cis.vtc.edu:

.. code-block:: sh

    source scripts/lemuria-env.sh
    sbt test package
    hadoop fs -rm -r '/user/jaudet/star-distance-spark-*'
    for ((i=1; i<=5; i++)); do
        env time --output "time-${i}.txt" scripts/run-app.sh "${i}"
        hadoop fs -cat "/user/jaudet/star-distance-spark-${i}/part*" | sort
    done

.. _Apache Spark: http://spark.apache.org/
