#!/bin/bash

inotifywait -q -m /botbuilder |
while read -r filename event; do
  # TODO: fix inotify stuff
  TMP_DIR=$(mktemp -d)
  mkdir -p $TMP_DIR
  cd $TMP_DIR
  echo "Building bot $filename"
  git clone /git/$filename.git .
  docker build -t localhost/bot/$filename
  cd
  rm -rf $TMP_DIR
done