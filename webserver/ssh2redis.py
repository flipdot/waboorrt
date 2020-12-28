#!/usr/bin/env python3

# this file only exists because I didn't want to install redis-tools in container
import os
import redis

HOME = os.environ["HOME"]
with open(f"{HOME}/.ssh/id_rsa.pub") as f:
    pubkey = f.read().strip()

db = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)
db.set("gitserver-root-sshkey", pubkey)
