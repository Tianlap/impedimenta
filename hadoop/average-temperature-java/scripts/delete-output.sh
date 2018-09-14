#!/usr/bin/env bash
# coding=utf-8
set -euo pipefail

# Delete output data created by application.
source scripts/hadoop-env.sh
data/hadoop-3.1.1/bin/hadoop fs -rm -r "/user/$(whoami)/output"
