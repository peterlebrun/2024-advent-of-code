#!/bin/bash
curl --cookie $(cat ./COOKIE) \
https://adventofcode.com/2024/day/$((10#$1))/input \
-o $1/01/input
