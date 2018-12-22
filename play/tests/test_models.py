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
        
        hand = player.get_total_hand()
        self.assertEqual(len(hand), 7)
        
    def test_is_flush_ids_a_flush(self):
        game = Game()
        
        hand = []
        for number in range(2, 8):
            card = Card(name=Suit.DIAMOND.value + str(number))
            hand.append(card)
            
        hand.append(Card(name='C2'))
        hand.append(Card(name='C3'))
        
        player = game.players[0]
        
        is_flush = player.is_flush(hand)

        self.assertEqual(is_flush, 7)
        
    def test_is_flush_returns_false_if_no_flush(self):
        game = Game()
        
        hand = []
            
        hand.append(Card(name='C2'))
        hand.append(Card(name='C3'))
        
        player = game.players[0]
        
        is_flush = player.is_flush(hand)

        self.assertFalse(is_flush)
    
    def test_is_straight_returns_high_card(self):
        game = Game()
        
        hand = []
        for number in range(2, 8):
            card = Card(name=Suit.DIAMOND.value + str(number))
            hand.append(card)
            
        hand.append(Card(name='C2'))
        hand.append(Card(name='C3'))
        
        player = game.players[0]
        
        is_straight = player.is_straight(hand)
        
        self.assertEqual(is_straight, 7)
        
    def test_isnt_straight_returns_false(self):
        game = Game()
        
        hand = []
            
        hand.append(Card(name='C2'))
        hand.append(Card(name='C3'))
        hand.append(Card(name='D5'))
        hand.append(Card(name='S4'))
        hand.append(Card(name='D3'))
        hand.append(Card(name='S10'))
        hand.append(Card(name='D14'))
        
        player = game.players[0]
        
        is_straight = player.is_straight(hand)
        
        self.assertFalse(is_straight)
        
    def test_is_four_of_a_kind_returns_number(self):
        game = Game()
        
        hand = []
            
        hand.append(Card(name='C2'))
        hand.append(Card(name='D2'))
        hand.append(Card(name='S2'))
        hand.append(Card(name='H2'))
        hand.append(Card(name='D3'))
        hand.append(Card(name='S10'))
        hand.append(Card(name='D14'))
        
        player = game.players[0]
        
        is_four_of_a_kind = player.is_four_of_a_kind(hand)
        
        self.assertEqual(is_four_of_a_kind, 2)
        
    def test_isnt_four_of_a_kind_returns_false(self):
        game = Game()
        
        hand = []
            
        hand.append(Card(name='C2'))
        hand.append(Card(name='D6'))
        hand.append(Card(name='S2'))
        hand.append(Card(name='H2'))
        hand.append(Card(name='D3'))
        hand.append(Card(name='S10'))
        hand.append(Card(name='D14'))
        
        player = game.players[0]
        
        is_four_of_a_kind = player.is_four_of_a_kind(hand)
        
        self.assertFalse(is_four_of_a_kind)
        
    def test_is_three_of_a_kind_returns_high_card(self):
        game = Game()
        
        hand = []
            
        hand.append(Card(name='C2'))
        hand.append(Card(name='D2'))
        hand.append(Card(name='S2'))
        hand.append(Card(name='H3'))
        hand.append(Card(name='D3'))
        hand.append(Card(name='S3'))
        hand.append(Card(name='D14'))
        
        player = game.players[0]
        
        is_three_of_a_kind = player.is_three_of_a_kind(hand)
        
        self.assertEqual(is_three_of_a_kind, 3)
        
    def test_isnt_three_of_a_kind_returns_false(self):
        game = Game()
        
        hand = []
            
        hand.append(Card(name='C2'))
        hand.append(Card(name='D3'))
        hand.append(Card(name='S4'))
        hand.append(Card(name='H5'))
        hand.append(Card(name='D6'))
        hand.append(Card(name='S7'))
        hand.append(Card(name='D8'))
        
        player = game.players[0]
        
        is_three_of_a_kind = player.is_three_of_a_kind(hand)
        
        self.assertFalse(is_three_of_a_kind)
        
        
    def test_is_pair_returns_value(self):
        game = Game()
        
        hand = []
            
        hand.append(Card(name='C2'))
        hand.append(Card(name='D2'))
        hand.append(Card(name='S3'))
        hand.append(Card(name='H4'))
        hand.append(Card(name='D5'))
        hand.append(Card(name='S6'))
        hand.append(Card(name='D7'))
        
        player = game.players[0]
        
        is_pair = player.is_pair(hand)
        
        self.assertEqual(is_pair, 2) 
        
    def test_isnt_pair_returns_false(self):
        game = Game()
        
        hand = []
            
        hand.append(Card(name='C14'))
        hand.append(Card(name='D2'))
        hand.append(Card(name='S3'))
        hand.append(Card(name='H4'))
        hand.append(Card(name='D5'))
        hand.append(Card(name='S6'))
        hand.append(Card(name='D7'))
        
        player = game.players[0]
        
        is_pair = player.is_pair(hand)
        
        self.assertFalse(is_pair) 
        
    def test_is_full_house_returns_tuple(self):
        game = Game()
        
        hand = []
            
        hand.append(Card(name='C2'))
        hand.append(Card(name='D2'))
        hand.append(Card(name='S3'))
        hand.append(Card(name='H3'))
        hand.append(Card(name='D3'))
        hand.append(Card(name='S6'))
        hand.append(Card(name='D6'))
        
        player = game.players[0]
        
        is_full_house = player.is_full_house(hand)
        
        self.assertEqual(is_full_house, (3,6))
        
    def test_is_two_pair_returns_tuple(self):
        game = Game()
        
        hand = []
            
        hand.append(Card(name='C2'))
        hand.append(Card(name='D2'))
        hand.append(Card(name='S3'))
        hand.append(Card(name='H3'))
        hand.append(Card(name='D7'))
        hand.append(Card(name='S9'))
        hand.append(Card(name='D9'))
        
        player = game.players[0]
        
        is_two_pair = player.is_two_pair(hand)
        
        self.assertEqual(is_two_pair, (9,3))
        
    def test_isnt_two_pair_returns_false(self):
        game = Game()
        
        hand = []
            
        hand.append(Card(name='C2'))
        hand.append(Card(name='D2'))
        hand.append(Card(name='S3'))
        hand.append(Card(name='H4'))
        hand.append(Card(name='D7'))
        hand.append(Card(name='S10'))
        hand.append(Card(name='D11'))
        
        player = game.players[0]
        
        is_two_pair = player.is_two_pair(hand)
        
        self.assertFalse(is_two_pair)
        
    def test_get_high_card_returns_highest(self):
        game = Game()
        
        hand = []
            
        hand.append(Card(name='C13'))
        hand.append(Card(name='D2'))
        hand.append(Card(name='S3'))
        hand.append(Card(name='H4'))
        hand.append(Card(name='D7'))
        hand.append(Card(name='S10'))
        hand.append(Card(name='D11'))
        
        player = game.players[0]
        
        high_card = player.get_high_card(hand)
        
        self.assertEqual(high_card, 13)
        

class CardTestCase(TestCase):
    def test_can_create_card(self):
        card = Card('D2')
        
        self.assertEqual(card.name, 'D2')

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
    

"""
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
     """   