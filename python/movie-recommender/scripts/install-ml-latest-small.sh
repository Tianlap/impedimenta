#!/usr/bin/env bash
# coding=utf-8
#
# Install data/ml-latest-small.
set -euo pipefail

readonly src_archive="$(
    realpath --canonicalize-missing ~/.cache/movie-recommender/ml-latest-small.zip
)"
readonly dst_dir="$(realpath --canonicalize-existing data)"

# Create a workspace, and schedule it for deletion.
cleanup() { if [ -n "${working_dir:-}" ]; then rm -rf "${working_dir}"; fi }
trap cleanup EXIT  # bash pseudo signal
trap 'cleanup ; trap - SIGINT ; kill -s SIGINT $$' SIGINT
trap 'cleanup ; trap - SIGTERM ; kill -s SIGTERM $$' SIGTERM
working_dir="$(mktemp --directory)"

# Download data set, move into per-user cache, and unpack into destination.
if [ ! -e "${src_archive}" ]; then
    curl -o "${working_dir}/ml-latest-small.zip" \
        http://files.grouplens.org/datasets/movielens/ml-latest-small.zip
    install -D "${working_dir}/ml-latest-small.zip" "${src_archive}"
fi
unzip -d "${dst_dir}" "${src_archive}"
