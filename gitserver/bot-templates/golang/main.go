package main

import (
	"log"

	"waboorrt/waboorrt"
)

type Bot struct {
}

func (b *Bot) NextAction(state waboorrt.GameState, yourName string) (waboorrt.Action, error) {
	return nil, nil
}

func main() {
	bot := new(Bot)

	if err := waboorrt.Run(bot); err != nil {
		log.Fatal(err)
	}
}
