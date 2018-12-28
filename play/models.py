from django.db import models
from play.handsorter import HandSorter
from play.rules import Suit, Hand, Stage
from random import shuffle

class Simulation:
    def __init__(self, runs=1000, additional_players=1, user_hand=[], *args):
        self.runs = runs
        self.user = Player(is_user=True)
        self.user_hand = user_hand
        
        self.other_players = []
        for player in range(additional_players):
            self.other_players.append(Player())
            
        self.all_players = [self.user] + self.other_players
        
    def run_simulation(self):
        
        results = {}
        for h in Hand:
            results[h] = {'count': 0, 'wins': 0, 'ties': 0}
        results['wins'] = 0
        results['ties'] = 0
        results['losses'] = 0
        
        
        for run in range(self.runs):
            for player in self.all_players:
                player.hand = []
            
            game = Game(other_players=self.other_players, user=self.user, user_hand=self.user_hand)
            game.deal()
            game.deal()
            game.deal()
            game.deal()
            game.set_player_hands()
            
            winners = game.get_winning_player()
            user_results = results[self.user.best_hand['score']]
            user_results['count'] += 1
            
            if self.user in winners:
                if len(winners) == 1:
                    results['wins'] +=1
                    user_results['wins'] += 1
                else:
                    results['ties'] += 1
                    user_results['ties'] += 1
            else:
                results['losses'] += 1
        
        return results
                     
class Game:
    def __init__(self, other_players, user, user_hand):
        self.deck = Deck()
        self.stage = Stage.PREDEAL
        self.user = user
        self.user_hand = user_hand
        self.other_players = other_players
        self.all_players = [user] + self.other_players
        self.community = []
            
    def deal(self):
        if self.stage == Stage.PREDEAL:
            if self.user_hand:
                user_cards = []
                for card in self.deck.cards:
                    if (card.suit == self.user_hand[0].suit and card.number == self.user_hand[0].number) or (card.suit == self.user_hand[1].suit and card.number == self.user_hand[1].number):
                        user_cards.append(card)
                        if len(user_cards) == 2:
                            break
                    
                self.user.hand.append(user_cards[0])
                self.user.hand.append(user_cards[1])
                self.deck.cards.remove(user_cards[0])
                self.deck.cards.remove(user_cards[1])
                if len(self.user.hand) == 1:
                    print(self.user.hand[0].suit)
                    print(self.user.hand[0].number)
                    print(len(self.deck.cards))
                
                #print(len(self.user.hand))
                for round in range(2):
                    for player in self.other_players:
                        card = self.deck.cards.pop()
                        player.hand.append(card)
            else:
                for round in range(2):
                    for player in self.all_players:
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
        for player in self.all_players:
            player.best_hand = HandSorter.get_best_hand(player.hand + self.community)
            
    def get_winning_player(self):
        
        contenders = [self.all_players[0]]
        for player in self.all_players[1:]:
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
        self.hand = starting_hand
        self.is_user = is_user
               
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