#!/bin/bash

while [ true ] ; do
  inotifywait -e create /botbuilder;
  while [ ! -z "$(ls /botbuilder/)" ]; do
    file=$(ls /botbuilder/ | head -n1);

    TMP_DIR=$(mktemp -d)
    mkdir -p $TMP_DIR
    cd $TMP_DIR
    echo "Building bot $file"
    git clone /git/$file.git .
    docker build -t localhost/bot/$file .
    redis-cli -h redis set "user:$file" "{\"botname\": \"$file\"}"
    cd

    rm /botbuilder/$file;
    done;
done
