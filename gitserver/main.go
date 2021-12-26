package main

import (
	"fmt"
	"github.com/sosedoff/gitkit"
	"os"
)

func main() {
	config := gitkit.Config{
		Dir:        "repos",
		KeyDir:     "keys",
		GitPath:    "git",
		AutoCreate: true,
		Auth:       true,
		AutoHooks:  true,
		Hooks: &gitkit.HookScripts{
			PostReceive: `#!/bin/sh
cat | /app/post-receive
			`,
		},
	}
	if len(os.Args) < 2 {
		fmt.Println("You need to pass the API key that this server uses to authenticate against the webserver as first parameter.")
		fmt.Println("If you don't have a key, go to $REPO/webserver and execute:")
		fmt.Println("	pipenv run python manage.py create-api-key")
	}
	webserverApiKey := os.Args[1]

	go ServeHttpApi(config)
	ServeGitSshServer(config, webserverApiKey)
}
