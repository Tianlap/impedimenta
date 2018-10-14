#!/usr/bin/awk -f
# coding=utf-8
#
# Calculate the distance from the sun to some number of stars.
#
# Calculate these distances using a `stars-*.txt` file, not an
# `observations-*.txt` file. Sample usage:
#
#   hadoop fs -cat /user/hadoop/stars-1.txt | star-distance.awk

BEGIN {
    FS = ","
}

{
    star_id = $1 + 0
    x_dist = $2 + 0
    y_dist = $3 + 0
    z_dist = $4 + 0
    abs_distance = sqrt(x_dist^2 + y_dist^2 + z_dist^2)
    printf star_id " " abs_distance "\n"
}
