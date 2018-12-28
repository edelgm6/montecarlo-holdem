from django.test import TestCase
from play.models import Game, Deck, Card, Stage, Suit, Hand, Player

class HighCardBreakerTestCase(TestCase):

    def test_returns_winner_for_tied_high_card(self):
        
        players = [Player(), Player()]
        game = Game(players)
        
        game.community.append(Card(suit=Suit.CLUB, number = 14))
        game.community.append(Card(suit=Suit.DIAMOND, number = 13))
        game.community.append(Card(suit=Suit.SPADE, number = 12))
        game.community.append(Card(suit=Suit.HEART, number = 11))
        game.community.append(Card(suit=Suit.DIAMOND, number = 8))
        
        player1 = game.players[0]
        player1.hand.append(Card(suit=Suit.DIAMOND, number = 2))
        player1.hand.append(Card(suit=Suit.DIAMOND, number = 3)) 
        
        player2 = game.players[1]
        player2.hand.append(Card(suit=Suit.CLUB, number = 9))
        player2.hand.append(Card(suit=Suit.DIAMOND, number = 5)) 
            
        players = [player1, player2]
        
        game.set_player_hands()
        
        winners = game.break_tie(players)
        
        self.assertFalse(player1 in winners)
        self.assertTrue(player2 in winners)
        self.assertEqual(player1.best_hand['score'], Hand.HIGH_CARD)
        self.assertEqual(player2.best_hand['score'], Hand.HIGH_CARD)
    
    def test_returns_winners_for_tied_pair(self):

        players = [Player(), Player()]
        game = Game(players)
        
        game.community.append(Card(suit=Suit.CLUB, number = 14))
        game.community.append(Card(suit=Suit.DIAMOND, number = 13))
        game.community.append(Card(suit=Suit.SPADE, number = 12))
        game.community.append(Card(suit=Suit.HEART, number = 11))
        game.community.append(Card(suit=Suit.DIAMOND, number = 8))
        
        player1 = game.players[0]
        player1.hand.append(Card(suit=Suit.DIAMOND, number = 2))
        player1.hand.append(Card(suit=Suit.DIAMOND, number = 3)) 
        
        player2 = game.players[1]
        player2.hand.append(Card(suit=Suit.CLUB, number = 4))
        player2.hand.append(Card(suit=Suit.DIAMOND, number = 5)) 
            
        players = [player1, player2]
        
        game.set_player_hands()
        
        winners = game.break_tie(players)
        
        self.assertTrue(player1 in winners)
        self.assertTrue(player2 in winners)
        self.assertEqual(player1.best_hand['score'], Hand.HIGH_CARD)
        self.assertEqual(player2.best_hand['score'], Hand.HIGH_CARD)


