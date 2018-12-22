from play.models import Stage, Suit

class HandSorter:
    #def __init__(self, hand):
    #    self.hand = []
    @staticmethod
    def get_suit(card):
        return card.name[0]
    
    @staticmethod
    def get_number(card):
        chars = len(card.name)
        return int(card.name[-(chars - 1):])
    
    def get_stripped_hand(hand, card_number_to_remove):
        hand_without_cards = [card for card in hand if HandSorter.get_number(card) != card_number_to_remove]
        
        return hand_without_cards
    
    def get_hand_numbers(hand):
        numbers = []
        for card in hand:
            numbers.append(HandSorter.get_number(card))
            
        return numbers
    
    def is_straight_flush(hand):
        is_flush = HandSorter.is_flush(hand)
        is_straight = HandSorter.is_straight(hand)
        
        if (is_flush and is_straight):
            return is_straight
        
        return False
    
    @staticmethod
    def is_flush(hand):
        suits = []
        for card in hand:
            suits.append(HandSorter.get_suit(card))
            
        for suit in [s.value for s in Suit]:
            if suits.count(suit) >= 5:
                high_card = 0
                
                for card in hand:
                    if HandSorter.get_suit(card) == suit:
                        number = HandSorter.get_number(card)
                        if number > high_card:
                            high_card = number
                
                return high_card
        
        return False
    
    def is_straight(hand):
        numbers = HandSorter.get_hand_numbers(hand)
        
        numbers.sort(reverse=True)
        for number in numbers[:3]:
            if (number - 1 in numbers
                and number - 2 in numbers
                and number - 3 in numbers
                and number - 4 in numbers):
                    return number
        
        return False
    
    def is_four_of_a_kind(hand):
        numbers = HandSorter.get_hand_numbers(hand)
            
        for number in numbers[:4]:
            if numbers.count(number) == 4:
                return number
            
        return False
    
    def is_three_of_a_kind(hand):
        numbers = HandSorter.get_hand_numbers(hand)
            
        numbers.sort(reverse=True)
        
        for number in numbers[:5]:
            if numbers.count(number) == 3:
                return number
            
        return False
    
    def is_pair(hand):
        numbers = HandSorter.get_hand_numbers(hand)
            
        numbers.sort(reverse=True)
        
        for number in numbers[:6]:
            if numbers.count(number) == 2:
                return number
            
        return False
    
    def is_two_pair(hand):
        high_pair_value = HandSorter.is_pair(hand)
        
        if high_pair_value:
            hand_without_pair = HandSorter.get_stripped_hand(hand, high_pair_value)
            low_pair_value = HandSorter.is_pair(hand_without_pair)
            
            if low_pair_value:
                return (high_pair_value, low_pair_value)
            
        return False
    
    def is_full_house(hand):
        three_of_a_kind_value = HandSorter.is_three_of_a_kind(hand)
        
        if three_of_a_kind_value:
            hand_without_three_cards = HandSorter.get_stripped_hand(hand, three_of_a_kind_value)
            
            two_of_a_kind_value = HandSorter.is_pair(hand_without_three_cards)
            if two_of_a_kind_value:
                return (three_of_a_kind_value, two_of_a_kind_value)
            
        return False
    
    def get_high_card(hand):
        numbers = HandSorter.get_hand_numbers(hand)
            
        numbers.sort()
        
        return numbers.pop()