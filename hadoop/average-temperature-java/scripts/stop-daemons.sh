#!/usr/bin/env bash
# coding=utf-8
#
# See:
# https://hadoop.apache.org/docs/r3.1.1/hadoop-project-dist/hadoop-common/ClusterSetup.html#Hadoop_Shutdown
make data/hadoop-3.1.1

source scripts/hadoop-env.sh
data/hadoop-3.1.1/sbin/stop-dfs.sh
data/hadoop-3.1.1/sbin/stop-yarn.sh
data/hadoop-3.1.1/bin/mapred --daemon stop historyserver
