package edu.vtc.cis4250.kafka;

import com.beust.jcommander.Parameter;

/** The root CLI argument parser. */
public class RootCommand {
    /** Allow a --help parameter. */
    @Parameter(names = "--help", help = true)
    private boolean help;

    /**
     * Get the runtime value of the --help parameter.
     *
     * @return The runtime value of the --help parameter.
     */
    public final boolean getHelp() {
        return help;
    }
}
