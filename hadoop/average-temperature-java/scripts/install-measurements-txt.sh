#!/usr/bin/env bash
# coding=utf-8
#
# Install data/measurements.txt.
set -euo pipefail

readonly src_archive="$(
    realpath --canonicalize-missing \
        ~/.cache/average-temperature/measurements.zip
)"
readonly dst_dir="$(realpath --canonicalize-existing data)"

# TODO: Download into /tmp/..., then move to ~/.cache/..., thus preventing
# partial downloads.
if [ ! -e "${src_archive}" ]; then
    mkdir -p "$(dirname "${src_archive}")"
    curl -o "${src_archive}" \
        'http://www.pchapin.org/VTC/cis-4250/20130101-20160531.zip'
fi
unzip -p "${src_archive}" 20130101-20160531.txt > "${dst_dir}/measurements.txt"
