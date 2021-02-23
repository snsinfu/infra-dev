#!/bin/sh -eu

name="$1"
dataset="main/data/volumes/${name}"

zfs create "${dataset}"
