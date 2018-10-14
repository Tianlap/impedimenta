package name.ichimonji10.star_distance

import org.apache.hadoop.conf.Configuration
import org.apache.hadoop.conf.Configured
import org.apache.hadoop.fs.Path
import org.apache.hadoop.io.DoubleWritable
import org.apache.hadoop.io.IntWritable
import org.apache.hadoop.mapreduce.Job
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat
import org.apache.hadoop.util.Tool
import org.apache.hadoop.util.ToolRunner

object StarDistance {
  /**
   * Parse arguments and call business logic.
   *
   * @param args A pair of arguments. The former is the path to a CSV file
   * containing observations about stars. The latter is the path to a directory
   * into which results should be placed. Both paths reference the HDFS
   * filesystem.
   */
  def main(args: Array[String]): Unit = {
    System.exit(
      ToolRunner.run(new Configuration(), new StarDistance(), args)
    )
  }
}

/**
 * Calculate the distance from the sun to some number of stars.
 *
 * Input is assumed to be a CSV file, where each row contains the ecliptic
 * coordinates of a star on a day (night). Input is assumed to be complete, with
 * no missing observations. Here's several sample rows:
 *
 *   001,00000000,-048.325347400,+21.583319175
 *   001,00000001,+062.658212890,-56.638050824
 *   001,00000002,+092.968021895,+43.397591907
 *
 * The columns are as follows:
 *
 * 1. Day number.
 * 2. Star number.
 * 3. Ecliptic longitude (degrees).
 * 4. Ecliptic latitude (degrees).
 */
class StarDistance extends Configured with Tool {
  override def run(args: Array[String]): Int = {
    // Create a job. The tool interface handles common CLI arguments for us, and
    // we get the results with getConf().
    val job: Job = Job.getInstance(getConf(), "star distance")
    job.setJarByClass(classOf[StarDistance])
    FileInputFormat.addInputPath(job, getInputFile(args))
    FileOutputFormat.setOutputPath(job, getOutputDir(args))

    // Describe mapping phase.
    job.setMapperClass(classOf[CSVParser])
    job.setMapOutputKeyClass(classOf[IntWritable])
    job.setMapOutputValueClass(classOf[DoubleWritable])

    // Describe reduction phase.
    job.setReducerClass(classOf[DistanceCalculator])
    job.setOutputKeyClass(classOf[IntWritable])
    job.setOutputValueClass(classOf[DoubleWritable])

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
