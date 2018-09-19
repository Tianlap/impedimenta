#!/usr/bin/env bash
# coding=utf-8
set -euo pipefail

make data/hadoop-3.1.1

source scripts/hadoop-env.sh
data/hadoop-3.1.1/bin/hadoop \
    jar target/scala-2.12/average-temperature_2.12-0.0.1.jar \
    -libjars /usr/share/scala/lib/scala-library.jar \
    "/user/$(whoami)/measurements.txt" \
    "/user/$(whoami)/output"
