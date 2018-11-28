package edu.vtc.cis4250.kafka;

import com.beust.jcommander.Parameter;
import com.beust.jcommander.Parameters;

/**
 * Define a "produce" subcommand.
 */
@Parameters(commandDescription = "Produce numbers and send them to Kafka.")
public class ProduceCommand {

    /**
     * The default value of the --count parameter.
     *
     * This value is arbitrary.
     */
    private static final Integer DEFAULT_COUNT = 256;

    /** Add the "topic" positional parameter. */
    @Parameter(description = "The topic to send messages to.", required = true)
    private String topic = new String();

    /**
     * Return the value of the "topic" parameter.
     *
     * @return The value of the "topic" parameter.
     */
    public final String getTopic() {
        return topic;
    }

    /** Add the --count parameter. */
    @Parameter(
        names = "--count",
        description = "The number of messages to produce.")
    private Integer count = DEFAULT_COUNT;

    /**
     * Return the value of the --count parameter.
     *
     * @return The value of the --count parameter.
     */
    public final Integer getCount() {
        return count;
    }
}
