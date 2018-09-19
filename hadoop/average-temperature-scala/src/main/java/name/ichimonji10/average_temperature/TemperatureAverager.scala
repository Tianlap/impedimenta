package name.ichimonji10.average_temperature

import java.lang.Float
import org.apache.hadoop.io.FloatWritable
import org.apache.hadoop.io.Text
import org.apache.hadoop.mapreduce.Reducer
import scala.collection.JavaConverters._

/** Average temperature readings by month. */
class TemperatureAverager
extends Reducer[Text, FloatWritable, Text, FloatWritable] {

  // NOTE: `values` *MUST* be a java.lang.Iterable, not a
  // scala.collection.Iterable. Otherwise, Hadoop will ignore this class and use
  // the IdentityReducer.
  /**
   * Average the measurements for a given year-month.
   *
   * @param key A string in the format "YYYYMM".
   * @param values Temperature measurements for that year-month.
   * @param context The object to which the reduced value is written.
   */
  override def reduce(
    key: Text,
    values: java.lang.Iterable[FloatWritable],
    context: Reducer[Text, FloatWritable, Text, FloatWritable]#Context
  ): Unit = {
    var sumMeasurements: Float = new Float(0);
    var numMeasurements: Integer = new Integer(0);
    for (measurement <- values.asScala) {
      sumMeasurements += measurement.get
      numMeasurements += new Integer(1)
    }
    val avg: FloatWritable = new FloatWritable(new Float(
      sumMeasurements / numMeasurements
    ))
    context.write(key, avg)
  }
}
