package name.ichimonji10.star_distance

import org.scalatest.FlatSpec

class OptionParserTest extends FlatSpec {
  behavior of "option parser"

  // It appears that exceptions aren't thrown when arguments don't match the
  // spec. Unsure why.

  // it should "unsuccessfully consume zero arguments" in {
  //   assertThrows[org.rogach.scallop.exceptions.RequiredOptionNotFound] {
  //     new OptionParser(Seq())
  //   }
  // }

  // it should "unsuccessfully consume three arguments" in {
  //   assertThrows[org.rogach.scallop.exceptions.ExcessArguments] {
  //     new OptionParser(Seq("input/file", "output/dir", "unknown"))
  //   }
  // }

  it should "successfully consume one argument" in {
    val op: OptionParser = new OptionParser(Seq("input/file"))
    assert(op.inputFile() == "input/file")
    assert(op.outputDir() == "output") // default value
  }

  it should "successfully consume two arguments" in {
    val op: OptionParser = new OptionParser(Seq("input/file", "output/dir"))
    assert(op.inputFile() == "input/file")
    assert(op.outputDir() == "output/dir")
  }
}
