from django.test import TestCase
from play.models import Game, Deck, Card, Stage, Suit, Hand
from play.handsorter import HandSorter

class HandSorterTestCase(TestCase):
    
    """
    TODO
    Test that the corect Hand enum is returned in each test
    """
    
    def test_sort_cards_sorts_high_to_low(self):
        hand = []
            
        hand.append(Card(suit=Suit.CLUB, number = 2))
        hand.append(Card(suit=Suit.CLUB, number = 14))
        hand.append(Card(suit=Suit.DIAMOND, number = 5))
        hand.append(Card(suit=Suit.SPADE, number = 3))
        hand.append(Card(suit=Suit.DIAMOND, number = 11))
        hand.append(Card(suit=Suit.SPADE, number = 10))
        hand.append(Card(suit=Suit.DIAMOND, number = 11)) 
            
        ordered_hand = HandSorter.sort_cards(hand)
        
        self.assertEqual(ordered_hand[0].number, 14)
        self.assertEqual(ordered_hand[6].number, 2)
    
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
        
        self.assertEqual(hand['score'], Hand.STRAIGHT_FLUSH)
        
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

        self.assertEqual(is_flush['score'], Hand.FLUSH)
        self.assertEqual(is_flush['hand'][0].number, 7)
        self.assertEqual(is_flush['hand'][4].number, 3)
        self.assertEqual(len(is_flush['hand']), 5)
        
    def test_is_flush_returns_false_if_no_flush(self):
        hand = []
            
        hand.append(Card(suit=Suit.CLUB, number=2))
        hand.append(Card(suit=Suit.CLUB, number=3))
        
        is_flush = HandSorter.is_flush(hand)

        self.assertFalse(is_flush)
    
    def test_is_straight_returns_straight_hand(self):
        hand = []
        for number in range(2, 7):
            card = Card(suit=Suit.DIAMOND, number=number)
            hand.append(card)
            
        hand.append(Card(suit=Suit.CLUB, number=6))
        hand.append(Card(suit=Suit.CLUB, number=5))
        
        is_straight = HandSorter.is_straight(hand)
        
        self.assertEqual(len(is_straight['hand']), 5)
        returned_hand = is_straight['hand']
        self.assertEqual(returned_hand[0].number, 6)
        self.assertEqual(returned_hand[4].number, 2)
        self.assertEqual(returned_hand[3].number, 3)
        self.assertEqual(returned_hand[2].number, 4)
        self.assertEqual(returned_hand[1].number, 5)
        self.assertEqual(is_straight['score'], Hand.STRAIGHT)
        
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
        
    def test_is_four_of_a_kind_returns_hand(self):
        hand = []
            
        hand.append(Card(suit=Suit.CLUB, number=2))
        hand.append(Card(suit=Suit.DIAMOND, number=2))
        hand.append(Card(suit=Suit.SPADE, number=2))
        hand.append(Card(suit=Suit.HEART, number=2))
        hand.append(Card(suit=Suit.DIAMOND, number=3))
        hand.append(Card(suit=Suit.SPADE, number=10))
        hand.append(Card(suit=Suit.DIAMOND, number=14))
        
        is_four_of_a_kind = HandSorter.is_four_of_a_kind(hand)
        
        self.assertEqual(is_four_of_a_kind['score'], Hand.FOUR_OF_A_KIND)
        self.assertEqual(is_four_of_a_kind['hand'][0].number, 2)
        self.assertEqual(is_four_of_a_kind['hand'][1].number, 2)
        self.assertEqual(is_four_of_a_kind['hand'][2].number, 2)
        self.assertEqual(is_four_of_a_kind['hand'][3].number, 2)
        self.assertEqual(is_four_of_a_kind['hand'][4].number, 14)
        
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
        
        for card in is_three_of_a_kind['hand']:
            print(card.suit)
            print(card.number)
        
        self.assertEqual(is_three_of_a_kind['score'], Hand.THREE_OF_A_KIND)
        self.assertEqual(is_three_of_a_kind['hand'][0].number, 3)
        self.assertEqual(is_three_of_a_kind['hand'][1].number, 3)
        self.assertEqual(is_three_of_a_kind['hand'][2].number, 3)
        self.assertEqual(is_three_of_a_kind['hand'][3].number, 14)
        self.assertEqual(is_three_of_a_kind['hand'][4].number, 2)
        
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
        
        self.assertEqual(is_pair['score'], Hand.PAIR)
        self.assertEqual(is_pair['hand'][0].number, 2)
        self.assertEqual(is_pair['hand'][1].number, 2)
        self.assertEqual(is_pair['hand'][2].number, 7)
        self.assertEqual(is_pair['hand'][3].number, 6)
        self.assertEqual(is_pair['hand'][4].number, 5)
        
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
            
        hand.append(Card(suit=Suit.CLUB, number=3))
        hand.append(Card(suit=Suit.CLUB, number=4))
        hand.append(Card(suit=Suit.CLUB, number=5))
        hand.append(Card(suit=Suit.CLUB, number=6))
        hand.append(Card(suit=Suit.CLUB, number=7))
        hand.append(Card(suit=Suit.CLUB, number=8))
        hand.append(Card(suit=Suit.CLUB, number=10))
        
        is_straight_flush = HandSorter.is_straight_flush(hand)
        
        hand = is_straight_flush['hand']
        self.assertEqual(len(hand), 5)
        self.assertEqual(hand[0].number, 8)
        self.assertEqual(hand[1].number, 7)
        self.assertEqual(hand[2].number, 6)
        self.assertEqual(hand[3].number, 5)
        self.assertEqual(hand[4].number, 4)
        self.assertEqual(is_straight_flush['score'], Hand.STRAIGHT_FLUSH)
        
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