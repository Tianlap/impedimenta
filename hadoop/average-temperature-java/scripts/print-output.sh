#!/usr/bin/env bash
# coding=utf-8
#
# Pretty-print the contents of `/user/$(whoami)/output/part*`.
set -euo pipefail

# Bash probably has facilities for printing localized date-time information, and
# if they exist, they should be used instead. This is an anglo-centric hack.
readonly months=(
    January
    February
    March
    April
    May
    June
    July
    August
    September
    October
    November
    December
)
readonly year=0
readonly month=1
readonly temp=2

source scripts/hadoop-env.sh
mapfile -t lines < <(data/hadoop-3.1.1/bin/hadoop fs -cat "/user/$(whoami)/output/part*" | sort)
for line in "${lines[@]}"; do
    # Split line into a (year month temp) array.
    mapfile -t fields < <(echo -n "${line}" \
        | awk -F '[-[:space:]]' '{print $1 "\n" $2 "\n" $3}'
    )
    # Year and month values may have leading zeroes. Strip them off, to privent
    # Bash from interpreting them as octal numbers.
    fields["${year}"]="${fields["${year}"]#0}"
    fields["${month}"]="${fields["${month}"]#0}"
    # Months range from 1–12. Ajust the range to 0–11.
    fields["${month}"]=$(("${fields["${month}"]}" - 1))
    echo "The average temperature for ${months["${fields["${month}"]}"]} ${fields["${year}"]} is ${fields["${temp}"]%.*} F."
done
