from django.db import models
from play.handsorter import HandSorter
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
            
    def set_player_hands(self):
        for player in self.players:
            player.best_hand = HandSorter.get_best_hand(player.hand + self.community)
            
    def get_winning_player(self):
        self.set_player_hands()
        
        hands = []
        for player in self.players:
            hands.append({'player': player, 'hand': player.best_hand})
        
        top_player = hands[0]
        for hand in hands[1:]:
            if hand['hand'][0].value == top_player['hand'][0].value:
                if hand['hand'][1] > top_player['hand'][1]:
                    top_player = hand
            
            
            
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
        suits = [s.value for s in Suit]
        numbers = [2,3,4,5,6,7,8,9,10,11,12,13,14]
        self.cards = []
        
        for suit in suits:
            for number in numbers:
                card = Card(name=suit + str(number))
                self.cards.append(card)
        
        shuffle(self.cards)
        
class Card:
    def __init__(self, name):
        self._name = name
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if len(name) not in range(2,4):
            raise Exception('Name must be two characters, got ' + name)
        
        if name[0] not in [Suit.DIAMOND, Suit.SPADE, Suit.HEART, Suit.CLUB]:
            raise Exception('Name must start with D, S, H, or C, got ' + name)
            
        if len(name) == 3:
            number = name[-2:]
        else:
            number = name[-1]
            
        if int(number) not in range(2,15):
            raise Exception('Name must end with a number between 2-14, got ' + number)