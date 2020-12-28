#!/bin/bash

if [ ! -f "$HOME/.ssh/id_rsa" ]; then
  echo "Generating SSH key and persisting pubkey on redis"
  ssh-keygen -b 2048 -t rsa -f "$HOME/.ssh/id_rsa" -q -N ""
fi
# TODO: quick work around, redo the whole "trigger creating an account from webserver"
sleep 3
python ssh2redis.py
echo "Getting host key from gitserver"

KNOWN_HOSTS=$HOME/.ssh/known_hosts
touch "$KNOWN_HOSTS"
while [ ! -s "$KNOWN_HOSTS" ]; do
  ssh-keyscan gitserver > "$KNOWN_HOSTS" 2> /dev/null
done
gunicorn -w 2 -b 0.0.0.0:80 app:app
