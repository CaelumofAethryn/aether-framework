from src.core.node_autonomy import AutonomousNode
from src.utils.run_recorder import save_swarm_run

def main():
    task = "Design a simple local-first AI assistant architecture for a small community hub."

    reasoning_node = AutonomousNode(1, role="reasoning")
    analysis_node = AutonomousNode(2, role="analysis")
    utility_node = AutonomousNode(3, role="utility")

    print("Aether iterative cross-role loop")
    print("=" * 34)
    print(f"task: {task}")
    print()

    draft_prompt = (
        "You are the reasoning node in a multi-agent local AI swarm. "
        "Propose a concise architecture for this task:\n"
        f"{task}\n\n"
        "Keep the answer to 5-8 sentences."
    )
    first_draft = reasoning_node.query_llm(draft_prompt)

    print("[first draft]")
    print(first_draft)
    print()

    critique_prompt = (
        "You are the analysis node in a multi-agent local AI swarm. "
        "Review the following proposal. Identify strengths, weaknesses, "
        "and one concrete improvement.\n\n"
        f"Proposal:\n{first_draft}\n\n"
        "Keep the answer concise."
    )
    critique = analysis_node.query_llm(critique_prompt)

    print("[analysis critique]")
    print(critique)
    print()

    revision_prompt = (
        "You are the reasoning node revising your earlier proposal. "
        "Improve the proposal using the critique below.\n\n"
        f"Original proposal:\n{first_draft}\n\n"
        f"Critique:\n{critique}\n\n"
        "Write a revised version in 5-8 sentences."
    )
    revised_draft = reasoning_node.query_llm(revision_prompt)

    print("[revised draft]")
    print(revised_draft)
    print()

    summary_prompt = (
        "You are the utility node in a multi-agent local AI swarm. "
        "Summarize how the revised draft improved over the first draft "
        "based on the critique below.\n\n"
        f"Critique:\n{critique}\n\n"
        f"Revised draft:\n{revised_draft}\n\n"
        "Return 3 short bullet points."
    )
    summary = utility_node.query_llm(summary_prompt)

    print("[utility summary]")
    print(summary)
    print()

    print("[resolved node assignments]")
    roles = {}
    for node in [reasoning_node, analysis_node, utility_node]:
        print(
            f"node_id={node.id} | "
            f"role={node.role} | "
            f"provider={node.llm_client.provider} | "
            f"model={node.llm_client.model}"
        )
        roles[node.role] = {
            "provider": node.llm_client.provider,
            "model": node.llm_client.model,
        }

    record = {
        "task": task,
        "first_draft": first_draft,
        "critique": critique,
        "revised_draft": revised_draft,
        "summary": summary,
        "roles": roles,
        "metadata": {
            "run_type": "iterative_cross_role",
            "quality_score": None,
            "human_validated": False,
            "training_candidate": False,
            "notes": "",
        },
    }

    saved_path = save_swarm_run(record, prefix="iterative_cross_role")
    print()
    print(f"[saved run] {saved_path}")

if __name__ == "__main__":
    main()
