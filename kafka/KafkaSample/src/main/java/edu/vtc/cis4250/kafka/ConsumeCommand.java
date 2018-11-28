package edu.vtc.cis4250.kafka;

import com.beust.jcommander.Parameter;
import com.beust.jcommander.Parameters;

/**
 * Define a "consume" subcommand.
 */
@Parameters(commandDescription = "Consume numbers from Kafka.")
public class ConsumeCommand {

    /** Add the "topic" positional parameter. */
    @Parameter(
        description = "The topic to consume messages from.",
        required = true)
    private String topic = new String();

    /**
     * Return the value of the "topic" parameter.
     *
     * @return The value of the "topic" parameter.
     */
    public final String getTopic() {
        return topic;
    }
}
