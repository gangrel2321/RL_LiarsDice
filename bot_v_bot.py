from __future__ import print_function
# tag::bot_vs_bot[]
from dlskull import agent
from dlskull import skullboard_slow
from dlskull import skulltypes
from dlskull.utils import print_table, print_move, clear_screen
import time


def main():
    bots = {
        skulltypes.Player.anne: agent.naive.RandomBot(),
        skulltypes.Player.bill: agent.naive.RandomBot(),
        skulltypes.Player.charlie: agent.naive.RandomBot()
    }
    game = skullboard_slow.GameState.new_game()
    while not game.is_over():
        time.sleep(1) 
        #clear_screen() 
        bot_move = bots[game.next_player].select_move(game)
        print_table(game.next_player, game.board)
        print_move(game.next_player, bot_move)
        game = game.apply_move(bot_move)
    

if __name__ == '__main__':
    main()
