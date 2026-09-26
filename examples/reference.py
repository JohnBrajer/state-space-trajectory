"""Reference implementation for John Brajer's State-Space Trajectory architecture."""
from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class State:
    values: Mapping[str, float]


@dataclass(frozen=True)
class Action:
    name: str
    delta: Mapping[str, float]
    path_expansion: float = 0.0


def apply_action(state: State, action: Action) -> State:
    keys = set(state.values) | set(action.delta)
    return State({
        key: state.values.get(key, 0.0) + action.delta.get(key, 0.0)
        for key in keys
    })


def trajectory_score(action: Action, weights: Mapping[str, float]) -> float:
    weighted_shift = sum(weights.get(k, 0.0) * v for k, v in action.delta.items())
    return weighted_shift + weights.get("path_expansion", 0.0) * action.path_expansion


if __name__ == "__main__":
    current = State({"money": 0.2, "network": 0.1})
    action = Action("attend meetup", {"network": 0.3, "money": -0.05}, path_expansion=0.4)
    print(apply_action(current, action))
    print(trajectory_score(action, {"network": 2.0, "money": 1.0, "path_expansion": 1.5}))
