#!/bin/bash

set -euo pipefail

if [ "$#" -ne 3 ]; then
    echo "Usage: newbot <username> <templaterepo> <ssh-pub-key>"
    exit 1
fi

USERNAME=$1
TEMPLATEREPO=$2
PUBKEY=$3

gitolite create "u/$USERNAME"
# prepopulate repo
TMP_DIR=$(mktemp -d)
git clone -q "git@localhost:u/$USERNAME.git" "$TMP_DIR"
cd "$TMP_DIR"
cp -r "/app/bot-templates/$TEMPLATEREPO/"* .
git add -A
git commit -qm "Initialized with $TEMPLATEREPO template"
gitolite push -q origin master
cd
rm -rf "$TMP_DIR"

# # install hooks
# ln -s /app/post-receive.sh "/git/$USERNAME.git/hooks/post-receive"
