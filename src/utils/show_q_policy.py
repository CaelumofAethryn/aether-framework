import sys

from src.config.workflow_registry import list_workflow_names
from src.utils.q_table import load_q_table, get_q_value


DEFAULT_STATE = "general"


def show_q_policy(state: str = DEFAULT_STATE):
    q_table = load_q_table()
    workflow_names = list_workflow_names()

    best_name = None
    best_value = None

    print(f"state={state}")

    for name in workflow_names:
        value = get_q_value(q_table, state, name)
        print(f"{name}={value}")

        if best_value is None or value > best_value:
            best_name = name
            best_value = value

    print(f"best_workflow={best_name}")
    print(f"best_q={best_value}")


def main(argv):
    state = argv[1] if len(argv) > 1 else DEFAULT_STATE
    show_q_policy(state)


if __name__ == "__main__":
    main(sys.argv)

