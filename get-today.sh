#!/bin/bash
source ./get-cookie.sh
TODAY_LEADING_ZERO=$(date +'%d')
TODAY=$(date +'%-d')

echo $TODAY_LEADING_ZERO
echo $TODAY

mkdir -p $TODAY_LEADING_ZERO/01

curl \
--cookie $COOKIE \
https://adventofcode.com/2024/day/$TODAY/input \
-o $TODAY_LEADING_ZERO/01/input

cp script-template $TODAY_LEADING_ZERO/01/script.py
