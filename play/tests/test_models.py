from django.test import TestCase
from play.models import Game, Deck, Card, Stage, Suit, Player, Simulation
from play.rules import Hand
import cProfile

class SimulationTestCase(TestCase):
    
    """
    def do_cprofile(func):
        def profiled_func(*args, **kwargs):
            profile = cProfile.Profile()
            try:
                profile.enable()
                result = func(*args, **kwargs)
                profile.disable()
                return result
            finally:
                profile.print_stats()
        return profiled_func
    
    def test_can_create_simulation(self):
        simulation = Simulation()
        
        self.assertEqual(simulation.runs, 1000)
        self.assertTrue(simulation.user.is_user)
    
    @do_cprofile
    """
    
    """
    TODO
    Test that specified user hands are actually enforced with each test
    """
    
    def test_simulation_with_user_and_multiple_other_starting_hand(self):
        user_hand = [Card(suit=Suit.DIAMOND, number=14), Card(suit=Suit.CLUB, number=14)]
        other_hands = [Card(suit=Suit.DIAMOND, number=13), Card(suit=Suit.CLUB, number=13), Card(suit=Suit.HEART, number=13), Card(suit=Suit.SPADE, number=14)]
        
        simulation = Simulation(user_hand=user_hand, additional_players=2, additional_hands=[other_hands])
        
        results = simulation.run_simulation()
        print(results)
        
        self.assertEqual(results['wins'] + results['losses'] + results['ties'], 1000)
        
        wins = 0
        ties = 0
        count = 0
        for h in Hand:
            wins += results[h]['wins']
            ties += results[h]['ties']
            count += results[h]['count']
            
        self.assertEqual(wins, results['wins'])
        self.assertEqual(ties, results['ties'])
        self.assertEqual(count, 1000)
        self.assertEqual(results[Hand.HIGH_CARD]['count'], 0)
    
    def test_simulation_with_user_and_other_starting_hand(self):
        user_hand = [Card(suit=Suit.DIAMOND, number=14), Card(suit=Suit.CLUB, number=14)]
        other_hand = [Card(suit=Suit.DIAMOND, number=13), Card(suit=Suit.CLUB, number=13)]
        
        simulation = Simulation(user_hand=user_hand, additional_hands=[other_hand])
        
        results = simulation.run_simulation()
        print(results)
        
        self.assertEqual(results['wins'] + results['losses'] + results['ties'], 1000)
        
        wins = 0
        ties = 0
        count = 0
        for h in Hand:
            wins += results[h]['wins']
            ties += results[h]['ties']
            count += results[h]['count']
            
        self.assertEqual(wins, results['wins'])
        self.assertEqual(ties, results['ties'])
        self.assertEqual(count, 1000)
        self.assertEqual(results[Hand.HIGH_CARD]['count'], 0)
    
    def test_simulation_with_user_starting_hand(self):
        hand = [Card(suit=Suit.DIAMOND, number=14), Card(suit=Suit.CLUB, number=14)]
        
        simulation = Simulation(user_hand=hand)
        
        results = simulation.run_simulation()
        #print(results)
        
        self.assertEqual(results['wins'] + results['losses'] + results['ties'], 1000)
        
        wins = 0
        ties = 0
        count = 0
        for h in Hand:
            wins += results[h]['wins']
            ties += results[h]['ties']
            count += results[h]['count']
            
        self.assertEqual(wins, results['wins'])
        self.assertEqual(ties, results['ties'])
        self.assertEqual(count, 1000)
        self.assertEqual(results[Hand.HIGH_CARD]['count'], 0)
    
    def test_simulation_returns_coherent_results(self):
        simulation = Simulation()
        
        results = simulation.run_simulation()
        #print(results)
        self.assertEqual(results['wins'] + results['losses'] + results['ties'], 1000)
        
        wins = 0
        ties = 0
        count = 0
        for h in Hand:
            wins += results[h]['wins']
            ties += results[h]['ties']
            count += results[h]['count']
            
        self.assertEqual(wins, results['wins'])
        self.assertEqual(ties, results['ties'])
        self.assertEqual(count, 1000)

