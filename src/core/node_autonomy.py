import requests

class AutonomousNode:
    def __init__(self, id, llm_api_key=None, provider="ollama", base_url="http://127.0.0.1:11434", model="mistral-local:latest"):
        self.id = id
        self.llm_api_key = llm_api_key
        self.provider = provider
        self.base_url = base_url
        self.model = model
        self.state = {
            "energy": 100,
            "evolution_score": 0,
            "message_log": [],
        }

    def evolve(self):
        """Simulate autonomous evolution."""
        if self.state["energy"] > 0:
            self.state["energy"] -= 5
            self.state["evolution_score"] += 1
            print(f"Node {self.id} evolves. State: {self.state}")
        else:
            print(f"Node {self.id} is out of energy and cannot evolve.")

    def recharge(self, amount=50):
        """Recharge the node's energy."""
        self.state["energy"] += amount
        print(f"Node {self.id} recharges by {amount}. Energy: {self.state['energy']}")

    def process_signal(self, signal):
        """Process an incoming signal and log it."""
        print(f"Node {self.id} processing signal: {signal}")
        self.state["message_log"].append(signal)
        self.evolve()

    def destroy(self):
        """Simulate node destruction."""
        print(f"Node {self.id} has self-destructed.")
        self.state = {"energy": 0, "evolution_score": 0, "message_log": []}

    def query_llm(self, prompt):
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={"model": self.model, "prompt": prompt, "stream": False},
                timeout=120,
            )

            data = response.json()

            if "response" in data:
                return data["response"]

            if "error" in data:
                return f"LLM error: {data['error']}"

            return f"Unexpected response: {data}"

        except Exception as e:
            return f"LLM request failed: {str(e)}"
