package name.ichimonji10.rfc_analyzer

import org.rogach.scallop.ScallopConf

/** A CLI option parser. */
class OptionParser(arguments: Seq[String]) extends ScallopConf(arguments) {
  val inputPath = trailArg[String](
    descr = "The path to a zip file, or a directory containing zip files."
  )
  val outputDir = trailArg[String](
    default = Some("output"),
    descr = "A directory into which to place results.",
    required = false
  )
  verify()
}
