#!/bin/bash

set -euo pipefail

if [ "$#" -ne 3 ]; then
    echo "Usage: newbot <username> <templaterepo> <ssh-pub-key>"
    exit 1
fi

USERNAME=$1
TEMPLATEREPO=$2
PUBKEY=$3

id -u "$USERNAME" &>/dev/null || adduser -q --disabled-password --gecos "" --shell /usr/bin/git-shell "$USERNAME"
# backup to volume
cp -p /etc/gshadow /opt/etc/gshadow
cp -p /etc/shadow /opt/etc/shadow
cp -p /etc/group /opt/etc/group
cp -p /etc/passwd /opt/etc/passwd

# init repository
if [ ! -d "/git/$USERNAME.git" ]; then
  mkdir -p "/git/$USERNAME.git"
  chown "$USERNAME:$USERNAME" "/git/$USERNAME.git"
  chmod 700 "/git/$USERNAME.git"
  cd "/git/$USERNAME.git"
  sudo -u "$USERNAME" git init --bare
  # prepopulate repo
  TMP_DIR=$(mktemp -d)
  cd "$TMP_DIR"
  git clone -q "/git/$USERNAME.git"
  cd "$USERNAME"
  cp -r "/app/bot-templates/$TEMPLATEREPO/"* .
  git add -A
  git commit -qm "Initialized with $TEMPLATEREPO template"
  git push -q origin master
  cd
  rm -rf "$TMP_DIR"

  # install hooks
  ln -s /app/post-receive.sh "/git/$USERNAME.git/hooks/post-receive"
fi

# everything ready; give the user access by adding their ssh key
mkdir -p "/home/$USERNAME/.ssh/"
echo "$PUBKEY" > "/home/$USERNAME/.ssh/authorized_keys"