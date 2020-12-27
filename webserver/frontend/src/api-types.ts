export type ThrowAction = {
  name: 'THROW';
  x: number;
  y: number;
};

export type WalkAction = {
  name: 'WALK_WEST' | 'WALK_SOUTH' | 'WALK_NORTH' | 'WALK_EAST';
};

export type NoOpAction = {
  name: 'NOOP';
};

export type Action = ThrowAction | WalkAction | NoOpAction;

export type ActionResult = {
  bot_name: string;
  intended_action: Action;
  success: boolean;
};

export type EntityType = 'BOT';

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
