#!/bin/sh

redis-cli -h redis del gitserver-root-sshkey > /dev/null # TODO: see ../webserver/start.sh
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

echo "Setting up gitolite"
echo "$AUTHORIZED_KEY" > /tmp/admin.pub
su - git -c 'gitolite setup -pk /tmp/admin.pub'

cp -f /app/gitolite.rc /home/git/.gitolite.rc
chown git:git /home/git/.gitolite.rc

echo "Starting sshd"
/usr/sbin/sshd -D
