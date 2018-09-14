package name.ichimonji10.average_temperature;

import java.io.IOException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

/** Parse arguments and call business logic. */
public final class AverageTemperature extends Configured implements Tool {

    /** Do nothing; this is a utility class. */
    private AverageTemperature() { }

    /**
     * Parse arguments and call business logic.
     *
     * @param args A pair of arguments. The former is the path to a CSV file
     * containing temperature measurements (and more). The latter is the path to
     * a directory into which results should be placed. Both paths reference the
     * HDFS filesystem.
     */
    public static void main(final String[] args) throws Exception {
        System.exit(
            ToolRunner.run(new Configuration(), new AverageTemperature(), args)
        );
    }

    @Override
    public int run(final String[] args)
    throws ClassNotFoundException, IOException, InterruptedException {
        // Create a job and parse custom arguments. The tool interface handles
        // common CLI arguments for us, and we get the results with getConf().
        Job job = Job.getInstance(getConf(), "average temperature");
        job.setJarByClass(AverageTemperature.class);
        FileInputFormat.addInputPath(job, getInputFile(args));
        FileOutputFormat.setOutputPath(job, getOutputDir(args));

        // Describe mapping phase.
        job.setMapperClass(CSVParser.class);
        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(FloatWritable.class);

        // Describe reduction phase.
        job.setReducerClass(TemperatureAverager.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(FloatWritable.class);

        // Run job.
        if (job.waitForCompletion(true)) {
            return 0;
        } else {
            return 1;
        }
    }

    /**
     * Return the path to the input CSV file.
     *
     * @param args Arguments to this program.
     * @throws ArrayIndexOutOfBoundsException If no argument providing this
     * information is present.
     * @return The path to the input CSV file.
     */
    private static Path getInputFile(final String[] args) {
        try {
            return new Path(args[0]);
        } catch (ArrayIndexOutOfBoundsException exc) {
            System.err.println("Specify an input file.");
            throw exc;
        }
    }

    /**
     * Return the path to the output directory.
     *
     * @param args Arguments to this program.
     * @throws ArrayIndexOutOfBoundsException If no argument providing this
     * information is present.
     * @return The path to the output directory.
     */
    private static Path getOutputDir(final String[] args) {
        try {
            return new Path(args[1]);
        } catch (ArrayIndexOutOfBoundsException exc) {
            System.err.println("Specify an output directory.");
            throw exc;
        }
    }
}
