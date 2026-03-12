import json
import random
from src.modules.social_media_orchestrator import SocialMediaOrchestrator
import queue
import numpy as np

from src.utils.llm_client import LLMClient
from src.utils.multi_modal_handler import MultiModalHandler
from src.swarm.swarm_consensus import SwarmConsensus
from src.utils.blockchain_manager import BlockchainManager
from src.utils.redis_task_queue import RedisTaskQueue
from src.utils.knowledge_graph import KnowledgeGraph
from src.utils.ipfs_client import IPFSClient
from src.utils.agent_collaboration import CollaborationFramework
from src.utils.reinforcement_learning import QLearning
from src.democracy.proposal_manager import ProposalManager
from nacl.signing import SigningKey

class AIAgent:
    """
    A fully modular AI agent with advanced features, including reinforcement learning,
    swarm intelligence, multi-modal capabilities, blockchain integration, IPFS communication,
    and social media orchestration.
    """

    def __init__(self, agent_id, role, provider, base_url, ethereum_rpc_url=None, state_size=5, action_size=3):
        self.agent_id = agent_id
        self.role = role
        self.llm_client = LLMClient(provider, base_url)
        self.multi_modal_handler = MultiModalHandler()
        self.consensus = SwarmConsensus(agent_id)
        self.blockchain_manager = BlockchainManager(ethereum_rpc_url=ethereum_rpc_url)
        self.redis_queue = RedisTaskQueue()
        self.knowledge_graph = KnowledgeGraph()
        self.ipfs_client = IPFSClient()
        self.collaboration = CollaborationFramework()
        self.rl_agent = QLearning(state_size, action_size)
        self.keypair = SigningKey.generate()  # Create agent's signing key for Solana
        self.proposal_manager = ProposalManager()
        self.social_media_orchestrator = SocialMediaOrchestrator(agent_id)
        self.knowledge_base = []
        self.task_queue = queue.PriorityQueue()

    # Multi-modal task execution
    def execute_text_task(self, task_description):
        result = self.llm_client.generate_text(task_description)
        print(f"Agent {self.agent_id}: Text task result - {result}")
        return result

    def execute_image_task(self, image_path, text_prompts):
        result = self.multi_modal_handler.process_image(image_path, text_prompts)
        print(f"Agent {self.agent_id}: Image task result - {result}")
        return result

    def execute_audio_task(self, audio_path):
        try:
            result = self.multi_modal_handler.process_audio(audio_path)
            print(f"Agent {self.agent_id}: Audio task result - {result}")
            return result
        except NotImplementedError as e:
            print(f"Agent {self.agent_id}: {e}")
            return None

    # Distributed task queue
    def push_task_to_queue(self, task_description):
        task = {
            "agent_id": self.agent_id,
            "role": self.role,
            "task_description": task_description
        }
        self.redis_queue.push_task(task)

    def pull_task_from_queue(self):
        task = self.redis_queue.pop_task()
        if task:
            print(f"Agent {self.agent_id}: Processing task from queue - {task['task_description']}")
            self.execute_task(task["task_description"])

    # Blockchain methods
    def log_task_on_chain(self, task_description, task_result):
        print(f"Agent {self.agent_id}: Logging task on-chain.")
        return self.blockchain_manager.log_task(
            sender_keypair=self.keypair,
            task_description=task_description,
            task_result=task_result
        )

    def get_sol_balance(self):
        return self.blockchain_manager.solana_get_balance(self.keypair.verify_key)

    def send_sol(self, recipient_pubkey, amount):
        return self.blockchain_manager.solana_send_transaction(self.keypair, recipient_pubkey, amount)

    def get_eth_balance(self, address):
        return self.blockchain_manager.ethereum_get_balance(address)

    def send_eth(self, sender_key, recipient_address, amount_ether):
        return self.blockchain_manager.ethereum_send_transaction(sender_key, recipient_address, amount_ether)

    # Knowledge graph methods
    def add_knowledge(self, concept, attributes=None):
        self.knowledge_graph.add_concept(concept, attributes)

    def add_knowledge_relationship(self, concept1, concept2, relationship_type):
        self.knowledge_graph.add_relationship(concept1, concept2, relationship_type)

    def query_knowledge(self, concept):
        return self.knowledge_graph.query_concept(concept)

    def visualize_knowledge_graph(self, output_path="knowledge_graph.png"):
        self.knowledge_graph.visualize_graph(output_path)

    # IPFS communication
    def upload_to_ipfs(self, file_path):
        return self.ipfs_client.upload_file(file_path)

    def download_from_ipfs(self, cid, output_path):
        self.ipfs_client.retrieve_file(cid, output_path)

    # Social media management
    def manage_social_media(self, platform, content):
        self.social_media_orchestrator.create_post(platform, content)
        self.social_media_orchestrator.publish_post(platform)

    # Reinforcement learning
    def optimize_task_execution(self, state):
        action = self.rl_agent.choose_action(state)
        reward = self.execute_action(action)
        next_state = self.get_environment_state()
        self.rl_agent.update_q_table(state, action, reward, next_state)
        self.rl_agent.decay_exploration()

    def execute_action(self, action):
        """Execute an RL-selected action and return a reward."""

        if action == 0:  # Example action: Process next queued task
            self.pull_task_from_queue()
            return 1

        elif action == 1:  # Example action: Store knowledge
            self.add_knowledge("New Task", {"status": "completed"})
            return 2

        elif action == 2:  # Example action: Log task outcome
            try:
                self.log_task_on_chain("Test Task", "Success")
            except Exception:
                print(f"Agent {self.agent_id}: Blockchain logging unavailable.")
            return 3

        return 0



    def get_environment_state(self):
        return np.random.randint(5)

    # Swarm decision-making
    def propose_task_to_swarm(self, task_description):
        return self.consensus.propose_task(task_description)

    def vote_on_task(self, proposal_id):
        self.consensus.vote(proposal_id)

    def check_consensus(self):
        return self.consensus.get_consensus()


 # Local task management
    def add_task(self, priority, task_description):
        self.task_queue.put((priority, task_description))
        print(f"Agent {self.agent_id}: Task added with priority {priority} - {task_description}")

    def process_next_task(self):
        if not self.task_queue.empty():
            priority, task_description = self.task_queue.get()
            print(f"Agent {self.agent_id}: Processing task with priority {priority} - {task_description}")
            self.execute_text_task(task_description)
        else:
            print(f"Agent {self.agent_id}: No tasks in the queue.")

    # Knowledge base management
    def add_to_knowledge_base(self, task_description, result):
        self.knowledge_base.append({"task": task_description, "result": result})

    def save_knowledge_base(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.knowledge_base, f)
        print(f"Agent {self.agent_id}: Knowledge base saved to {filename}.")

    def load_knowledge_base(self, filename):
        try:
            with open(filename, 'r') as f:
                self.knowledge_base = json.load(f)
            print(f"Agent {self.agent_id}: Knowledge base loaded from {filename}.")
        except FileNotFoundError:
            print(f"Agent {self.agent_id}: No existing knowledge base found at {filename}. Starting fresh.")


    def delegate_task(self, recipient_id, task_description):
        message = f"TASK DELEGATION: {task_description}"
        self.collaboration.send_message(self.agent_id, recipient_id, message)
        print(f"Agent {self.agent_id}: Delegated task to Agent {recipient_id} - {task_description}")

    # Collaboration
    def send_message(self, recipient_id, message):
        self.collaboration.send_message(self.agent_id, recipient_id, message)

    def receive_messages(self):
        messages = self.collaboration.receive_message(self.agent_id)
        for msg in messages:
            print(f"Agent {self.agent_id} received message: {msg['message']}")

# Example usage
if __name__ == "__main__":
    agent = AIAgent(agent_id="JEDI-01", role="coordinator", provider="huggingface", base_url="http://localhost:8000")
    agent.execute_text_task("Generate a project plan for the next phase.")
