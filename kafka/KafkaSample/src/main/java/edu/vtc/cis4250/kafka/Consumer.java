package edu.vtc.cis4250.kafka;

import java.time.Duration;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Properties;

import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.PartitionInfo;

/** Consume values from Kafka and print them to stdout. */
public final class Consumer {
    /** Properites for connecting to Kafka. */
    private final Properties props;

    /** How often should the consumer check for new records? */
    private static final Duration POLL_FREQ = Duration.ofMillis(1000);

    /** How often should consumer offsets be auto-committed, in ms? */
    private static final Integer AUTO_COMMIT_FREQ = 1000;

    /** Initialize private attributes. */
    public Consumer() {
        props = new Properties();
        props.put("bootstrap.servers", "localhost:9092");
        props.put("group.id", "PrimaryWorkers");
        props.put("auto.commit.interval.ms", AUTO_COMMIT_FREQ);
        props.put(
            "key.deserializer",
            "org.apache.kafka.common.serialization.StringDeserializer");
        props.put(
            "value.deserializer",
            "org.apache.kafka.common.serialization.DoubleDeserializer");
    }

    /**
     * For each partition, create a thread and call {@link consume}.
     *
     * By default, Kafka balances workload within a consumer workload by
     * partition. For example, "if there is a topic with four partitions, and a
     * consumer group with two processes, each process would consume from two
     * partitions." Consequently, we don't need to explicitly assign consumers
     * to partitions. Instead, we can create as many consumers as there are
     * partitions.
     *
     * @param topic The topic to consume messages from.
     * @throws InterruptedException If an active thread is interrupted.
     */
    public void consumeThreaded(final String topic)
    throws InterruptedException {
        KafkaConsumer<String, Double> consumer = new KafkaConsumer<>(props);
        List<PartitionInfo> partitions = consumer.partitionsFor(topic);
        Runnable consumeWrapper = new Runnable() {
            @Override
            public void run() {
                consume(topic);
            }
        };
        ArrayList<Thread> threads = new ArrayList<>();
        for (Integer i = new Integer(0); i < partitions.size(); i++) {
            threads.add(new Thread(consumeWrapper));
        }
        for (Thread thread : threads) {
            thread.start();
        }
        for (Thread thread : threads) {
            thread.join();
        }
    }

    /**
     * Consume values from the given topic and print their average to stdout.
     *
     * @param topic The topic to consume messages from.
     */
    public void consume(final String topic) {
        long threadId = Thread.currentThread().getId();
        KafkaConsumer<String, Double> consumer = new KafkaConsumer<>(props);
        consumer.subscribe(Collections.singletonList(topic));
        Integer consumed = 0;
        Double avgVal = 0.0;
        try {
            while (true) {
                ConsumerRecords<String, Double> records =
                    consumer.poll(POLL_FREQ);
                for (ConsumerRecord<String, Double> record : records) {
                    // If we have an average derived from ten numbers and we
                    // want to incorporate an eleventh number, do the following:
                    //
                    //     ((avgVal + * 10) + newVal) / 11
                    //
                    // https://www.bennadel.com/blog/1627-create-a-running-average-without-storing-individual-values.htm
                    Double newVal = record.value();
                    avgVal = ((avgVal * consumed) + record.value())
                             / (consumed + 1);
                    consumed += 1;
                    System.out.printf(
                        "consumed = %.3f, new average = %.3f (thread %d)%n",
                        newVal,
                        avgVal,
                        threadId
                    );
                }
            }
        } finally {
            consumer.close(); // close connection with broker
        }
    }
}
