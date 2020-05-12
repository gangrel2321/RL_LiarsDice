import platform
import subprocess

import numpy as np
from dlskull import skulltypes

def print_table(player, board):
    print("%s's data:" % player)
    print("Hand: %s" % board.get_hand(player))
    print("Table: %s" % board.get_table())
    print("Phase: %s" % board.phase)

def print_move(player, move):
    if move.place:
        move_str = 'places ' + str(move.place)
    elif move.bet:
        move_str = 'bets ' + str(move.bet)
    elif move.choice:
        move_str = 'chooses ' + str(move.choice)
    else:
        move_str = 'passes'
    print('%s %s' % (player, move_str))
    print()

def clear_screen():
    # see https://stackoverflow.com/a/23075152/323316
    if platform.system() == "Windows":
        subprocess.Popen("cls", shell=True).communicate()
    else:  # Linux and Mac
        # the link uses print("\033c", end=""), but this is the original sequence given in the book.
        print(chr(27) + "[2J")
