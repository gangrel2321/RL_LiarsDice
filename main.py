import SkullsGame as sg
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

def betPhase():
    pass

if __name__ == "__main__":
    #Start Game
    cardColor = {"RED": True, "BLACK":False, True:"RED", False:"BLACK"}
    numPlayers = int(input("Enter the number of players: "))
    playersList = []
    print("Enter the player names (Separated by ENTER):")
    for i in range(numPlayers):
        playersList.append(input())
    curGame = sg(playersList)
    roundCount = 0
    while True:
        roundCount += 1
        print("Round %d\n" % roundCount)
        topBet = 0
        topPlayer = -1
        for i in range(len(playersList)):
            curPlay = curGame.players[i]
            print("Current Player: %s\n" % curPlay )
            print("[Current Hand - %s]\n" % str( curPlay.getHand() ) )
            if curGame.getPhase() == "PLACING": #placing cards phase
                decision = input("Would you like to start betting? (y/n): ").toUpper()
                while ((decision != "N") and (decision != "Y")):
                    decision = input("ERROR: Enter \"y\" or \"n\": ").toUpper()
                if decision == "N":
                    card = input("Play a card (RED, BLACK): ").toUpper()
                    while ((card != "RED") and (card != "BLACK")):
                        card = input("ERROR: Enter \"RED\" or \"BLACK\": ").toUpper()
                    if not curPlay.playCard(card):
                        print("ERROR: You do not have enough \"%s\"." % card)
                        card = cardColor[not cardColor[card]]
                    print("%s played %s." % (curPlay.getName(), card))
                else:
                    print("[Played Cards - %s]\n" % str( curPlay.getTable() ))
                    topBet = int(input("Enter Bet:"))
                    topPlayer = i
                    #betPhase()
            else: #betting phase
                #betPhase()
                print("[Played Cards - %s]\n" % str( curPlay.getTable() ))
                print("Current Highest Bet:", topBet)
                curBet = input("Enter Bet (-1 = pass):")
                if curBet > topBet:
                    topBet = curBet
                    topPlayer= i
                
            print("Clearing Screen For Next Player ...")
            sleep(1)
            clear()
            sleep(1)
        
        print("Player with Highest Bet: %s" % curGame.players[topPlayer].getName())
        print()