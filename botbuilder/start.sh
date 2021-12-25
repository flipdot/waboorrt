#!/bin/bash

# TODO: tell webserver to authorize botbuilder for all repos

while true; do
  botname="$(redis-cli -h redis BZPOPMIN 'botbuilder:queue' 0 | head -n 2 | tail -n 1)"
  imageName=$(printf %s "$file" | sha1sum | head -c 32)

  TMP_DIR=$(mktemp -d)
  cd "$TMP_DIR" || exit
  echo "Building bot $botname"
  git clone "ssh://git@gitserver:2222/$botname.git" .
  docker build -t "localhost/bot/$imageName" .
  redis-cli -h redis set "user:$botname" "{\"botname\": \"$botname\"}"
  cd "$HOME" || exit
done
