#!/bin/sh

mkdir -p /opt/etc

if [ -f "/opt/etc/shadow" ]; then
    cp -p /opt/etc/shadow /etc/shadow
    echo "copied /etc/shadow from volume"
fi

if [ -f "/opt/etc/passwd" ]; then
    cp -p /opt/etc/passwd /etc/passwd
    echo "copied /etc/passwd from volume"
fi

if [ -f "/opt/etc/group" ]; then
    cp -p /opt/etc/group /etc/group
    echo "copied /etc/group from volume"
fi

if [ -f "/opt/etc/gshadow" ]; then
    cp -p /opt/etc/gshadow /etc/gshadow
    echo "copied /etc/gshadow from volume"
fi

redis-cli -h redis del gitserver-root-sshkey > /dev/null
echo "Getting SSH pubkey from redis..."
AUTHORIZED_KEY=""
while [ -z "$AUTHORIZED_KEY" ]; do
  AUTHORIZED_KEY=$(redis-cli -h redis get gitserver-root-sshkey)
  sleep 1
done

mkdir -p /root/.ssh
echo "Writing $AUTHORIZED_KEY to /root/.ssh/authorized_keys"
echo "$AUTHORIZED_KEY" > /root/.ssh/authorized_keys

redis-cli -h redis del gitserver-root-sshkey > /dev/null
echo "Starting sshd"
/usr/sbin/sshd -D