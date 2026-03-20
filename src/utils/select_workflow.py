import sys

from src.config.workflow_registry import get_workflow, list_workflow_names
from src.utils.q_table import load_q_table, get_q_value


DEFAULT_WORKFLOW = "reasoning_analysis_revision_summary"
DEFAULT_STATE = "general"


def best_workflow_for_state(state: str):
    workflow_names = list_workflow_names()
    if not workflow_names:
        return DEFAULT_WORKFLOW

    best_name = DEFAULT_WORKFLOW
    best_value = get_q_value(load_q_table(), state, best_name)

    q_table = load_q_table()

    for name in workflow_names:
        value = get_q_value(q_table, state, name)
        if value > best_value:
            best_name = name
            best_value = value

    return best_name


def select_workflow(requested_name: str = None, state: str = DEFAULT_STATE):
    if requested_name:
        workflow = get_workflow(requested_name)
        if workflow is not None:
            return requested_name, workflow

    selected_name = best_workflow_for_state(state)
    workflow = get_workflow(selected_name)

    if workflow is None:
        selected_name = DEFAULT_WORKFLOW
        workflow = get_workflow(DEFAULT_WORKFLOW)

    return selected_name, workflow


def main(argv):
    requested_name = argv[1] if len(argv) > 1 else None
    state = argv[2] if len(argv) > 2 else DEFAULT_STATE

    selected_name, workflow = select_workflow(requested_name, state)

    print(f"state={state}")
    print(f"selected_workflow={selected_name}")
    print(f"steps={','.join(workflow['steps'])}")
    print(f"available={','.join(list_workflow_names())}")


if __name__ == "__main__":
    main(sys.argv)
