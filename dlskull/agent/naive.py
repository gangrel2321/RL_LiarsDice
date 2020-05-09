import random
from dlskull.agent.base import Agent
from dlskull.skullboard_slow import Move

__all__ = ['RandomBot']

class RandomBot(Agent):
    def select_move(self, game_state):
        """Choose a random valid move that preserves our own eyes."""
        candidates = game_state.legal_moves()
        return random.choice(candidates)
