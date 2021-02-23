#!/bin/sh -eu

name="$1"
repo_template="/usr/local/share/git-templates/autodeploy"
repo_name="${name}"

git init --bare --template "${repo_template}" "${repo_name}"
