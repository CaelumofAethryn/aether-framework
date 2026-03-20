import json
import sys
from pathlib import Path

from src.config.storage_config import TRAINING_CANDIDATES_DIR, ensure_storage_dirs


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, record: dict):
    with path.open("w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
        f.write("\n")


def set_candidate_reward(filename: str, reward: float, reward_notes: str = ""):
    ensure_storage_dirs()

    candidate_file = TRAINING_CANDIDATES_DIR / filename
    if not candidate_file.exists():
        print(f"error: file not found: {candidate_file}")
        return 1

    record = load_json(candidate_file)

    metadata = record.get("metadata")
    if not isinstance(metadata, dict):
        metadata = {}

    metadata["reward"] = float(reward)

    if reward_notes:
        metadata["reward_notes"] = reward_notes

    record["metadata"] = metadata
    save_json(candidate_file, record)

    print(f"updated_reward: {candidate_file.name} reward={float(reward)}")
    return 0


def parse_args(argv):
    if len(argv) < 3:
        print("usage: python -m src.utils.set_candidate_reward <filename> <reward> [reward_notes]")
        return None

    filename = argv[1]

    try:
        reward = float(argv[2])
    except ValueError:
        print("error: reward must be a number")
        return None

    reward_notes = ""
    if len(argv) >= 4:
        reward_notes = argv[3]

    return filename, reward, reward_notes


if __name__ == "__main__":
    parsed = parse_args(sys.argv)
    if parsed is None:
        raise SystemExit(1)

    filename, reward, reward_notes = parsed
    raise SystemExit(set_candidate_reward(filename, reward, reward_notes))
