#!/bin/bash
source ./get-cookie.sh
TODAY_LEADING_ZERO=$(date +'%d')
TODAY=$(date +'%-d')

mkdir -p $TODAY_LEADING_ZERO/01

pushd $TODAY_LEADING_ZERO/01
curl \
--cookie $COOKIE \
https://adventofcode.com/2024/day/$TODAY/input \
-o input

cp ../../script-template script.py
touch input_test
popd

git add $TODAY_LEADING_ZERO
