from django.test import TestCase
from play.models import Game, Deck, Card, Stage, Suit

class PlayerTestCase(TestCase):
    def test_can_create_player(self):
        game = Game()
        game.deal()
        game.deal()
        game.deal()
        game.deal()
        
        player = game.players[0]
        
        self.assertEqual(len(player.hand), 2)
        
    def test_set_player_best_hands(self):
        game = Game()
        game.deal()
        game.deal()
        game.deal()
        game.deal()
        
        game.set_player_hands()
        player = game.players[0]
        
    def test_get_winning_player(self):
        game = Game()
        game.deal()
        game.deal()
        game.deal()
        game.deal()
        
        game.get_winning_player()

class CardTestCase(TestCase):
    def test_can_create_card(self):
        card = Card(suit=Suit.DIAMOND, number=2)
        
        self.assertEqual(card.suit, Suit.DIAMOND)
        self.assertEqual(card.number, 2)

class DeckTestCase(TestCase):
    def test_creates_52_cards(self):
        
        deck = Deck()
        
        self.assertEqual(len(deck.cards),52)
        
class GameTestCase(TestCase):
    def test_game_creates_deck(self):
        game = Game(additional_players=2)
        
        self.assertTrue(game.deck)
        self.assertEqual(len(game.deck.cards), 52)
        
    def test_preflop_deal_gives_each_player_2_cards(self):
        game = Game(additional_players=2)
        
        game.deal()
        
        for player in game.players:
            self.assertEqual(len(player.hand),2)
            
        self.assertEqual(len(game.deck.cards), 52 - len(game.players) * 2)
        self.assertEqual(game.stage, Stage.PREFLOP)
        
    def test_flop_deal_puts_3_cards_in_community(self):
        game = Game(additional_players=2)
        
        game.deal()
        game.deal()
        
        for player in game.players:
            self.assertEqual(len(player.hand),2)
        
        # Deck length is less the initial deal minus 3 community - 1 burn
        self.assertEqual(len(game.deck.cards), 52 - len(game.players) * 2 - 3 - 1)
        self.assertEqual(game.stage, Stage.FLOP)
        
    def test_turn_deal_puts_1_card_in_community(self):
        game = Game(additional_players=2)
        
        game.deal()
        game.deal()
        game.deal()
        
        for player in game.players:
            self.assertEqual(len(player.hand),2)
        
        # Deck length is less the initial deal minus 3 community - 1 burn
        self.assertEqual(len(game.deck.cards), 52 - len(game.players) * 2 - 3 - 1 - 1 - 1)
        self.assertEqual(game.stage, Stage.TURN)
        
    def test_river_deal_puts_1_card_in_community(self):
        game = Game(additional_players=2)
        
        game.deal()
        game.deal()
        game.deal()
        game.deal()
        
        for player in game.players:
            self.assertEqual(len(player.hand),2)
        
        # Deck length is less the initial deal minus 3 community - 1 burn
        self.assertEqual(len(game.deck.cards), 52 - len(game.players) * 2 - 3 - 1 - 1 - 1 - 1 - 1)
        self.assertEqual(game.stage, Stage.RIVER)  