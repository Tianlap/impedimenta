#!/usr/bin/env bash
# coding=utf-8
#
# Install data/hadoop-3.1.1/.
set -euo pipefail

readonly src_archive="$(
    realpath --canonicalize-missing ~/.cache/average-temperature/hadoop-3.1.1.tar.gz
)"
readonly dst_dir="$(realpath --canonicalize-existing data)"

# TODO: Download into /tmp/..., then move to ~/.cache/..., thus preventing
# partial downloads.
if [ ! -e "${src_archive}" ]; then
    mkdir -p "$(dirname "${src_archive}")"
    curl -o "${src_archive}" \
        'https://www.apache.org/dyn/closer.cgi/hadoop/common/hadoop-3.1.1/hadoop-3.1.1-src_archive.tar.gz'
fi
tar -xz --directory "${dst_dir}" -f "${src_archive}"
