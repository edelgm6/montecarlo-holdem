from django.test import TestCase
from play.models import Game, Deck, Card, Stage, Suit, Hand
from play.handsorter import HandSorter

class HandSorterTestCase(TestCase):
    
    def test_returns_best_hand(self):
        hand = []
            
        hand.append(Card(suit=Suit.CLUB, number = 2))
        hand.append(Card(suit=Suit.CLUB, number = 2))
        hand.append(Card(suit=Suit.DIAMOND, number = 2))
        hand.append(Card(suit=Suit.SPADE, number = 2))
        hand.append(Card(suit=Suit.DIAMOND, number = 3))
        hand.append(Card(suit=Suit.SPADE, number = 3))
        hand.append(Card(suit=Suit.DIAMOND, number = 3))
        
        hand = HandSorter.get_best_hand(hand)
        
        self.assertEqual(hand, (Hand.FOUR_OF_A_KIND, 2))
        
        hand = []
            
        hand.append(Card(suit=Suit.CLUB, number = 2))
        hand.append(Card(suit=Suit.CLUB, number = 3))
        hand.append(Card(suit=Suit.CLUB, number = 4))
        hand.append(Card(suit=Suit.CLUB, number = 5))
        hand.append(Card(suit=Suit.CLUB, number = 6))
        hand.append(Card(suit=Suit.SPADE, number = 3))
        hand.append(Card(suit=Suit.DIAMOND, number = 3))
        
        hand = HandSorter.get_best_hand(hand)
        
        self.assertEqual(hand, (Hand.STRAIGHT_FLUSH, 6))
        
        hand = []
            
        hand.append(Card(suit=Suit.CLUB, number = 2))
        hand.append(Card(suit=Suit.CLUB, number = 2))
        hand.append(Card(suit=Suit.CLUB, number = 3))
        hand.append(Card(suit=Suit.CLUB, number = 3))
        hand.append(Card(suit=Suit.CLUB, number = 7))
        hand.append(Card(suit=Suit.SPADE, number = 7))
        hand.append(Card(suit=Suit.DIAMOND, number = 7))
        
        hand = HandSorter.get_best_hand(hand)
        
        self.assertEqual(hand, (Hand.FULL_HOUSE, (7, 3)))
    
    def test_is_flush_ids_a_flush(self):
        hand = []
        for number in range(2, 8):
            card = Card(suit=Suit.DIAMOND, number=number)
            hand.append(card)
            
        hand.append(Card(suit=Suit.CLUB, number=2))
        hand.append(Card(suit=Suit.CLUB, number=3))
        
        is_flush = HandSorter.is_flush(hand)

        self.assertEqual(is_flush, 7)
        
    def test_is_flush_returns_false_if_no_flush(self):
        hand = []
            
        hand.append(Card(suit=Suit.CLUB, number=2))
        hand.append(Card(suit=Suit.CLUB, number=3))
        
        is_flush = HandSorter.is_flush(hand)

        self.assertFalse(is_flush)
    
    def test_is_straight_returns_high_card(self):
        hand = []
        for number in range(2, 8):
            card = Card(suit=Suit.DIAMOND, number=number)
            hand.append(card)
            
        hand.append(Card(suit=Suit.CLUB, number=2))
        hand.append(Card(suit=Suit.CLUB, number=3))
        
        is_straight = HandSorter.is_straight(hand)
        
        self.assertEqual(is_straight, 7)
        
    def test_isnt_straight_returns_false(self):
        hand = []
            
        hand.append(Card(suit=Suit.CLUB, number=2))
        hand.append(Card(suit=Suit.CLUB, number=3))
        hand.append(Card(suit=Suit.DIAMOND, number=5))
        hand.append(Card(suit=Suit.SPADE, number=4))
        hand.append(Card(suit=Suit.DIAMOND, number=3))
        hand.append(Card(suit=Suit.SPADE, number=10))
        hand.append(Card(suit=Suit.DIAMOND, number=14))
        
        is_straight = HandSorter.is_straight(hand)
        
        self.assertFalse(is_straight)
        
    def test_is_four_of_a_kind_returns_number(self):
        hand = []
            
        hand.append(Card(suit=Suit.CLUB, number=2))
        hand.append(Card(suit=Suit.DIAMOND, number=2))
        hand.append(Card(suit=Suit.SPADE, number=2))
        hand.append(Card(suit=Suit.HEART, number=2))
        hand.append(Card(suit=Suit.DIAMOND, number=3))
        hand.append(Card(suit=Suit.SPADE, number=10))
        hand.append(Card(suit=Suit.DIAMOND, number=14))
        
        is_four_of_a_kind = HandSorter.is_four_of_a_kind(hand)
        
        self.assertEqual(is_four_of_a_kind, 2)
        
    def test_isnt_four_of_a_kind_returns_false(self):
        hand = []
         
            
        hand.append(Card(suit=Suit.CLUB, number=2))
        hand.append(Card(suit=Suit.DIAMOND, number=6))
        hand.append(Card(suit=Suit.SPADE, number=2))
        hand.append(Card(suit=Suit.HEART, number=2))
        hand.append(Card(suit=Suit.DIAMOND, number=3))
        hand.append(Card(suit=Suit.SPADE, number=10))
        hand.append(Card(suit=Suit.DIAMOND, number=14))            
        
        is_four_of_a_kind = HandSorter.is_four_of_a_kind(hand)
        
        self.assertFalse(is_four_of_a_kind)
        
    def test_is_three_of_a_kind_returns_high_card(self):
        hand = []
         
        hand.append(Card(suit=Suit.CLUB, number=2))
        hand.append(Card(suit=Suit.DIAMOND, number=2))
        hand.append(Card(suit=Suit.SPADE, number=2))
        hand.append(Card(suit=Suit.HEART, number=3))
        hand.append(Card(suit=Suit.DIAMOND, number=3))
        hand.append(Card(suit=Suit.SPADE, number=3))
        hand.append(Card(suit=Suit.DIAMOND, number=14))  
        
        is_three_of_a_kind = HandSorter.is_three_of_a_kind(hand)
        
        self.assertEqual(is_three_of_a_kind, 3)
        
    def test_isnt_three_of_a_kind_returns_false(self):
        hand = []
            
        hand.append(Card(suit=Suit.CLUB, number=2))
        hand.append(Card(suit=Suit.DIAMOND, number=3))
        
        hand.append(Card(suit=Suit.SPADE, number=4))
        hand.append(Card(suit=Suit.HEART, number=5))
        hand.append(Card(suit=Suit.DIAMOND, number=6))
        hand.append(Card(suit=Suit.SPADE, number=7))
        hand.append(Card(suit=Suit.DIAMOND, number=8))  
        
        is_three_of_a_kind = HandSorter.is_three_of_a_kind(hand)
        
        self.assertFalse(is_three_of_a_kind)
        
        
    def test_is_pair_returns_value(self):
        hand = []
            
        hand.append(Card(suit=Suit.CLUB, number=2))
        hand.append(Card(suit=Suit.DIAMOND, number=2))
        hand.append(Card(suit=Suit.SPADE, number=3))
        hand.append(Card(suit=Suit.HEART, number=4))
        hand.append(Card(suit=Suit.DIAMOND, number=5))
        hand.append(Card(suit=Suit.SPADE, number=6))
        hand.append(Card(suit=Suit.DIAMOND, number=7))  
        
        is_pair = HandSorter.is_pair(hand)
        
        self.assertEqual(is_pair, 2) 
        
    def test_isnt_pair_returns_false(self):
        hand = []
          
        hand.append(Card(suit=Suit.CLUB, number=14))
        hand.append(Card(suit=Suit.DIAMOND, number=2))
        hand.append(Card(suit=Suit.SPADE, number=3))
        hand.append(Card(suit=Suit.HEART, number=4))
        hand.append(Card(suit=Suit.DIAMOND, number=5))
        hand.append(Card(suit=Suit.SPADE, number=6))
        hand.append(Card(suit=Suit.DIAMOND, number=7))  

        is_pair = HandSorter.is_pair(hand)
        
        self.assertFalse(is_pair) 
        
    def test_is_full_house_returns_tuple(self):        
        hand = []
            
        hand.append(Card(suit=Suit.CLUB, number=2))
        hand.append(Card(suit=Suit.DIAMOND, number=2))
        hand.append(Card(suit=Suit.SPADE, number=3))
        hand.append(Card(suit=Suit.HEART, number=3))
        hand.append(Card(suit=Suit.DIAMOND, number=3))
        hand.append(Card(suit=Suit.SPADE, number=6))
        hand.append(Card(suit=Suit.DIAMOND, number=6))  
        
        is_full_house = HandSorter.is_full_house(hand)
        
        self.assertEqual(is_full_house, (3,6))
        
    def test_is_two_pair_returns_tuple(self):
        hand = []
            
        hand.append(Card(suit=Suit.CLUB, number=2))
        hand.append(Card(suit=Suit.DIAMOND, number=2))
        hand.append(Card(suit=Suit.SPADE, number=3))
        hand.append(Card(suit=Suit.HEART, number=3))
        hand.append(Card(suit=Suit.DIAMOND, number=7))
        hand.append(Card(suit=Suit.SPADE, number=9))
        hand.append(Card(suit=Suit.DIAMOND, number=9))  
        
        is_two_pair = HandSorter.is_two_pair(hand)
        
        self.assertEqual(is_two_pair, (9,3))
        
    def test_isnt_two_pair_returns_false(self):
        hand = []
            
        hand.append(Card(suit=Suit.CLUB, number=2))
        hand.append(Card(suit=Suit.DIAMOND, number=2))
        hand.append(Card(suit=Suit.SPADE, number=3))
        hand.append(Card(suit=Suit.HEART, number=4))
        hand.append(Card(suit=Suit.DIAMOND, number=7))
        hand.append(Card(suit=Suit.SPADE, number=10))
        hand.append(Card(suit=Suit.DIAMOND, number=11))  

        is_two_pair = HandSorter.is_two_pair(hand)
        
        self.assertFalse(is_two_pair)
        
    def test_get_high_card_returns_highest(self):        
        hand = []
            
            
        hand.append(Card(suit=Suit.CLUB, number=13))
        hand.append(Card(suit=Suit.DIAMOND, number=2))
        hand.append(Card(suit=Suit.SPADE, number=3))
        hand.append(Card(suit=Suit.HEART, number=4))
        hand.append(Card(suit=Suit.DIAMOND, number=7))
        hand.append(Card(suit=Suit.SPADE, number=10))
        hand.append(Card(suit=Suit.DIAMOND, number=11)) 
        
        high_card = HandSorter.get_high_card(hand)
        
        self.assertEqual(high_card, 13)
        
    def test_is_straight_flush_returns_high_card(self):
        hand = []
            
        hand.append(Card(suit=Suit.CLUB, number=2))
        hand.append(Card(suit=Suit.CLUB, number=3))
        hand.append(Card(suit=Suit.CLUB, number=4))
        hand.append(Card(suit=Suit.CLUB, number=5))
        hand.append(Card(suit=Suit.CLUB, number=6))
        hand.append(Card(suit=Suit.SPADE, number=10))
        hand.append(Card(suit=Suit.DIAMOND, number=11)) 
        
        is_straight_flush = HandSorter.is_straight_flush(hand)
        
        self.assertEqual(is_straight_flush, 6) 
        
    def test_isnt_straight_flush_returns_false(self):
        hand = []
            
        hand.append(Card(suit=Suit.CLUB, number=2))
        hand.append(Card(suit=Suit.CLUB, number=3))
        hand.append(Card(suit=Suit.DIAMOND, number=4))
        hand.append(Card(suit=Suit.CLUB, number=5))
        hand.append(Card(suit=Suit.CLUB, number=6))
        hand.append(Card(suit=Suit.SPADE, number=10))
        hand.append(Card(suit=Suit.DIAMOND, number=11)) 

        is_straight_flush = HandSorter.is_straight_flush(hand)
        
        self.assertFalse(is_straight_flush)