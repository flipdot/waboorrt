#!/bin/bash

echo "Reticulating splines..."
echo "Please be excellent to us and do not mine coins or things like that. We will build your stuff with docker build in a few moments"

BOTNAME=$(pwd | sed -E 's%(^/git/([a-zA-Z0-9_-]+)\.git)|.*$%\2%')

if [ -z "$BOTNAME" ]; then
  echo "We couldn't read your botname. Either you are doing nasty things, or we aren't prepared for some chars in your username."
  echo "Feel free to contact me at soerface@flipdot.org"
  exit 1
fi

touch "/botbuilder/$BOTNAME"
