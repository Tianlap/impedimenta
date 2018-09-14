#!/usr/bin/env bash
# coding=utf-8
#
# See:
# https://hadoop.apache.org/docs/r3.1.1/hadoop-project-dist/hadoop-common/ClusterSetup.html#Hadoop_Startup
make data/hadoop-3.1.1

source scripts/hadoop-env.sh
data/hadoop-3.1.1/sbin/start-dfs.sh
data/hadoop-3.1.1/sbin/start-yarn.sh
data/hadoop-3.1.1/bin/mapred --daemon start historyserver
