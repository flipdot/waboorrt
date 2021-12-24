package main

import (
	"github.com/sosedoff/gitkit"
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

	go ServeHttpApi(config)
	ServeGitSshServer(config)
}
