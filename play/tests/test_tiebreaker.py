from django.test import TestCase
from play.models import Game, Deck, Card, Stage, Suit, Hand, Player
from play.tiebreaker import TieBreaker


class FourBreakerTestCase(TestCase):

    def test_returns_winner_for_tied_four(self):

        game = Game(additional_players=1)
        
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
        
        winners = TieBreaker.break_tie(players)
        
        self.assertTrue(player1 in winners)
        self.assertFalse(player2 in winners)
        self.assertEqual(player1.best_hand['score'], Hand.FOUR_OF_A_KIND)
        self.assertEqual(player2.best_hand['score'], Hand.FOUR_OF_A_KIND)
    
    def test_returns_winners_for_tied_four(self):

        game = Game(additional_players=1)
        
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
        
        winners = TieBreaker.break_tie(players)
        
        self.assertTrue(player1 in winners)
        self.assertTrue(player2 in winners)
        self.assertEqual(player1.best_hand['score'], Hand.FOUR_OF_A_KIND)
        self.assertEqual(player2.best_hand['score'], Hand.FOUR_OF_A_KIND)

class StraightBreakerTestCase(TestCase):

    def test_returns_winner_for_straights(self):
        
        game = Game(additional_players=1)
        
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
        
        winners = TieBreaker.break_tie(players)
        
        self.assertTrue(player1 in winners)
        self.assertFalse(player2 in winners)
        self.assertEqual(player1.best_hand['score'], Hand.STRAIGHT)
        self.assertEqual(player2.best_hand['score'], Hand.STRAIGHT)

    
    
    def test_returns_tie_for_straights(self):
        
        game = Game(additional_players=1)
        
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
        
        winners = TieBreaker.break_tie(players)
        
        self.assertTrue(player1 in winners)
        self.assertTrue(player2 in winners)
        self.assertEqual(player1.best_hand['score'], Hand.STRAIGHT)
        self.assertEqual(player2.best_hand['score'], Hand.STRAIGHT)



class FlushBreakerTestCase(TestCase):
    
    def test_returns_tie_for_flushes(self):
        
        game = Game(additional_players=2)
        
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
        
        winners = TieBreaker.break_tie(players)
        
        self.assertTrue(player1 in winners)
        self.assertTrue(player2 in winners)
        self.assertTrue(player3 in winners)
        self.assertEqual(player1.best_hand['score'], Hand.FLUSH)
        self.assertEqual(player2.best_hand['score'], Hand.FLUSH)
        self.assertEqual(player3.best_hand['score'], Hand.FLUSH)
        
    def test_flush_breaker_returns_single_player(self):
        
        game = Game(additional_players=2)
        
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
        
        winners = TieBreaker.break_tie(players)
        
        self.assertTrue(player1 in winners)
        self.assertFalse(player2 in winners)
        self.assertFalse(player3 in winners)
        self.assertEqual(player1.best_hand['score'], Hand.FLUSH)
        self.assertEqual(player2.best_hand['score'], Hand.FLUSH)
        self.assertEqual(player3.best_hand['score'], Hand.FLUSH)