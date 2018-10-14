package name.ichimonji10.star_distance

import java.util.regex.Pattern
import org.apache.hadoop.io.DoubleWritable
import org.apache.hadoop.io.IntWritable
import org.apache.hadoop.io.LongWritable
import org.apache.hadoop.io.Text
import org.apache.hadoop.mapreduce.Mapper

/** Extract values from a CSV file. */
class CSVParser extends Mapper[LongWritable, Text, IntWritable, DoubleWritable] {
  private val SPLITTER: Pattern = Pattern.compile(",")
  private val STAR_ID: Int = 1
  private val E_LONGITUDE: Int = 2

  /**
   * Extract values from a CSV file row.
   *
   * More specifically, map star number to ecliptic longitude.
   */
  override def map(
    offset: LongWritable,
    row: Text,
    context: Mapper[LongWritable, Text, IntWritable, DoubleWritable]#Context
  ): Unit = {
    val fields: Seq[String] = splitRow(row.toString)
    val starId: IntWritable = new IntWritable(getStarId(fields))
    val eLongitude: DoubleWritable = new DoubleWritable(getEclipticLongitude(fields))
    context.write(starId, eLongitude)
  }

  /** Split the given row on commas (and drop the commas). */
  def splitRow(row: String): Seq[String] = {
    SPLITTER.split(row)
  }

  /** Extract the star ID from the given row. */
  def getStarId(fields: Seq[String]): Int = {
    fields(STAR_ID).toInt
  }

  /** Extract the ecliptic longitude from the given row. */
  def getEclipticLongitude(fields: Seq[String]): Double = {
    fields(E_LONGITUDE).toDouble
  }
}