class FullHouseBreakerTestCase(TestCase):

    def test_returns_winner_for_tied_full_house(self):

        players = [Player(), Player()]
        game = Game(players)
        
        game.community.append(Card(suit=Suit.CLUB, number = 12))
        game.community.append(Card(suit=Suit.DIAMOND, number = 12))
        game.community.append(Card(suit=Suit.SPADE, number = 11))
        game.community.append(Card(suit=Suit.HEART, number = 11))
        game.community.append(Card(suit=Suit.DIAMOND, number = 11))
        
        player1 = game.players[0]
        player1.hand.append(Card(suit=Suit.DIAMOND, number = 10))
        player1.hand.append(Card(suit=Suit.DIAMOND, number = 10)) 
        
        player2 = game.players[1]
        player2.hand.append(Card(suit=Suit.CLUB, number = 14))
        player2.hand.append(Card(suit=Suit.DIAMOND, number = 14)) 
            
        players = [player1, player2]
        
        game.set_player_hands()
        
        winners = game.break_tie(players)
        
        self.assertFalse(player1 in winners)
        self.assertTrue(player2 in winners)
        self.assertEqual(player1.best_hand['score'], Hand.FULL_HOUSE)
        self.assertEqual(player2.best_hand['score'], Hand.FULL_HOUSE)
    
    def test_returns_winners_for_tied_pair(self):

        players = [Player(), Player()]         
        game = Game(players)
        
        game.community.append(Card(suit=Suit.CLUB, number = 12))
        game.community.append(Card(suit=Suit.DIAMOND, number = 12))
        game.community.append(Card(suit=Suit.SPADE, number = 11))
        game.community.append(Card(suit=Suit.HEART, number = 11))
        game.community.append(Card(suit=Suit.DIAMOND, number = 11))
        
        player1 = game.players[0]
        player1.hand.append(Card(suit=Suit.DIAMOND, number = 14))
        player1.hand.append(Card(suit=Suit.DIAMOND, number = 3)) 
        
        player2 = game.players[1]
        player2.hand.append(Card(suit=Suit.CLUB, number = 14))
        player2.hand.append(Card(suit=Suit.DIAMOND, number = 5)) 
            
        players = [player1, player2]
        
        game.set_player_hands()
        
        winners = game.break_tie(players)
        
        self.assertTrue(player1 in winners)
        self.assertTrue(player2 in winners)
        self.assertEqual(player1.best_hand['score'], Hand.FULL_HOUSE)
        self.assertEqual(player2.best_hand['score'], Hand.FULL_HOUSE)

class TwoPairBreakerTestCase(TestCase):

    def test_returns_winner_for_tied_pair(self):

        players = [Player(), Player()]
        game = Game(players)
        
        game.community.append(Card(suit=Suit.CLUB, number = 12))
        game.community.append(Card(suit=Suit.DIAMOND, number = 12))
        game.community.append(Card(suit=Suit.SPADE, number = 11))
        game.community.append(Card(suit=Suit.HEART, number = 11))
        game.community.append(Card(suit=Suit.DIAMOND, number = 13))
        
        player1 = game.players[0]
        player1.hand.append(Card(suit=Suit.DIAMOND, number = 10))
        player1.hand.append(Card(suit=Suit.DIAMOND, number = 3)) 
        
        player2 = game.players[1]
        player2.hand.append(Card(suit=Suit.CLUB, number = 14))
        player2.hand.append(Card(suit=Suit.DIAMOND, number = 5)) 
            
        players = [player1, player2]
        
        game.set_player_hands()
        
        winners = game.break_tie(players)
        
        self.assertFalse(player1 in winners)
        self.assertTrue(player2 in winners)
        self.assertEqual(player1.best_hand['score'], Hand.TWO_PAIR)
        self.assertEqual(player2.best_hand['score'], Hand.TWO_PAIR)
    
    def test_returns_winners_for_tied_pair(self):

        players = [Player(), Player()]         
        game = Game(players)
        
        game.community.append(Card(suit=Suit.CLUB, number = 12))
        game.community.append(Card(suit=Suit.DIAMOND, number = 12))
        game.community.append(Card(suit=Suit.SPADE, number = 11))
        game.community.append(Card(suit=Suit.HEART, number = 11))
        game.community.append(Card(suit=Suit.DIAMOND, number = 13))
        
        player1 = game.players[0]
        player1.hand.append(Card(suit=Suit.DIAMOND, number = 14))
        player1.hand.append(Card(suit=Suit.DIAMOND, number = 3)) 
        
        player2 = game.players[1]
        player2.hand.append(Card(suit=Suit.CLUB, number = 14))
        player2.hand.append(Card(suit=Suit.DIAMOND, number = 5)) 
            
        players = [player1, player2]
        
        game.set_player_hands()
        
        winners = game.break_tie(players)
        
        self.assertTrue(player1 in winners)
        self.assertTrue(player2 in winners)
        self.assertEqual(player1.best_hand['score'], Hand.TWO_PAIR)
        self.assertEqual(player2.best_hand['score'], Hand.TWO_PAIR)


