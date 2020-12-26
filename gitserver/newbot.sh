#!/bin/bash

set -euo pipefail

if [ "$#" -ne 3 ]; then
    echo "Usage: newbot <username> <templaterepo> <ssh-pub-key>"
    exit 1
fi

USERNAME=$1
TEMPLATEREPO=$2
PUBKEY=$3

id -u $USERNAME &>/dev/null || adduser -q --disabled-password --gecos "" --shell /usr/bin/git-shell $USERNAME
# backup to volume
cp -p /etc/gshadow /opt/etc/gshadow
cp -p /etc/shadow /opt/etc/shadow
cp -p /etc/group /opt/etc/group
cp -p /etc/passwd /opt/etc/passwd

# add ssh key
mkdir -p /home/$USERNAME/.ssh/
echo $PUBKEY > /home/$USERNAME/.ssh/authorized_keys

# init repository
mkdir -p /git/$USERNAME.git
chown $USERNAME:$USERNAME /git/$USERNAME.git
chmod 700 /git/$USERNAME.git
cd /git/$USERNAME.git
sudo -u $USERNAME git init --bare