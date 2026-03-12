import json
from datetime import datetime

from src.config.storage_config import SWARM_RUNS_DIR, ensure_storage_dirs


def _timestamp():
    return datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")


def save_swarm_run(record, prefix="swarm_run"):
    """
    Save a structured swarm run record to disk as JSON.
    Returns the full path to the saved file.
    """
    ensure_storage_dirs()

    filename = f"{prefix}_{_timestamp()}.json"
    output_path = SWARM_RUNS_DIR / filename

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)

    return output_path
