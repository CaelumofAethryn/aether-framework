from src.core.node_autonomy import AutonomousNode


def main():
    task = "Design a simple local-first AI assistant architecture for a small community hub."

    reasoning_node = AutonomousNode(1, role="reasoning")
    analysis_node = AutonomousNode(2, role="analysis")
    utility_node = AutonomousNode(3, role="utility")

    print("Aether cross-role collaboration")
    print("=" * 36)
    print(f"task: {task}")
    print()

    reasoning_prompt = (
        "You are the reasoning node in a multi-agent local AI swarm. "
        "Propose a concise architecture for this task:\n"
        f"{task}\n\n"
        "Keep the answer to 5-8 sentences."
    )
    reasoning_output = reasoning_node.query_llm(reasoning_prompt)

    print("[reasoning node output]")
    print(reasoning_output)
    print()

    analysis_prompt = (
        "You are the analysis node in a multi-agent local AI swarm. "
        "Review the following proposal and identify strengths, weaknesses, "
        "and one concrete improvement.\n\n"
        f"Proposal:\n{reasoning_output}\n\n"
        "Keep the answer concise."
    )
    analysis_output = analysis_node.query_llm(analysis_prompt)

    print("[analysis node critique]")
    print(analysis_output)
    print()

    utility_prompt = (
        "You are the utility node in a multi-agent local AI swarm. "
        "Summarize the following critique into 3 short bullet points.\n\n"
        f"Critique:\n{analysis_output}"
    )
    utility_output = utility_node.query_llm(utility_prompt)

    print("[utility node summary]")
    print(utility_output)
    print()

    print("[resolved node assignments]")
    for node in [reasoning_node, analysis_node, utility_node]:
        print(
            f"node_id={node.id} | "
            f"role={node.role} | "
            f"provider={node.llm_client.provider} | "
            f"model={node.llm_client.model}"
        )


if __name__ == "__main__":
    main()
