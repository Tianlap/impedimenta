package name.ichimonji10.star_distance

import org.scalatest.FlatSpec

class MainTest extends FlatSpec {
  behavior of "splitLine function"

  it should "split its input string on commas and retain whitespace" in {
    val input: String = " foo , bar "
    val targetOutput: Seq[String] = Seq(" foo ", " bar ")
    val actualOutput: Seq[String] = Main.splitLine(input)
    assert(targetOutput == actualOutput)
  }

  behavior of "getStarIdELongitude function"

  it should "select and cast the correct fields" in {
    val input: Seq[String] = Seq("foo", "020", "+062.658212890", "bar")
    val targetOutput: (Int, Double) = (20, 62.658212890)
    val actualOutput = Main.getStarIdELongitude(input)
    assert(targetOutput == actualOutput)
  }

  behavior of "getMinLongitude function"

  it should "return the minimum of ascending numbers" in {
    val min: Double = -2.0
    val max: Double = -1.0
    val output = Main.getMinLongitude(min, max)
    assert(min == output)
  }

  it should "return the minimum of descending numbers" in {
    val min: Double = -2.0
    val max: Double = -1.0
    val output = Main.getMinLongitude(max, min)
    assert(min == output)
  }

  behavior of "getMaxLongitude function"

  it should "return the maximum of ascending numbers" in {
    val min: Double = -2.0
    val max: Double = -1.0
    val output = Main.getMaxLongitude(min, max)
    assert(max == output)
  }

  it should "return the maximum of descending numbers" in {
    val min: Double = -2.0
    val max: Double = -1.0
    val output = Main.getMaxLongitude(max, min)
    assert(max == output)
  }

  behavior of "getLightYears function"

  it should "calculate distance" in {
    // Taken from star 1 in /user/hadoop/observations-1.txt on lemuria.
    val input: (Double, Double) = (
      62.658208353, // min
      62.658212890  // max
    )
    val targetOutput: Double = 399.37488765
    val actualOutput: Double = Main.getLightYears(input)
    assert(targetOutput - actualOutput < 0.00000001)
  }
}
