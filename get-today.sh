#!/bin/bash
source ./get-cookie.sh
TODAY=$(date +'%d')

echo $TODAY

for i in {01,02};
do
    mkdir -p $TODAY/$i

    curl \
    --cookie $COOKIE \
    https://adventofcode.com/2023/day/$TODAY/input \
    -o $TODAY/$i/input

    touch $TODAY/$i/script.py
    echo "with open('input', 'r') as f:" > $TODAY/$i/script.py
done
