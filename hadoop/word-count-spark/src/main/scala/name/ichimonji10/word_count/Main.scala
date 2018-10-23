package name.ichimonji10.word_count

import org.apache.spark.SparkConf
import org.apache.spark.SparkContext

object WordCount {

  def main(args: Array[String]): Unit = {
    val optionParser = new OptionParser(args)

    // Create a Spark Context.
    val conf = new SparkConf().setAppName("WordCount")
    val sc = new SparkContext(conf)

    // Define and run application.
    val input = sc.textFile(optionParser.inputFile())
    val counts =
      input
      .flatMap({ _.split(" ") })
      .map({ (_, 1) })
      .reduceByKey({ case (x, y) => x + y })
    counts.saveAsTextFile(optionParser.outputDir())

    System.exit(0)
  }
}
