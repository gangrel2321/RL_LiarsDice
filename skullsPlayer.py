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
        self.table = []
        self.debug = False
        self.game = game
        self.curBet = -1

    """
    Get your current cards
    @return tuple of cards (#red, #black)
    """
    def getHand(self):
        return "(R:" + str(self.red_hand) + " , " + "B:" + str(self.black_hand) + ")"

    def getTable(self):
        return self.table

    def getTableData(self):
        return ( sum([int(card == "R") for card in self.table]), sum([int(card == "B") for card in self.table]) )

    def getTableString(self):
        table_string = ""
        for i in range(len(self.table)):
            table_string += str(i) + ": " + str(self.table[i])
            if i < len(self.table) - 1:
                table_string += ", "
        return table_string 

    def getName(self):
        return self.name

    def popTable(self):
        self.table.pop()
        return self.table

    def resetHand(self):
        self.black_hand = self.black_total
        self.red_hand = self.red_total

    def playCard(self, color):
        if color == "BLACK":
            if self.black_total >= 1:
                self.black_hand -= 1
                self.table.append('B')
                return True
        else:
            if self.red_total >= 1:
                self.red_hand -= 1
                self.table.append('R')
                return True
        return False
    
    def bet(self):
        #ADD: make sure num is valid
        self.curBet = int(input("Enter Bet (-1 = pass): "))
        return self.curBet
    
    def passBet(self):
        pass

    def toggleDebug(self):
        self.debug = not self.debug