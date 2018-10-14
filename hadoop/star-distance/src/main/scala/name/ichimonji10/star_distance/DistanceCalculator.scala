package name.ichimonji10.star_distance

import org.apache.hadoop.io.DoubleWritable
import org.apache.hadoop.io.IntWritable
import org.apache.hadoop.mapreduce.Reducer
import scala.collection.JavaConverters._

/** Calculate the distance to a star. */
class DistanceCalculator
extends Reducer[IntWritable, DoubleWritable, IntWritable, DoubleWritable] {

  // NOTE: `eLongitudes` must be a java.lang.Iterable, not a
  // scala.collection.Iterable, as per the parent class' interface.
  /**
   * Calculate the distance to a star.
   *
   * @param starId A star ID.
   * @param eLongitudes Observed ecliptic longitudes of that star.
   * @param context The object to which the reduced value is written.
   */
  override def reduce(
    starId: IntWritable,
    eLongitudes: java.lang.Iterable[DoubleWritable],
    context: Reducer[
      IntWritable, DoubleWritable, IntWritable, DoubleWritable
    ]#Context,
  ): Unit = {
    val minMax: (Double, Double) = getMinMax(eLongitudes.asScala)
    val lightYears: Double = getLightYearsToStar(minMax)
    context.write(starId, new DoubleWritable(lightYears))
  }

  /**
   * Get the minimum and maximum ecliptic longitude from the given iterable.
   *
   * @param eLongitudes Observed ecliptic longitudes of a star, in degrees. Must
   * contain at least one element.
   */
  def getMinMax(eLongitudes: Iterable[DoubleWritable]): (Double, Double) = {
    // This method originally had the following logic:
    //
    //   min = eLongitudes.head.get
    //   max = min
    //   _getMinMax(min, max, eLongitudes.tail)
    //
    // This implementation passed unit tests, but it broke in the real world.
    // The exact reason is unknown, but logging showed that only two (random?)
    // elements from ther iterable were ever considered. It's as if the call to
    // head() within _getMinMax() always returned the same value.
    val eLongitudesIterator: Iterator[DoubleWritable] = eLongitudes.iterator
    val min: Double = eLongitudesIterator.next.get
    val max: Double = min
    _getMinMax(min, max, eLongitudesIterator)
  }

  /** Recursive implementation of getMinMax. */
  def _getMinMax(
    parentMin: Double,
    parentMax: Double,
    eLongitudesIterator: Iterator[DoubleWritable]
  ): (Double, Double) = {
    if (!eLongitudesIterator.hasNext) {
      return new Tuple2(parentMin, parentMax)
    }
    val candidate: Double = eLongitudesIterator.next.get
    val ourMin: Double = if (candidate < parentMin) {candidate} else {parentMin}
    val ourMax: Double = if (candidate > parentMax) {candidate} else {parentMax}
    _getMinMax(ourMin, ourMax, eLongitudesIterator)
  }

  /**
   * Get the distance to a star, in light years.
   *
   * @param eLongitudes The minimum and maximum observed ecliptic longitudes to
   * a star, in degrees.
   */
  def getLightYearsToStar(eLongitudes: (Double, Double)): Double = {
    val baselineInAUs: Double = 1
    // 1 degree == 3600 arcseconds. We multiply by 3600 before dividing by 2 to
    // ensure that precision isn't lost. Also see:
    // https://www.e-education.psu.edu/astro801/content/l4_p3.html
    val parallaxInArcseconds: Double = ((eLongitudes._2 - eLongitudes._1) * 3600) / 2
    val distanceInParsecs: Double = baselineInAUs / parallaxInArcseconds
    distanceInParsecs * 3.261564 // parsec → light-year
  }
}
