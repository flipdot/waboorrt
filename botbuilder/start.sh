#!/bin/bash
set -euo pipefail

# TODO: tell webserver to authorize botbuilder for all repos

build () {
  imageName=$(printf %s "$1" | sha1sum | head -c 32)

  TMP_DIR=$(mktemp -d)
  cd "$TMP_DIR"
  echo "Building bot $1"
  git clone "ssh://git@gitserver:2222/$1.git" . || return 1
  docker build -t "localhost/bot/$imageName" . || return 1
  redis-cli -h redis set "user:$1" "{\"botname\": \"$1\"}"
  cd "$HOME"
}

while true; do
  botname="$(redis-cli -h redis BZPOPMIN 'botbuilder:queue' 0 | head -n 2 | tail -n 1)"
  build $botname || echo "Warning: Failed to build bot $botname"
done
