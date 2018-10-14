#!/usr/bin/env bash
# coding=utf-8
#
# Provide environment variables to the Hadoop client. Use by sourcing.
#
# This script is specific to lemuria.cis.vtc.edu.

HADOOP_CONF_DIR="$(realpath --canonicalize-existing /home/hadoop/conf)"
HADOOP_HOME="$(realpath --canonicalize-existing '/usr/local/hadoop-3.1.1')"
PATH="/usr/local/hadoop-3.1.1/bin:${PATH}"
export HADOOP_CONF_DIR
export HADOOP_HOME
export PATH