class PairBreakerTestCase(TestCase):

    def test_returns_winner_for_tied_pair(self):

        players = [Player(), Player()]         
        game = Game(players)
        
        game.community.append(Card(suit=Suit.CLUB, number = 12))
        game.community.append(Card(suit=Suit.DIAMOND, number = 12))
        game.community.append(Card(suit=Suit.SPADE, number = 11))
        game.community.append(Card(suit=Suit.HEART, number = 2))
        game.community.append(Card(suit=Suit.DIAMOND, number = 13))
        
        player1 = game.players[0]
        player1.hand.append(Card(suit=Suit.DIAMOND, number = 10))
        player1.hand.append(Card(suit=Suit.DIAMOND, number = 3)) 
        
        player2 = game.players[1]
        player2.hand.append(Card(suit=Suit.CLUB, number = 14))
        player2.hand.append(Card(suit=Suit.DIAMOND, number = 5)) 
            
        players = [player1, player2]
        
        game.set_player_hands()
        
        winners = game.break_tie(players)
        
        self.assertFalse(player1 in winners)
        self.assertTrue(player2 in winners)
        self.assertEqual(player1.best_hand['score'], Hand.PAIR)
        self.assertEqual(player2.best_hand['score'], Hand.PAIR)
    
    def test_returns_winners_for_tied_pair(self):

        players = [Player(), Player()]         
        game = Game(players)
        
        game.community.append(Card(suit=Suit.CLUB, number = 12))
        game.community.append(Card(suit=Suit.DIAMOND, number = 12))
        game.community.append(Card(suit=Suit.SPADE, number = 11))
        game.community.append(Card(suit=Suit.HEART, number = 2))
        game.community.append(Card(suit=Suit.DIAMOND, number = 13))
        
        player1 = game.players[0]
        player1.hand.append(Card(suit=Suit.DIAMOND, number = 14))
        player1.hand.append(Card(suit=Suit.DIAMOND, number = 3)) 
        
        player2 = game.players[1]
        player2.hand.append(Card(suit=Suit.CLUB, number = 14))
        player2.hand.append(Card(suit=Suit.DIAMOND, number = 5)) 
            
        players = [player1, player2]
        
        game.set_player_hands()
        
        winners = game.break_tie(players)
        
        self.assertTrue(player1 in winners)
        self.assertTrue(player2 in winners)
        self.assertEqual(player1.best_hand['score'], Hand.PAIR)
        self.assertEqual(player2.best_hand['score'], Hand.PAIR)


class ThreeBreakerTestCase(TestCase):

    def test_returns_winner_for_tied_three(self):

        players = [Player(), Player()]         
        game = Game(players)
        
        game.community.append(Card(suit=Suit.CLUB, number = 12))
        game.community.append(Card(suit=Suit.DIAMOND, number = 12))
        game.community.append(Card(suit=Suit.SPADE, number = 12))
        game.community.append(Card(suit=Suit.HEART, number = 2))
        game.community.append(Card(suit=Suit.DIAMOND, number = 13))
        
        player1 = game.players[0]
        player1.hand.append(Card(suit=Suit.DIAMOND, number = 10))
        player1.hand.append(Card(suit=Suit.DIAMOND, number = 3)) 
        
        player2 = game.players[1]
        player2.hand.append(Card(suit=Suit.CLUB, number = 14))
        player2.hand.append(Card(suit=Suit.DIAMOND, number = 5)) 
            
        players = [player1, player2]
        
        game.set_player_hands()
        
        winners = game.break_tie(players)
        
        self.assertFalse(player1 in winners)
        self.assertTrue(player2 in winners)
        self.assertEqual(player1.best_hand['score'], Hand.THREE_OF_A_KIND)
        self.assertEqual(player2.best_hand['score'], Hand.THREE_OF_A_KIND)
    
    def test_returns_winners_for_tied_three(self):

        players = [Player(), Player()]         
        game = Game(players)
        
        game.community.append(Card(suit=Suit.CLUB, number = 12))
        game.community.append(Card(suit=Suit.DIAMOND, number = 12))
        game.community.append(Card(suit=Suit.SPADE, number = 12))
        game.community.append(Card(suit=Suit.HEART, number = 2))
        game.community.append(Card(suit=Suit.DIAMOND, number = 13))
        
        player1 = game.players[0]
        player1.hand.append(Card(suit=Suit.DIAMOND, number = 14))
        player1.hand.append(Card(suit=Suit.DIAMOND, number = 3)) 
        
        player2 = game.players[1]
        player2.hand.append(Card(suit=Suit.CLUB, number = 14))
        player2.hand.append(Card(suit=Suit.DIAMOND, number = 5)) 
            
        players = [player1, player2]
        
        game.set_player_hands()
        
        winners = game.break_tie(players)
        
        self.assertTrue(player1 in winners)
        self.assertTrue(player2 in winners)
        self.assertEqual(player1.best_hand['score'], Hand.THREE_OF_A_KIND)
        self.assertEqual(player2.best_hand['score'], Hand.THREE_OF_A_KIND)

