Kafka Sample
============

Generate random numbers, partition them with Kafka, and print their averages.

To use, start by getting Kafka running. For full instructions, see the `Kafka
Documentation`_. If you have a pre-compiled binary, something like this
suffices:

.. code-block:: sh

    bin/zookeeper-server-start.sh config/zookeeper.properties
    bin/kafka-server-start.sh config/server.properties
    bin/kafka-topics.sh \
        --create \
        --zookeeper localhost:2181 \
        --replication-factor 1 \
        --partitions 2 \
        --topic numbers

Once Kafka is running, generate a far jar with Maven [1]_:

.. code-block:: sh

    mvn package

.. note:: The fat jar is generated with the shade plugin, which supercedes the
    assembly plugin. Notably, the former shades (i.e. renames) some dependencies
    to prevent dependency conflicts.

To send values to Kafka:

.. code-block:: sh

    java -jar target/KafkaSample-1.0-SNAPSHOT.jar produce numbers

To consume values from Kafka:

.. code-block:: sh

    java -jar target/KafkaSample-1.0-SNAPSHOT.jar consume numbers

.. [1] Maven is akin to a genie that repeatedly claims "wishes are easy" and
    who, upon being asked to explain the actual rules of wish-granting,
    disappears into his oil lamp and mutters deflective comments like "I've lost
    my mojo!"

    SBT is Maven's conspiratorial cousin who, when asked about wish-granting,
    insists that one should start by triangulating the wish within a
    four-dimensional matrix and creating a (thankfully finite) stack of turtles.

    Unsurprisingly, ``pom.xml`` contains cargo-culted blobs of XML, and I'm
    sorry if builds are screwed up.

.. _Kafka Documentation: https://kafka.apache.org/documentation/
