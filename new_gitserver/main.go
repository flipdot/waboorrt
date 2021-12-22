package main

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"net/http"

	"github.com/sosedoff/gitkit"
)

type checkPublicKeyRequest struct {
	PublicKey string `json:"publicKey"`
}

type checkPublicKeyResponse struct {
	Id string `json:"id"`
}

func httpSuccess(statusCode int) bool {
	return statusCode >= 200 && statusCode <= 299
}

// User-defined key lookup function. You can make a call to a database or
// some sort of cache storage (redis/memcached) to speed things up.
// Content is a string containing ssh public key of a user.
func lookupKey(content string) (*gitkit.PublicKey, error) {
	body, err := json.Marshal(&checkPublicKeyRequest{PublicKey: content})
	if err != nil {
		return nil, err
	}
	resp, err := http.Post("http://webserver/git/check-public-key", "application/json", bytes.NewBuffer(body))
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode == http.StatusNotFound {
		return nil, errors.New(fmt.Sprintf("public key not registered: %s", content))
	}

	if !httpSuccess(resp.StatusCode) {
		return nil, errors.New(fmt.Sprintf("Checking public key failed with status code %d", resp.StatusCode))
	}

	var respBody []byte
	_, err = resp.Body.Read(respBody)
	if err != nil {
		return nil, err
	}
	responseData := checkPublicKeyResponse{}
	err = json.Unmarshal(respBody, &responseData)
	if err != nil {
		return nil, err
	}

	return &gitkit.PublicKey{Id: responseData.Id}, nil
}

type checkAuthorizationRequest struct {
	KeyId string `json:"keyId"`
	Repo  string `json:"repo"`
}

type checkAuthorizationResponse struct {
	Authorized bool `json:"authorized"`
}

func authorize(keyId string, repo string) (bool, error) {
	body, err := json.Marshal(&checkAuthorizationRequest{KeyId: keyId, Repo: repo})
	if err != nil {
		return false, err
	}
	resp, err := http.Post("http://webserver/git/check-access", "application/json", bytes.NewBuffer(body))
	if err != nil {
		return false, err
	}
	defer resp.Body.Close()

	if !httpSuccess(resp.StatusCode) {
		return false, errors.New(fmt.Sprintf("Checking authorization key failed with status code %d\n", resp.StatusCode))
	}

	var respBody []byte
	_, err = resp.Body.Read(respBody)
	if err != nil {
		return false, err
	}
	responseData := checkAuthorizationResponse{}
	err = json.Unmarshal(respBody, &responseData)
	if err != nil {
		return false, err
	}

	return responseData.Authorized, nil
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
