package name.ichimonji10.rfc_analyzer

import java.util.Scanner
import java.util.zip.ZipEntry
import java.util.zip.ZipInputStream
import org.apache.spark.SparkConf
import org.apache.spark.SparkContext
import org.apache.spark.input.PortableDataStream
import org.apache.spark.rdd.RDD
import scala.util.matching.Regex

object RFCAnalyzer {
  private val ASCII_NAME_CHARS: Regex = raw"^[a-zA-Z\.\- ]+$$".r

  private val ENDS_WITH_YEAR: Regex = raw"\d{4}$$".r

  private val RIGHT_ALIGNED_TEXT: Regex = raw"\s{20,}(\S.*\S)$$".r

  private val RFC_FILENAME: Regex = raw"rfc(\d{1,4}).txt$$".r

  /** Parse CLI arguments and call business logic. */
  def main(args: Array[String]): Unit = {
    val optionParser: OptionParser = new OptionParser(args)
    val cfg: SparkConf = new SparkConf().setAppName("RFC Analyzer")
    val context: SparkContext = new SparkContext(cfg)
    val dataStreams: RDD[PortableDataStream] =
      context
      .binaryFiles(optionParser.inputPath())
      .filter((binaryFile: (String, PortableDataStream)) => {
        binaryFile._1.endsWith(".zip")
      })
      .map((binaryFile: (String, PortableDataStream)) => binaryFile._2)
    val authors: RDD[(String, Iterable[Int])] =
      dataStreams
      .flatMap(dataStream => getRfcIdsToAuthors(dataStream))
      .flatMap((rfcIdToAuthors: (Int, Seq[String])) => {
        val rfcId: Int = rfcIdToAuthors._1
        val rfcAuthors: Seq[String] = rfcIdToAuthors._2
        rfcAuthors.map(rfcAuthor => (rfcAuthor, rfcId))
      })
      .groupByKey
    authors.saveAsTextFile(optionParser.outputDir())
  }

  /**
   * For each RFC in the given zip file, map RFC ID to authors.
   *
   * @param zipStream A handle on a zip file.
   * @return A sequence of (rfcId, rfcAuthors) tuples.
   */
  def getRfcIdsToAuthors(dataStream: PortableDataStream): Seq[(Int, Seq[String])] = {
    val zipInputStream: ZipInputStream = new ZipInputStream(dataStream.open)
    Stream
      .continually(zipInputStream.getNextEntry)
      .takeWhile((entry: ZipEntry) => entry != null)
      .filter((entry: ZipEntry) => entry.getName match {
        case RFC_FILENAME(_*) => true
        case _ => false
      })
      .map((entry: ZipEntry) => (
        getRfcId(entry.getName),
        getRfcAuthors(getTextFile(zipInputStream))
      ))
      .toBuffer
  }

  /**
   * Given the path to an RFC, return its ID.
   *
   * @param path The path to an RFC file, e.g. "path/to/rfc123.txt".
   * @return An RFC ID, e.g. 123.
   */
  def getRfcId(path: String): Int = {
    path match {
      case RFC_FILENAME(rfcId) => rfcId.toInt
      case _ => -1
    }
  }

  /**
   * Given the contents of an RFC, return its authors.
   *
   * @param file The plain-text contents of an RFC.
   * @return A sequence of author names.
   */
  def getRfcAuthors(file: String): Seq[String] = {
    file
      .split("\u000c") // form feed character, delimits pages
      .head
      .lines
      .map(line => line match {
        case RIGHT_ALIGNED_TEXT(rat) => rat
        case _ => ""
      })
      .filter(line => line != "")
      .map(line => line match {
        case ASCII_NAME_CHARS(_*) => line
        case _ => ""
      })
      .filter(line => line != "")
      .filter(line => !line.toLowerCase.contains("college"))
      .filter(line => !line.toLowerCase.contains("corp."))
      .filter(line => !line.toLowerCase.contains("corporation"))
      .filter(line => !line.toLowerCase.contains("inc."))
      .filter(line => !line.toLowerCase.contains("incorporated"))
      .filter(line => !line.toLowerCase.contains("university"))
      .toList
  }

  /**
   * Extract the contents of the current text file in the given zip file.
   *
   * @param dataStream A handle on a zip file.
   * @return The contents of the current text file.
   */
  def getTextFile(zipInputStream: ZipInputStream): String = {
    // See: https://stackoverflow.com/a/5445161
    val scanner: Scanner = new Scanner(zipInputStream).useDelimiter("\\A")
    if (scanner.hasNext) {
      scanner.next
    } else {
      ""
    }
  }
}
