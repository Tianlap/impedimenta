ThisBuild / organization := "name.ichimonji10"
ThisBuild / scalaVersion := "2.11.8"
ThisBuild / version := "0.0.1"

lazy val root = (project in file("."))
  .settings(
    name := "Star Distance",

    // For application.
    libraryDependencies += "org.apache.spark" %% "spark-core" % "2.3.1",
    libraryDependencies += "org.rogach" %% "scallop" % "3.1.+",

    // For unit tests.
    libraryDependencies += "org.scalatest" %% "scalatest" % "3.0.+" % "test",
  )
