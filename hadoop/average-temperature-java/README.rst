Average Rating
==============

Calculate the average temperatures for each month in a given data set.

Hadoop deployments can significantly vary. I've tested this application on a
pseudo-distributed deployment, like so:

.. code-block:: sh

    sudo systemctl start sshd
    scripts/format-fs.sh
    scripts/start-daemons.sh
    scripts/populate-fs.sh
    mvn package
    scripts/run-app.sh
    scripts/print-output.sh

To clean up:

.. code-block:: sh

    scripts/delete-output.sh
    scripts/stop-daemons.sh

You can completely blow away the HDFS filesystem with: ``rm -rf
"/tmp/hadoop-$(whoami)"``.
