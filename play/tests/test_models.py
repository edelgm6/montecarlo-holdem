from django.test import TestCase
from play.models import Game, Deck, Card, Stage, Suit, Player, Simulation
from play.rules import Hand
import cProfile

class SimulationTestCase(TestCase):
    
    """
    TODO
    Add in test for being fewer additional hands than additional users
    """
 
    def test_simulation_with_single_card_hands(self):
        user_hand = ['D14', '']
        other_hands = [['', 'C4'], ['D5', 'C5']]
        
        simulation = Simulation(runs=1000, user_hand=user_hand, additional_players=2, additional_hands=other_hands)
        
        simulation.run_simulation()
        results = simulation.results
        
        self.assertEqual(simulation.wins + simulation.losses + simulation.ties, 1000)
        
        wins = 0
        ties = 0
        count = 0
        for h in Hand:
            wins += results[str(h)]['wins']
            ties += results[str(h)]['ties']
            count += results[str(h)]['count']
            
        self.assertEqual(wins, simulation.wins)
        self.assertEqual(ties, simulation.ties)
        self.assertFalse(simulation.ties == 0)
        self.assertFalse(simulation.wins == 0)
        self.assertFalse(simulation.losses == 0)
        
        for player in simulation.all_players:
            self.assertEqual(len(player.hand), 2)
            
        self.assertTrue('D14' in [repr(simulation.user.hand[0]), repr(simulation.user.hand[1])])
        self.assertTrue('C4' in [repr(simulation.all_players[1].hand[0]), repr(simulation.all_players[1].hand[1])])
        self.assertTrue('D5' in simulation.all_players[2].get_hand())
        self.assertTrue('C5' in simulation.all_players[2].get_hand())

    def test_simulation_with_blank_card_hands(self):
        user_hand = ['', '']
        other_hands = [['', ''], ['', '']]
        
        simulation = Simulation(user_hand=user_hand, additional_players=2, additional_hands=other_hands)
        
        simulation.run_simulation()
        results = simulation.results
        
        self.assertEqual(simulation.wins + simulation.losses + simulation.ties, 1000)
        
        wins = 0
        ties = 0
        count = 0
        for h in Hand:
            wins += results[str(h)]['wins']
            ties += results[str(h)]['ties']
            count += results[str(h)]['count']
            
        self.assertEqual(wins, simulation.wins)
        self.assertEqual(ties, simulation.ties)
        self.assertEqual(count, 1000)
        self.assertFalse(simulation.ties == 0)
        self.assertFalse(simulation.wins == 0)
        self.assertFalse(simulation.losses == 0)
        
        for player in simulation.all_players:
            self.assertEqual(len(player.hand), 2)
    
    def test_simulation_with_more_hands_than_players(self):
        user_hand = ['D14', 'C14']
        other_hands = [['D13', 'C13'], ['D2', 'C3']]
        
        simulation = Simulation(user_hand=user_hand, additional_players=1, additional_hands=other_hands)
        
        simulation.run_simulation()
        results = simulation.results
        
        self.assertEqual(simulation.wins + simulation.losses + simulation.ties, 1000)
        
        wins = 0
        ties = 0
        count = 0
        for h in Hand:
            wins += results[str(h)]['wins']
            ties += results[str(h)]['ties']
            count += results[str(h)]['count']
            
        self.assertEqual(wins, simulation.wins)
        self.assertEqual(ties, simulation.ties)
        self.assertEqual(count, 1000)
        self.assertEqual(results[str(Hand.HIGH_CARD)]['count'], 0)
        self.assertFalse(simulation.ties == 0)
        self.assertFalse(simulation.wins == 0)
        self.assertFalse(simulation.losses == 0)
        
        non_user_player = [player for player in simulation.all_players if not player.is_user]
        self.assertEqual(non_user_player[0].starting_hand, other_hands[0])
    
    def test_simulation_with_fewer_hands_than_players(self):
        user_hand = ['D14', 'C14']
        other_hands = [['D13', 'C13']]
        
        simulation = Simulation(user_hand=user_hand, additional_players=2, additional_hands=other_hands)
        
        simulation.run_simulation()
        results = simulation.results
        
        self.assertEqual(simulation.wins + simulation.losses + simulation.ties, 1000)
        
        wins = 0
        ties = 0
        count = 0
        for h in Hand:
            wins += results[str(h)]['wins']
            ties += results[str(h)]['ties']
            count += results[str(h)]['count']
            
        self.assertEqual(wins, simulation.wins)
        self.assertEqual(ties, simulation.ties)
        self.assertEqual(count, 1000)
        self.assertEqual(results[str(Hand.HIGH_CARD)]['count'], 0)
        self.assertFalse(simulation.ties == 0)
        self.assertFalse(simulation.wins == 0)
        self.assertFalse(simulation.losses == 0)
    
    
    def test_simulation_with_user_and_multiple_other_starting_hand(self):
        user_hand = ['D14', 'C14']
        other_hands = [['D13', 'C13'], ['H13', 'H14']]
        
        simulation = Simulation(user_hand=user_hand, additional_players=2, additional_hands=other_hands)
        
        simulation.run_simulation()
        results = simulation.results
        
        self.assertEqual(simulation.wins + simulation.losses + simulation.ties, 1000)
        
        wins = 0
        ties = 0
        count = 0
        for h in Hand:
            wins += results[str(h)]['wins']
            ties += results[str(h)]['ties']
            count += results[str(h)]['count']
            
        self.assertEqual(wins, simulation.wins)
        self.assertEqual(ties, simulation.ties)
        self.assertEqual(count, 1000)
        self.assertEqual(results[str(Hand.HIGH_CARD)]['count'], 0)
        self.assertFalse(simulation.ties == 0)
        self.assertFalse(simulation.wins == 0)
        self.assertFalse(simulation.losses == 0)
    
    def test_simulation_with_user_and_other_starting_hand(self):
        user_hand = ['D14', 'C14']
        other_hands = [['D13', 'C13']]
        
        simulation = Simulation(user_hand=user_hand, additional_hands=other_hands)
        
        simulation.run_simulation()
        results = simulation.results
        
        self.assertEqual(simulation.wins + simulation.losses + simulation.ties, 1000)
        
        wins = 0
        ties = 0
        count = 0
        for h in Hand:
            wins += results[str(h)]['wins']
            ties += results[str(h)]['ties']
            count += results[str(h)]['count']
            
        self.assertEqual(wins, simulation.wins)
        self.assertEqual(ties, simulation.ties)
        self.assertEqual(count, 1000)
        self.assertEqual(results[str(Hand.HIGH_CARD)]['count'], 0)
        self.assertFalse(simulation.ties == 0)
        self.assertFalse(simulation.wins == 0)
        self.assertFalse(simulation.losses == 0)
    
    def test_simulation_with_user_starting_hand(self):
        hand = ['D14', 'C14']
        
        simulation = Simulation(user_hand=hand)
        
        simulation.run_simulation()
        results = simulation.results
        
        self.assertEqual(simulation.wins + simulation.losses + simulation.ties, 1000)
        
        wins = 0
        ties = 0
        count = 0
        for h in Hand:
            wins += results[str(h)]['wins']
            ties += results[str(h)]['ties']
            count += results[str(h)]['count']
            
        self.assertEqual(wins, simulation.wins)
        self.assertEqual(ties, simulation.ties)
        self.assertEqual(count, 1000)
        self.assertEqual(results[str(Hand.HIGH_CARD)]['count'], 0)
        self.assertFalse(simulation.ties == 0)
        self.assertFalse(simulation.wins == 0)
        self.assertFalse(simulation.losses == 0)
    
    def test_simulation_returns_coherent_results(self):
        simulation = Simulation()
        
        simulation.run_simulation()
        results = simulation.results

        self.assertEqual(simulation.wins + simulation.losses + simulation.ties, 1000)
        
        wins = 0
        ties = 0
        count = 0
        for h in Hand:
            wins += results[str(h)]['wins']
            ties += results[str(h)]['ties']
            count += results[str(h)]['count']
            
        self.assertEqual(wins, simulation.wins)
        self.assertEqual(ties, simulation.ties)
        self.assertEqual(count, 1000)
        self.assertFalse(simulation.ties == 0)
        self.assertFalse(simulation.wins == 0)
        self.assertFalse(simulation.losses == 0)

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
    
    def test_deal_maintains_player_start_hands(self):
        user_hand = ['D4', 'C14']
        other_hand = [['D13', 'C13']]
        player1 = Player(is_user=True, starting_hand=user_hand)
        player2 = Player(starting_hand=other_hand[0])
        
        players = [player1, player2]         
        game = Game(players)
        
        game.deal()
        
        self.assertTrue(repr(player1.hand[0]) in [player1.starting_hand[0], player1.starting_hand[1]])
        self.assertTrue(repr(player1.hand[1]) in [player1.starting_hand[0], player1.starting_hand[1]])
        self.assertTrue(repr(player2.hand[0]) in [player2.starting_hand[0], player2.starting_hand[1]])
        self.assertTrue(repr(player2.hand[1]) in [player2.starting_hand[0], player2.starting_hand[1]])
    
    def test_game_creates_shuffled_deck(self):
        players = [Player(), Player(), Player()]         
        game = Game(players)
        
        self.assertTrue(game.deck)
        self.assertEqual(len(game.deck.cards), 52)
        self.assertTrue(game.deck.cards[0].number != 2 or game.deck.cards[0].number != 3)
    
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