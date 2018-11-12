#!/usr/bin/env bash
# coding=utf-8
set -euo pipefail

spark-submit \
    --packages 'org.rogach:scallop_2.11:3.1.3' \
    --class name.ichimonji10.rfc_analyzer.RFCAnalyzer \
    target/scala-2.11/rfc-analyzer_2.11-0.0.1.jar \
    /user/hadoop/RFCs.zip
