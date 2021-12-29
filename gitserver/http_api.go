package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"regexp"

	"github.com/sosedoff/gitkit"
)

type createRepoBody struct {
	Id       string `json:"id"`
	Template string `json:"template"`
}

var ID_REGEX = regexp.MustCompile("^[a-zA-Z0-9_\\-/\\.]+$")

func ServeHttpApi(config gitkit.Config) {
	http.HandleFunc("/repos", func(resp http.ResponseWriter, req *http.Request) {
		defer req.Body.Close()

		if req.Method != "POST" {
			resp.WriteHeader(400)
			resp.Write([]byte("Method not allowed."))
			return
		}

		body, err := io.ReadAll(req.Body)
		if err != nil {
			log.Println("Could not read body:", err)
			return
		}

		reqBody := createRepoBody{}
		if err := json.Unmarshal(body, &reqBody); err != nil {
			log.Println("Could not parse JSON:", err)
			return
		}

		if reqBody.Id == "" {
			resp.WriteHeader(400)
			resp.Write([]byte("Parameter 'id' is required."))
			return
		}

		// prevent weird repo names and path traversal
		if !ID_REGEX.MatchString(reqBody.Id) {
			resp.WriteHeader(400)
			resp.Write([]byte("Invalid 'id' specified."))
			return
		}

		log.Printf("Initializing repo %s with template %s\n", reqBody.Id, reqBody.Template)

		if reqBody.Template != "" {
			// clone from template
			err = gitkit.CloneRepo(
				reqBody.Id,
				&config,
				fmt.Sprintf("https://github.com/flipdot/waboorrt-template-%s.git", reqBody.Template),
			)
		} else {
			// init without template
			err = gitkit.InitRepo(reqBody.Id, &config)
		}

		if err != nil {
			log.Println("Could not init repo:", err)
			resp.WriteHeader(500)
			resp.Write([]byte(fmt.Sprintf("Failed to create repo: %s", err)))
			return
		}

		resp.Write([]byte(fmt.Sprintf("repo %s created", reqBody.Id)))
	})

	log.Print("HTTP API listening on port 2223")
	err := http.ListenAndServe(":2223", nil)
	if err != nil {
		log.Fatal(err)
	}
}
