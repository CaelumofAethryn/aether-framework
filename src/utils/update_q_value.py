import sys

from src.config.workflow_registry import list_workflow_names
from src.utils.q_table import load_q_table, save_q_table, get_q_value, set_q_value


DEFAULT_ALPHA = 0.5
DEFAULT_GAMMA = 0.9


def max_next_q(q_table: dict, next_state: str) -> float:
    actions = list_workflow_names()
    if not actions:
        return 0.0
    return max(get_q_value(q_table, next_state, action) for action in actions)


def update_q_value(
    state: str,
    action: str,
    reward: float,
    next_state: str,
    alpha: float = DEFAULT_ALPHA,
    gamma: float = DEFAULT_GAMMA,
):
    q_table = load_q_table()

    old_value = get_q_value(q_table, state, action)
    next_max = max_next_q(q_table, next_state)

    new_value = old_value + alpha * (reward + gamma * next_max - old_value)

    set_q_value(q_table, state, action, new_value)
    save_q_table(q_table)

    print(f"state={state}")
    print(f"action={action}")
    print(f"reward={float(reward)}")
    print(f"next_state={next_state}")
    print(f"old_q={old_value}")
    print(f"next_max_q={next_max}")
    print(f"new_q={new_value}")


def parse_args(argv):
    if len(argv) < 5:
        print(
            "usage: python -m src.utils.update_q_value "
            "<state> <action> <reward> <next_state> [alpha] [gamma]"
        )
        return None

    state = argv[1]
    action = argv[2]

    try:
        reward = float(argv[3])
    except ValueError:
        print("error: reward must be a number")
        return None

    next_state = argv[4]

    alpha = DEFAULT_ALPHA
    if len(argv) >= 6:
        try:
            alpha = float(argv[5])
        except ValueError:
            print("error: alpha must be a number")
            return None

    gamma = DEFAULT_GAMMA
    if len(argv) >= 7:
        try:
            gamma = float(argv[6])
        except ValueError:
            print("error: gamma must be a number")
            return None

    return state, action, reward, next_state, alpha, gamma


if __name__ == "__main__":
    parsed = parse_args(sys.argv)
    if parsed is None:
        raise SystemExit(1)

    update_q_value(*parsed)

