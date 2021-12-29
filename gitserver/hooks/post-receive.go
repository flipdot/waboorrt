package main

import (
	"context"
	"log"
	"os"
	"strings"
	"time"

	"github.com/go-redis/redis/v8"
	"github.com/sosedoff/gitkit"
)

func receive(hook *gitkit.HookInfo, tmpPath string) error {
	if hook.Action == gitkit.BranchPushAction && hook.RefName == "main" {
		// pushing to main -> trigger botbuilder
		ctx := context.Background()

		rdb := redis.NewClient(&redis.Options{
			Addr: "redis:6379",
		})

		repoPath := strings.TrimPrefix(hook.RepoPath, os.Getenv("REPOS_FOLDER"))

		rdb.ZAdd(ctx, "botbuilder:queue", &redis.Z{Score: float64(time.Now().Unix()), Member: repoPath})
	}

	return nil
}

func main() {
	receiver := gitkit.Receiver{
		MainOnly:    false,
		TmpDir:      "/tmp/gitkit",
		HandlerFunc: receive,
	}

	if err := receiver.Handle(os.Stdin); err != nil {
		log.Println("Error:", err)
		os.Exit(1)
	}
}
