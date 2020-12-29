package waboorrt

type MeInfo struct {
	X         float64 `json:"x"`
	Y         float64 `json:"y"`
	Coins     float64 `json:"coins"`
	ViewRange float64 `json:"view_range"`
	Name      string  `json:"name"`
	Health    float64 `json:"health"`
}
