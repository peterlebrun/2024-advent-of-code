#!/bin/bash
source ./get-cookie.sh
TODAY_LEADING_ZERO=$(date +'%d')
TODAY=$(date +'%-d')

echo $TODAY_LEADING_ZERO
echo $TODAY

for i in {01,02};
do
    mkdir -p $TODAY_LEADING_ZERO/$i

    curl \
    --cookie $COOKIE \
    https://adventofcode.com/2024/day/$TODAY/input \
    -o $TODAY_LEADING_ZERO/$i/input

    touch $TODAY_LEADING_ZERO/$i/script.py
    echo "with open('input', 'r') as f:" > $TODAY_LEADING_ZERO/$i/script.py
done
