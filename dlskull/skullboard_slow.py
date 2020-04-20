import numpy as np
import copy
from dlskull.skulltypes import Player
from dlskull.skulltypes import GamePhase

__all__ = [
    'Board',
    'GameState',
    'Move',
]

class IllegalMoveError(Exception):
    pass

class Chart():
    def __init__(self, ordered=True):
        self.ordered = ordered
        if self.ordered:
            self._chart = {Player.anne : [], Player.bill: [], Player.charlie : []}
        else:
            self._chart = {Player.anne : set(), Player.bill: set(), Player.charlie : set()}
        self.chart_cards = 0

    #adds a card to "player's" pile
    def add(self, player, card):
        self.chart_cards += 1
        self._chart[player].append(card)

    #removes the top card placed by "player"
    def remove(self, player, value = None):
        if value = None:
            assert self.ordered = True
            self.chart_cards -= 1    
            return self._chart[player].pop()
        else
            assert self.ordered = False 
            self.chart_cards -= 1
            return self._chart[player].remove(value)

    def get_total_cards(self):
        return self.chart_cards

    def has_card(self, player, card):
        return self._chart[player].contains(card)

    def get_player_cards(self, player):
        return len(self._chart[player])

    def __eq__(self, other):
        return isinstance(other, Chart) and \
            self._chart == other._chart and \
            self.chart_cards == other.chart_cards

class Board():  
    def __init__(self, phase = GamePhase.placing):
        self._table = Chart(True)
        self._hands = Chart(False)
        self.players_bet = set()
        self.phase = phase
        self._bets = {}
        self.top_bet = (None,-1)

    def place_card(self, player, card):
        assert self.phase == GamePhase.placing
        assert self._hands.has_card(card)
        self._hands.remove(player,card) 
        self._table.add(player, card)

    def place_bet(self, player, bet):
        assert bet > self.top_bet[1]
        self.phase = GamePhase.betting
        self._bets[player] = bet
        self.top_bet = (player, bet)
        #the maximum value has been bet
        if bet >= _table.get_total_cards():
            self.phase.next
        #everyone has now bet
        elif len(self.players_bet) == 3:
            self.phase.next
        assert not self.player_bet.contains(player)
        self.players_bet.add(player)

    def choose_card(self, start_player, dest_player):
        assert self._table.get_player_cards(dest_player) > 0
        assert start_player != dest_player
        card = self._table.remove(dest_player)
        return card

    def has_card(self, player, card):
        return self._hands.has_card(player, card)

    def __eq__(self, other):
        return isinstance(other, Board) and \
            self._table == other._table and \
            self._hands == other._hands


class Move():
    def __init__(self, place=None, bet=None, choice=None, is_pass=False):
        assert (place is not None) ^ (bet is not None) ^ (choice is not None) ^ is_pass
        self.place = place
        self.bet = bet 
        self.choice = choice
        self.is_pass = is_pass

    @classmethod
    def place(cls, card): 
        return Move(place=card)

     @classmethod
    def bet(cls, amount): 
        return Move(bet=amount)

    @classmethod
    def choice(cls, player):
        return Move(choice=player)
    
    @classmethod
    def pass_bet(cls):  
        return Move(is_pass=True)



class GameState():
    def __init__(self, board, next_player, previous, move):
        self.board = board
        self.next_player = next_player
        self.previous_state = previous
        self.last_move = move

    def apply_move(self, move):  # <1>
        next_board = copy.deepcopy(self.board)
        if move.place:
            next_board.place_card(self.next_player, move.place)
        elif move.bet:
            next_board.place_bet(self.next_player, move.bet)
        else:
            next_board.choose_card(self.next_player, move.choice)

        return GameState(next_board, self.next_player.other, self, move)
    
    @classmethod
    def new_game(cls):
        board = Board(GamePhase.placing)
        return GameState(board, Player.anne, None, None)

    def is_valid_move(self,move):
        if self.is_over():
            return False
        if move.is_pass:
            return True
        if move.place is not None:
            return self.board.phase == GamePhase.placing and \
            self.board.has_card(self.next_player, move.place)
                
        if move.bet is not None:
            return self.board.phase == GamePhase.betting and \

        if move.choice is not None:
            return self.board.phase == GamePhase.choice and \
                self.board.top_bet[0] == self.next_player and \
                self.next_player != move.choice and \
                self.board._table.get_player_cards(move.choice) > 0 


assert self._table.get_player_cards(dest_player) > 0
        assert start_player != dest_player
#--------------------------------------------------------------------------------------
    @property
    def situation(self):
        return (self.next_player, self.board)

# tag::is_valid_move[]
    def is_valid_move(self, move):
        if self.is_over():
            return False
        if move.is_pass or move.is_resign:
            return True
        return (
            self.board.get(move.point) is None and
            not self.is_move_self_capture(self.next_player, move) and
            not self.does_move_violate_ko(self.next_player, move))
# end::is_valid_move[]

# tag::is_over[]
    def is_over(self):
        if self.last_move is None:
            return False
        if self.last_move.is_resign:
            return True
        second_last_move = self.previous_state.last_move
        if second_last_move is None:
            return False
        return self.last_move.is_pass and second_last_move.is_pass
# end::is_over[]

    def legal_moves(self):
        moves = []
        for row in range(1, self.board.num_rows + 1):
            for col in range(1, self.board.num_cols + 1):
                move = Move.play(Point(row, col))
                if self.is_valid_move(move):
                    moves.append(move)
        # These two moves are always legal.
        moves.append(Move.pass_turn())
        moves.append(Move.resign())

        return moves

    def winner(self):
        if not self.is_over():
            return None
        if self.last_move.is_resign:
            return self.next_player
        game_result = compute_game_result(self)
        return game_result