import json
from pathlib import Path

from src.config.storage_config import TRAINING_CANDIDATES_DIR, ensure_storage_dirs


INDEX_FILE = TRAINING_CANDIDATES_DIR / "index.json"


def iter_candidate_files(candidate_dir: Path):
    if not candidate_dir.exists():
        return
    for path in sorted(candidate_dir.glob("*.json")):
        if path.is_file() and path.name != "index.json":
            yield path


def load_json(path: Path):
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def build_entry(path: Path, record: dict) -> dict:
    metadata = record.get("metadata", {})
    return {
        "filename": path.name,
        "run_type": metadata.get("run_type"),
        "quality_score": metadata.get("quality_score"),
        "human_validated": metadata.get("human_validated"),
        "training_candidate": metadata.get("training_candidate"),
        "notes": metadata.get("notes", ""),
        "reward": metadata.get("reward"),
        "reward_notes": metadata.get("reward_notes", ""),
    }


def build_candidate_index():
    ensure_storage_dirs()

    entries = []
    scanned = 0
    skipped = 0

    for candidate_file in iter_candidate_files(TRAINING_CANDIDATES_DIR):
        scanned += 1
        record = load_json(candidate_file)

        if record is None:
            skipped += 1
            continue

        entries.append(build_entry(candidate_file, record))

    index = {
        "candidate_count": len(entries),
        "entries": entries,
    }

    with INDEX_FILE.open("w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"scanned={scanned} indexed={len(entries)} skipped={skipped}")


if __name__ == "__main__":
    build_candidate_index()


