package name.ichimonji10.star_distance

import org.apache.hadoop.io.DoubleWritable
import org.scalatest.FlatSpec

class DistanceCalculatorTest extends FlatSpec {
  behavior of "getMinMax method"

  it should "handle an iterable of 1 item" in {
    val input: Iterable[DoubleWritable] = Seq(
      new DoubleWritable(3),
    )
    val targetOutput: (Double, Double) = new Tuple2(3, 3)
    val actualOutput: (Double, Double) = new DistanceCalculator().getMinMax(input)
    assert(targetOutput == actualOutput)
  }

  it should "handle an iterable of 2 items" in {
    val input: Iterable[DoubleWritable] = Seq(
      new DoubleWritable(0),
      new DoubleWritable(-3),
    )
    val targetOutput: (Double, Double) = new Tuple2(-3, 0)
    val actualOutput: (Double, Double) = new DistanceCalculator().getMinMax(input)
    assert(targetOutput == actualOutput)
  }

  it should "handle an iterable of 3+ items" in {
    val input: Iterable[DoubleWritable] = Seq(
      new DoubleWritable(-1),
      new DoubleWritable(1),
      new DoubleWritable(-2),
      new DoubleWritable(2),
      new DoubleWritable(0),
    )
    val targetOutput: (Double, Double) = new Tuple2(-2, 2)
    val actualOutput: (Double, Double) = new DistanceCalculator().getMinMax(input)
    assert(targetOutput == actualOutput)
  }

  behavior of "getLightYearsToStar method"

  it should "calculate distance" in {
    // Taken from star 1 in /user/hadoop/observations-1.txt on lemuria.
    val input: (Double, Double) = new Tuple2(
      62.658208353, // min
      62.658212890, // max
    )
    val targetOutput: Double = 399.37488765
    val actualOutput: Double =
      new DistanceCalculator().getLightYearsToStar(input)
    assert(targetOutput - actualOutput < 0.00000001)
  }
}
