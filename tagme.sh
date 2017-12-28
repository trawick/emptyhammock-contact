#!/usr/bin/env bash

VERSION=`python -c "import e_contact; print e_contact.__version__"`
if git tag -a ${VERSION} -m "version ${VERSION}"; then
    exec git push --tags
fi
