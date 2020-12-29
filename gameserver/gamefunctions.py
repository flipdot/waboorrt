import logging
import random
import copy
import math

from gameobjects import GameState, Bot, Action
from typing import Tuple, Optional

logger = logging.getLogger(__name__)


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


def action_noop(game_state, bot, action) -> Tuple[bool, Optional[str]]:
    bot.coins += 1
    return True, None


def action_walk(game_state, bot, action) -> Tuple[bool, Optional[str]]:
    if action.get("direction") == "north":
        if can_walk_north(game_state, bot):
            bot.y -= 1
            return True, None

    elif action.get("direction") == "east":
        if can_walk_east(game_state, bot):
            bot.x += 1
            return True, None

    elif action.get("direction") == "south":
        if can_walk_south(game_state, bot):
            bot.y += 1
            return True, None

    elif action.get("direction") == "west":
        if can_walk_west(game_state, bot):
            bot.x -= 1
            return True, None

    return False, "position was occupied or you walked out of the map"


def action_throw(game_state, bot, action) -> Tuple[bool, Optional[str]]:

    if dist((bot.x, bot.y), (action.get("x", 0), action.get("y", 0))) > bot.coins:
        return False, "not enough coins to throw this far"
    for other in game_state.bots:
        other.health -= compute_damage(
            dist(
                (other.x, other.y),
                (action.get("x", bot.x), action.get("y", bot.y)),
            )
        )
    return True, None


def action_look(game_state, bot, action) -> Tuple[bool, Optional[str]]:
    view_price = 1.0
    desired_range = int(action.get(
        "range",
        max(  # what it wants or the max necessary
            dist((bot.x, bot.y), (0, 0)),
            dist((bot.x, bot.y), (game_state.map_w, 0)),
            dist((bot.x, bot.y), (0, game_state.map_h)),
            dist((bot.x, bot.y), (game_state.map_w, game_state.map_h)),
        ),
    ))
    if desired_range > (bot.coins / view_price):
        return False, "not enough coins to look this far"
    bot.view_range = desired_range
    bot.coins -= int(bot.view_range * view_price)
    return True, None


def tick(
    game_state: GameState, actions: Tuple[dict, ...]
) -> (GameState, Tuple[dict, ...]):
    if len(game_state.bots) != len(actions):
        raise ValueError("number of actions does not match number of bots")

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
            # for convenience for the bot authors: convert every action to lowercase
            action = {k.lower(): (v.lower() if isinstance(v, str) else v) for k, v in action.items()}
            if action.get("name") == current_action_type:
                success, failure_reason = action_function(game_state, bot, action)
                executed = {
                    "bot_name": bot.name,
                    "intended_action": action,
                    "success": success,
                }
                if not success:
                    executed["reason"] = failure_reason
                executed_actions.append(executed)
                action["_was_handled"] = True

    # list unknown actions
    # for bot, action in action_list:
    #     if not action.get("_was_handled"):
    #         executed_actions.append(
    #             {
    #                 "bot_name": bot.name,
    #                 "intended_action": action,
    #                 "success": False,
    #                 "message": "Unknown action",
    #             }
    #         )

    # for action in executed_actions:
    #     if "_was_handled" in action:
    #         del action["_was_handled"]
    #     if "_was_handled" in action["intended_action"]:
    #         del action["intended_action"]["_was_handled"]

    if game_state.tick >= game_state.max_ticks:
        game_state.running = False

    return game_state, tuple(executed_actions)
