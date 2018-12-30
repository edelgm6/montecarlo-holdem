from django.db import models
from play.handsorter import HandSorter
from play.rules import Suit, Hand, Stage
from random import shuffle

class Simulation:
    def __init__(self, runs=1000, user_hand=[], additional_players=1, additional_hands=[]):
        self.runs = runs
        # Strip out '' values
        self.user_hand = [card for card in user_hand if card]
        self.additional_players = additional_players
        self.additional_hands = additional_hands
        
        
        self.user = Player(is_user=True, starting_hand=self.user_hand)
        self.results = self.generate_results_dict()
        self.wins = 0
        self.losses = 0
        self.ties = 0
        
        """
        TODO
        Update such that this can take only 1 card in a hand
        """
        
        self.other_players = []
        for i in range(additional_players):
            try:
                starting_hand = [card for card in additional_hands[i] if card]
            except IndexError:
                starting_hand = []
                
            self.other_players.append(Player(starting_hand=starting_hand))
            
        self.all_players = [self.user] + self.other_players
        
    def generate_results_dict(self):

        results = {}
        
        for h in Hand:
            results[str(h)] = {'count': 0, 'wins': 0, 'ties': 0, 'losses': 0}
        
        return results
        
    def run_simulation(self):
        
        for run in range(self.runs):
            for player in self.all_players:
                player.hand = []
            
            game = Game(players=self.all_players)
            game.deal()
            game.deal()
            game.deal()
            game.deal()
            game.set_player_hands()
            
            winners = game.get_winning_player()
            hand_results = self.results[str(self.user.best_hand['score'])]
            hand_results['count'] += 1
            
            if self.user in winners:
                if len(winners) == 1:
                    self.wins +=1
                    hand_results['wins'] += 1
                else:
                    self.ties += 1
                    hand_results['ties'] += 1
            else:
                self.losses += 1
                hand_results['losses'] += 1
                     
class Game:
    def __init__(self, players):
        self.deck = Deck()
        self.stage = Stage.PREDEAL
        self.players = players
        self.community = []
            
    def deal(self):
        if self.stage == Stage.PREDEAL:
            
            players_with_starting_hands = [player for player in self.players if player.starting_hand]
            
            for player in players_with_starting_hands:
                starting_hand = player.starting_hand
                for card in self.deck.cards:
                    if repr(card) in starting_hand:
                        player.hand.append(card) 
                        if len(player.hand) == len(starting_hand):
                            break    
            
            current_hands = [player.hand for player in players_with_starting_hands]
            for hand in current_hands:
                for card in hand:
                    self.deck.cards.remove(card)
                
            players_with_remaining_hands = [player for player in self.players if len(player.hand) != 2]
            for i in range(2):
                for player in players_with_remaining_hands:
                    if len(player.hand) == 2:
                        continue
                    else:
                        card = self.deck.cards.pop()
                        player.hand.append(card) 
      
            self.stage = Stage.PREFLOP
        
        elif self.stage == Stage.PREFLOP:
            #burn a card
            self.deck.cards.pop()
            
            flop = self.deck.cards[-3:]
            self.community = flop
            self.deck.cards = self.deck.cards[:-3]
            
            self.stage = Stage(self.stage.value + 1)
        
        elif self.stage.value < Stage.RIVER.value:
            self.deck.cards.pop()
            
            self.community.append(self.deck.cards.pop())
            self.stage = Stage(self.stage.value + 1)
     
    
    #Get rid of this and fold into the get_winning_player method
    def set_player_hands(self):
        for player in self.players:
            player.best_hand = HandSorter.get_best_hand(player.hand + self.community)
            
    def get_winning_player(self):
        
        contenders = [self.players[0]]
        for player in self.players[1:]:
            top_score = contenders[0].best_hand['score'].value
            player_score = player.best_hand['score'].value
            if player_score == top_score:
                contenders.append(player)
            elif player_score < top_score:
                contenders = [player]
          
        if len(contenders) > 1:
            winners = self.break_tie(contenders)
        else:
            winners = contenders
            
        return winners
    
    def break_tie(self, players):
        score = players[0].best_hand['score']
        if score == Hand.FULL_HOUSE:
            cards = [0, 3]
        elif score == Hand.TWO_PAIR:
            cards = [0, 2, 4]
        elif score == Hand.FLUSH or score == Hand.HIGH_CARD:
            cards = range(5)
        elif score == Hand.STRAIGHT or score == Hand.STRAIGHT_FLUSH:
            cards = [0]
        elif score == Hand.FOUR_OF_A_KIND:
            cards = [0, 4]
        elif score == Hand.THREE_OF_A_KIND:
            cards = [0, 3, 4]
        elif score == Hand.PAIR:
            cards = [0, 2, 3, 4]
        
        top_players = [players[0]]
        for player in players[1:]:
            append_player = True
            top_hand = top_players[0].best_hand['hand']
            player_hand = player.best_hand['hand']

            for i in cards:
                if top_hand[i].number < player_hand[i].number:
                    top_players = [player]
                    append_player = False
                elif top_hand[i].number > player_hand[i].number:
                    append_player = False
                    break

            if append_player:
                top_players.append(player)

        return top_players
            
class Player:
    def __init__(self, is_user=False, starting_hand=[]):
        self.hand = []
        self.starting_hand = starting_hand
        self.is_user = is_user
        
    def get_hand(self):
        return [repr(self.hand[0]), repr(self.hand[1])]
               
class Deck:
    def __init__(self):
        suits = [s for s in Suit]
        numbers = [2,3,4,5,6,7,8,9,10,11,12,13,14]
        self.cards = [Card(suit=suit, number=number) for suit in suits for number in numbers]
            
        shuffle(self.cards)
        
class Card:
    def __init__(self, suit, number):
        self._suit = suit
        self._number = number

    def __repr__(self):
        return self._suit.value + str(self._number)
    
    @property
    def suit(self):
        return self._suit
    
    @suit.setter
    def suit(self, suit):
        if suit not in [suit for suit in Suit]:
            raise Exception('Suit must be value in Suit enum')
                                   
    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, number):
        if number not in range(2,15):
            raise Exception('Number must be between 2-14, got ' + number)