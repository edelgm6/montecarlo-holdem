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
    
    
