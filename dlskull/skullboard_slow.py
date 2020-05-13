import numpy as np
import copy
from dlskull.skulltypes import Player
from dlskull.skulltypes import GamePhase
from dlskull.skulltypes import Card
from dlskull.scoring import compute_game_result

__all__ = [
    'Board',
    'GameState',
    'Move',
]

NUM_PLAYERS = 3
DEBUG_MODE = False

class Chart():
    def __init__(self, empty=True, default_hand=True):
        start = []
        if default_hand:
            start = [Card.skull, Card.rose, Card.rose, Card.rose]
        self.is_empty = empty
        if self.is_empty:
            self._chart = {Player.anne : [], Player.bill: [], Player.charlie : []}
            self.chart_cards = 0
        else:
            self._chart = {Player.anne : start[:], Player.bill: start[:], Player.charlie : start[:]}
            self.chart_cards = sum([len(x) for x in self._chart.values()]) 

    #adds a card to "player's" pile
    def add(self, player, card):
        self.chart_cards += 1
        self._chart[player].append(card)

    #removes the top card placed by "player"
    def remove(self, player, value = None):
        if value == None:
            assert self.is_empty == True
            self.chart_cards -= 1    
            return self._chart[player].pop()
        else:
            assert self.is_empty == False 
            self.chart_cards -= 1
            return self._chart[player].remove(value)

    def get_player(self, player):
        return self._chart[player]

    def get_total_cards(self):
        return self.chart_cards

    def has_card(self, player, card):
        return card in self._chart[player]

    def get_player_cards(self, player):
        return len(self._chart[player])

    def update_chart_cards():
        self.chart_cards = sum([len(x) for x in self._chart.values()]) 

    def __eq__(self, other):
        return isinstance(other, Chart) and \
            self._chart == other._chart and \
            self.chart_cards == other.chart_cards

    def __str__(self):
        return str(self._chart)

class Board():  
    def __init__(self, phase = GamePhase.placing):
        self._table = Chart(empty=True)
        self._hands = Chart(empty=False)
        self._scores = Chart(empty=True) #list of rounds won
        self.players_bet = set()
        self.phase = phase
        self._bets = {}
        self.chosen_cards = 0
        self.last_chosen = None
        self.top_bet = (None,-1)
        self.round = 0

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
        elif len(self.players_bet) == NUM_PLAYERS:
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

    def round_reset(self,player,win=True):
        # move table cards back to hands
        # if loser not none then remove one of their cards
        self.round += 1
        for pair in self._table._chart.items()
            self._hand._chart[pair[0]].extend(pair[1])
        self._table = Chart(empty=True)
        if win:
            self._scores[player].append(self.round-1)
            return
        else:
            old_hand = self._table._chart[player]
            old_hand.remove(random.choice(old_hand))

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
    def __init__(self, board, next_player, previous, move):
        self.board = board
        self.next_player = next_player
        self.previous_state = previous
        self.last_move = move

    def apply_move(self, move):
        next_board = copy.deepcopy(self.board)
        if move.place:
            next_board.place_card(self.next_player, move.place)
        elif move.bet:
            next_board.place_bet(self.next_player, move.bet)
        elif move.choice:
            next_board.choose_card(self.next_player, move.choice)
        elif move.is_pass:
            next_board.place_bet(self.next_player, -1)

        return GameState(next_board, self.next_player.other, self, move)
    
    @classmethod
    def new_game(cls):
        board = Board(GamePhase.placing)
        return GameState(board, Player.anne, None, None)

    def is_valid_move(self,move):

        if self.is_round_over():
            self.board.round_reset()
            return False

        if move.is_pass and self.board.phase != GamePhase.placing:
            return True

        if move.place is not None:
            return self.board.phase == GamePhase.placing and \
                self.board.has_card(self.next_player, move.place)
                
        if move.bet is not None:
            return (self.board.phase == GamePhase.betting and \
                move.bet > 0 and \
                move.bet <= self.board._table.get_total_cards() and \
                move.bet > self.board.top_bet[1]) or \
                (self.board.phase == GamePhase.placing and \
                move.bet > 0 and \
                self.board._table.get_total_cards() >= NUM_PLAYERS and \
                move.bet <= self.board._table.get_total_cards() )

        if move.choice is not None:
            return self.board.phase == GamePhase.choice and \
                self.board.top_bet[0] == self.next_player and \
                self.next_player != move.choice and \
                self.board._table.get_player_cards(move.choice) > 0 
        
        return False

    def is_round_over(self):
        if self.last_move is None:
            return False
        if self.last_move.is_choice and self.board.all_cards_chosen():
            return True
        #if the card drawn is black then the game ends
        if DEBUG_MODE and self.last_move.is_choice:
            print("Testing1:", self.last_move.choice)
            print("Testing:", self.board.get_table()._chart)
            print("Chosen cards:", self.board.chosen_cards)
        if self.last_move.is_choice and \
            (self.board.last_chosen == Card.skull or \
            len(self.board.get_table().get_player(self.last_move.choice)) == 0 ): 
            return True
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
        for user in Player:
            move = Move(choice=user)
            if self.is_valid_move(move):
                moves.append(move)
        print("Possible Moves:", len(moves))
        return moves