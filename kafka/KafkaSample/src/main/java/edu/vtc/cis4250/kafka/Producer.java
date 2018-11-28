package edu.vtc.cis4250.kafka;

import java.util.List;
import java.util.Properties;
import java.util.Random;

import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.PartitionInfo;

/** Generate random doubles, and send them to Kafka. */
public final class Producer {

    /** A random number generator. */
    private final Random generator;

    /** Properites for connecting to Kafka. */
    private final Properties props;

    /** The number of partitions the target topic should have. */
    private static final Integer NUM_PARTITIONS = 2;

    /** The value used to choose which partition doubles go in to. */
    private static final Double BOUNDARY = 0.5;

    /** Initialize private attributes. */
    public Producer() {
        generator = new Random(0);

        props = new Properties();
        props.put("bootstrap.servers", "localhost:9092");
        props.put("acks", "all");
        props.put("linger.ms", 1);
        props.put(
            "key.serializer",
            "org.apache.kafka.common.serialization.StringSerializer");
        props.put(
            "value.serializer",
            "org.apache.kafka.common.serialization.DoubleSerializer");
    }

    /**
     * Generate random doubles and send them to Kafka.
     *
     * @param topic The topic to send messages to.
     * @param count The number of messages to generate.
     * @throws PartitioningError If the chosen topic has an incorrect number of
     * partitions.
     */
    public void produce(final String topic, final Integer count)
    throws PartitioningError {
        KafkaProducer<String, Double> producer = new KafkaProducer<>(props);

        // Are the target partitions present?
        List<PartitionInfo> partitions = producer.partitionsFor(topic);
        Integer numPartitions = partitions.size();
        if (numPartitions != NUM_PARTITIONS) {
            throw new PartitioningError(
                "Topic " + topic + " should have " + NUM_PARTITIONS
                + " partition(s), but it has " + numPartitions
                + " partition(s)."
            );
        }

        try {
            for (Integer recordCount = 0; recordCount < count; recordCount++) {
                String key = null;
                Double val = generator.nextDouble();
                Integer partition = choosePartition(partitions, val);
                ProducerRecord<String, Double> record = new ProducerRecord<>(
                    topic,
                    partition,
                    key,
                    val
                );
                producer.send(record);
            }
        } finally {
            producer.close(); // close connection with broker
        }
    }

    /**
     * Choose which partition the given value should be placed in to.
     *
     * @param partitions The candidate partitions.
     * @param val The value being sorted. If less than {@link
     * Producer#BOUNDARY}, place in partition 0, else partition 1.
     * @return A partition ID.
     */
    public static Integer choosePartition(
            final List<PartitionInfo> partitions,
            final Double val) {
        if (val < BOUNDARY) {
            return partitions.get(0).partition();
        } else {
            return partitions.get(1).partition();
        }
    }
}
