package name.ichimonji10.average_temperature

import org.apache.hadoop.conf.Configuration
import org.apache.hadoop.conf.Configured
import org.apache.hadoop.fs.Path
import org.apache.hadoop.io.FloatWritable
import org.apache.hadoop.io.Text
import org.apache.hadoop.mapreduce.Job
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat
import org.apache.hadoop.util.Tool
import org.apache.hadoop.util.ToolRunner

object AverageTemperature {
  /**
   * Parse arguments and call business logic.
   *
   * @param args A pair of arguments. The former is the path to a CSV file
   * containing temperature measurements (and more). The latter is the path to
   * a directory into which results should be placed. Both paths reference the
   * HDFS filesystem.
   */
  def main(args: Array[String]): Unit = {
    System.exit(
      ToolRunner.run(new Configuration(), new AverageTemperature(), args)
    )
  }
}

/**
 * Calculate the average Fahrenheit temperatures of each month in a year.
 *
 * Input is assumed to be a CSV file, where the first several rows are header
 * information, and subsequent rows contain several measurements from a weather
 * station at a point in time. One column contains the average temperature for
 * the past five minutes, and another column contains the time stamp of the
 * measurement.
 *
 * Input is assumed to be complete, with no missing measurements.
 */
class AverageTemperature extends Configured with Tool {

  override def run(args: Array[String]): Int = {
    // Create a job. The tool interface handles common CLI arguments for us, and
    // we get the results with getConf().
    val job: Job = Job.getInstance(getConf(), "average temperature")
    job.setJarByClass(classOf[AverageTemperature])
    FileInputFormat.addInputPath(job, getInputFile(args))
    FileOutputFormat.setOutputPath(job, getOutputDir(args))

    // Describe mapping phase.
    job.setMapperClass(classOf[CSVParser])
    job.setMapOutputKeyClass(classOf[Text])
    job.setMapOutputValueClass(classOf[FloatWritable])

    // Describe reduction phase.
    job.setReducerClass(classOf[TemperatureAverager])
    job.setOutputKeyClass(classOf[Text])
    job.setOutputValueClass(classOf[FloatWritable])

    // Run job.
    if (job.waitForCompletion(true)) {
      0
    } else {
      1
    }
  }

  /**
   * Return the path to the input CSV file.
   *
   * Throw an exception if no argument providing this information is present.
   */
  private def getInputFile(args: Array[String]): Path = {
    try {
      new Path(args(0))
    } catch {
      case err: ArrayIndexOutOfBoundsException => {
        Console.err.println("Specify an input file.")
        throw err
      }
    }
  }

  /**
   * Return the path to the output directory.
   *
   * Throw an exception if no argument providing this information is present.
   */
  private def getOutputDir(args: Array[String]): Path = {
    try {
      new Path(args(1))
    } catch {
      case err: ArrayIndexOutOfBoundsException => {
        Console.err.println("Specify an output directory.")
        throw err
      }
    }
  }
}
