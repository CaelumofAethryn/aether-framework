#!/usr/bin/env python3
"""
Convert Obsidian markdown dialogues to training candidate format.
Reads from safe copy (including subdirectories), never touches originals.
"""

import json
from pathlib import Path
from datetime import datetime

# Paths
DIALOGUES_SAFE_DIR = Path("/home/caef/aether-framework/data/dialogues_safe")
TRAINING_CANDIDATES_DIR = Path("/home/caef/aether-framework/data/learning/training_candidates")

def ensure_dirs():
    """Make sure directories exist."""
    TRAINING_CANDIDATES_DIR.mkdir(parents=True, exist_ok=True)

def find_all_markdown_files(base_dir):
    """Recursively find all .md files in directory and subdirectories."""
    return list(base_dir.rglob("*.md"))

def extract_conversation_from_md(file_path):
    """Extract the conversation content from a markdown file."""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Simple extraction: the whole file is the conversation
    return content

def create_safe_filename(original_path, base_dir):
    """Create a safe filename that preserves context but avoids path issues."""
    # Get relative path from the base directory
    rel_path = original_path.relative_to(base_dir)
    # Replace directory separators with underscores
    safe_name = str(rel_path).replace('/', '_').replace('\\', '_')
    # Remove .md extension for the base name
    safe_name = safe_name[:-3] if safe_name.endswith('.md') else safe_name
    return safe_name

def convert_to_run(file_path, base_dir):
    """Convert a single markdown file to run format."""
    print(f"Processing: {file_path}")
    
    # Get the conversation
    conversation = extract_conversation_from_md(file_path)
    
    # Skip empty files
    if not conversation.strip():
        print(f"  ⚠ Skipping empty file")
        return None
    
    # Create a safe filename
    safe_name = create_safe_filename(file_path, base_dir)
    
    # Create a run structure that the witness can read
    run = {
        "task": "Deep dialogue between human and AI",
        "first_draft": conversation[:2000] + ("..." if len(conversation) > 2000 else ""),
        "critique": "This is not a critique but a complete conversation",
        "revised_draft": conversation,  # Full conversation here
        "summary": f"Complete dialogue from {file_path.name}",
        "roles": {
            "human": {"provider": "human", "model": "Caelum"},
            "ai": {"provider": "unknown", "model": "original_ai"}
        },
        "metadata": {
            "run_type": "dialogue",
            "source_file": str(file_path),
            "source_format": "obsidian_markdown",
            "original_path": str(file_path),
            "timestamp": datetime.utcnow().isoformat(),
            "training_candidate": True,
            "human_validated": True,
            "quality_score": 1.0,
            "dialogue_complete": True
        }
    }
    
    # Save to training candidates with safe name
    out_file = TRAINING_CANDIDATES_DIR / f"dialogue_{safe_name}.json"
    
    # Avoid overwriting if names collide
    counter = 1
    while out_file.exists():
        out_file = TRAINING_CANDIDATES_DIR / f"dialogue_{safe_name}_{counter}.json"
        counter += 1
    
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(run, f, indent=2, ensure_ascii=False)
    
    print(f"  → Created: {out_file.name}")
    return out_file

def main():
    """Convert all markdown files in the safe directory."""
    ensure_dirs()
    
    # Recursively find all markdown files
    md_files = find_all_markdown_files(DIALOGUES_SAFE_DIR)
    
    if not md_files:
        print(f"No markdown files found in {DIALOGUES_SAFE_DIR}")
        print("Check that the copy step worked correctly.")
        return
    
    print(f"Found {len(md_files)} dialogue files to convert")
    
    # Convert each one
    converted = []
    skipped = 0
    for md_file in md_files:
        try:
            out_file = convert_to_run(md_file, DIALOGUES_SAFE_DIR)
            if out_file:
                converted.append(out_file)
            else:
                skipped += 1
        except Exception as e:
            print(f"  ❌ Error on {md_file.name}: {e}")
            skipped += 1
    
    print(f"\n✅ Converted {len(converted)} dialogues to training candidates")
    print(f"⚠ Skipped {skipped} files")
    print(f"Location: {TRAINING_CANDIDATES_DIR}")

if __name__ == "__main__":
    main()
