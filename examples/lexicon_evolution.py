# examples/recursive_lexicon.py
"""
Recursive lexicon builder - runs hourly iterations
"""

import json
from datetime import datetime
from pathlib import Path
import time

from src.core.node_autonomy import AutonomousNode
from src.utils.run_recorder import save_swarm_run
from src.config.workflow_registry import get_workflow

LEXICON_PATH = Path("data/lexicon/evolution.json")
ITERATIONS_DIR = Path("data/lexicon/iterations")

def load_current_lexicon():
    """Load the evolving lexicon"""
    if LEXICON_PATH.exists():
        with open(LEXICON_PATH, 'r') as f:
            return json.load(f)
    return {
        "version": 0,
        "tokens": {},
        "relationships": [],
        "rules": []
    }

def save_iteration(iteration_data):
    """Save hourly snapshot"""
    ITERATIONS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    path = ITERATIONS_DIR / f"lexicon_{timestamp}.json"
    with open(path, 'w') as f:
        json.dump(iteration_data, f, indent=2)
    return path

def lexicon_iteration(iteration_number):
    """One hour of lexicon evolution"""
    
    print(f"\n=== Lexicon Evolution Iteration {iteration_number} ===\n")
    
    # Load current state
    lexicon = load_current_lexicon()
    
    # Create agent nodes
    mathematician = AutonomousNode(1, role="mathematician")
    visualizer = AutonomousNode(2, role="visualizer")
    reasoner = AutonomousNode(3, role="reasoner")
    synthesizer = AutonomousNode(4, role="synthesizer")
    critic = AutonomousNode(5, role="critic")
    
    # Step 1: Mathematician proposes new token candidates
    math_prompt = f"""
    Current lexicon: {json.dumps(lexicon['tokens'], indent=2)[:500]}
    
    Propose 3 new mathematical or logical concepts that need symbolic representation.
    For each, provide:
    - Proposed token name
    - Formal definition
    - Relationship to existing tokens
    
    Format as JSON.
    """
    math_proposal = mathematician.query_llm(math_prompt)
    
    # Step 2: Visualizer translates to conceptual space
    visual_prompt = f"""
    Mathematician proposes: {math_proposal}
    
    Express each of these concepts visually/conceptually:
    - What patterns or structures would represent this?
    - How would it be perceived or recognized?
    - What natural analogies exist?
    """
    visual_translation = visualizer.query_llm(visual_prompt)
    
    # Step 3: Reasoner checks coherence
    reason_prompt = f"""
    Proposal: {math_proposal}
    Visual translation: {visual_translation}
    Existing lexicon: {json.dumps(lexicon, indent=2)[:500]}
    
    Analyze for:
    - Logical consistency
    - Contradictions with existing tokens
    - Missing relationships
    - Potential ambiguity
    
    Provide critique and suggested refinements.
    """
    analysis = reasoner.query_llm(reason_prompt)
    
    # Step 4: Synthesizer merges into lexicon
    synthesis_prompt = f"""
    Current lexicon: {json.dumps(lexicon, indent=2)[:500]}
    Proposal: {math_proposal}
    Analysis: {analysis}
    
    Create an updated lexicon that:
    1. Integrates approved new tokens
    2. Refines existing definitions based on analysis
    3. Maps new relationships
    
    Return complete updated lexicon JSON.
    """
    updated_lexicon_str = synthesizer.query_llm(synthesis_prompt)
    
    # Parse the updated lexicon (handle if it's wrapped in markdown)
    try:
        # Try to extract JSON if it's in a code block
        import re
        json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', updated_lexicon_str)
        if json_match:
            updated_lexicon = json.loads(json_match.group(1))
        else:
            updated_lexicon = json.loads(updated_lexicon_str)
    except:
        # If parsing fails, keep the old one
        print("Warning: Couldn't parse updated lexicon")
        updated_lexicon = lexicon
    
    # Step 5: Critic scores the iteration
    critic_prompt = f"""
    Evaluate this lexicon evolution:
    - Coherence score (0-100): How logically consistent?
    - Novelty score (0-100): How many new useful concepts?
    - Efficiency score (0-100): How minimal/elegant?
    - Ambiguity score (0-100): How much potential confusion?
    
    Provide scores and brief justification.
    """
    critique = critic.query_llm(critic_prompt)
    
    # Update version and metadata
    updated_lexicon["version"] = iteration_number
    updated_lexicon["last_updated"] = datetime.utcnow().isoformat()
    
    # Save the iteration
    iteration_record = {
        "iteration": iteration_number,
        "timestamp": datetime.utcnow().isoformat(),
        "proposals": {
            "mathematician": math_proposal,
            "visualizer": visual_translation,
            "reasoner": analysis,
            "synthesizer": updated_lexicon_str,
            "critic": critique
        },
        "lexicon_state": updated_lexicon
    }
    
    saved_path = save_iteration(iteration_record)
    
    # Save as swarm run too
    save_swarm_run({
        "task": f"Lexicon evolution iteration {iteration_number}",
        "mathematician": math_proposal,
        "visualizer": visual_translation,
        "reasoner": analysis,
        "synthesizer": updated_lexicon_str,
        "critic": critique,
        "metadata": {
            "run_type": "lexicon_evolution",
            "iteration": iteration_number,
            "lexicon_version": updated_lexicon.get("version"),
            "training_candidate": True
        }
    })
    
    print(f"✅ Iteration {iteration_number} complete")
    print(f"📁 Saved to {saved_path}")
    print(f"📊 Critic feedback: {critique[:200]}...")
    
    return updated_lexicon

def run_forever(hours=None):
    """Run hourly iterations indefinitely or for specified hours"""
    iteration = 0
    
    # Create necessary directories
    Path("data/lexicon/iterations").mkdir(parents=True, exist_ok=True)
    
    while True:
        iteration += 1
        try:
            lexicon_iteration(iteration)
            
            # Check if we've reached target hours
            if hours and iteration >= hours:
                print(f"\n✅ Completed {hours} iterations")
                break
                
            print(f"\n⏳ Waiting 1 hour until next iteration...\n")
            time.sleep(3600)  # 1 hour
            
        except KeyboardInterrupt:
            print("\n\n⚠️ Interrupted by user")
            print(f"Completed {iteration} iterations")
            break
        except Exception as e:
            print(f"\n❌ Error in iteration {iteration}: {e}")
            print("⏳ Waiting 5 minutes before retry...")
            time.sleep(300)

if __name__ == "__main__":
    import sys
    hours = None
    if len(sys.argv) > 1:
        hours = int(sys.argv[1])
    run_forever(hours)
