#!/usr/bin/awk -f
# coding=utf-8
#
# Calculate the average Fahrenheit temperatures of each month in a year.
#
# The input is assumed to be a CSV file, where the first several rows are header
# information, and subsequent rows contain several measurements from a weather
# station at a point in time. One column contains the average temperature in
# fahrenheit for the past five minutes. Given such an input, this program will
# calculate and print the average temperature for each month.
#
# Input is assumed to be in chronological order. If a "back-in-time" row is
# encountered, a warning is printed, and the row is discarded. Also, input is
# assumed to be complete, with no missing measurements. If missing measurements
# are discovered, a warning is printed, and program execution continues as
# normal. These two assumptions allow the program to be implemented in a
# streamer, more efficient manner.
#
# A "year" argument may be passesd. If omitted, it defaults to 2013.
#
# Associate: Connor Schlatz

BEGIN {
    FS = ","
    if (year == "") {
        year = 2013
    } else {
        year = year + 0
    }
}

# Skip headers.
NR >= 5 {
    # Parse values from record. Sample input timestamp: "2013-01-01 00:00:00"
    temp = $11 + 0
    timestamp = $1
    gsub("\"", "", timestamp)
    gsub(/[-:]/, " ", timestamp)
    timestamp = mktime(timestamp)
    if (strftime("%Y", timestamp) + 0 != year) {next}
    month = strftime("%m", timestamp) + 0

    if (initialized) {
        # If the current record is older than the previous record, print an error
        # and discard the current record.
        if (timestamp < prev_timestamp) {
            printf \
                "Records should be in chronological order, but %s < %s. " \
                "Ignoring record.\n",
                strftime("%F %T", timestamp),
                strftime("%F %T", prev_timestamp) \
                > "/dev/stderr"
            next
        }

        # If we have not jumped exactly five minutes, print a warning and continue.
        if (timestamp != prev_timestamp + 300) {
            printf \
                "Records should be in five minute increments, but the jump " \
                "from %s to %s is %d seconds. Using record anyway.\n",
                strftime("%F %T", timestamp),
                strftime("%F %T", prev_timestamp),
                timestamp - prev_timestamp \
                > "/dev/stderr"
        }

        # If we have jumped to the next month, print the average temperature for
        # last month and reset counters.
        if (month > prev_month) {
            printf \
                "Average temperature for %s: %.1f F\n",
                strftime("%b %Y", prev_timestamp),
                summed_temp / num_measurements
            summed_temp = 0
            num_measurements = 0
        }
    }

    # Update counters.
    summed_temp += temp
    num_measurements += 1
    prev_timestamp = timestamp
    prev_month = month
    initialized = 1
}

# Print average temperature for final month.
END {
    printf \
        "Average temperature for Dec %s: %.1f F\n",
        year,
        summed_temp / num_measurements
}
