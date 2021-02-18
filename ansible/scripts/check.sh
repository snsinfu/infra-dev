#!/bin/sh -eu

test -n "${AWS_ACCESS_KEY_ID}"
test -n "${AWS_SECRET_ACCESS_KEY}"
test -n "${AWS_DEFAULT_REGION}"
test -n "${ANSIBLE_INVENTORY_S3_BUCKET}"
