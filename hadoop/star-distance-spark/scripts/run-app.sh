#!/usr/bin/env bash
# coding=utf-8
#
# Run the Star Distance application against one of the observations-*.txt files.
#
# This script is specific to lemuria.cis.vtc.edu.
set -euo pipefail

spark-submit \
    --packages 'org.rogach:scallop_2.11:3.1.3' \
    --class name.ichimonji10.star_distance.Main \
    target/scala-2.11/star-distance_2.11-0.0.1.jar \
    "/user/hadoop/observations-${1}.txt" \
    "star-distance-spark-${1}"
