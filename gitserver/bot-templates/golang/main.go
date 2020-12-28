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
	switch rand.Intn(4) {
	case 0:
		return actions.NewNoOp()

	case 1:
		dirs := []actions.WalkDirection{
			actions.WalkNorth,
			actions.WalkWest,
			actions.WalkSouth,
			actions.WalkEast,
		}

		return actions.NewWalkOp(dirs[rand.Intn(len(dirs))])

	case 2:
		return actions.NewThrowOp(rand.Intn(state.Meta.Width), rand.Intn(state.Meta.Height))

	case 3:
		d := state.Meta.Width
		if state.Meta.Height > d {
			d = state.Meta.Height
		}

		return actions.NewLookOp(rand.Intn(d))
	}

	return nil
}

func main() {
	bot := new(Bot)

	if err := waboorrt.Run(bot); err != nil {
		log.Fatal(err)
	}
}
