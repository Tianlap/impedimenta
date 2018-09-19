package name.ichimonji10.average_temperature

import java.lang.Float
import org.apache.hadoop.io.FloatWritable
import org.apache.hadoop.io.LongWritable
import org.apache.hadoop.io.Text
import org.apache.hadoop.mapreduce.Mapper
import org.mockito.Mockito
import org.scalatest.FlatSpec

class CSVParserTest extends FlatSpec {
  behavior of "map method"

  it should "do nothing when input is a header row" in {
    // The row is copied from an actual measurements file.
    val offset: LongWritable = new LongWritable(0)
    val row: Text = new Text(new String(
      "\"TOA5\",\"CR1000\",\"CR1000\",\"10113\",\"CR1000.Std.13\",\"CPU:combined_cr1000_17Dec2008.CR1\",\"8735\",\"Table1\""
    ))
    val context: Mapper[LongWritable, Text, Text, FloatWritable]#Context =
      Mockito.mock(
        classOf[Mapper[LongWritable, Text, Text, FloatWritable]#Context]
      )
    new CSVParser().map(offset, row, context)

    // The goal is to verify that write() isn't called. This assertion is
    // overly aggressive, and can fail valid code. Something like
    // MockingDetails.getInvocations would probably be better.
    Mockito.verifyZeroInteractions(context);
  }

  it should "create a mapping when input is a data row" in {
    // The row is copied from an actual measurements file.
    val offset: LongWritable = new LongWritable(new java.lang.Long(0))
    val row: Text = new Text(new String(
      "\"2013-01-02 00:00:00\",424706,3.651,0,0.984,2.099,1.092,187.4,23.91,23.42,23.69,97.8,97.3,0,1002,1001,1002,0.341,0,0.119,1.365,1.365,1.365,0.205,0,0.107,2.154,1.641,1.853,-5.749,267.4,-1.024,-1.365,-1.246,-1.539,-2.052,-1.746,\"INF\",4,\"NAN\",0.546,0,0.226,3.52,3.007,3.218,-2.563,-3.417,-2.992,290.5,289.8,290.1,292.3,291.5,291.9,23.32,22.85,23.09,23.91,18.2,23.59"
    ));
    val context: Mapper[LongWritable, Text, Text, FloatWritable]#Context =
      Mockito.mock(
        classOf[Mapper[LongWritable, Text, Text, FloatWritable]#Context]
      )
    new CSVParser().map(offset, row, context)

    Mockito.verify(context).write(
      new Text(new String("2013-01")),
      new FloatWritable(new Float(23.69)),
    )
  }

  behavior of "splitRow method"

  it should "split its input string on commas" in {
    val input: String = "foo,bar,biz,baz"
    val targetOutput: Seq[String] = Seq("foo", "bar", "biz", "baz")
    val actualOutput: Seq[String] = new CSVParser().splitRow(input)
    assert(targetOutput == actualOutput)
  }

  it should "retain whitespace" in {
    val input: String = " foo , bar "
    val targetOutput: Seq[String] = Seq(" foo ", " bar ")
    val actualOutput: Seq[String] = new CSVParser().splitRow(input)
    assert(targetOutput == actualOutput)
  }

  behavior of "isHeaderRow method"

  it should "return true when a row looks like a header" in {
    val input: Seq[String] = Seq(
      "\"TS\"", "only", "the", "first", "column", "matters"
    )
    val targetOutput: Boolean = true
    val actualOutput: Boolean = new CSVParser().isHeaderRow(input)
    assert(targetOutput == actualOutput)
  }

  it should "return false when a row doesn't look like a header" in {
    val input: Seq[String] = Seq("only", "the", "first", "column", "matters")
    val targetOutput: Boolean = false
    val actualOutput: Boolean = new CSVParser().isHeaderRow(input)
    assert(targetOutput == actualOutput)
  }

  behavior of "getYearMonth method"

  it should "extract year and month, and format as YYYY-MM" in {
    val input: Seq[String] = Seq(
      "\"2013-01-02 00:00:00\"", "only", "the", "first", "column", "matters"
    )
    val targetOutput: String = "2013-01"
    val actualOutput: String = new CSVParser().getYearMonth(input)
    assert(targetOutput == actualOutput)
  }

  behavior of "getTemp method"

  it should "extract temperature" in {
    val input: Seq[String] = Seq(
      "0", "10", "20", "30", "40", "50", "60", "70", "80", "90", "100", "110"
    )
    val targetOutput: Float = new Float(100)
    val actualOutput: Float = new CSVParser().getTemp(input)
    assert(targetOutput == actualOutput)
  }
}
