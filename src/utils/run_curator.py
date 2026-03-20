import json
import shutil
from pathlib import Path

from src.config.storage_config import (
    SWARM_RUNS_DIR,
    TRAINING_CANDIDATES_DIR,
    ensure_storage_dirs,
)


def is_training_candidate(record: dict) -> bool:
    metadata = record.get("metadata", {})
    return metadata.get("training_candidate") is True


def iter_run_files(run_dir: Path):
    if not run_dir.exists():
        return
    for path in sorted(run_dir.glob("*.json")):
        if path.is_file():
            yield path


def load_json(path: Path):
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def promote_training_candidates():
    ensure_storage_dirs()

    scanned = 0
    promoted = 0
    skipped = 0
    already_present = 0

    for run_file in iter_run_files(SWARM_RUNS_DIR):
        scanned += 1
        record = load_json(run_file)

        if record is None:
            skipped += 1
            continue

        if not is_training_candidate(record):
            continue

        destination = TRAINING_CANDIDATES_DIR / run_file.name

        if destination.exists():
            already_present += 1
            continue

        shutil.copy2(run_file, destination)
        promoted += 1

    print(
        f"scanned={scanned} promoted={promoted} "
        f"already_present={already_present} skipped={skipped}"
    )


if __name__ == "__main__":
    promote_training_candidates()
