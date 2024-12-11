#!/bin/bash
source ./get-cookie.sh

pushd $1/01
curl --cookie $COOKIE \
https://adventofcode.com/2024/day/$((10#$1))/input \
-o input
popd
