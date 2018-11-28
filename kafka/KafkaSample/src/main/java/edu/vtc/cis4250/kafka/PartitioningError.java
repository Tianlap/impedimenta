package edu.vtc.cis4250.kafka;

/**
 * Indicates that a Kafka topic has an incorrect number of partitions.
 *
 * This application requires that the Kafka topic to which numbers are sent and
 * from which numbers are consumed have {@link
 * edu.vtc.cis4250.kafka.Producer#numPartitions} partitions. If not so, this
 * exception is raised.
 */
public final class PartitioningError extends Exception {

    /**
     * Initialize the exception.
     *
     * @param msg Details about the partitioning error.
     */
    public PartitioningError(final String msg) {
        super(msg);
    }
}
