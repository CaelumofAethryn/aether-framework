from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = PROJECT_ROOT / "data"

SWARM_RUNS_DIR = DATA_ROOT / "swarm_runs"
CORPUS_RAW_DIR = DATA_ROOT / "corpus" / "raw"
CORPUS_PROCESSED_DIR = DATA_ROOT / "corpus" / "processed"
INDEXES_DIR = DATA_ROOT / "indexes"
CACHE_DIR = DATA_ROOT / "cache"
EXPORTS_DIR = DATA_ROOT / "exports"

LEARNING_DIR = DATA_ROOT / "learning"
TRAINING_CANDIDATES_DIR = LEARNING_DIR / "training_candidates"
CURATED_DATASETS_DIR = LEARNING_DIR / "curated_datasets"
ADAPTERS_DIR = LEARNING_DIR / "adapters"
EVALS_DIR = LEARNING_DIR / "evals"

IPFS_DIR = DATA_ROOT / "ipfs"
IPFS_QUEUE_DIR = IPFS_DIR / "queue"
IPFS_MANIFESTS_DIR = IPFS_DIR / "manifests"


def ensure_storage_dirs():
    paths = [
        DATA_ROOT,
        SWARM_RUNS_DIR,
        CORPUS_RAW_DIR,
        CORPUS_PROCESSED_DIR,
        INDEXES_DIR,
        CACHE_DIR,
        EXPORTS_DIR,
        LEARNING_DIR,
        TRAINING_CANDIDATES_DIR,
        CURATED_DATASETS_DIR,
        ADAPTERS_DIR,
        EVALS_DIR,
        IPFS_DIR,
        IPFS_QUEUE_DIR,
        IPFS_MANIFESTS_DIR,
    ]

    for path in paths:
        path.mkdir(parents=True, exist_ok=True)

    return paths
