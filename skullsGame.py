#add stuff from typing package
from skullsPlayer import SkullsPlayer as sp
from enum import Enum 

class GamePhase(Enum):
    PLACING = False
    BETTING = True

class SkullsGame:
    """ Class Representing a Game of Skulls """

    """
    Initialize Game
    @param players list of players in the game
    @return None
    """
    def __init__(self, players=None):
        self.players = []
        if isinstance(players,list):
            for i in range(len(players)):
                self.players.append(sp(i, players[i], self) )
        self.phase = False

    """
    @return List of SkullsPlayer objects
    """
    def getPlayers(self):
        return self.players
    
    """
    Returns current score of specified player
    @return player's score (0-2)
    """
    def getScore(self, player):
        return player.getScore()

    def getPhase(self):
        return GamePhase(self.phase).name

    def getDownCards(self):
        return sum([sum(player.getTableData()) for player in self.players])
            
    """
    Adds a player object to list of players
    """
    def addPlayer(self, player):
        self.players.append(player)
        return None

    """
    Removes a player object to list of players
    """
    def removePlayer(self, player):
        self.players.remove(player)
        return None
    
    def togglePhase(self):
        self.phase = not self.phase

    def checkRules(self):
        pass
