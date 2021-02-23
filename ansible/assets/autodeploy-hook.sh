#!/bin/sh -eu

reponame="$(basename "${PWD}")"
buildroot="${HOME}/.tmp/${reponame}"

rm -rf "${buildroot}"

while read oldrev newrev refname; do
    echo "Creating build directory"
    mkdir -p "${buildroot}"

    branch="${refname#refs/heads/}"
    echo "Checking out ${branch}:${newrev}"
    git archive "${newrev}" | tar -x -C "${buildroot}"
    cd "${buildroot}"

    echo "Running deploy.sh"
    ./deploy.sh

    echo "Cleaning up build directory"
    cd -
    rm -rf "${buildroot}"
done
