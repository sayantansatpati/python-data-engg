#!/usr/bin/env python
__author__ = 'ssatpati'

import sys

last_comp_key = None
last_artist = None
last_date = None

total_performances = 0


def emit():
    """Emit the output from Reducer"""
    print("{0}\t{1}\t{2}".format(last_artist, last_date, total_performances))


# input comes from STDIN (standard input)
for line in sys.stdin:
    try:
         # remove leading and trailing whitespace
        line = line.strip()
        # Split the line into tokens
        (comp_key, artist, perf_per_day) = line.split('\t')
        # Split the sorted compound key
        (key, dt) = comp_key.split('^')

        if comp_key != last_comp_key:
            if last_comp_key:
                # Emit
                emit()
            # Reset
            last_comp_key = comp_key;
            last_date = dt;
            last_artist = artist
            total_performances = int(perf_per_day)
        else:
            if last_date != dt:  # Same Artist but different dates
                # Emit
                emit()
                # Reset
                last_date = dt;
                total_performances = int(perf_per_day)
            else:  # Same Artist & Dates
                total_performances += int(perf_per_day)
    except:
        print("[Reducer] Ignoring record: {0}".format(line))
        pass

# The last set of Artist
emit()
