package waboorrt

type EntityType string

const (
	ENTITY_TYPE_BOT = "BOT"
)

type Entity struct {
	X    int        `json:"x"`
	Y    int        `json:"y"`
	Type EntityType `json:"type"`
}
