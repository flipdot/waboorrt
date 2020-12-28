import random
import copy
import math

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


def dist(a: Tuple[int, int], b: Tuple[int, int]) -> float:
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return math.sqrt(dx * dx + dy * dy)


def compute_damage(dist: float) -> int:
    radius = 3
    return int(max(10 * math.pow(10, -(dist / radius)), 0))


def tick(
    game_state: GameState, actions: Tuple[dict, ...]
) -> (GameState, Tuple[dict, ...]):
    if len(game_state.bots) != len(actions):
        raise ValueError("number of actions does not match number of bots")
    actions = tuple(
        map(lambda a: a if (type(a) == dict) else Action.noaction, actions)
    )  # replace illegal actions by NOOP

    game_state = copy.deepcopy(game_state)
    game_state.tick += 1

    executed_actions = []

    # order: noop, throw, walk, look
    # NOOP
    for bot, action in zip(game_state.bots, actions):
        if action.get("name") == Action.NOOP:
            bot.coins += 1  # get one coin per noop
            executed_actions.append(
                {"bot_name": bot.name, "intended_action": action, "success": True}
            )

    # THROW snowballs
    for bot, action in zip(game_state.bots, actions):
        if action.get("name") == Action.THROW:
            for other in game_state.bots:
                other.health -= compute_damage(
                    dist(
                        (other.x, other.y),
                        (action.get("x", bot.x), action.get("y", bot.y)),
                    )
                )
            executed_actions.append(
                {"bot_name": bot.name, "intended_action": action, "success": True}
            )

    # WALK: Randomly determine which bot goes first. This makes the game more fair.
    for bot, action in random.sample(list(zip(game_state.bots, actions)), len(actions)):
        action_success = False

        if action.get("name") == Action.WALK_NORTH:
            if can_walk_north(game_state, bot):
                bot.y -= 1
                action_success = True

        elif action.get("name") == Action.WALK_EAST:
            if can_walk_east(game_state, bot):
                bot.x += 1
                action_success = True

        elif action.get("name") == Action.WALK_SOUTH:
            if can_walk_south(game_state, bot):
                bot.y += 1
                action_success = True

        elif action.get("name") == Action.WALK_WEST:
            if can_walk_west(game_state, bot):
                bot.x -= 1
                action_success = True

        if action.get("name") in [
            Action.WALK_NORTH,
            Action.WALK_EAST,
            Action.WALK_SOUTH,
            Action.WALK_WEST,
        ]:
            executed_actions.append(
                {
                    "bot_name": bot.name,
                    "intended_action": action,
                    "success": action_success,
                }
            )

    # LOOK
    for bot, action in zip(game_state.bots, actions):
        if action.get("name") == Action.LOOK:
            view_price = 1.0
            bot.view_range = min(
                bot.coins / view_price,  # what the bot can afford
                action.get("range", max(  # what it wants or the max necessary
                    dist((bot.x, bot.y), (0, 0)),
                    dist((bot.x, bot.y), (game_state.map_w, 0)),
                    dist((bot.x, bot.y), (0, game_state.map_h)),
                    dist((bot.x, bot.y), (game_state.map_w, game_state.map_h)),
                ))
            )
            if bot.view_range > 1:  # get up to 1 for free
                bot.coins -= bot.view_range * view_price
            else:  # tried to view in range <=1, makes no sense
                bot.view_range = 1
            executed_actions.append({
                "bot_name": bot.name,
                "intended_action": action,
                "success": bot.view_range > 1,  # if <=1, the bot would waste coins
            })
        else:
            bot.view_range = 1  # get 1 for free

    # list unknown actions
    for bot, action in zip(game_state.bots, actions):
        if action.get("name") not in [
            Action.NOOP,
            Action.THROW,
            Action.LOOK,
            Action.WALK_NORTH,
            Action.WALK_EAST,
            Action.WALK_SOUTH,
            Action.WALK_WEST,
        ]:
            executed_actions.append(
                {
                    "bot_name": bot.name,
                    "intended_action": action,
                    "success": False,
                }
            )

    if game_state.tick >= game_state.max_ticks:
        game_state.running = False

    return game_state, tuple(executed_actions)
