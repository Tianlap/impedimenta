Star Distance
=============

Calculate the distance from the sun to some number of stars.

The Star Distance application can be tested and built with SBT:

.. code-block:: sh

    sbt test package

I've tested the application on lemuria.cis.vtc.edu:

.. code-block:: sh

    source scripts/hadoop-env.sh
    for ((i=1; i<=5; i++)); do
        env time --output "time-${i}.txt" scripts/run-app.sh "${i}"
        scripts/cat-output.sh "${i}"
        scripts/delete-output.sh "${i}"
    done
