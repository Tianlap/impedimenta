#!/usr/bin/env bash
# coding=utf-8
set -euo pipefail

make data/hadoop-3.1.1

source scripts/hadoop-env.sh
data/hadoop-3.1.1/bin/hadoop \
    jar target/average-temperature-1-SNAPSHOT.jar \
    name.ichimonji10.average_temperature.AverageTemperature \
    "/user/$(whoami)/measurements.txt" \
    "/user/$(whoami)/output"
