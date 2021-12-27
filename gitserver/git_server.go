package main

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"net/url"
	"os"
	"time"

	"github.com/sosedoff/gitkit"
)

// Defaults suitable for local development if webserver is started via compose
var WEBSERVER_HOST = getenv("WEBSERVER_HOST", "localhost")
var WEBSERVER_PORT = getenv("WEBSERVER_PORT", "80")
var apiKey string

func getenv(key, defaultValue string) string {
	value, exists := os.LookupEnv(key)
	if !exists {
		return defaultValue
	}
	return value
}

type loginRequest struct {
	Username string `json:"username"`
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
	httpClient := &http.Client{}
	apiUrl := endpointUrl("/internal/users/by-ssh-key/" + url.PathEscape(content))
	req, err := http.NewRequest("GET", apiUrl, nil)
	req.Header.Add("X-API-Key", apiKey)
	resp, err := httpClient.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode == http.StatusUnauthorized {
		return nil, errors.New("API returned 401 unauthorized. Invalid API key?")
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

type checkAuthorizationRequest struct {
	UserId string `json:"user_id"`
	Repo   string `json:"repository_name"`
}

type checkAuthorizationResponse struct {
	Read  bool `json:"read"`
	Write bool `json:"write"`
}

func authorize(userId string, repo string) (bool, error) {
	body, err := json.Marshal(&checkAuthorizationRequest{UserId: userId, Repo: repo})
	if err != nil {
		return false, err
	}

	httpClient := &http.Client{}
	apiUrl := endpointUrl("/internal/query/check-repository-permissions")
	req, err := http.NewRequest("POST", apiUrl, bytes.NewBuffer(body))
	req.Header.Add("Content-Type", "application/json")
	req.Header.Add("X-API-Key", apiKey)
	resp, err := httpClient.Do(req)
	if err != nil {
		return false, err
	}
	defer resp.Body.Close()

	if !httpSuccess(resp.StatusCode) {
		return false, errors.New(fmt.Sprintf("Checking authorization key failed with status code %d\n", resp.StatusCode))
	}

	respBody, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return false, err
	}
	responseData := checkAuthorizationResponse{}
	err = json.Unmarshal(respBody, &responseData)
	if err != nil {
		return false, err
	}

	return responseData.Write, nil
}

func ServeGitSshServer(config gitkit.Config, webserverApiKey string) {
	apiKey = webserverApiKey
	// In the example below you need to specify a full path to a directory that
	// contains all git repositories, and also a directory that has a gitkit specific
	// ssh private and public key pair that used to run ssh server.
	server := gitkit.NewSSH(config)

	// User-defined key lookup function. All requests will be rejected if this function
	// is not provider. SSH server only accepts key-based authentication.
	server.PublicKeyLookupFunc = lookupKey
	server.Authorize = authorize

	for {
		resp, err := http.Get(endpointUrl("/health"))
		if err == nil && resp.StatusCode == http.StatusOK {
			break
		}
		log.Println("Waiting for webserver at " + endpointUrl("") + " to become ready.")
		time.Sleep(3 * time.Second)
	}
	httpClient := &http.Client{}
	apiUrl := endpointUrl("/internal/auth_test")
	req, err := http.NewRequest("GET", apiUrl, nil)
	req.Header.Add("X-API-Key", apiKey)
	resp, err := httpClient.Do(req)
	if err != nil {
		log.Fatal(err)
	}
	if resp.StatusCode != http.StatusOK {
		log.Fatal("Can't authorize to webserver. Please check your API-Key")
	}

	// Specify host and port to run the server on.
	log.Println("SSH server listening on port 2222")
	err = server.ListenAndServe(":2222")
	if err != nil {
		log.Fatal(err)
	}
}
