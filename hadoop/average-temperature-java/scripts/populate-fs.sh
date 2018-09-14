#!/usr/bin/env bash
# coding=utf-8
set -euo pipefail

# Get data.
readonly src='data/measurements.txt'
make "${src}"
readonly dst="/user/$(whoami)/$(basename "${src}")"

# Copy data into HDFS.
source scripts/hadoop-env.sh
if data/hadoop-3.1.1/bin/hadoop fs -ls "${dst}" >/dev/null; then
    echo 'FS already populated.'
else
    echo 'Populating FS'
    data/hadoop-3.1.1/bin/hadoop fs -mkdir -p "$(dirname "${dst}")"
    data/hadoop-3.1.1/bin/hadoop fs -put "${src}" "$(dirname "${dst}")/"
fi
