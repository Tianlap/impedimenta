#!/usr/bin/env bash
# coding=utf-8
#
# Run the Star Distance application against one of the observations-*.txt files.
#
# This script is specific to lemuria.cis.vtc.edu.
set -euo pipefail

hadoop jar star-distance_2.12-0.0.1.jar \
    -libjars /usr/local/scala-2.11.8/lib/scala-library.jar \
    "/user/hadoop/observations-${1}.txt" \
    "star-distance-${1}"
