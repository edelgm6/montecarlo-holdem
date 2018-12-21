from django.test import TestCase
from play.models import Card, Stack, Player

class StackTestCase(TestCase):
    def test_is_deck_creates_fifty_two_cards(self):
        
        deck = Stack.objects.create_deck()
        
        cards = Card.objects.all()
        
        self.assertEqual(cards.count(), 52)
        self.assertTrue(deck.is_deck)
        
        last_card = Card.objects.get(order=52)
        first_card = Card.objects.get(order=1)
        
    def test_not_deck_creates_no_cards(self):
        
        deck = Stack.objects.create()
        
        cards = Card.objects.all()
        
        self.assertEqual(cards.count(), 0)
        
    def test_deal_removes_cards_and_adds_to_player_stacks(self):
        garrett = Player.objects.create_player(name='Garrett')
        woodhaven = Player.objects.create_player(name='Woodhaven')
        
        deck = Stack.objects.create_deck()
        
        deck.deal()
        
        deck_cards = Card.objects.filter(stack=deck)
        self.assertEqual(deck_cards.count(), 48)
        
        garrett_hand = Card.objects.filter(stack__player=garrett)
        self.assertEqual(garrett_hand.count(), 2)
        
        woodhaven_hand = Card.objects.filter(stack__player=woodhaven)
        self.assertEqual(woodhaven_hand.count(), 2)
        
    def test_pocket_win_probability_returns_correct_amount(self):
        hand = Stack.objects.create()
        five_clubs = Card.objects.create(suit=Card.CLUBS, number=Card.FIVE, stack=hand, order=1)
        five_hearts = Card.objects.create(suit=Card.HEARTS, number=Card.FIVE, stack=hand, order=2)
        
        hand.get_pocket_win_probability()
        
        
class PlayerTestCase(TestCase):
    
    def test_can_create_player(self):
        player = Player.objects.create(name='Garrett')
        self.assertEqual(player.chips, 0)
        