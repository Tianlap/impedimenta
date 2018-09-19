ThisBuild / organization := "name.ichimonji10"
ThisBuild / scalaVersion := "2.12.6"
ThisBuild / version := "0.0.1"

lazy val root = (project in file("."))
  .settings(
    name := "Average Temperature",

    libraryDependencies += "org.apache.hadoop" % "hadoop-client" % "2.+",
    // For unit tests.
    libraryDependencies += "org.scalatest" %% "scalatest" % "3.0.+" % "test",
    libraryDependencies += "org.mockito" % "mockito-core" % "2.+" % "test",
  )
