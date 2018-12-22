from django.db import models
from random import shuffle
from enum import Enum
import weakref

class Stage(Enum):
    PREDEAL = 0
    PREFLOP = 1
    FLOP = 2
    TURN = 3
    RIVER = 4
    
class Suit(Enum):
    HEART = 'H'
    SPADE = 'S'
    CLUB = 'C'
    DIAMOND = 'D'
    

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
            
class Player:
    def __init__(self, game, is_user=False):
        self.hand = []
        self.is_user = is_user
        self.game = game
    
    def get_total_hand(self):
        total_hand = []
        
        return self.hand + self.game.community
    
    def get_suit(self, card):
        return card.name[0]
    
    def get_number(self, card):
        chars = len(card.name)
        return int(card.name[-(chars - 1):])
    
    def get_stripped_hand(self, hand, card_number_to_remove):
        hand_without_cards = [card for card in hand if self.get_number(card) != card_number_to_remove]
        
        return hand_without_cards
    
    def get_hand_numbers(self, hand):
        numbers = []
        for card in hand:
            numbers.append(self.get_number(card))
            
        return numbers
    
    
    def is_flush(self, hand):
        suits = []
        for card in hand:
            suits.append(self.get_suit(card))
            
        for suit in [s.value for s in Suit]:
            if suits.count(suit) >= 5:
                high_card = 0
                
                for card in hand:
                    if self.get_suit(card) == suit:
                        number = self.get_number(card)
                        if number > high_card:
                            high_card = number
                
                return high_card
        
        return False
    
    def is_straight(self, hand):
        numbers = self.get_hand_numbers(hand)
        
        numbers.sort(reverse=True)
        for number in numbers[:3]:
            if (number - 1 in numbers
                and number - 2 in numbers
                and number - 3 in numbers
                and number - 4 in numbers):
                    return number
        
        return False
    
    def is_four_of_a_kind(self, hand):
        numbers = self.get_hand_numbers(hand)
            
        for number in numbers[:4]:
            if numbers.count(number) == 4:
                return number
            
        return False
    
    def is_three_of_a_kind(self, hand):
        numbers = self.get_hand_numbers(hand)
            
        numbers.sort(reverse=True)
        
        for number in numbers[:5]:
            if numbers.count(number) == 3:
                return number
            
        return False
    
    def is_pair(self, hand):
        numbers = self.get_hand_numbers(hand)
            
        numbers.sort(reverse=True)
        
        for number in numbers[:6]:
            if numbers.count(number) == 2:
                return number
            
        return False
    
    def is_two_pair(self, hand):
        high_pair_value = self.is_pair(hand)
        
        if high_pair_value:
            hand_without_pair = self.get_stripped_hand(hand, high_pair_value)
            low_pair_value = self.is_pair(hand_without_pair)
            
            if low_pair_value:
                return (high_pair_value, low_pair_value)
            
        return False
    
    def is_full_house(self, hand):
        three_of_a_kind_value = self.is_three_of_a_kind(hand)
        
        if three_of_a_kind_value:
            hand_without_three_cards = self.get_stripped_hand(hand, three_of_a_kind_value)
            
            two_of_a_kind_value = self.is_pair(hand_without_three_cards)
            if two_of_a_kind_value:
                return (three_of_a_kind_value, two_of_a_kind_value)
            
        return False
    
    def get_high_card(self, hand):
        numbers = self.get_hand_numbers(hand)
            
        numbers.sort()
        
        return numbers.pop()
        
        
        
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