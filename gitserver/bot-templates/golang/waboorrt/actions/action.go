package actions

type ActionType string

const (
	ActionNoop  ActionType = "NOOP"
	ActionWalk  ActionType = "WALK"
	ActionThrow ActionType = "THROW"
	ActionLook  ActionType = "LOOK"
)

type Action interface {
	Action()
}

type ActionImpl struct {
	Name ActionType `json:"name"`
}

func (ActionImpl) Action() {}

type NoOp struct {
	ActionImpl
}

func NewNoOp() Action {
	return &NoOp{
		ActionImpl{
			Name: ActionNoop,
		},
	}
}

type WalkDirection string

const (
	WalkNorth WalkDirection = "NORTH"
	WalkWest  WalkDirection = "WEST"
	WalkSouth WalkDirection = "SOUTH"
	WalkEast  WalkDirection = "EAST"
)

type WalkOp struct {
	ActionImpl

	Direction WalkDirection `json:"direction"`
}

func NewWalkOp(dir WalkDirection) Action {
	return &WalkOp{
		ActionImpl: ActionImpl{
			Name: ActionWalk,
		},
		Direction: dir,
	}
}

type ThrowOp struct {
	ActionImpl

	X float64 `json:"x"`
	Y float64 `json:"y"`
}

func NewThrowOp(x, y float64) Action {
	return &ThrowOp{
		ActionImpl: ActionImpl{
			Name: ActionThrow,
		},
		X: x,
		Y: y,
	}
}

type LookOp struct {
	ActionImpl

	Range float64 `json:"range"`
}

func NewLookOp(lookRange float64) Action {
	return &LookOp{
		ActionImpl: ActionImpl{
			Name: ActionLook,
		},
		Range: lookRange,
	}
}
