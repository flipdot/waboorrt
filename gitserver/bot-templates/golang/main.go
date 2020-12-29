package main

import (
	"log"
	"math/rand"

	"waboorrt/waboorrt"
	"waboorrt/waboorrt/actions"
)

type Bot struct {
}

func (b *Bot) NextAction(state *waboorrt.GameState) actions.Action {
	dirs := []actions.WalkDirection{
		actions.WalkNorth,
		actions.WalkWest,
		actions.WalkSouth,
		actions.WalkEast,
	}

	switch rand.Intn(4) {
	case 0:
		return actions.NewWalkOp(dirs[rand.Intn(len(dirs))])

	case 1:
		return actions.NewLookOp(16)

	case 2:
		return actions.NewThrowOp(float64(rand.Intn(int(state.Meta.Width))), float64(rand.Intn(int(state.Meta.Height))))

	default:
		return actions.NewNoOp()
	}
}

func main() {
	bot := &Bot{}

	if err := waboorrt.Run(bot); err != nil {
		log.Fatal(err)
	}
}
