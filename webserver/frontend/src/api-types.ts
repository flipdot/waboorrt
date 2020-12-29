export type ThrowAction = {
  name: 'throw';
  x: number;
  y: number;
};

export type WalkAction = {
  name: 'walk';
  direction: 'west' | 'south' | 'north' | 'east';
};

export type NoOpAction = {
  name: 'noop';
};

export type Action = ThrowAction | WalkAction | NoOpAction;

export type ActionResult = {
  bot_name: string;
  intended_action: Action;
  success: boolean;
};

export type EntityType = 'bot';

export type Entity = {
  x: number;
  y: number;
  type: EntityType;
  health: number;
  name: string;
};

export type GameState = {
  tick: number;
  max_ticks: number;
  map_w: number;
  map_h: number;
  entities: Entity[];
};

export type ReplayEntry = {
  game_state: GameState;
  actions: ActionResult[];
};

export type GameReplay = ReplayEntry[];
