from django.db import models

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
    
    """Need to change this to players in game"""
    """Need to make Deck a subset of Stack"""
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
                
    
    """General algorithm for current view
    1) What is my best hand
    2) How many combinations of that hand are in a deck
    3) How many beating/tying combinations of that hand are in a deck
    4) What is the probability of each other player selecting a losing hand"""
    
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
    
    
