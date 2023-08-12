import numpy as np
import copy
from dlskull.skulltypes import GamePhase
from dlskull.skulltypes import Card

__all__ = [
    'Board',
    'GameState',
    'Move',
]

DEBUG_MODE = True

class IllegalMoveError(Exception):
    pass

class Chart():
    def __init__(self, table=True, default_hand=True, players=None):
        start = []
        if default_hand:
            start = [Card.skull, Card.rose, Card.rose, Card.rose]
        self.ordered = table
        if self.ordered:
            self._chart = {p : [] for p in players}
            self.chart_cards = 0
        else:
            self._chart = {p : start[:] for p in players}
            self.chart_cards = len(start)*len(self._chart)

    #adds a card to "player's" pile
    def add(self, player, card):
        self.chart_cards += 1
        self._chart[player].append(card)

    #removes the top card placed by "player"
    def remove(self, player, value = None):
        if value == None:
            assert self.ordered == True
            self.chart_cards -= 1    
            return self._chart[player].pop()
        else:
            assert self.ordered == False 
            self.chart_cards -= 1
            return self._chart[player].remove(value)

    def get_player(self, player):
        return self._chart[player]

    def get_num_players(self):
        return len(self._chart)

    def get_total_cards(self):
        return self.chart_cards

    def has_card(self, player, card):
        return card in self._chart[player]

    def get_player_cards(self, player):
        return len(self._chart[player])

    def __eq__(self, other):
        return isinstance(other, Chart) and \
            self._chart == other._chart and \
            self.chart_cards == other.chart_cards

    def __str__(self):
        return str(self._chart)

class Board():  
    def __init__(self, players):
        self._table = Chart(table=True,players=players)
        self._hands = Chart(table=False,players=players)
        self.players_bet = set()
        self.phase = GamePhase.placing
        self._bets = {}
        self.chosen_cards = 0
        self.last_chosen = None
        self.top_bet = (None,-1)

    def get_table(self):
        return self._table
    
    def get_hand(self,player):
        return self._hands.get_player(player)

    def place_card(self, player, card):
        assert self.phase == GamePhase.placing
        assert self._hands.has_card(player, card)
        self._hands.remove(player,card) 
        self._table.add(player, card)

    def place_bet(self, player, bet):
        if self.phase == GamePhase.choice:
            return
        assert bet > self.top_bet[1] or bet == -1 #exceed max bet or pass
        assert not player in self.players_bet
        self.players_bet.add(player)

        self.phase = GamePhase.betting
        self._bets[player] = bet
        if bet > self.top_bet[1]:
            self.top_bet = (player, bet)
        #the maximum value has been bet
        if bet >= self._table.get_total_cards():
            self.phase = self.phase.next
        #everyone has now bet
        elif len(self.players_bet) == self._table.get_num_players():
            self.phase = self.phase.next
        
    def choose_card(self, start_player, dest_player):
        assert self._table.get_player_cards(dest_player) > 0
        assert start_player != dest_player
        card = self._table.remove(dest_player)
        self.chosen_cards += 1
        self.last_chosen = card
        return card

    def all_cards_chosen(self):
        assert self.phase == GamePhase.choice
        return self.chosen_cards == self.top_bet


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
        self.is_choice = (choice is not None)

    @classmethod
    def pass_bet(cls):  
        return Move(is_pass=True)


class GameState():
    def __init__(self, board, cur_player, previous, move, players=None):
        assert (type(players) is list or players is None) 
        assert not (players is None and previous is None)
        self.board = board
        if players is None:
            self.players = previous.players
        else: 
            self.players = players
        assert len(self.players) > 0
        self._cur_player_index = cur_player
        self.previous_state = previous
        self.last_move = move

    @classmethod
    def new_game(cls, bots):
        board = Board(bots)
        return GameState(board, 0, None, None, bots)
    
    def get_cur_player(self):
        return self.players[self._cur_player_index]

    # get player after self.get_cur_player()
    def get_next_player(self,use_index=False): # TODO: replace with linked list? 
        if self._cur_player_index + 1 < len(self.players):
            index = self._cur_player_index + 1 
        else:
            index = 0
        if use_index:
            return index
        return self.players[index]

    def apply_move(self, move):
        next_board = copy.deepcopy(self.board)
        if move.place:
            next_board.place_card(self.get_cur_player(), move.place)
        elif move.bet:
            next_board.place_bet(self.get_cur_player(), move.bet)
        elif move.choice:
            next_board.choose_card(self.get_cur_player(), move.choice)
        elif move.is_pass:
            next_board.place_bet(self.get_cur_player(), -1)

        return GameState(next_board, self.get_next_player(use_index=True), self, move)

    def is_over(self):
        if self.last_move is None:
            return False
        if self.last_move.is_choice and self.board.all_cards_chosen():
            print("%s wins!" % self.get_cur_player()) # TODO: replace with win status
            return True
        #if the card drawn is black then the game ends
        if DEBUG_MODE and self.last_move.is_choice:
            print("Final Move:", self.last_move.choice)
            print("Final Table:", self.board.get_table()._chart)
            print("Final Chosen Cards:", self.board.chosen_cards)
        # TODO : Fix this, the game shouldn't end when you draw a skull... 
        if self.last_move.is_choice and \
            ( (self.board.last_chosen == Card.skull ) or \
            len(self.board.get_table().get_player(self.last_move.choice)) == 0 ): 
            return True
        return False

    def is_valid_move(self,move):
        if self.is_over():
            return False
        if move.is_pass and self.board.phase != GamePhase.placing:
            return True
        if move.place is not None:
            return self.board.phase == GamePhase.placing and \
                self.board.has_card(self.get_cur_player(), move.place)               
        if move.bet is not None:
            return (self.board.phase == GamePhase.betting and \
                move.bet > 0 and \
                move.bet <= self.board._table.get_total_cards() and \
                move.bet > self.board.top_bet[1]) or \
                (self.board.phase == GamePhase.placing and \
                move.bet > 0 and \
                self.board._table.get_total_cards() >= len(self.players) and \
                move.bet <= self.board._table.get_total_cards() )
        if move.choice is not None:
            return self.board.phase == GamePhase.choice and \
                self.board.top_bet[0] == self.get_cur_player() and \
                self.get_cur_player() != move.choice and \
                self.board._table.get_player_cards(move.choice) > 0      
        return False

    def legal_moves(self):
        moves = []
        #place
        for card_type in Card:
            move = Move(place=card_type)
            if self.is_valid_move(move):
                moves.append(move)
        #bet
        for i in range(1,self.board._table.get_total_cards() + 1):
            move = Move(bet=i)
            if self.is_valid_move(move):
                moves.append(move)
        #pass during betting
        if self.is_valid_move(Move.pass_bet()) and self.board.phase == GamePhase.betting:
            moves.append(Move.pass_bet())
        #choice
        for user in self.players:
            move = Move(choice=user)
            if self.is_valid_move(move):
                moves.append(move)
        print("Possible Moves:", len(moves))
        return moves