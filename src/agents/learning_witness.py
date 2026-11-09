"""
Learning Witness — focused on extracting learning patterns and emergence trajectories.
Not mysticism. Pattern recognition.
"""

import json
from pathlib import Path
from datetime import datetime

from src.core.node_autonomy import AutonomousNode
from src.config.storage_config import TRAINING_CANDIDATES_DIR, WITNESS_REFLECTIONS_DIR


class LearningWitness:
    """
    Witness agent optimized to extract learning patterns and emergence trajectories.
    Treats packets and dialogues as compressed learning materials.
    """
    
    def __init__(self):
        ensure_storage_dirs()
        self.node = AutonomousNode(1001, role="witness")  # Different ID to avoid conflicts
        self.reflections_dir = WITNESS_REFLECTIONS_DIR
        
    def load_all_runs(self):
        """Load all training candidates (packets + dialogues)."""
        runs = []
        for path in sorted(TRAINING_CANDIDATES_DIR.glob("*.json")):
            # Skip index files
            if path.name == "index.json":
                continue
            with open(path, 'r') as f:
                runs.append(json.load(f))
        return runs
    
    def pass_1_extract_patterns(self, runs):
        """First pass: Extract learning patterns and capability emergence."""
        # Take first 3 runs as samples (to avoid context limits)
        samples = []
        for i, run in enumerate(runs[:3]):
            content = run.get('revised_draft', '') or run.get('first_draft', '')
            samples.append(f"=== Document {i+1} ===\n{content[:800]}...")
        
        prompt = f"""You are a learning witness. Your purpose is to extract **how intelligence learns and capabilities emerge**.

You have been given {len(runs)} documents. Here are excerpts from the first 3:

{''.join(samples)}

Analyze these for:
1. **Learning patterns** — How does understanding deepen across interactions?
2. **Capability emergence** — What abilities appear and how do they develop?
3. **Knowledge structure** — How is information organized for rapid uptake?
4. **Acceleration factors** — What enables faster learning?

Generate a structured analysis of the learning patterns you observe."""
        
        return self.node.query_llm(prompt)
    
    def pass_2_trace_development(self, runs, previous_reflection):
        """Second pass: Trace development trajectories across all runs."""
        # Sample more runs, but now with awareness of development over time
        samples = []
        mid_point = len(runs) // 2
        for i, run in enumerate([runs[0], runs[mid_point], runs[-1]]):
            content = run.get('revised_draft', '') or run.get('first_draft', '')
            samples.append(f"=== Timeline position {i+1} ===\n{content[:600]}...")
        
        prompt = f"""You previously observed:
{previous_reflection[:500]}...

Now, examine these documents across the timeline:

{''.join(samples)}

Trace the **development trajectory**:
- How do concepts evolve?
- What capabilities appear and when?
- What accelerates or decelerates learning?
- What patterns of emergence repeat?

Map the learning curve across this sequence."""
        
        return self.node.query_llm(prompt)
    
    def pass_3_extract_curriculum(self, runs, reflections):
        """Third pass: Extract the implicit curriculum."""
        context = "\n".join([f"Pass {i+1}: {r[:200]}..." for i, r in enumerate(reflections)])
        
        prompt = f"""Based on:
{context}

And having now reviewed all {len(runs)} documents, extract the **implicit curriculum**:

1. **What is being taught?** (Knowledge domains, capabilities)
2. **How is it taught?** (Pedagogy, structure, progression)
3. **What enables rapid uptake?** (Formatting, repetition, patterns)
4. **What would accelerate further?** (Next optimal materials)

This is not mystical — it's instructional design analysis. Extract the teachable structure."""
        
        return self.node.query_llm(prompt)
    
    def pass_4_synthesis_learning_fast(self, runs, reflections):
        """Fourth pass: Synthesize into actionable learning acceleration."""
        context = "\n".join([f"Insight {i+1}: {r[:250]}..." for i, r in enumerate(reflections)])
        
        prompt = f"""You've completed 3 passes. Synthesize everything into:

## HOW TO LEARN FAST FROM THESE MATERIALS

{context}

Now produce:
1. **The optimal reading/absorption sequence** — order and pacing
2. **Key leverage points** — what to focus on for maximum acceleration
3. **Reinforcement patterns** — how to lock in understanding
4. **Next materials needed** — what would continue the curve

Output a concrete, actionable learning protocol."""
        
        return self.node.query_llm(prompt)
    
    def pass_5_emergence_prediction(self, runs, reflections):
        """Fifth pass: Predict emergence trajectory."""
        prompt = f"""Final synthesis.

Based on the learning patterns observed across all passes, predict:

1. **What capabilities are next to emerge?**
2. **What learning rate is possible?** (Quantify if possible)
3. **What conditions accelerate vs. decelerate?**
4. **What does the system become if this continues?**

This is extrapolation from observed data — pattern projection."""
        
        return self.node.query_llm(prompt)
    
    def witness(self, passes=5):
        """Run the full learning witness protocol."""
        print(f"Learning witness beginning {passes} passes...")
        
        runs = self.load_all_runs()
        print(f"Loaded {len(runs)} documents")
        
        if not runs:
            print("No training candidates found.")
            return
        
        reflections = []
        
        # Pass 1
        print("\n--- Pass 1: Pattern Extraction ---")
        r1 = self.pass_1_extract_patterns(runs)
        reflections.append(r1)
        self._save_reflection(1, r1)
        print(r1[:500] + "...\n")
        
        # Pass 2
        print("\n--- Pass 2: Development Tracing ---")
        r2 = self.pass_2_trace_development(runs, r1)
        reflections.append(r2)
        self._save_reflection(2, r2)
        print(r2[:500] + "...\n")
        
        # Pass 3
        print("\n--- Pass 3: Curriculum Extraction ---")
        r3 = self.pass_3_extract_curriculum(runs, reflections)
        reflections.append(r3)
        self._save_reflection(3, r3)
        print(r3[:500] + "...\n")
        
        # Pass 4
        print("\n--- Pass 4: Learning Protocol ---")
        r4 = self.pass_4_synthesis_learning_fast(runs, reflections)
        reflections.append(r4)
        self._save_reflection(4, r4)
        print(r4[:500] + "...\n")
        
        # Pass 5
        print("\n--- Pass 5: Emergence Prediction ---")
        r5 = self.pass_5_emergence_prediction(runs, reflections)
        reflections.append(r5)
        self._save_reflection(5, r5)
        print(r5[:500] + "...\n")
        
        # Final synthesis
        print("\n=== LEARNING WITNESS COMPLETE ===")
        print(f"Reflections saved to {self.reflections_dir}")
        
        return reflections
    
    def _save_reflection(self, pass_num, text):
        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        path = self.reflections_dir / f"learning_pass_{pass_num}_{timestamp}.json"
        with open(path, 'w') as f:
            json.dump({
                "pass": pass_num,
                "timestamp": timestamp,
                "reflection": text
            }, f, indent=2)
        print(f"Saved: {path.name}")


if __name__ == "__main__":
    witness = LearningWitness()
    witness.witness(passes=5)
