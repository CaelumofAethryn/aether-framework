import json
from pathlib import Path

from src.config.storage_config import ensure_storage_dirs


Q_TABLE_PATH = Path("data/learning/q_table.json")


def load_q_table() -> dict:
    ensure_storage_dirs()

    if not Q_TABLE_PATH.exists():
        return {}

    try:
        with Q_TABLE_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return data
    except Exception:
        pass

    return {}


def save_q_table(q_table: dict):
    ensure_storage_dirs()
    Q_TABLE_PATH.parent.mkdir(parents=True, exist_ok=True)

    with Q_TABLE_PATH.open("w", encoding="utf-8") as f:
        json.dump(q_table, f, indent=2, ensure_ascii=False)
        f.write("\n")


def get_q_value(q_table: dict, state: str, action: str) -> float:
    state_row = q_table.get(state, {})
    value = state_row.get(action, 0.0)
    return float(value)


def set_q_value(q_table: dict, state: str, action: str, value: float):
    if state not in q_table or not isinstance(q_table[state], dict):
        q_table[state] = {}

    q_table[state][action] = float(value)


if __name__ == "__main__":
    q_table = load_q_table()
    print(f"states={len(q_table)}")
    print(f"path={Q_TABLE_PATH}")
