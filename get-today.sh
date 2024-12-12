#!/bin/bash
TODAY=$(date +'%d')
FORCE=${1#*=}

echo -e "\nCreating day $TODAY"
echo "---------------------"

if [ ! -d "$TODAY/01" ] || [ "$FORCE" = "true" ] ; then
    echo "$TODAY/01 created."
    mkdir -p $TODAY/01
else
    echo "Directory $TODAY/01 already exists."
fi

if [ ! -e "$TODAY/01/script.py" ] || [ "$FORCE" = "true" ]; then
    echo "$TODAY/01/script.py created."
    cp script-template $TODAY/01/script.py
else
    echo "$TODAY/01/script.py already exists."
fi

if [ ! -e "$TODAY/01/input_test" ] || [ "$FORCE" = "true" ]; then
    echo "$TODAY/01/input_test created."
    touch $TODAY/01/input_test
else
    echo "$TODAY/01/input_test already exists."
fi

if [ ! -e "$TODAY/01/input" ] || [ "$FORCE" = "true" ]; then
    echo -e "Downloading day $((10#$TODAY)) input.\n"
    ./get-input.sh $TODAY
else
    echo "$TODAY/01/input already exist."
fi

git add $TODAY

echo -e "\nCreated:"

tree $TODAY

echo -e "\nInput:"
head -n 2 $TODAY/01/input
echo "..."
tail -n 2 $TODAY/01/input
