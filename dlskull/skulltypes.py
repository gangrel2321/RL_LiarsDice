import enum
from collections import namedtuple

__all__ = [
    'Player',
]


class Player(enum.Enum):
    anne = 1
    bill = 2
    charlie = 3
    
    #gets next player
    @property
    def other(self):
        if self == Player.anne:
            return Player.bill
        elif self == Player.bill:
            return Player.charlie
        else 
            return Player.anne

class GamePhase(enum.Enum):
    placing = 1
    betting = 2
    choice = 3

    #update phase
    @property
    def next(self):
        if self == GamePhase.placing:
            return GamePhase.betting
        elif self == GamePhase.betting:
            return GamePhase.choice
        return None