class PlayerTestCase(TestCase):
    def test_can_create_player(self):
        players = [Player(), Player()]         
        game = Game(players)
        game.deal()
        game.deal()
        game.deal()
        game.deal()
        
        player = game.players[0]
        
        self.assertEqual(len(player.hand), 2)
        
    def test_set_player_best_hands(self):
        players = [Player(), Player()]         
        game = Game(players)
        game.deal()
        game.deal()
        game.deal()
        game.deal()
        
        game.set_player_hands()
        player = game.players[0]

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
        players = [Player(), Player(), Player()]         
        game = Game(players)
        
        self.assertTrue(game.deck)
        self.assertEqual(len(game.deck.cards), 52)
        
    def test_get_winning_player_returns_player1(self):
        players = [Player(), Player()]         
        game = Game(players)
        
        #community cards
        game.community.append(Card(suit=Suit.CLUB, number=2))
        game.community.append(Card(suit=Suit.DIAMOND, number=11))
        game.community.append(Card(suit=Suit.SPADE, number=5))
        game.community.append(Card(suit=Suit.HEART, number=6))
        game.community.append(Card(suit=Suit.DIAMOND, number=7))
        
        #player1 cards
        player1 = game.players[0]
        player1.hand.append(Card(suit=Suit.CLUB, number=8))
        player1.hand.append(Card(suit=Suit.CLUB, number=9))
        
        #player2 cards
        player2 = game.players[1]
        player2.hand.append(Card(suit=Suit.DIAMOND, number=2))
        player2.hand.append(Card(suit=Suit.SPADE, number=2))
        
        game.set_player_hands()
        winner = game.get_winning_player()
        
        self.assertEqual(winner[0], player1)
        self.assertEqual(winner[0].best_hand['score'], Hand.STRAIGHT)
        self.assertEqual(player2.best_hand['score'], Hand.THREE_OF_A_KIND)
        
    def test_get_winning_player_returns_player1_with_tie(self):
        players = [Player(), Player()]         
        game = Game(players)
        
        #community cards
        game.community.append(Card(suit=Suit.CLUB, number=2))
        game.community.append(Card(suit=Suit.DIAMOND, number=11))
        game.community.append(Card(suit=Suit.SPADE, number=5))
        game.community.append(Card(suit=Suit.HEART, number=6))
        game.community.append(Card(suit=Suit.DIAMOND, number=7))
        
        #player1 cards
        player1 = game.players[0]
        player1.hand.append(Card(suit=Suit.CLUB, number=8))
        player1.hand.append(Card(suit=Suit.CLUB, number=9))
        
        #player2 cards
        player2 = game.players[1]
        player2.hand.append(Card(suit=Suit.DIAMOND, number=4))
        player2.hand.append(Card(suit=Suit.SPADE, number=3))
        
        game.set_player_hands()
        winner = game.get_winning_player()
        
        self.assertEqual(winner[0], player1)
        self.assertEqual(winner[0].best_hand['score'], Hand.STRAIGHT)
        self.assertEqual(player2.best_hand['score'], Hand.STRAIGHT)
        self.assertEqual(player2.best_hand['hand'][0].number, 7)
        self.assertEqual(player1.best_hand['hand'][0].number, 9)
        
    def test_get_winning_player_returns_both_players_with_true_tie(self):
        players = [Player(), Player()]         
        game = Game(players)
        
        #community cards
        game.community.append(Card(suit=Suit.CLUB, number=2))
        game.community.append(Card(suit=Suit.DIAMOND, number=11))
        game.community.append(Card(suit=Suit.SPADE, number=5))
        game.community.append(Card(suit=Suit.HEART, number=6))
        game.community.append(Card(suit=Suit.DIAMOND, number=7))
        
        #player1 cards
        player1 = game.players[0]
        player1.hand.append(Card(suit=Suit.CLUB, number=8))
        player1.hand.append(Card(suit=Suit.CLUB, number=9))
        
        #player2 cards
        player2 = game.players[1]
        player2.hand.append(Card(suit=Suit.DIAMOND, number=8))
        player2.hand.append(Card(suit=Suit.DIAMOND, number=9))
        
        game.set_player_hands()
        winners = game.get_winning_player()
        
        self.assertTrue(player1 in winners)
        self.assertTrue(player2 in winners)

    
    def test_preflop_deal_gives_each_player_2_cards(self):
        players = [Player(), Player(), Player()]         
        game = Game(players)
        
        game.deal()
        
        for player in game.players:
            self.assertEqual(len(player.hand),2)
            
        self.assertEqual(len(game.deck.cards), 52 - len(game.players) * 2)
        self.assertEqual(game.stage, Stage.PREFLOP)
        
    def test_flop_deal_puts_3_cards_in_community(self):
        players = [Player(), Player(), Player()]         
        game = Game(players)
        
        game.deal()
        game.deal()
        
        for player in game.players:
            self.assertEqual(len(player.hand),2)
        
        # Deck length is less the initial deal minus 3 community - 1 burn
        self.assertEqual(len(game.deck.cards), 52 - len(game.players) * 2 - 3 - 1)
        self.assertEqual(game.stage, Stage.FLOP)
        
    def test_turn_deal_puts_1_card_in_community(self):
        players = [Player(), Player(), Player()]         
        game = Game(players)
        
        game.deal()
        game.deal()
        game.deal()
        
        for player in game.players:
            self.assertEqual(len(player.hand),2)
        
        # Deck length is less the initial deal minus 3 community - 1 burn
        self.assertEqual(len(game.deck.cards), 52 - len(game.players) * 2 - 3 - 1 - 1 - 1)
        self.assertEqual(game.stage, Stage.TURN)
        
    def test_river_deal_puts_1_card_in_community(self):
        players = [Player(), Player(), Player()]         
        game = Game(players)
        
        game.deal()
        game.deal()
        game.deal()
        game.deal()
        
        for player in game.players:
            self.assertEqual(len(player.hand),2)
        
        # Deck length is less the initial deal minus 3 community - 1 burn
        self.assertEqual(len(game.deck.cards), 52 - len(game.players) * 2 - 3 - 1 - 1 - 1 - 1 - 1)
        self.assertEqual(game.stage, Stage.RIVER)  