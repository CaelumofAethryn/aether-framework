"""
Model role registry for Aether.
Maps agent roles to preferred models.
These values can be adjusted as your local model library evolves.
"""
MODEL_ROLE_MAP = {
    "reasoning": "deepseek-r1-14b-q4-local",
    "analysis": "qwen2.5-coder-14b-local",
    "coding": "qwen2.5-coder-14b-local",
    "utility": "qwen2.5-coder-14b-local",
    "synthesis": "deepseek-r1-14b-q4-local",
}

def get_model_for_role(role):
    """
    Return the preferred model for a given agent role.
    """
    return MODEL_ROLE_MAP.get(role, MODEL_ROLE_MAP["utility"])
