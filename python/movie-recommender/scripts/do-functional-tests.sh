#!/usr/bin/env bash
# coding=utf-8
#
# Execute several rudimentary functional tests.
set -euo pipefail

mr-dataset install fixture
mr-db create fixture --overwrite
mr-analyze
rc=0

# Arguments: user ID, movie ID, target prediction
predict() {
    local prediction="$(mr-predict "$1" "$2")"
    local target="$3"
    if [ "${prediction}" != "${target}" ]; then
        echo "User $1, movie $2: ${prediction} != ${target}"
        rc=1
    fi
}

# best predictor: genre:Animation
predict 1 10 '1.0'
predict 1 11 '4.5'
predict 1 12 '1.0'
predict 1 13 '1.0'

# best predictor: year
# Inverse linear relationship between year and rating. Can't get predictions for
# movies that lack year data.
predict 2 10 '4.0'
predict 2 11 '2.0'

# best predictor: (no genres listed)
# All of the movies this user has rated have the `genre:(no genres listed)`
# genre. As a result, the scatter plot is a vertical line, and the
# recommendation is the average of ratings: 3.5.
predict 3 10 '3.5'
predict 3 11 '3.5'
predict 3 12 '3.5'
predict 3 13 '3.5'

# Best predictor: (no genres listed)
# The user hasn't rated any movies with year data, so the SSE for a
# year-based predictor is infinite.
predict 4 10 '4.5'
predict 4 11 '4.5'
predict 4 12 '4.5'
predict 4 13 '4.5'

exit "${rc}"
