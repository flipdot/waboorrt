package waboorrt

import (
	"net/http"
)

type wrapper struct {
	bot Bot
}

func newWrapper(bot Bot) *wrapper {
	return &wrapper{
		bot: bot,
	}
}

func (w *wrapper) NextAction(r *http.Request, args *NextActionArgs, result *Action) error {
	ret, err := w.bot.NextAction(args.GameState, args.YourName)
	if err != nil {
		return err
	}
	
	*result = ret
	return nil
}

func (w *wrapper) Health(r *http.Request, args *interface{}, result *bool) error {
	*result = true
	return nil
}
