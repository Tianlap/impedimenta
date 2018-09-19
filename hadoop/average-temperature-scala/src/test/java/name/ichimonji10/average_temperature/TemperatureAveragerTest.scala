package name.ichimonji10.average_temperature

import java.lang.Float
import org.apache.hadoop.io.FloatWritable
import org.apache.hadoop.io.Text
import org.apache.hadoop.mapreduce.Reducer
import org.mockito.Mockito
import org.scalatest.FlatSpec
import scala.collection.JavaConverters._

class TemperatureAveragerTest extends FlatSpec {
  private val rawValues: Iterable[Float] = Seq(new Float(1.2), new Float(3.4))
  private val rawAverage: Float = new Float(rawValues.reduce(_ + _) / new Float(2))

  behavior of "reduce function"

  it should "average the given measurements" in {
    val key: Text = new Text(new String("foo"))
    val values: java.lang.Iterable[FloatWritable] = rawValues.map(new FloatWritable(_)).asJava
    val context: Reducer[Text, FloatWritable, Text, FloatWritable]#Context =
      Mockito.mock(
        classOf[Reducer[Text, FloatWritable, Text, FloatWritable]#Context]
      )
    new TemperatureAverager().reduce(key, values, context)
    Mockito.verify(context).write(key, new FloatWritable(rawAverage))
  }
}
