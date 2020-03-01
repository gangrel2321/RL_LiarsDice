#add stuff from typing package
class SkullsGame:
    """ Class Representing a Game of Skulls """

    """
    Initialize Game
    @param players list of players in the game
    @return None
    """
    def __init__(self, players=None):
        if isinstance(players,list):
            self.players = players
        else:
            self.players = []

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
    
    def checkRules(self):
        pass
