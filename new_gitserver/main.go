package main

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"github.com/sosedoff/gitkit"
	"io/ioutil"
	"log"
	"net/http"
	"net/url"
	"os"
)

// Defaults suitable for local development if webserver is started via compose
var WEBSERVER_HOST = getenv("WEBSERVER_HOST", "localhost")
var WEBSERVER_PORT = getenv("WEBSERVER_PORT", "80")
var sessionToken string

func getenv(key, defaultValue string) string {
	value, exists := os.LookupEnv(key)
	if !exists {
		return defaultValue
	}
	return value
}

type checkPublicKeyRequest struct {
	PublicKey string `json:"publicKey"`
}

type checkPublicKeyResponse struct {
	Id string `json:"id"`
}

func httpSuccess(statusCode int) bool {
	return statusCode >= 200 && statusCode <= 299
}

func endpointUrl(endpoint string) string {
	var baseUrl string
	if WEBSERVER_PORT == "443" {
		baseUrl = "https://" + WEBSERVER_HOST
	} else if WEBSERVER_PORT == "80" {
		baseUrl = "http://" + WEBSERVER_HOST
	} else {
		baseUrl = "http://" + WEBSERVER_HOST + ":" + WEBSERVER_PORT
	}
	return baseUrl + "/api" + endpoint
}

func getSessionToken() (string, error) {
	reqBody, err := json.Marshal(&loginRequest{Username: "gitserver"})
	if err != nil {
		return "", err
	}
	// TODO: this endpoint is currently only available for local development since it doesn't check credentials
	resp, err := http.Post(endpointUrl("/auth/login"), "application/json", bytes.NewBuffer(reqBody))
	if err != nil {
		return "", err
	}
	resBody, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}
	return string(resBody), nil
}

// User-defined key lookup function. You can make a call to a database or
// some sort of cache storage (redis/memcached) to speed things up.
// Content is a string containing ssh public key of a user.
func lookupKey(content string) (*gitkit.PublicKey, error) {
	httpClient := &http.Client{}
	if sessionToken == "" {
		var err error
		sessionToken, err = getSessionToken()
		if err != nil {
			return nil, err
		}
	}
	apiUrl := endpointUrl("/internal/users/by-ssh-key/" + url.PathEscape(content))
	req, err := http.NewRequest("GET", apiUrl, nil)
	req.Header.Add("X-Session-Key", sessionToken)
	resp, err := httpClient.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode == http.StatusForbidden {
		sessionToken = ""
		return nil, errors.New("API returned 403 forbidden. Session expired? Try again")
	}

	if resp.StatusCode == http.StatusNotFound {
		return nil, errors.New(fmt.Sprintf("public key not registered: %s", content))
	}

	if !httpSuccess(resp.StatusCode) {
		return nil, errors.New(fmt.Sprintf("Checking public key failed with status code %d", resp.StatusCode))
	}

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}
	responseData := checkPublicKeyResponse{}
	err = json.Unmarshal(body, &responseData)
	if err != nil {
		return nil, err
	}
	return &gitkit.PublicKey{Id: responseData.Id}, nil
}

type loginRequest struct {
	Username string `json:"username"`
}

type checkAuthorizationRequest struct {
	KeyId string `json:"keyId"`
	Repo  string `json:"repo"`
}

type checkAuthorizationResponse struct {
	Authorized bool `json:"authorized"`
}

func authorize(userId string, repo string) (bool, error) {
	//fmt.Println(userId)
	//fmt.Println(repo)
	//return false, nil
	body, err := json.Marshal(&checkAuthorizationRequest{KeyId: userId, Repo: repo})
	if err != nil {
		return false, err
	}

	resp, err := http.Post(endpointUrl("/internal/repositories/OWNER/REPO_NAME/permissions"), "application/json", bytes.NewBuffer(body))
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
	fmt.Println("Git / SSH server listening on localhost:2222")
	err := server.ListenAndServe(":2222")
	if err != nil {
		log.Fatal(err)
	}
}
