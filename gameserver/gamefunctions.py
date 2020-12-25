import random
import copy

from gameobjects import GameState, Bot, Action
from typing import Tuple


def can_walk_north(state: GameState, bot: Bot) -> bool:
    new_pos = bot.y - 1
    if new_pos < 0:
        return False
    return not is_position_occupied(state, bot.x, new_pos)


def can_walk_south(state: GameState, bot: Bot) -> bool:
    new_pos = bot.y + 1
    if new_pos >= state.map_h:
        return False
    return not is_position_occupied(state, bot.x, new_pos)


def can_walk_west(state: GameState, bot: Bot) -> bool:
    new_pos = bot.x - 1
    if new_pos < 0:
        return False
    return not is_position_occupied(state, new_pos, bot.y)


def can_walk_east(state: GameState, bot: Bot) -> bool:
    new_pos = bot.x + 1
    if new_pos >= state.map_w:
        return False
    return not is_position_occupied(state, new_pos, bot.y)


def is_position_occupied(state: GameState, x: int, y: int) -> bool:
    for entity in state.bots:
        if x == entity.x and y == entity.y:
            return True
    return False


def tick(game_state: GameState, actions: Tuple[Action, ...]) -> (GameState, Tuple[dict, ...]):
    if len(game_state.bots) != len(actions):
        raise ValueError("number of actions does not match number of bots")

    game_state = copy.deepcopy(game_state)
    game_state.tick += 1

    executed_actions = []

    # Randomly determine which bot goes first. This makes the game more fair.
    for bot, action in random.sample(list(zip(game_state.bots, actions)), len(actions)):
        action_success = False

        if action == Action.NOOP:
            action_success = True

        elif action == Action.WALK_NORTH:
            if can_walk_north(game_state, bot):
                bot.y -= 1
                action_success = True

        elif action == Action.WALK_EAST:
            if can_walk_east(game_state, bot):
                bot.x += 1
                action_success = True

        elif action == Action.WALK_SOUTH:
            if can_walk_south(game_state, bot):
                bot.y += 1
                action_success = True

        elif action == Action.WALK_WEST:
            if can_walk_west(game_state, bot):
                bot.x -= 1
                action_success = True

        executed_actions.append({"bot_name": bot.name, "intended_action": action, "success": action_success})

    if game_state.tick >= game_state.max_ticks:
        game_state.running = False

    return game_state, tuple(executed_actions)
