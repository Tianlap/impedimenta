package name.ichimonji10.average_temperature

import java.lang.Float
import java.util.regex.Pattern
import org.apache.hadoop.io.FloatWritable
import org.apache.hadoop.io.LongWritable
import org.apache.hadoop.io.Text
import org.apache.hadoop.mapreduce.Mapper

/** Extract timestamps and temperatures from lines in an input CSV file. */
class CSVParser extends Mapper[LongWritable, Text, Text, FloatWritable] {
  private val HEADER_LEFT_COLUMN: Set[String] = Set(
    "\"TIMESTAMP\"",
    "\"TOA5\"",
    "\"TS\"",
    "\"\"",
  )
  private val SPLITTER: Pattern = Pattern.compile(",")
  private val TEMPERATURE: Int = 10;
  private val TIMESTAMP: Int = 0
  private val TIMESTAMP_MONTH_END: Int = 8
  private val TIMESTAMP_MONTH_START: Int = 6
  private val TIMESTAMP_YEAR_END: Int = 5
  private val TIMESTAMP_YEAR_START: Int = 1

  /**
   * Extract a timestamp and a temperature from a CSV file row.
   *
   * Map the timestamp's year-month to the fahrenheit temperature.
   *
   * @param offset The offset into the input file.
   * @param row The input line.
   * @param context The object to which the mapping is written.
   */
  override def map(
    offset: LongWritable,
    row: Text,
    context: Mapper[LongWritable, Text, Text, FloatWritable]#Context
  ): Unit = {
    val fields: Seq[String] = splitRow(row.toString)
    if (isHeaderRow(fields)) {
      return
    }
    val yearMonth: Text = new Text(getYearMonth(fields))
    val temp: FloatWritable = new FloatWritable(getTemp(fields))
    context.write(yearMonth, temp)
  }

  /** Split the given row on commas (and drop the commas). */
  def splitRow(row: String): Seq[String] = {
    SPLITTER.split(row)
  }

  /** Return true if this row appears to be a header row. */
  def isHeaderRow(fields: Seq[String]): Boolean = {
    HEADER_LEFT_COLUMN.contains(fields(TIMESTAMP));
  }

  /** Extract the year and month from this row as a YYYY-MM string. */
  def getYearMonth(fields: Seq[String]): String = {
    val timestamp: String = fields(TIMESTAMP)
    val year: String = timestamp.substring(
      TIMESTAMP_YEAR_START,
      TIMESTAMP_YEAR_END,
    )
    val month: String = timestamp.substring(
      TIMESTAMP_MONTH_START,
      TIMESTAMP_MONTH_END,
    )
    year + "-" + month
  }

  /** Extract the average fahrenheit temperature from this row. */
  def getTemp(fields: Seq[String]): Float = {
    new Float(fields(TEMPERATURE))
  }
}
