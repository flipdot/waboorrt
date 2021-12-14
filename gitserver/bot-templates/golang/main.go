package main

import (
	"fmt"
	"log"
	"math"
	"math/rand"

	"github.com/flipdot/waboorrt-go"
	"github.com/flipdot/waboorrt-go/actions"
	"github.com/flipdot/waboorrt-go/actions/constants"
	"github.com/flipdot/waboorrt-go/types"
)

type Bot struct {
	waboorrt.BotDebugger
}

func (b *Bot) NextAction(state *waboorrt.GameState) actions.Action {
	dirs := []constants.WalkDirection{
		constants.WalkNorth,
		constants.WalkWest,
		constants.WalkSouth,
		constants.WalkEast,
	}

	switch rand.Intn(4) {
	case 0:
		dir := dirs[rand.Intn(len(dirs))]
		b.Debug(fmt.Sprintf("going %s", dir))
		return actions.NewWalkOp(dir)

	case 1:
		lookRange := rand.Float64() * math.Max(state.Meta.Width, state.Meta.Height)
		b.Debug(fmt.Sprintf("looing for enemies n range %.0f", lookRange))
		return actions.NewLookOp(lookRange)

	case 2:
		p := types.Pos{
			X: float64(rand.Intn(int(state.Meta.Width))),
			Y: float64(rand.Intn(int(state.Meta.Height))),
		}

		b.Debug(fmt.Sprintf("throwing at (%.0f %.0f)", p.X, p.Y))
		return actions.NewThrowOp(p)

	default:
		b.Debug("idling")
		return actions.NewNoOp()
	}
}

func main() {
	bot := &Bot{}

	bot.EnableDebug()

	if err := waboorrt.Run(bot); err != nil {
		log.Fatal(err)
	}
}
