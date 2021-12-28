#!/bin/bash
set -euo pipefail

mkdir -p /root/.ssh

ssh-keyscan -p $GITSERVER_PORT $GITSERVER_HOST > /root/.ssh/known_hosts

if [ ! -f /root/.ssh/id_ed25519 ]; then
  ssh-keygen -b 2048 -t ed25519 -f /root/.ssh/id_ed25519 -q -N ""
fi

SSH_PUBLIC_KEY=$(cat /root/.ssh/id_ed25519.pub)

echo "Copying SSH key to http://$WEBSERVER_HOST/api/internal/users"
curl -s -X POST "http://$WEBSERVER_HOST/api/internal/users" \
        -H "Content-Type: application/json" \
        -H "X-API-Key: $WEBSERVER_API_KEY" \
        --data "{\"ssh_public_key\": \"$SSH_PUBLIC_KEY\"}"

build () {
  imageName=$(printf %s "$1" | sha1sum | head -c 32)

  TMP_DIR=$(mktemp -d)
  cd "$TMP_DIR"
  echo "Building bot $1" >&2
  git clone "ssh://git@$GITSERVER_HOST:$GITSERVER_PORT/$1" . || return 1
  docker build -t "localhost/bot/$imageName" . || return 1
  redis-cli -h redis set "user:$1" "{\"botname\": \"$1\"}"
  cd "$HOME"
}

while true; do
  botname="$(redis-cli -h redis BZPOPMIN 'botbuilder:queue' 0 | head -n 2 | tail -n 1)"
  build $botname || echo "Warning: Failed to build bot $botname"
done
