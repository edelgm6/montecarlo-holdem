from enum import Enum

class Stage(Enum):
    PREDEAL = 0
    PREFLOP = 1
    FLOP = 2
    TURN = 3
    RIVER = 4
    
class Suit(Enum):
    HEART = 'H'
    SPADE = 'S'
    CLUB = 'C'
    DIAMOND = 'D'
    
class Hand(Enum):
    STRAIGHT_FLUSH = 1
    FOUR_OF_A_KIND = 2
    FULL_HOUSE = 3
    FLUSH = 4
    STRAIGHT = 5
    THREE_OF_A_KIND = 6
    TWO_PAIR = 7
    PAIR = 8
    HIGH_CARD = 9