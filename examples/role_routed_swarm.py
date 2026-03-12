from src.core.node_autonomy import AutonomousNode


def main():
    nodes = [
        AutonomousNode(1, role="reasoning"),
        AutonomousNode(2, role="coding"),
        AutonomousNode(3, role="analysis"),
        AutonomousNode(4, role="utility"),
    ]

    print("Aether role-routed swarm")
    print("=" * 32)

    for node in nodes:
        print(
            f"node_id={node.id} | "
            f"role={node.role} | "
            f"provider={node.llm_client.provider} | "
            f"model={node.llm_client.model}"
        )


if __name__ == "__main__":
    main()
