#!/usr/bin/env python3

# snapshot_retention.py
#   --prefix <snapshot prefix>
#   --ttl <time-to-live>
#   --now <current time>
#
# This script takes a list of zfs snapshots from stdin and prints "expired"
# ones to stdout. Snapshots are assumed to be named as
#
#   prefix YYYYMMDD "T" hhmmss
#
# where prefix is an arbitrary prefix (given as --prefix flag), YYYY is the
# year, MM is the month, DD is the day of the month and hh:mm:ss is the time
# when the snapshot is taken. This time is compared against the current time
# (given as --now flag) and the snapshot is flagged as expired if it's older
# than given time-to-live.

import argparse
import datetime
import os
import re
import signal
import sys


RE_TTL = re.compile(r"(\d+)(\w+)")


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    signal.signal(signal.SIGTERM, signal.SIG_DFL)
    run(**parse_args())


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prefix", type=str)
    parser.add_argument("--ttl", type=str)
    parser.add_argument("--now", type=str)
    return vars(parser.parse_args())


def run(prefix, ttl, now):
    ttl = parse_ttl(ttl)
    now = parse_time(now)
    snap_list = (line.rstrip() for line in sys.stdin)

    for snap in snap_list:
        if not snap.startswith(prefix):
            continue

        snap_time = snap[len(prefix):]
        try:
            snap_time = parse_time(snap_time)
        except ValueError:
            continue

        if now >= snap_time + ttl:
            print(snap)


def parse_ttl(s):
    match = RE_TTL.match(s)
    if not match:
        raise Exception("invalid TTL")

    amount = int(match[1])
    unit = match[2]

    if unit == "hour":
        return datetime.timedelta(hours=amount)
    if unit == "day":
        return datetime.timedelta(days=amount)
    if unit == "week":
        return datetime.timedelta(weeks=amount)

    raise Exception("unrecognized unit for TTL")


def parse_time(s):
    return datetime.datetime.strptime(s, "%Y%m%dT%H%M%S")


if __name__ == "__main__":
    main()