class FourBreakerTestCase(TestCase):

    def test_returns_winner_for_tied_four(self):

        players = [Player(), Player()]         
        game = Game(players)
        
        game.community.append(Card(suit=Suit.CLUB, number = 12))
        game.community.append(Card(suit=Suit.DIAMOND, number = 12))
        game.community.append(Card(suit=Suit.SPADE, number = 12))
        game.community.append(Card(suit=Suit.HEART, number = 12))
        game.community.append(Card(suit=Suit.DIAMOND, number = 13))
        
        player1 = game.players[0]
        player1.hand.append(Card(suit=Suit.DIAMOND, number = 14))
        player1.hand.append(Card(suit=Suit.DIAMOND, number = 3)) 
        
        player2 = game.players[1]
        player2.hand.append(Card(suit=Suit.CLUB, number = 11))
        player2.hand.append(Card(suit=Suit.DIAMOND, number = 5)) 
            
        players = [player1, player2]
        
        game.set_player_hands()
        
        winners = game.break_tie(players)
        
        self.assertTrue(player1 in winners)
        self.assertFalse(player2 in winners)
        self.assertEqual(player1.best_hand['score'], Hand.FOUR_OF_A_KIND)
        self.assertEqual(player2.best_hand['score'], Hand.FOUR_OF_A_KIND)
    
    def test_returns_winners_for_tied_four(self):

        players = [Player(), Player()]         
        game = Game(players)
        
        game.community.append(Card(suit=Suit.CLUB, number = 12))
        game.community.append(Card(suit=Suit.DIAMOND, number = 12))
        game.community.append(Card(suit=Suit.SPADE, number = 12))
        game.community.append(Card(suit=Suit.HEART, number = 12))
        game.community.append(Card(suit=Suit.DIAMOND, number = 13))
        
        player1 = game.players[0]
        player1.hand.append(Card(suit=Suit.DIAMOND, number = 14))
        player1.hand.append(Card(suit=Suit.DIAMOND, number = 3)) 
        
        player2 = game.players[1]
        player2.hand.append(Card(suit=Suit.CLUB, number = 14))
        player2.hand.append(Card(suit=Suit.DIAMOND, number = 5)) 
            
        players = [player1, player2]
        
        game.set_player_hands()
        
        winners = game.break_tie(players)
        
        self.assertTrue(player1 in winners)
        self.assertTrue(player2 in winners)
        self.assertEqual(player1.best_hand['score'], Hand.FOUR_OF_A_KIND)
        self.assertEqual(player2.best_hand['score'], Hand.FOUR_OF_A_KIND)


