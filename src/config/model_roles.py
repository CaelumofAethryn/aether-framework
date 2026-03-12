"""
Model role registry for Aether.

Maps agent roles to preferred models.
These values can be adjusted as your local model library evolves.
"""

MODEL_ROLE_MAP = {
    "reasoning": "mistral-local:latest",
    "analysis": "mistral-local:latest",
    "coding": "mistral-local:latest",
    "utility": "mistral-local:latest",
}


def get_model_for_role(role):
    """
    Return the preferred model for a given agent role.
    """
    return MODEL_ROLE_MAP.get(role, MODEL_ROLE_MAP["utility"])
