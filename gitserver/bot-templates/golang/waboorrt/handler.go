package waboorrt

import (
	"log"
	"net/http"

	"github.com/gorilla/mux"
	"github.com/gorilla/rpc/v2"
)

type GameState interface{}

type Action interface {}

type NextActionArgs struct {
	GameState string `json:"game_state"`
	YourName  string `json:"your_name"`
}

type Bot interface {
	NextAction(state GameState, yourName string) (Action, error)
}

func Run(bot Bot) error {
	s := rpc.NewServer()
	c := newCustomCodec()
	s.RegisterCodec(c, "application/json")
	s.RegisterCodec(c, "application/json;charset=UTF-8")

	if err := s.RegisterService(newWrapper(bot), "Bot"); err != nil {
		log.Fatal(err)
	}

	r := mux.NewRouter()
	r.Handle("/jsonrpc", s)

	return http.ListenAndServe(":4000", r)
}
