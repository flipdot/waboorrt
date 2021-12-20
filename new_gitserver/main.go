package main

import (
	"fmt"
	"log"

	"github.com/sosedoff/gitkit"
	"golang.org/x/crypto/ssh"
)

// User-defined key lookup function. You can make a call to a database or
// some sort of cache storage (redis/memcached) to speed things up.
// Content is a string containing ssh public key of a user.
func lookupKey(content string) (*gitkit.PublicKey, error) {
	fmt.Println(content)
	key, _, _, _, err := ssh.ParseAuthorizedKey([]byte(content))
	if err != nil {
		fmt.Println(err)
		return nil, err
	}

	fingerprint := ssh.FingerprintSHA256(key)
	return &gitkit.PublicKey{Id: fingerprint}, nil
}

func authorize(keyId string, repo string) bool {
	fmt.Printf("Trying to access repo '%s' with key '%s'\n", repo, keyId)
	return true
}

func main() {
	// In the example below you need to specify a full path to a directory that
	// contains all git repositories, and also a directory that has a gitkit specific
	// ssh private and public key pair that used to run ssh server.
	server := gitkit.NewSSH(gitkit.Config{
		Dir:        "repos",
		KeyDir:     "keys",
		AutoCreate: true,
		Auth:       true,
	})

	// User-defined key lookup function. All requests will be rejected if this function
	// is not provider. SSH server only accepts key-based authentication.
	server.PublicKeyLookupFunc = lookupKey

	server.Authorize = authorize

	// Specify host and port to run the server on.
	err := server.ListenAndServe(":2222")
	if err != nil {
		log.Fatal(err)
	}
}
