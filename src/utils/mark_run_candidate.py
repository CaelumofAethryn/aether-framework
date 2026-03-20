import json
import sys
from pathlib import Path

from src.config.storage_config import SWARM_RUNS_DIR, ensure_storage_dirs


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, record: dict):
    with path.open("w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
        f.write("\n")


def mark_run_candidate(
    filename: str,
    quality_score=None,
    human_validated=True,
    notes=""
):
    ensure_storage_dirs()

    run_file = SWARM_RUNS_DIR / filename
    if not run_file.exists():
        print(f"error: file not found: {run_file}")
        return 1

    record = load_json(run_file)

    metadata = record.get("metadata")
    if not isinstance(metadata, dict):
        metadata = {}

    metadata["training_candidate"] = True
    metadata["human_validated"] = bool(human_validated)

    if quality_score is not None:
        metadata["quality_score"] = quality_score

    if notes:
        metadata["notes"] = notes

    record["metadata"] = metadata
    save_json(run_file, record)

    print(f"marked: {run_file.name}")
    return 0


def parse_args(argv):
    if len(argv) < 2:
        print("usage: python -m src.utils.mark_run_candidate <filename> [quality_score] [notes]")
        return None

    filename = argv[1]

    quality_score = None
    if len(argv) >= 3 and argv[2].strip():
        try:
            quality_score = float(argv[2])
        except ValueError:
            print("error: quality_score must be a number")
            return None

    notes = ""
    if len(argv) >= 4:
        notes = argv[3]

    return filename, quality_score, notes


if __name__ == "__main__":
    parsed = parse_args(sys.argv)
    if parsed is None:
        raise SystemExit(1)

    filename, quality_score, notes = parsed
    raise SystemExit(
        mark_run_candidate(
            filename=filename,
            quality_score=quality_score,
            human_validated=True,
            notes=notes,
        )
    )
