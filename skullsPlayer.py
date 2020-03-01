#add stuff from typing package
class SkullsPlayer:
    """ Class Representing a Game of Skulls """

    """
    Initialize Player
    @param players list of players in the game
    @return None
    """
    def __init__(self, ident, name, game):
        self.ident = ident 
        self.name = name
        self.red_total = 3
        self.red_hand = 3
        self.black_total = 1
        self.black_hand = 1
        self.debug = False
        self.game = game
        self.curBet = -1

    """
    Get your current cards
    @return tuple of cards (#red, #black)
    """
    def getHand(self):
        return (self.red_hand, self.black_hand)

    def getTable(self):
        return (self.red_total - self.red_hand, self.black_total - self.black_hand)

    def getName(self):
        return self.name

    def resetHand(self):
        self.black_hand = self.black_total
        self.red_hand = self.red_total

    def playCard(self, color):
        if color == "BLACK":
            if self.black_total >= 1:
                self.black_hand -= 1
                return True
        else:
            if self.red_total >= 1:
                self.red_hand -= 1
                return True
        return False
    
    def bet(self, num):
        #ADD: make sure num is valid
        self.curBet = num
    
    def passBet(self):
        pass

    def toggleDebug(self):
        self.debug = not self.debug