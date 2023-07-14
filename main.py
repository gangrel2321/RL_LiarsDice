from skullsGame import SkullsGame
from skullsPlayer import SkullsPlayer
from os import system, name 
from time import sleep 
  
# define our clear function 
def clear(): 
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

#Define gamestate

if __name__ == "__main__":
    #Start Game
    cardColor = {"RED": True, "BLACK":False, True:"RED", False:"BLACK"}
    numPlayers = int(input("Enter the number of players: "))
    playersList = []
    print("Enter the player names (Separated by ENTER):")
    for i in range(numPlayers):
        playersList.append(input())
    curGame = SkullsGame(playersList)
    gameOver = False
    roundCount = 0
    roundOver = False
    while not roundOver:
        roundCount += 1
        print("Round %d\n" % roundCount)
        topBet = 0
        topPlayer = None
        for i in range(len(playersList)):
            curPlay = curGame.players[i]
            print("Current Player: %s" % curPlay.getName() )
            print("[Current Hand - %s]" % str( curPlay.getHand() ) )
            print("Cards down: ",end="")
            data = ""
            for j in range(len(playersList)):
                data += str(curGame.players[j].getName())
                data += " " + str(len(curGame.players[j].getTable())) + ", "
            data = data[:-2]
            print(data)
            print()
            if curGame.getPhase() == "PLACING": #placing cards phase
                if roundCount > 1:
                    decision = input("Would you like to start betting? (y/n): ").upper()
                else: decision = "N"
                while ((decision != "N") and (decision != "Y")):
                    decision = input("ERROR: Enter \"y\" or \"n\": ").upper()
                if decision == "N":
                    card = input("Play a card (RED, BLACK): ").upper()
                    while ((card != "RED") and (card != "BLACK")):
                        card = input("ERROR: Enter \"RED\" or \"BLACK\": ").upper()
                    if not curPlay.playCard(card):
                        print("ERROR: You do not have enough \"%s\"." % card)
                        card = cardColor[not cardColor[card]]
                    print("%s played %s." % (curPlay.getName(), card))
                else:
                    print("[Played Cards - %s]\n" % str( curPlay.getTableString() ))
                    topBet = int(input("Enter Bet: "))
                    topPlayer = curGame.players[i]
                    curGame.togglePhase() #switch to betting phase

            else: #betting phase
                #betPhase()
                roundOver = True
                print("[Played Cards - %s]\n" % str( curPlay.getTableString() ))
                print("Current Highest Bet:", topBet)
                curBet = curPlay.bet()
                if curBet > topBet:
                    topBet = curBet
                    if topBet >= curGame.getDownCards(): topBet = curGame.getDownCards()
                    topPlayer= curGame.players[i]
            if topBet == curGame.getDownCards():
                break 
            print("Clearing Screen For Next Player ...\n")
            sleep(1)
            clear()
            sleep(2)
        if topBet == curGame.getDownCards():
            break 
        if roundCount > 1 and topPlayer != None:
            print("Player with Highest Bet: %s" % topPlayer.getName())
            print()
    
    #decision phase
    print("Decision Phase:\n%s must choose %s cards." % (topPlayer.getName(), topBet))
    cardsRemain = topBet

    #choose from your own side
    while cardsRemain > 0 and sum(topPlayer.getTableData()) > 0:
        topCard = topPlayer.popTable()
        if topCard == 'B':
            print("%s draws their own Black." % topPlayer.getName() )
            print("%s loses." % topPlayer.getName() )
            gameOver = True
            break
        else:
            print("%s draws their own Red." % topPlayer.getName() )
            cardsRemain -= 1

    #choose from other players
    while not gameOver:
        if cardsRemain <= 0: 
            print("%s wins!" % topPlayer.getName())
            gameOver = True
            break
        playersInList = curGame.getPlayers(cardsDown=True)
        for player in playersInList:
            print("%s has %d cards down." % (player.getName(), sum(player.getTableData())) )
        print()
        #print("TEST:",playersInList)
        chosenPlayerName = input("Choose a player to take cards from: ")
        while not any(chosenPlayerName.upper() == x.getName().upper() for x in playersInList):
            print("Error: Player not found.")
            chosenPlayerName = input("Choose a player to take cards from: ")
        chosenPlayer = next((x for x in playersInList if x.getName() == chosenPlayerName), None)
        assert(chosenPlayer != None)
        chosenCard = chosenPlayer.popTable()
        cardsRemain -= 1
        if chosenCard == 'B':
            print("%s draws Black." % topPlayer.getName() )
            print("%s loses." % topPlayer.getName())
            gameOver = True
            break
        else:
            print("%s draws Red." % topPlayer.getName() )
            if cardsRemain > 0:
                print("%s must choose %d more cards" % (topPlayer.getName(), cardsRemain))