class StraightFlushBreakerTestCase(TestCase):

    def test_returns_winner_for_straight_flush(self):
        
        players = [Player(), Player()]         
        game = Game(players)
        
        game.community.append(Card(suit=Suit.CLUB, number = 10))
        game.community.append(Card(suit=Suit.CLUB, number = 11))
        game.community.append(Card(suit=Suit.CLUB, number = 12))
        game.community.append(Card(suit=Suit.CLUB, number = 13))
        game.community.append(Card(suit=Suit.CLUB, number = 9))
        
        player1 = game.players[0]
        player1.hand.append(Card(suit=Suit.DIAMOND, number = 8))
        player1.hand.append(Card(suit=Suit.DIAMOND, number = 3)) 
        
        player2 = game.players[1]
        player2.hand.append(Card(suit=Suit.CLUB, number = 14))
        player2.hand.append(Card(suit=Suit.DIAMOND, number = 5)) 
            
        players = [player1, player2]
        
        game.set_player_hands()
        
        winners = game.break_tie(players)
        
        self.assertFalse(player1 in winners)
        self.assertTrue(player2 in winners)
        self.assertEqual(player1.best_hand['score'], Hand.STRAIGHT_FLUSH)
        self.assertEqual(player2.best_hand['score'], Hand.STRAIGHT_FLUSH)

    
    
    def test_returns_tie_for_straights(self):
        
        players = [Player(), Player()]         
        game = Game(players)
        
        game.community.append(Card(suit=Suit.CLUB, number = 10))
        game.community.append(Card(suit=Suit.CLUB, number = 11))
        game.community.append(Card(suit=Suit.CLUB, number = 12))
        game.community.append(Card(suit=Suit.CLUB, number = 13))
        game.community.append(Card(suit=Suit.CLUB, number = 9))
        
        player1 = game.players[0]
        player1.hand.append(Card(suit=Suit.DIAMOND, number = 8))
        player1.hand.append(Card(suit=Suit.DIAMOND, number = 3)) 
        
        player2 = game.players[1]
        player2.hand.append(Card(suit=Suit.CLUB, number = 2))
        player2.hand.append(Card(suit=Suit.DIAMOND, number = 5)) 
            
        players = [player1, player2]
        
        game.set_player_hands()
        
        winners = game.break_tie(players)
        
        self.assertTrue(player1 in winners)
        self.assertTrue(player2 in winners)
        self.assertEqual(player1.best_hand['score'], Hand.STRAIGHT_FLUSH)
        self.assertEqual(player2.best_hand['score'], Hand.STRAIGHT_FLUSH)        
        
        
class StraightBreakerTestCase(TestCase):

    def test_returns_winner_for_straights(self):
        
        players = [Player(), Player()]         
        game = Game(players)
        
        game.community.append(Card(suit=Suit.CLUB, number = 9))
        game.community.append(Card(suit=Suit.CLUB, number = 10))
        game.community.append(Card(suit=Suit.CLUB, number = 11))
        game.community.append(Card(suit=Suit.CLUB, number = 12))
        game.community.append(Card(suit=Suit.DIAMOND, number = 13))
        
        player1 = game.players[0]
        player1.hand.append(Card(suit=Suit.DIAMOND, number = 14))
        player1.hand.append(Card(suit=Suit.DIAMOND, number = 3)) 
        
        player2 = game.players[1]
        player2.hand.append(Card(suit=Suit.DIAMOND, number = 4))
        player2.hand.append(Card(suit=Suit.DIAMOND, number = 5)) 
            
        players = [player1, player2]
        
        game.set_player_hands()
        
        winners = game.break_tie(players)
        
        self.assertTrue(player1 in winners)
        self.assertFalse(player2 in winners)
        self.assertEqual(player1.best_hand['score'], Hand.STRAIGHT)
        self.assertEqual(player2.best_hand['score'], Hand.STRAIGHT)

    
    
    def test_returns_tie_for_straights(self):
        
        players = [Player(), Player()]         
        game = Game(players)
        
        game.community.append(Card(suit=Suit.CLUB, number = 9))
        game.community.append(Card(suit=Suit.CLUB, number = 10))
        game.community.append(Card(suit=Suit.CLUB, number = 11))
        game.community.append(Card(suit=Suit.CLUB, number = 12))
        game.community.append(Card(suit=Suit.DIAMOND, number = 13))
        
        player1 = game.players[0]
        player1.hand.append(Card(suit=Suit.DIAMOND, number = 2))
        player1.hand.append(Card(suit=Suit.DIAMOND, number = 3)) 
        
        player2 = game.players[1]
        player2.hand.append(Card(suit=Suit.DIAMOND, number = 4))
        player2.hand.append(Card(suit=Suit.DIAMOND, number = 5)) 
            
        players = [player1, player2]
        
        game.set_player_hands()
        
        winners = game.break_tie(players)
        
        self.assertTrue(player1 in winners)
        self.assertTrue(player2 in winners)
        self.assertEqual(player1.best_hand['score'], Hand.STRAIGHT)
        self.assertEqual(player2.best_hand['score'], Hand.STRAIGHT)



