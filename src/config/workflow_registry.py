WORKFLOW_REGISTRY = {
    "reasoning_only": {
        "steps": ["reasoning"],
        "description": "Single-pass reasoning response.",
    },
    "reasoning_analysis": {
        "steps": ["reasoning", "analysis"],
        "description": "Draft followed by critique.",
    },
    "reasoning_analysis_revision": {
        "steps": ["reasoning", "analysis", "reasoning"],
        "description": "Draft, critique, then revision.",
    },
    "reasoning_analysis_revision_summary": {
        "steps": ["reasoning", "analysis", "reasoning", "utility"],
        "description": "Draft, critique, revision, then utility summary.",
    },
}


def get_workflow(name: str):
    return WORKFLOW_REGISTRY.get(name)


def list_workflow_names():
    return list(WORKFLOW_REGISTRY.keys())

