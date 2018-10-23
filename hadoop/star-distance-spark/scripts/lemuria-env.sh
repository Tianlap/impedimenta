#!/usr/bin/env bash
# coding=utf-8
#
# Set environment variables specific to lemuria.cis.vtc.edu. Use by sourcing.

HADOOP_CONF_DIR="$(realpath --canonicalize-existing /home/hadoop/conf)"
HADOOP_HOME="$(realpath --canonicalize-existing '/usr/local/hadoop-3.1.1')"
PATH="${PATH}:${HADOOP_HOME}/bin"
PATH="${PATH}:/usr/local/sbt/bin"
PATH="${PATH}:/usr/local/jdk1.8.0_181/bin"
PATH="${PATH}:/usr/local/spark-2.3.1-bin-hadoop2.7/bin"
export HADOOP_CONF_DIR
export HADOOP_HOME
export PATH
