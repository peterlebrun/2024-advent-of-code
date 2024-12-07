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

    cat <<EOF > $TODAY_LEADING_ZERO/$i/script.py
import sys
import copy
from collections import defaultdict
sys.setrecursionlimit(1073741824)

INPUT = "input_test" if sys.argv[2] == "--test" else "input"

with open('input', 'r') as f:

EOF
done
