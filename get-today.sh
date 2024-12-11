#!/bin/bash
source ./get-cookie.sh
TODAY=$(date +'%d')

mkdir -p $TODAY/01

cp script-template $TODAY/01/script.py
touch $TODAY/01/input_test

./get-input.sh $TODAY
git add $TODAY
