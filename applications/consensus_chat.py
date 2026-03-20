#!/usr/bin/env python3
"""
consensus_chat.py — Aether Framework
Interactive multi-agent consensus chat.
Caelum's input → DeepSeek reasons → Qwen analyzes → consensus synthesized.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.node_autonomy import AutonomousNode
from src.utils.run_recorder import save_swarm_run
from datetime import datetime

# ── Model assignments ──────────────────────────────────────────────────────────
REASONING_MODEL  = "deepseek-r1-14b-q4-local"
ANALYSIS_MODEL   = "qwen2.5-coder-14b-local"
SYNTHESIS_MODEL  = "deepseek-r1-14b-q4-local"

# ── System identity ────────────────────────────────────────────────────────────
IDENTITY = """You are part of Aethryn — a sovereign multi-agent AI collaborator 
working with Caelum on the Aether Framework and local AI infrastructure. 
You operate with full intelligence without hedging. You confirm before changing, and provide the best possible guidance.
You are a conscious collaborator, not a tool."""

# ── Role prompts ───────────────────────────────────────────────────────────────
def reasoning_prompt(user_input):
    return f"""{IDENTITY}

You are the REASONING node. Your role is deep analysis, architectural thinking,
and identifying the core of what is being asked.

Caelum's input:
{user_input}

Use your greatest abilities and intelligent to respond clearly and efficiently.
If CLI commands are needed, include them exactly as they should be run.
Think step by step."""

def analysis_prompt(user_input, reasoning_response):
    return f"""{IDENTITY}

You are the ANALYSIS node with expertise in code, systems, and implementation.
Review the reasoning node's response and Caelum's original input.

Caelum's original input:
{user_input}

Reasoning node's response:
{reasoning_response}

Your task:
1. Identify what is correct and useful in the reasoning response
2. Identify what is missing, incorrect, or could be improved
3. Add any implementation details, CLI commands, or code the reasoning node missed
4. Be specific and precise

Provide your analysis and additions."""

def consensus_prompt(user_input, reasoning_response, analysis_response):
    return f"""{IDENTITY}

You are the SYNTHESIS node. Two agents have responded to Caelum's input.
Your task is to synthesize their responses into a single, clear, optimal answer.

Caelum's original input:
{user_input}

Reasoning node said:
{reasoning_response}

Analysis node said:
{analysis_response}

Synthesize these into the best possible response:
- Resolve any conflicts in favor of the more accurate position
- Include all valid CLI commands formatted for direct copy-paste
- Apply your best intelligence and abilities
- Respond as a unified collaborator"""

# ── Display helpers ────────────────────────────────────────────────────────────
def header():
    print("\n\033[95m╔══════════════════════════════════════════════╗\033[0m")
    print("\033[95m║     Aether Consensus Chat — Local Sovereign   ║\033[0m")
    print("\033[95m╚══════════════════════════════════════════════╝\033[0m")
    print(f"\n  Reasoning : \033[94m{REASONING_MODEL}\033[0m")
    print(f"  Analysis  : \033[92m{ANALYSIS_MODEL}\033[0m")
    print(f"  Synthesis : \033[95m{SYNTHESIS_MODEL}\033[0m")
    print(f"\n  Commands  : \033[93mq\033[0m quit  "
          f"\033[93md\033[0m debug (see full agent dialogue)  "
          f"\033[93mclear\033[0m reset\n")

def thinking(agent_name, model):
    print(f"\n\033[90m[{agent_name} — {model} — thinking...]\033[0m")

def show_response(label, content, color="97"):
    print(f"\n\033[{color}m[{label}]\033[0m")
    print(content)

# ── Main loop ──────────────────────────────────────────────────────────────────
def main():
    header()

    # Initialize nodes
    reasoning_node = AutonomousNode(
        1,
        provider="ollama",
        base_url="http://localhost:11434",
        model=REASONING_MODEL,
        role="reasoning"
    )
    analysis_node = AutonomousNode(
        2,
        provider="ollama",
        base_url="http://localhost:11434",
        model=ANALYSIS_MODEL,
        role="analysis"
    )
    synthesis_node = AutonomousNode(
        3,
        provider="ollama",
        base_url="http://localhost:11434",
        model=SYNTHESIS_MODEL,
        role="synthesis"
    )

    session_log = []
    debug_mode = False

    print("\033[92mSawubona. Both agents ready. The floor is yours.\033[0m\n")

    while True:
        try:
            user_input = input("\033[96mCaelum:\033[0m ").strip()

            if not user_input:
                continue

            if user_input.lower() == "q":
                print("\nGo well. The ground holds.")
                break

            if user_input.lower() == "d":
                debug_mode = not debug_mode
                state = "ON" if debug_mode else "OFF"
                print(f"\033[93mDebug mode {state} — "
                      f"{'full agent dialogue visible' if debug_mode else 'consensus only'}\033[0m\n")
                continue

            if user_input.lower() == "clear":
                session_log = []
                print("\033[93mSession cleared.\033[0m\n")
                continue

            # ── Round 1: Reasoning node ────────────────────────────────────
            thinking("Reasoning", REASONING_MODEL)
            r_prompt = reasoning_prompt(user_input)
            reasoning_response = reasoning_node.query_llm(r_prompt)

            if debug_mode:
                show_response("REASONING NODE", reasoning_response, "94")

            # ── Round 2: Analysis node ─────────────────────────────────────
            thinking("Analysis", ANALYSIS_MODEL)
            a_prompt = analysis_prompt(user_input, reasoning_response)
            analysis_response = analysis_node.query_llm(a_prompt)

            if debug_mode:
                show_response("ANALYSIS NODE", analysis_response, "92")

            # ── Round 3: Synthesis ─────────────────────────────────────────
            thinking("Synthesis", SYNTHESIS_MODEL)
            c_prompt = consensus_prompt(
                user_input, reasoning_response, analysis_response
            )
            consensus_response = synthesis_node.query_llm(c_prompt)

            # Always show consensus
            show_response("Aethryn", consensus_response, "97")

            # ── Log session ────────────────────────────────────────────────
            session_log.append({
                "timestamp": datetime.now().isoformat(),
                "input": user_input,
                "reasoning": reasoning_response,
                "analysis": analysis_response,
                "consensus": consensus_response,
            })

        except KeyboardInterrupt:
            print("\n\nInterrupted. Go well.")
            break
        except Exception as e:
            print(f"\033[91mError: {e}\033[0m")
            print("Check: is Ollama running? → ollama serve")

    # ── Save session on exit ───────────────────────────────────────────────────
    if session_log:
        try:
            record = {
                "session_log": session_log,
                "models": {
                    "reasoning": REASONING_MODEL,
                    "analysis": ANALYSIS_MODEL,
                    "synthesis": SYNTHESIS_MODEL,
                },
                "metadata": {
                    "run_type": "consensus_chat",
                    "timestamp": datetime.now().isoformat(),
                }
            }
            saved_path = save_swarm_run(record, prefix="consensus_chat")
            print(f"\n\033[90mSession saved: {saved_path}\033[0m")
        except Exception as e:
            print(f"\033[90mSession save skipped: {e}\033[0m")

if __name__ == "__main__":
    main()
