package name.ichimonji10.star_distance

import java.util.regex.Pattern
import org.apache.spark.SparkConf
import org.apache.spark.SparkContext
import scala.math

object Main {
  private val SPLITTER: Pattern = Pattern.compile(",")
  private val STAR_ID: Int = 1
  private val E_LONGITUDE: Int = 2

  def main(args: Array[String]): Unit = {
    val optionParser: OptionParser = new OptionParser(args)
    val cfg: SparkConf = new SparkConf().setAppName("Star Distance")
    val context: SparkContext = new SparkContext(cfg)

    // (starId, eLongitude) pairs
    val eLongitudes =
      context
      .textFile(optionParser.inputFile())
      .map(splitLine)
      .map(getStarIdELongitude)

    // (starId, minELongitude)
    val minELongitudes = eLongitudes.reduceByKey(getMinLongitude)

    // (starId, maxELongitude)
    val maxELongitudes = eLongitudes.reduceByKey(getMaxLongitude)

    // (starId, distanceInLightYears)
    val distances =
      minELongitudes
      .join(maxELongitudes)
      .mapValues(getLightYears)
    distances.saveAsTextFile(optionParser.outputDir())
  }

  /** Split the given line on commas (and drop the commas). */
  def splitLine(line: String): Seq[String] = {
    SPLITTER.split(line)
  }

  /** Extract and cast star's ID and ecliptic longitude. */
  def getStarIdELongitude(fields: Seq[String]): (Int, Double) = {
    (fields(STAR_ID).toInt, fields(E_LONGITUDE).toDouble)
  }

  /** Return the smallest given longitude. */
  def getMinLongitude(longitudeA: Double, longitudeB: Double): Double = {
    math.min(longitudeA, longitudeB)
  }

  /** Return the largest given longitude. */
  def getMaxLongitude(longitudeA: Double, longitudeB: Double): Double = {
    math.max(longitudeA, longitudeB)
  }

  /**
   * Calculate the distance to a star, in light years.
   *
   * @param eLongitudes The minimum and maximum observed ecliptic longitudes to
   * a star, in degrees.
   */
  def getLightYears(eLongitudes: (Double, Double)): Double = {
    val baselineInAUs: Double = 1
    // 1 degree == 3600 arcseconds. We multiply by 3600 before dividing by 2 to
    // ensure that precision isn't lost. Also see:
    // https://www.e-education.psu.edu/astro801/content/l4_p3.html
    val parallaxInArcseconds: Double = ((eLongitudes._2 - eLongitudes._1) * 3600) / 2
    val distanceInParsecs: Double = baselineInAUs / parallaxInArcseconds
    val distanceInLightYears: Double = distanceInParsecs * 3.261564
    distanceInLightYears
  }
}
