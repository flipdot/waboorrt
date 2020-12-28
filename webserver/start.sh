#!/bin/bash

if [ ! -f "$HOME/.ssh/id_rsa" ]; then
  echo "Generating SSH key and persisting pubkey on redis"
  ssh-keygen -b 2048 -t rsa -f "$HOME/.ssh/id_rsa" -q -N ""
fi
python ssh2redis.py
gunicorn -w 2 -b 0.0.0.0:80 app:app
