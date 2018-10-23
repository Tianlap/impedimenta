package name.ichimonji10.star_distance

import org.rogach.scallop.ScallopConf

/** A CLI option parser. */
class OptionParser(arguments: Seq[String]) extends ScallopConf(arguments) {
  val inputFile = trailArg[String](
    descr = "The CSV file containing star position observations."
  )
  val outputDir = trailArg[String](
    default = Some("output"),
    descr = "The directory into which to place results.",
    required = false
  )
  verify()
}
