from __future__ import print_function
# tag::bot_vs_bot[]
from dlskull import agent
from dlskull import skullboard_slow
from dlskull import skulltypes
from dlskull.utils import print_table, print_move, clear_screen
import time


def main():
    bots = {
        "anne": agent.naive.RandomBot(),
        "bill": agent.naive.RandomBot(),
        "charlie": agent.naive.RandomBot()
    }
    players = list(bots.keys())
    game = skullboard_slow.GameState.new_game(players)
    while not game.is_over():
        time.sleep(1) 
        #clear_screen() 
        print(game.players)
        bot_move = bots[game.get_next_player()].select_move(game)
        print_table(game.get_next_player(), game.board)
        print_move(game.get_next_player(), bot_move)
        game = game.apply_move(bot_move)
    

if __name__ == '__main__':
    main()
