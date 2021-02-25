#!/bin/sh -eu

dataset="main/data"
ttl="7day"
prefix="${dataset}@daily-"
now="$(date +%Y%m%dT%H%M%S)"
snapshot="${prefix}${now}"

echo "Taking snapshot ${snapshot}"
zfs snapshot -r "${snapshot}" || true

zfs list -t snapshot -H -o name "${dataset}" |
snapshot_retention.py --prefix "${prefix}" --ttl "${ttl}" --now "${now}" |
while read snap; do
    echo "Destroying expired snapshot ${snap}"
    zfs destroy -r "${snap}" || true
done
