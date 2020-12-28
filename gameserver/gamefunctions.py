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


def action_noop(game_state, bot, action):
    bot.coins += 1
    return True


def action_walk(game_state, bot, action):
    if action.get("direction") == "north":
        if can_walk_north(game_state, bot):
            bot.y -= 1
            return True

    elif action.get("direction") == "east":
        if can_walk_east(game_state, bot):
            bot.x += 1
            return True

    elif action.get("direction") == "south":
        if can_walk_south(game_state, bot):
            bot.y += 1
            return True

    elif action.get("direction") == "west":
        if can_walk_west(game_state, bot):
            bot.x -= 1
            return True

    return False


def action_throw(game_state, bot, action):
    for other in game_state.bots:
        other.health -= compute_damage(
            dist(
                (other.x, other.y),
                (action.get("x", bot.x), action.get("y", bot.y)),
            )
        )
    return True


def action_look(game_state, bot, action):
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
    return bot.view_range > 1  # if <=1, the bot would waste coins


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

    action_list = random.sample(list(zip(game_state.bots, actions)), len(actions))

    action_execution_order = [
        (Action.NOOP, action_noop),
        (Action.THROW, action_throw),
        (Action.WALK, action_walk),
        (Action.LOOK, action_look),
    ]

    for current_action_type, action_function in action_execution_order:
        for bot, action in action_list:
            if action.get("name") == current_action_type:
                executed_actions.append({
                    "bot_name": bot.name,
                    "intended_action": action,
                    "success": action_function(game_state, bot, action)
                })
                action["_was_handled"] = True

    # list unknown actions
    for bot, action in action_list:
        if not action.get("_was_handled"):
            executed_actions.append(
                {
                    "bot_name": bot.name,
                    "intended_action": action,
                    "success": False,
                    "message": "Unknown action"
                }
            )

    if game_state.tick >= game_state.max_ticks:
        game_state.running = False

    return game_state, tuple(executed_actions)
