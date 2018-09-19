#!/usr/bin/env bash
# coding=utf-8
#
# Provide environment variables to Hadoop. Use this script by sourcing it.

# For Hadoop.
export HADOOP_CONF_DIR="$(realpath --canonicalize-existing configs)"
export HADOOP_HOME="$(realpath --canonicalize-existing 'data/hadoop-3.1.1')"
export JAVA_HOME=/usr/lib/jvm/default
