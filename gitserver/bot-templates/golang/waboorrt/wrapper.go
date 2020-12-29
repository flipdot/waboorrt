package waboorrt

import (
	"net/http"

	"waboorrt/waboorrt/actions"
)

type wrapper struct {
	bot Bot
}

func newWrapper(bot Bot) *wrapper {
	return &wrapper{
		bot: bot,
	}
}

func (w *wrapper) NextAction(r *http.Request, args *GameState, result *actions.Action) error {
	*result = w.bot.NextAction(args)
	return nil
}

func (w *wrapper) Health(r *http.Request, args *interface{}, result *bool) error {
	*result = true
	return nil
}