class FlushBreakerTestCase(TestCase):
    
    def test_returns_tie_for_flushes(self):
        
        players = [Player(), Player(), Player()]         
        game = Game(players)
        
        game.community.append(Card(suit=Suit.CLUB, number = 8))
        game.community.append(Card(suit=Suit.CLUB, number = 14))
        game.community.append(Card(suit=Suit.CLUB, number = 9))
        game.community.append(Card(suit=Suit.CLUB, number = 10))
        game.community.append(Card(suit=Suit.CLUB, number = 13))
        
        player1 = game.players[0]
        player1.hand.append(Card(suit=Suit.CLUB, number = 2))
        player1.hand.append(Card(suit=Suit.CLUB, number = 3)) 
        
        player2 = game.players[1]
        player2.hand.append(Card(suit=Suit.CLUB, number = 4))
        player2.hand.append(Card(suit=Suit.CLUB, number = 5)) 
        
        player3 = game.players[2]
        player3.hand.append(Card(suit=Suit.CLUB, number = 6))
        player3.hand.append(Card(suit=Suit.DIAMOND, number = 7)) 
            
        players = [player1, player2, player3]
        
        game.set_player_hands()
        
        winners = game.break_tie(players)
        
        self.assertTrue(player1 in winners)
        self.assertTrue(player2 in winners)
        self.assertTrue(player3 in winners)
        self.assertEqual(player1.best_hand['score'], Hand.FLUSH)
        self.assertEqual(player2.best_hand['score'], Hand.FLUSH)
        self.assertEqual(player3.best_hand['score'], Hand.FLUSH)
        
    def test_flush_breaker_returns_single_player(self):
        
        players = [Player(), Player(), Player()]         
        game = Game(players)
        
        game.community.append(Card(suit=Suit.CLUB, number = 8))
        game.community.append(Card(suit=Suit.CLUB, number = 14))
        game.community.append(Card(suit=Suit.CLUB, number = 9))
        game.community.append(Card(suit=Suit.CLUB, number = 10))
        game.community.append(Card(suit=Suit.CLUB, number = 13))
        
        player1 = game.players[0]
        player1.hand.append(Card(suit=Suit.CLUB, number = 2))
        player1.hand.append(Card(suit=Suit.CLUB, number = 14)) 
        
        player2 = game.players[1]
        player2.hand.append(Card(suit=Suit.CLUB, number = 4))
        player2.hand.append(Card(suit=Suit.CLUB, number = 5)) 
        
        player3 = game.players[2]
        player3.hand.append(Card(suit=Suit.CLUB, number = 6))
        player3.hand.append(Card(suit=Suit.DIAMOND, number = 7)) 
            
        players = [player1, player2, player3]
        
        game.set_player_hands()
        
        winners = game.break_tie(players)
        
        self.assertTrue(player1 in winners)
        self.assertFalse(player2 in winners)
        self.assertFalse(player3 in winners)
        self.assertEqual(player1.best_hand['score'], Hand.FLUSH)
        self.assertEqual(player2.best_hand['score'], Hand.FLUSH)
        self.assertEqual(player3.best_hand['score'], Hand.FLUSH)