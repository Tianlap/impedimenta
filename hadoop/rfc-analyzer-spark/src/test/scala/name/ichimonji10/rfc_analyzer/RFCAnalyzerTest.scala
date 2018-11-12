package name.ichimonji10.rfc_analyzer

import org.scalatest.FlatSpec

class RFCAnalyzerTest extends FlatSpec {
  private val SPACE = "                    "

  behavior of "getAuthorsFromFile()"

  it should "handle an empty file" in {
    val targetOutput: Seq[String] = Seq()
    val actualOutput: Seq[String] = RFCAnalyzer.getRfcAuthors("")
    assert(targetOutput == actualOutput)
  }

  it should "handle a file with one page, one line" in {
    val file: String = SPACE + "foo"
    val targetOutput: Seq[String] = Seq("foo")
    val actualOutput: Seq[String] = RFCAnalyzer.getRfcAuthors(file)
    assert(targetOutput == actualOutput)
  }

  it should "handle a file with one page, two lines" in {
    val file: String = SPACE + "foo\n" + SPACE + "bar"
    val targetOutput: Seq[String] = Seq("foo", "bar")
    val actualOutput: Seq[String] = RFCAnalyzer.getRfcAuthors(file)
    assert(targetOutput == actualOutput)
  }

  it should "handle a file with two pages, one line each" in {
    val file: String = SPACE + "foo\u000c" + SPACE + "bar"
    val targetOutput: Seq[String] = Seq("foo")
    val actualOutput: Seq[String] = RFCAnalyzer.getRfcAuthors(file)
    assert(targetOutput == actualOutput)
  }

  it should "handle a file with two pages, two lines each" in {
    val file: String =
      SPACE + "foo\n" + SPACE + "bar\u000c" + SPACE + "biz\n" + SPACE + "baz"
    val targetOutput: Seq[String] = Seq("foo", "bar")
    val actualOutput: Seq[String] = RFCAnalyzer.getRfcAuthors(file)
    assert(targetOutput == actualOutput)
  }

  it should "ignore empty lines" in {
    val file: String = SPACE + "foo\n\n" + SPACE + "bar"
    val targetOutput: Seq[String] = Seq("foo", "bar")
    val actualOutput: Seq[String] = RFCAnalyzer.getRfcAuthors(file)
    assert(targetOutput == actualOutput)
  }

  it should "ignore lines that end with a space" in {
    val file: String = SPACE + "foo \n" + SPACE + "bar"
    val targetOutput: Seq[String] = Seq("bar")
    val actualOutput: Seq[String] = RFCAnalyzer.getRfcAuthors(file)
    assert(targetOutput == actualOutput)
  }

  it should "ignore lines that aren't right-aligned" in {
    val file: String = SPACE + "foo" + SPACE
    val targetOutput: Seq[String] = Seq()
    val actualOutput: Seq[String] = RFCAnalyzer.getRfcAuthors(file)
    assert(targetOutput == actualOutput)
  }

  it should "ignore words that don't have whitespace on their left" in {
    val file: String = "foo"
    val targetOutput: Seq[String] = Seq()
    val actualOutput: Seq[String] = RFCAnalyzer.getRfcAuthors(file)
    assert(targetOutput == actualOutput)
  }

  it should "accept names containing spaces" in {
    val file: String = SPACE + "foo bar"
    val targetOutput: Seq[String] = Seq("foo bar")
    val actualOutput: Seq[String] = RFCAnalyzer.getRfcAuthors(file)
    assert(targetOutput == actualOutput)
  }

  it should "accept names containing dots" in {
    val file: String = SPACE + "foo.bar"
    val targetOutput: Seq[String] = Seq("foo.bar")
    val actualOutput: Seq[String] = RFCAnalyzer.getRfcAuthors(file)
    assert(targetOutput == actualOutput)
  }

  it should "accept names containing dashes" in {
    val file: String = SPACE + "foo-bar"
    val targetOutput: Seq[String] = Seq("foo-bar")
    val actualOutput: Seq[String] = RFCAnalyzer.getRfcAuthors(file)
    assert(targetOutput == actualOutput)
  }

  it should "ignore lines that contain special characters" in {
    val files: Seq[String] = Seq(
      SPACE + "a(b\n" + SPACE + "bar",
      SPACE + "a)b\n" + SPACE + "bar",
      SPACE + "a+b\n" + SPACE + "bar",
      SPACE + "a/b\n" + SPACE + "bar",
      SPACE + "a,b\n" + SPACE + "bar"
    )
    val targetOutput: Seq[String] = Seq("bar")
    for (file <- files) {
      val actualOutput: Seq[String] = RFCAnalyzer.getRfcAuthors(file)
      assert(targetOutput == actualOutput)
    }
  }

  it should "ignore lines containing 'inc.'" in {
    val file: String = SPACE + "foo\n" + SPACE + "Inc."
    val targetOutput: Seq[String] = Seq("foo")
    val actualOutput: Seq[String] = RFCAnalyzer.getRfcAuthors(file)
    assert(targetOutput == actualOutput)
  }

  it should "ignore lines containing 'corp.'" in {
    val file: String = SPACE + "foo\n" + SPACE + "Corp."
    val targetOutput: Seq[String] = Seq("foo")
    val actualOutput: Seq[String] = RFCAnalyzer.getRfcAuthors(file)
    assert(targetOutput == actualOutput)
  }

  it should "ignore lines containing 'incorporated'" in {
    val file: String = SPACE + "foo\n" + SPACE + "INCORPORATED"
    val targetOutput: Seq[String] = Seq("foo")
    val actualOutput: Seq[String] = RFCAnalyzer.getRfcAuthors(file)
    assert(targetOutput == actualOutput)
  }

  it should "ignore lines containing 'corporation'" in {
    val file: String = SPACE + "foo\n" + SPACE + "CORPORATION"
    val targetOutput: Seq[String] = Seq("foo")
    val actualOutput: Seq[String] = RFCAnalyzer.getRfcAuthors(file)
    assert(targetOutput == actualOutput)
  }

  it should "ignore lines containing 'university'" in {
    val file: String = SPACE + "foo\n" + SPACE + "UNIVERSITY"
    val targetOutput: Seq[String] = Seq("foo")
    val actualOutput: Seq[String] = RFCAnalyzer.getRfcAuthors(file)
    assert(targetOutput == actualOutput)
  }

  it should "ignore lines containing 'college'" in {
    val file: String = SPACE + "foo\n" + SPACE + "COLLEGE"
    val targetOutput: Seq[String] = Seq("foo")
    val actualOutput: Seq[String] = RFCAnalyzer.getRfcAuthors(file)
    assert(targetOutput == actualOutput)
  }
}
