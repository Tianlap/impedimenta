package name.ichimonji10.star_distance

import org.apache.hadoop.io.DoubleWritable
import org.apache.hadoop.io.IntWritable
import org.apache.hadoop.io.LongWritable
import org.apache.hadoop.io.Text
import org.apache.hadoop.mapreduce.Mapper
import org.mockito.Mockito
import org.scalatest.FlatSpec

class CSVParserTest extends FlatSpec {
  behavior of "map method"

  it should "map star ID to ecliptic longitude" in {
    // The row is copied from an actual input file.
    val offset: LongWritable = new LongWritable(25)
    val row: Text = new Text(new String(
      "001,00000050,-048.325347400,+21.583319175"
    ))
    val context: Mapper[LongWritable, Text, IntWritable, DoubleWritable]#Context =
      Mockito.mock(
        classOf[Mapper[LongWritable, Text, IntWritable, DoubleWritable]#Context]
      )
    new CSVParser().map(offset, row, context)

    Mockito.verify(context).write(
      new IntWritable(50),
      new DoubleWritable(-48.325347400),
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

  behavior of "getStarId method"

  it should "cast a valid integer" in {
    val input: Seq[String] = Seq("foo", "020", "biz", "baz")
    val targetOutput: Int = 20
    val actualOutput: Int = new CSVParser().getStarId(input)
    assert(targetOutput == actualOutput)
  }

  it should "fail to cast an invalid integer" in {
    val input: Seq[String] = Seq("foo", "bar", "biz", "baz")
    assertThrows[NumberFormatException] {
      new CSVParser().getStarId(input)
    }
  }

  behavior of "getEclipticLongitude method"

  it should "cast a positive longitude" in {
    val input: Seq[String] = Seq("foo", "bar", "+062.658212890", "baz")
    val targetOutput: Double = 62.658212890
    val actualOutput: Double = new CSVParser().getEclipticLongitude(input)
    assert(targetOutput == actualOutput)
  }

  it should "cast a negative longitude" in {
    val input: Seq[String] = Seq("foo", "bar", "-048.325347400", "baz")
    val targetOutput: Double = -48.325347400
    val actualOutput: Double = new CSVParser().getEclipticLongitude(input)
    assert(targetOutput == actualOutput)
  }

  it should "fail to cast an invalid longitude" in {
    val input: Seq[String] = Seq("foo", "bar", "biz", "baz")
    assertThrows[NumberFormatException] {
      new CSVParser().getEclipticLongitude(input)
    }
  }
}
