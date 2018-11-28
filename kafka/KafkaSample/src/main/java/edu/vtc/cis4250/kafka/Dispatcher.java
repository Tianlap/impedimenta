package edu.vtc.cis4250.kafka;

import com.beust.jcommander.JCommander;

/** The main entry point for the CLI. */
public final class Dispatcher {
    /** Do nothing. Prevent instantiation of this class. */
    private Dispatcher() { }

    /**
     * Parse CLI args and call business logic.
     *
     * @param args CLI arguments.
     * @throws InterruptedException If an active thread is interrupted.
     */
    public static void main(final String[] args) throws InterruptedException {
        RootCommand rootCommand = new RootCommand();
        ConsumeCommand consumeCommand = new ConsumeCommand();
        ProduceCommand produceCommand = new ProduceCommand();
        JCommander parser = JCommander
            .newBuilder()
            .addObject(rootCommand)
            .addCommand("consume", consumeCommand)
            .addCommand("produce", produceCommand)
            .build();
        parser.parse(args);

        // handle --help
        if (rootCommand.getHelp()) {
            parser.usage();
            return;
        }

        // handle subcommand
        String command = parser.getParsedCommand();
        if (command == null) {
            handleNoCommand(parser);
            return;
        }
        switch (command) {
            case "consume":
                handleConsumeCommand(consumeCommand);
                break;
            case "produce":
                handleProduceCommand(produceCommand);
                break;
            default:
                handleIllegalState(parser);
                break;
        }
    }

    /**
     * Handle the case where the "consume" command was called.
     *
     * @param consumeCommand Values associated with the "consume" command.
     * @throws InterruptedException If an active thread is interrupted.
     */
    private static void handleConsumeCommand(
            final ConsumeCommand consumeCommand)
            throws InterruptedException {
        new Consumer().consumeThreaded(consumeCommand.getTopic());
    }

    /**
     * Handle the case where the "produce" command was called.
     *
     * @param produceCommand Values associated with the "produce" command.
     */
    private static void handleProduceCommand(
            final ProduceCommand produceCommand) {
        try {
            new Producer().produce(
                produceCommand.getTopic(),
                produceCommand.getCount()
            );
        } catch (PartitioningError err) {
            System.err.println(err);
            System.exit(1);
        }
    }

    /**
     * Handle the case where no arguments were passed.
     *
     * @param parser The parser that parsed CLI arguments.
     */
    private static void handleNoCommand(final JCommander parser) {
        parser.usage();
        System.exit(1);
    }

    /**
     * Handle the case where CLI arguments were incorrectly handled.
     *
     * @param parser The parser that parsed CLI arguments.
     */
    private static void handleIllegalState(final JCommander parser) {
        System.err.println(
            "The application failed to correctly handle CLI arguments. Please "
            + "Please report this error to the developers, along with the "
            + "command that triggered this error."
        );
    }
}
