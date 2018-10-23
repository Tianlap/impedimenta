package name.ichimonji10.word_count

import org.rogach.scallop.ScallopConf

/** A CLI option parser. */
class OptionParser(arguments: Seq[String]) extends ScallopConf(arguments) {
  val inputFile = trailArg[String](descr = "The input file.")
  val outputDir = trailArg[String](
    default = Some("output"),
    descr = "The output directory.",
    required = false
  )
  verify()
}
