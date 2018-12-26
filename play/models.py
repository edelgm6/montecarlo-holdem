from django.db import models
from play.handsorter import HandSorter
from play.tiebreaker import TieBreaker
from play.rules import Suit, Hand, Stage
from random import shuffle
from operator import itemgetter

class Game:
    def __init__(self, additional_players=1):
        self.deck = Deck()
        self.stage = Stage.PREDEAL
        self.players = []
        self.community = []
        
        self.players.append(Player(game=self, is_user=True))
        
        for player in range(additional_players):
            self.players.append(Player(game=self))
            
    def deal(self):
        if self.stage == Stage.PREDEAL:
            for round in range(2):
                for player in self.players:
                    card = self.deck.cards.pop()
                    player.hand.append(card)
                    
            self.stage = Stage.PREFLOP
        
        elif self.stage == Stage.PREFLOP:
            #burn a card
            self.deck.cards.pop()
            
            flop = self.deck.cards[-3:]
            self.community = flop
            self.deck.cards = self.deck.cards[:-3]
            
            self.stage = Stage(self.stage.value + 1)
        
        elif self.stage.value < Stage.RIVER.value:
            self.deck.cards.pop()
            
            self.community.append(self.deck.cards.pop())
            self.stage = Stage(self.stage.value + 1)
     
    
    #Get rid of this and fold into the get_winning_player method
    def set_player_hands(self):
        for player in self.players:
            player.best_hand = HandSorter.get_best_hand(player.hand + self.community)
            
    def get_winning_player(self):
        
        contenders = [self.players[0]]
        for player in self.players[1:]:
            top_score = contenders[0].best_hand['score'].value
            player_score = player.best_hand['score'].value
            if player_score == top_score:
                contenders.append(player)
            elif player_score < top_score:
                contenders = [player]
          
        if len(contenders) > 1:
            winners = TieBreaker.break_tie(contenders)
        else:
            winners = contenders
            
        return winners
                
            
            
            
    
    """
    TODO:
    1. Make set hands method set the name of the hand and the cards themselves
    2. Compare each player's hand to see which one wins
    3. If there is a tie, pass each player's cards to a tie-breaker method
    
    def get_winning_player(self):
        self.set_player_hands()
        
        top_hands = [self.players[0].best_hand]
        top_hand = self.players.best_hand
        for player in self.players[1::
    """        
            
            
            
class Player:
    def __init__(self, game, is_user=False):
        self.hand = []
        self.is_user = is_user
        #self.game = game
    
    #def get_total_hand(self):
    #    total_hand = []
        
    #    return self.hand + self.game.community
        
        
class Deck:
    def __init__(self):
        #suits = [Suit.DIAMOND, Suit.SPADE, Suit.HEART, Suit.CLUB]
        suits = [s for s in Suit]
        numbers = [2,3,4,5,6,7,8,9,10,11,12,13,14]
        self.cards = []
        
        for suit in suits:
            for number in numbers:
                card = Card(suit=suit, number=number)
                self.cards.append(card)
        
        shuffle(self.cards)
        
class Card:
    def __init__(self, suit, number):
        self._suit = suit
        self._number = number
    
    @property
    def suit(self):
        return self._suit
    
    @suit.setter
    def suit(self, suit):
        if suit not in [suit for suit in Suit]:
            raise Exception('Suit must be value in Suit enum')
                                   
    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, number):
        if number not in range(2,15):
            raise Exception('Number must be between 2-14, got ' + number)