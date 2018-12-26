from django.test import TestCase
from play.models import Game, Deck, Card, Stage, Suit, Hand, Player
from play.tiebreaker import TieBreaker

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