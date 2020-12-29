package waboorrt

type EntityType string

const (
	ENTITY_TYPE_BOT = "BOT"
)

type Entity struct {
	X    float64        `json:"x"`
	Y    float64        `json:"y"`
	Type EntityType `json:"type"`
}
