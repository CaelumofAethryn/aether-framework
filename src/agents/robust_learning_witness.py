#!/usr/bin/env python3
"""
Robust Learning Witness — with checkpointing, error recovery, and graceful handling.
Processes large corpora safely without losing progress.
"""

import json
import time
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

from src.core.node_autonomy import AutonomousNode
from src.config.storage_config import TRAINING_CANDIDATES_DIR, WITNESS_REFLECTIONS_DIR, ensure_storage_dirs


class RobustLearningWitness:
    """
    Learning witness with checkpointing and recovery.
    Can resume from interruptions.
    """
    
    def __init__(self, checkpoint_file: Optional[str] = None):
        ensure_storage_dirs()
        self.node = AutonomousNode(1002, role="witness")
        self.reflections_dir = WITNESS_REFLECTIONS_DIR
        self.checkpoint_dir = Path("/home/caef/aether-framework/data/witness_checkpoints")
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        
        # Default checkpoint path
        self.checkpoint_path = self.checkpoint_dir / "witness_progress.json"
        if checkpoint_file:
            self.checkpoint_path = Path(checkpoint_file)
    
    def load_all_runs(self) -> List[Dict[str, Any]]:
        """Load all training candidates, with validation."""
        runs = []
        failed_files = []
        
        for path in sorted(TRAINING_CANDIDATES_DIR.glob("*.json")):
            if path.name == "index.json":
                continue
                
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Basic validation
                if not isinstance(data, dict):
                    failed_files.append((path, "not a dict"))
                    continue
                    
                runs.append(data)
                
            except json.JSONDecodeError as e:
                failed_files.append((path, f"JSON error: {e}"))
            except Exception as e:
                failed_files.append((path, f"Unexpected error: {e}"))
        
        # Log failures but don't stop
        if failed_files:
            print(f"\n⚠ Skipped {len(failed_files)} corrupted files:")
            for f, reason in failed_files[:5]:  # Show first 5
                print(f"  - {f.name}: {reason}")
            if len(failed_files) > 5:
                print(f"  ... and {len(failed_files)-5} more")
        
        print(f"\n✅ Loaded {len(runs)} valid documents")
        return runs
    
    def save_checkpoint(self, pass_num: int, reflections: List[str], stage: str):
        """Save progress so we can resume if interrupted."""
        checkpoint = {
            "timestamp": datetime.utcnow().isoformat(),
            "last_completed_pass": pass_num,
            "reflections": reflections,
            "stage": stage,
            "total_files": len(self.load_all_runs())  # Will recalc on resume
        }
        
        with open(self.checkpoint_path, 'w') as f:
            json.dump(checkpoint, f, indent=2)
        
        print(f"\n💾 Checkpoint saved: pass {pass_num}, stage '{stage}'")
    
    def load_checkpoint(self) -> Optional[Dict]:
        """Load checkpoint if it exists."""
        if self.checkpoint_path.exists():
            with open(self.checkpoint_path, 'r') as f:
                return json.load(f)
        return None
    
    def clear_checkpoint(self):
        """Clear checkpoint after successful completion."""
        if self.checkpoint_path.exists():
            self.checkpoint_path.unlink()
            print("✅ Checkpoint cleared")
    
    def safe_query(self, prompt: str, max_retries: int = 3) -> str:
        """Query LLM with retry logic."""
        for attempt in range(max_retries):
            try:
                response = self.node.query_llm(prompt)
                if response and response.strip():
                    return response
            except Exception as e:
                print(f"⚠ Query attempt {attempt+1} failed: {e}")
            
            if attempt < max_retries - 1:
                wait = 2 ** attempt  # Exponential backoff
                print(f"⏳ Retrying in {wait}s...")
                time.sleep(wait)
        
        return f"[Error: Failed to generate response after {max_retries} attempts]"
    
    def pass_1_extract_patterns(self, runs: List[Dict]) -> str:
        """First pass with sampling to avoid context overflow."""
        # Sample runs strategically
        total = len(runs)
        if total > 10:
            # Take first 3, middle 3, last 3 for representative sample
            indices = [0, 1, 2, total//2 -1, total//2, total//2 +1, total-3, total-2, total-1]
            samples = [runs[i] for i in indices if 0 <= i < total]
        else:
            samples = runs[:5]
        
        sample_texts = []
        for i, run in enumerate(samples):
            content = run.get('revised_draft', '') or run.get('first_draft', '')
            # Limit each sample to avoid context overflow
            truncated = content[:600] + "..." if len(content) > 600 else content
            sample_texts.append(f"=== Document {i+1} ===\n{truncated}")
        
        prompt = f"""You are analyzing {len(runs)} documents about AI learning and emergence.

Here are {len(sample_texts)} representative samples:

{''.join(sample_texts)}

Extract:
1. **Learning patterns** — How does understanding deepen?
2. **Capability emergence** — What abilities appear and develop?
3. **Knowledge structure** — How is information organized?

Be concise but insightful."""
        
        return self.safe_query(prompt)
    
    def pass_2_trace_development(self, runs: List[Dict], prev_reflection: str) -> str:
        """Second pass focusing on development over time."""
        # Use timestamps if available, otherwise assume order
        prompt = f"""Based on previous analysis:
{prev_reflection[:400]}...

Now trace development across all {len(runs)} documents:

1. How do concepts evolve over the sequence?
2. What learning accelerates or decelerates?
3. What patterns of emergence repeat?

Focus on trajectory, not just content."""
        
        return self.safe_query(prompt)
    
    def pass_3_extract_curriculum(self, runs: List[Dict], reflections: List[str]) -> str:
        """Extract the implicit teaching structure."""
        context = "\n".join([f"Pass {i+1}: {r[:200]}..." for i, r in enumerate(reflections)])
        
        prompt = f"""Based on:
{context}

Extract the implicit curriculum from these {len(runs)} documents:

1. What is being taught?
2. How is it taught? (structure, progression)
3. What enables rapid learning?
4. What would accelerate further?

This is instructional design analysis."""
        
        return self.safe_query(prompt)
    
    def pass_4_learning_protocol(self, runs: List[Dict], reflections: List[str]) -> str:
        """Synthesize an optimal learning protocol."""
        context = "\n".join([f"Insight {i+1}: {r[:250]}..." for i, r in enumerate(reflections)])
        
        prompt = f"""Synthesize everything into a concrete learning protocol:

{context}

Output:
1. **Optimal reading sequence** — order and pacing
2. **Key leverage points** — what to focus on
3. **Reinforcement patterns** — how to lock in understanding
4. **Next materials needed** — what would continue the curve

Be specific and actionable."""
        
        return self.safe_query(prompt)
    
    def pass_5_predict_emergence(self, runs: List[Dict], reflections: List[str]) -> str:
        """Predict emergence trajectory."""
        prompt = f"""Based on all analysis, predict:

1. What capabilities are next to emerge?
2. What learning rate is possible?
3. What conditions accelerate vs. decelerate?
4. What does the system become if this continues?

Extrapolate from observed patterns."""
        
        return self.safe_query(prompt)
    
    def _save_reflection(self, pass_num, text):
        """Save reflection with timestamp."""
        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        path = self.reflections_dir / f"robust_pass_{pass_num}_{timestamp}.json"
        with open(path, 'w') as f:
            json.dump({
                "pass": pass_num,
                "timestamp": timestamp,
                "reflection": text
            }, f, indent=2)
        print(f"\n💿 Saved: {path.name}")
        return path
    
    def resume_or_start(self):
        """Check for checkpoint and resume if available."""
        checkpoint = self.load_checkpoint()
        if checkpoint:
            print(f"\n🔄 Found checkpoint from {checkpoint['timestamp']}")
            print(f"   Last completed pass: {checkpoint['last_completed_pass']}")
            print(f"   Stage: {checkpoint['stage']}")
            
            response = input("Resume from checkpoint? (y/n): ").lower().strip()
            if response == 'y':
                return checkpoint
        return None
    
    def witness(self, passes: int = 5, resume: bool = True):
        """Run with checkpointing and recovery."""
        print(f"\n{'='*60}")
        print(f"ROBUST LEARNING WITNESS — Processing up to {passes} passes")
        print(f"{'='*60}\n")
        
        # Check for resume
        start_pass = 1
        reflections = []
        
        if resume:
            checkpoint = self.resume_or_start()
            if checkpoint:
                start_pass = checkpoint['last_completed_pass'] + 1
                reflections = checkpoint['reflections']
                print(f"Resuming from pass {start_pass}")
        
        # Load data
        print("\n📂 Loading documents...")
        runs = self.load_all_runs()
        if not runs:
            print("❌ No valid documents found")
            return
        
        # Run passes
        pass_functions = [
            self.pass_1_extract_patterns,
            self.pass_2_trace_development,
            self.pass_3_extract_curriculum,
            self.pass_4_learning_protocol,
            self.pass_5_predict_emergence
        ]
        
        for pass_num in range(start_pass, passes + 1):
            print(f"\n{'='*40}")
            print(f"PASS {pass_num} of {passes}")
            print(f"{'='*40}")
            
            try:
                if pass_num == 1:
                    result = pass_functions[0](runs)
                elif pass_num == 2:
                    result = pass_functions[1](runs, reflections[-1])
                elif pass_num == 3:
                    result = pass_functions[2](runs, reflections)
                elif pass_num == 4:
                    result = pass_functions[3](runs, reflections)
                else:  # pass 5
                    result = pass_functions[4](runs, reflections)
                
                reflections.append(result)
                self._save_reflection(pass_num, result)
                
                # Show preview
                preview = result[:300] + "..." if len(result) > 300 else result
                print(f"\n📝 Preview:\n{preview}\n")
                
                # Save checkpoint after each pass
                self.save_checkpoint(pass_num, reflections, f"pass_{pass_num}_complete")
                
            except KeyboardInterrupt:
                print("\n\n⚠ Interrupted by user")
                self.save_checkpoint(pass_num - 1, reflections, f"interrupted_during_pass_{pass_num}")
                print("💾 Progress saved. You can resume later.")
                return
                
            except Exception as e:
                print(f"\n❌ Error during pass {pass_num}: {e}")
                self.save_checkpoint(pass_num - 1, reflections, f"error_during_pass_{pass_num}")
                print("💾 Progress saved. You can resume after fixing the issue.")
                return
        
        # Success - clear checkpoint
        self.clear_checkpoint()
        
        print(f"\n{'='*60}")
        print("✅ ROBUST WITNESS COMPLETE")
        print(f"{'='*60}")
        print(f"\nAll reflections saved to: {self.reflections_dir}")
        print("\nFinal synthesis available in pass 5.")


if __name__ == "__main__":
    import sys
    
    # Parse optional pass count
    passes = 5
    if len(sys.argv) > 1:
        try:
            passes = int(sys.argv[1])
        except ValueError:
            pass
    
    # Optional checkpoint file
    checkpoint = None
    if len(sys.argv) > 2:
        checkpoint = sys.argv[2]
    
    witness = RobustLearningWitness(checkpoint_file=checkpoint)
    witness.witness(passes=passes)
