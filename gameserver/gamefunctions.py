import logging
import random
import copy
import math
from typing import Tuple, Optional

from gameobjects import GameState, Bot, RpcAction, LookAction, NoopAction, ThrowAction, WalkAction, ChargeAction

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


def action_charge(game_state, bot, action: NoopAction) -> Tuple[bool, Optional[str]]:
    bot.energy += 1
    return True, None


def action_walk(game_state, bot, action: WalkAction) -> Tuple[bool, Optional[str]]:
    if action.direction == "north":
        if can_walk_north(game_state, bot):
            bot.y -= 1
            return True, None

    elif action.direction == "east":
        if can_walk_east(game_state, bot):
            bot.x += 1
            return True, None

    elif action.direction == "south":
        if can_walk_south(game_state, bot):
            bot.y += 1
            return True, None

    elif action.direction == "west":
        if can_walk_west(game_state, bot):
            bot.x -= 1
            return True, None

    return False, "position was occupied or you walked out of the map"


def default(nonable, default_value):
    return default_value if nonable is None else nonable


def action_throw(game_state, bot, action: ThrowAction) -> Tuple[bool, Optional[str]]:
    costs = round(dist((bot.x, bot.y), (default(action.x, 0), default(action.y, 0))))
    if costs > bot.energy:
        return False, "not enough energy to throw this far"
    for other in game_state.bots:
        other.health -= compute_damage(
            dist(
                (other.x, other.y),
                (default(action.x, bot.x), default(action.y, bot.y)),
            )
        )
        # don't allow negative health
        other.health = max(other.health, 0)
    bot.energy -= costs
    return True, None


def action_look(game_state, bot, action: LookAction) -> Tuple[bool, Optional[str]]:
    view_price = 1.0
    desired_range = int(default(
        action.range,
        max(  # what it wants or the max necessary
            dist((bot.x, bot.y), (0, 0)),
            dist((bot.x, bot.y), (game_state.map_w, 0)),
            dist((bot.x, bot.y), (0, game_state.map_h)),
            dist((bot.x, bot.y), (game_state.map_w, game_state.map_h)),
        ),
    ))
    if desired_range > (bot.energy / view_price):
        return False, "not enough energy to look this far"
    bot.view_range = desired_range
    bot.energy -= int(bot.view_range * view_price)
    return True, None


def tick(
    game_state: GameState, actions: Tuple[RpcAction, ...]
) -> Tuple[GameState, Tuple[dict, ...]]:
    if len(game_state.bots) != len(actions):
        raise ValueError("number of actions does not match number of bots")

    game_state = copy.deepcopy(game_state)
    game_state.tick += 1

    executed_actions = []

    action_list = random.sample(list(zip(game_state.bots, actions)), len(actions))

    action_execution_order = [
        (NoopAction, action_charge),  # For compatibility, still call charge when noop is issued
        (ChargeAction, action_charge),
        (ThrowAction, action_throw),
        (WalkAction, action_walk),
        (LookAction, action_look),
    ]

    for current_action_type, action_function in action_execution_order:
        for bot, action in action_list:
            if isinstance(action, current_action_type):
                success, failure_reason = action_function(game_state, bot, action)
                action_result = action.dict()
                executed = {
                    "bot_name": bot.name,
                    "intended_action": action_result,
                    "success": success,
                }
                if not success:
                    executed["reason"] = failure_reason
                executed_actions.append(executed)
                action_result["_was_handled"] = True

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

    alive_bots = [x for x in game_state.bots if x.health > 0]
    if len(alive_bots) <= 1:
        game_state.running = False
    if game_state.tick >= game_state.max_ticks:
        game_state.running = False

    return game_state, tuple(executed_actions)
