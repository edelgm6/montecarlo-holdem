from django.db import models
from random import shuffle

class Stage:
    PREDEAL = 0
    PREFLOP = 1
    FLOP = 2
    TURN = 3
    RIVER = 4
    

class Game:
    def __init__(self, additional_players):
        self.deck = Deck()
        self.stage = Stage.PREDEAL
        self.players = []
        self.community = []
        
        self.players.append(Player(is_user=True))
        
        for player in range(additional_players):
            self.players.append(Player())
            
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
            
            self.stage = self.stage + 1
        
        elif self.stage < Stage.RIVER:
            self.deck.cards.pop()
            
            self.community.append(self.deck.cards.pop())
            self.stage = self.stage + 1
            
class Player:
    def __init__(self, is_user=False):
        self.hand = []
        self.is_user = is_user
        
class Deck:
    def __init__(self):
        suits = ['D', 'S', 'H', 'C']
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
        
        if name[0] not in ['D','S','H','C']:
            raise Exception('Name must start with D, S, H, or C, got ' + name)
            
        if len(name) == 3:
            number = name[-2:]
        else:
            number = name[-1]
            
        if int(number) not in range(2,15):
            raise Exception('Name must end with a number between 2-14, got ' + number)







"""
class PlayerManager(models.Manager):
    def create_player(self, name):
        player = self.create(name=name)
        stack = Stack.objects.create()
        player.hand = stack
        player.save()
        
        return player   

class Player(models.Model):
    name = models.CharField(max_length=100)
    hand = models.OneToOneField('Stack', on_delete=models.PROTECT, null=True)
    chips = models.PositiveIntegerField(default=0)
    #game = models.ForeignKey('Game', on_delete=models.CASCADE)
    
    objects = PlayerManager()

class StackManager(models.Manager):
    def create_deck(self):
        counter = 1
        deck = self.create(is_deck=True)
        for suit in Card.SUITS:
            for number in Card.NUMBERS:
                Card.objects.create(
                    suit=suit[0],
                    number=number[0],
                    stack=deck,
                    order=counter
                )
                counter = counter + 1
        
        return deck
            
class Stack(models.Model):
    is_deck = models.BooleanField(default=False)
    
    objects = StackManager()
    
    def deal(self):
        counter = 1
        players = Player.objects.all()
        for round in (1,2):
            for player in players:
                card = Card.objects.get(stack=self, order=counter)
                card.stack = player.hand
                card.order = round
                card.save()
                
                counter = counter + 1
                
    
    General algorithm for current view
    1) What is my best hand
    2) How many combinations of that hand are in a deck
    3) How many beating/tying combinations of that hand are in a deck
    4) What is the probability of each other player selecting a losing hand
    
    def get_pocket_win_probability(self):
        cards = Card.objects.filter(stack=self)
        #other_players_count = Player.objects.all().count() - 1
        other_players_count = 3
        
        numbers = []
        for card in cards:
            numbers.append(card.number)
            
        is_pair = False
        if numbers[0] == numbers[1]:
            is_pair = True
        
        if is_pair:
            pair_value = numbers[0]
            
            POCKET_COMBINATIONS = 52*51 / 2
            PAIR_COMBINATIONS = 52*3 / 2
            
            BEATING_PAIR_COMBINATIONS = (14 - pair_value) / 13 * PAIR_COMBINATIONS
            TYING_PAIR_COMBINATIONS = 1
            
            LOSING_POCKET_COMBINATIONS = POCKET_COMBINATIONS - 1 - (BEATING_PAIR_COMBINATIONS + TYING_PAIR_COMBINATIONS)
            
            #probability_win = LOSING_POCKET_COMBINATIONS / (POCKET_COMBINATIONS - 1)
            probability_win = 1
            for count in range(0, other_players_count):
                probability = (LOSING_POCKET_COMBINATIONS - count) / (POCKET_COMBINATIONS - 1 - count)
                probability_win = probability_win * probability
                
            print(probability_win)
            
            
               

class Card(models.Model):
    
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14
    
    HEARTS = 15
    SPADES = 16
    CLUBS = 17
    DIAMONDS = 18
    
    NUMBERS = (
        (TWO, '2'),
        (THREE, '3'),
        (FOUR, '4'),
        (FIVE, '5'),
        (SIX, '6'),
        (SEVEN, '7'),
        (EIGHT, '8'),
        (NINE, '9'),
        (TEN, '10'),
        (JACK, 'Jack'),
        (QUEEN, 'Queen'),
        (KING, 'King'),
        (ACE, 'Ace'),
    )
    
    SUITS = (
        (HEARTS, 'Hearts'),
        (SPADES, 'Spades'),
        (CLUBS, 'Clubs'),
        (DIAMONDS, 'Diamonds')
    )
    
    suit = models.PositiveIntegerField(choices=SUITS)
    number = models.PositiveIntegerField(choices=NUMBERS)
    stack = models.ForeignKey('Stack', on_delete=models.PROTECT)
    order = models.PositiveIntegerField()
    
    
"""