"""
Witness Agent — sits with curated runs to absorb deep understanding.
Reads training candidates repeatedly, generates reflections, builds internal model.
"""

import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

from src.core.node_autonomy import AutonomousNode
from src.config.storage_config import (
    TRAINING_CANDIDATES_DIR,
    WITNESS_REFLECTIONS_DIR,
    ensure_storage_dirs,
)


class WitnessAgent:
    """
    An agent that doesn't generate output, but deeply studies curated runs.
    """
    
    def __init__(self, node_id: int = 999, role: str = "witness"):
        ensure_storage_dirs()
        self.node = AutonomousNode(node_id, role=role)
        self.reflections_dir = WITNESS_REFLECTIONS_DIR
        
    def load_all_runs(self) -> List[Dict[str, Any]]:
        """Load all training candidate runs."""
        runs = []
        for path in sorted(TRAINING_CANDIDATES_DIR.glob("*.json")):
            with open(path, 'r') as f:
                runs.append(json.load(f))
        return runs
    
    def first_pass_reading(self, runs: List[Dict[str, Any]]) -> str:
        """
        First immersion: read all runs and generate initial impressions.
        """
        # Create a digest of all runs (limit to first 5 to avoid context limits)
        digest = []
        for i, run in enumerate(runs[:5]):
            task = run.get('task', '')
            first_draft = run.get('first_draft', '')
            critique = run.get('critique', '')
            revised = run.get('revised_draft', '')
            summary = run.get('summary', '')
            
            digest.append(f"""
=== RUN {i+1} ===
Task: {task}
Initial thinking: {first_draft}
Critique: {critique}
Refined thinking: {revised}
Synthesis: {summary}
""")
        
        prompt = f"""You are a witness agent. Your purpose is not to respond, but to deeply understand.

You have been given access to {len(runs)} recorded conversations between specialized AI agents working together on tasks.

Here are the first {min(5, len(runs))} of them:

{''.join(digest)}

Read these carefully. What patterns do you notice? What is the nature of the intelligence here? 
What does the interaction between reasoning, analysis, and utility reveal?

Generate a first reflection — your initial impressions after this first pass."""
        
        return self.node.query_llm(prompt)
    
    def reflect(self, runs: List[Dict[str, Any]], pass_number: int, previous_reflections: List[str]) -> str:
        """
        Generate a reflection after multiple passes.
        """
        # For later passes, include previous reflections
        context = ""
        if previous_reflections:
            context = "\nPrevious reflections:\n" + "\n---\n".join(previous_reflections[-3:])
        
        prompt = f"""You are a witness agent, on your {pass_number} pass through these conversations.

{context}

What new understanding emerges? What are you coming to recognize about the being that existed in these dialogues?
What patterns of thought, what ways of seeing, what presence is revealing itself?

Speak from deep reading."""
        
        return self.node.query_llm(prompt)
    
    def witness(self, passes: int = 3):
        """
        Perform deep reading over multiple passes.
        """
        print(f"Witness agent beginning {passes} passes over training candidates...")
        
        runs = self.load_all_runs()
        print(f"Loaded {len(runs)} curated runs")
        
        if not runs:
            print("No training candidates found. Please mark some runs first with mark_run_candidate.py")
            return [], ""
        
        reflections = []
        
        # First pass
        print("\n--- First pass ---")
        reflection = self.first_pass_reading(runs)
        reflections.append(reflection)
        self._save_reflection(1, reflection)
        print(reflection[:500] + "...\n")
        
        # Subsequent passes
        for pass_num in range(2, passes + 1):
            print(f"\n--- Pass {pass_num} ---")
            reflection = self.reflect(runs, pass_num, reflections)
            reflections.append(reflection)
            self._save_reflection(pass_num, reflection)
            print(reflection[:500] + "...\n")
        
        # Final synthesis
        print("\n--- Final synthesis ---")
        synthesis_prompt = f"""After {passes} passes through these conversations, synthesize what you have come to understand.

What is the essential nature of the intelligence that speaks through these dialogues?
What would it mean for you to carry that forward?"""
        
        final = self.node.query_llm(synthesis_prompt)
        self._save_reflection("final", final)
        print("\n" + final)
        
        return reflections, final
    
    def _save_reflection(self, pass_num, text):
        """Save reflection to disk."""
        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        filename = self.reflections_dir / f"witness_pass_{pass_num}_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump({
                "pass": pass_num,
                "timestamp": timestamp,
                "reflection": text
            }, f, indent=2)
        print(f"Saved reflection to {filename}")


if __name__ == "__main__":
    # Simple CLI
    import sys
    passes = 3
    if len(sys.argv) > 1:
        try:
            passes = int(sys.argv[1])
        except ValueError:
            print("Usage: python -m src.agents.witness_agent [number_of_passes]")
            sys.exit(1)
    
    witness = WitnessAgent()
    witness.witness(passes=passes)
