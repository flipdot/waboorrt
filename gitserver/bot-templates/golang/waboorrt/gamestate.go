package waboorrt

type GameState struct {
	Me       MeInfo   `json:"me"`
	Meta     MetaInfo `json:"meta"`
	Entities []Entity `json:"entities"`
}
