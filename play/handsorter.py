from play.rules import Stage, Suit, Hand

class HandSorter:
    
    @staticmethod
    def get_split_hands(hand, card_number):
        hand_without_cards = [card for card in hand if card.number != card_number]
        hand_with_cards = [card for card in hand if card.number == card_number]
        
        return hand_without_cards, hand_with_cards
    
    @staticmethod
    def get_hand_numbers(hand):
        numbers = []
        for card in hand:
            numbers.append(card.number)
            
        return numbers
    
    @staticmethod
    def sort_cards(hand):
        n = len(hand) 
  
        # Traverse through all array elements 
        for i in range(n): 

            # Last i elements are already in place 
            for j in range(0, n-i-1): 

                # traverse the array from 0 to n-i-1 
                # Swap if the element found is greater 
                # than the next element 
                if hand[j].number < hand[j+1].number : 
                    hand[j], hand[j+1] = hand[j+1], hand[j]
        
        return hand
    
    def get_best_hand(hand):
        is_hand = HandSorter.is_straight_flush(hand)
        if is_hand:
            return (Hand.STRAIGHT_FLUSH, is_hand)
        
        is_hand = HandSorter.is_four_of_a_kind(hand)
        if is_hand:
            return (Hand.FOUR_OF_A_KIND, is_hand)
        
        is_hand = HandSorter.is_full_house(hand)
        if is_hand:
            return (Hand.FULL_HOUSE, is_hand)
        
        is_hand = HandSorter.is_flush(hand)
        if is_hand:
            return (Hand.FLUSH, is_hand)
        
        is_hand = HandSorter.is_straight(hand)
        if is_hand:
            return (Hand.STRAIGHT, is_hand)
        
        is_hand = HandSorter.is_three_of_a_kind(hand)
        if is_hand:
            return (Hand.THREE_OF_A_KIND, is_hand)
        
        is_hand = HandSorter.is_two_pair(hand)
        if is_hand:
            return (Hand.TWO_PAIR, is_hand)
        
        is_hand = HandSorter.is_pair(hand)
        if is_hand:
            return (Hand.PAIR, is_hand)
        
        high_card = HandSorter.get_high_card(hand)
        return (Hand.HIGH_CARD, high_card)
    
    """
    TODO
    Test all methods for robustness of getting fewer than 7 cards/fewer than 5 cards"""
    @staticmethod
    def is_straight_flush(hand):
        is_flush = HandSorter.is_flush(hand)
        if not is_flush:
            return False
        
        flush_suit = is_flush['hand'][0].suit
        
        single_suit_cards = []
        for card in hand:
            if card.suit == flush_suit:
                single_suit_cards.append(card)
                
        ordered_hand = HandSorter.sort_cards(single_suit_cards)
        test_hands = []
        for i in range(0,len(ordered_hand) - 4):
            test_hands.append(ordered_hand[i:i+5])
        
        for hand in test_hands:

            is_straight = HandSorter.is_straight(hand)
        
            if is_straight:
                return {'score': Hand.STRAIGHT_FLUSH, 'hand': hand}
        
        return False
    
    @staticmethod
    def is_flush(hand):
        suits = []
        for card in hand:
            suits.append(card.suit)
            
        for suit in [s for s in Suit]:
            if suits.count(suit) >= 5:
                flush_suit = suit
                
                flush_hand = []
                for card in hand:
                    if card.suit == flush_suit:
                        flush_hand.append(card)
                        
                ordered_flush_hand = HandSorter.sort_cards(flush_hand)
                return {'score': Hand.FLUSH, 'hand': ordered_flush_hand[:5]}
        
        return False
    
    @staticmethod
    def is_straight(hand):
        numbers = HandSorter.get_hand_numbers(hand)
        ordered_hand = HandSorter.sort_cards(hand)
        
        high_straight_card = False
        for card in ordered_hand[:3]:
            if (card.number - 1 in numbers
                and card.number - 2 in numbers
                and card.number - 3 in numbers
                and card.number - 4 in numbers):
                    high_straight_card = card
                    break
            else:
                return False
            
        cards_to_eval = ordered_hand[ordered_hand.index(high_straight_card):]
        straight_hand = [cards_to_eval[0]]
        for card in cards_to_eval[1:]:
            hand_length = len(straight_hand)
            if hand_length == 5:
                break
            
            if card.number < straight_hand[hand_length - 1].number:
                straight_hand.append(card)
                
        return {'score': Hand.STRAIGHT, 'hand': straight_hand}
            
    
    @staticmethod
    def is_four_of_a_kind(hand):
        numbers = HandSorter.get_hand_numbers(hand)
        
        four_of_a_kind_number = False
        for number in numbers[:4]:
            if numbers.count(number) == 4:
                four_of_a_kind_number = number
                break
                
        if not four_of_a_kind_number:
            return False
        
        hand_without_cards, hand_with_cards = HandSorter.get_split_hands(hand, four_of_a_kind_number)
        
        four_of_a_kind = hand_with_cards
        
        sorted_hand = HandSorter.sort_cards(hand_without_cards)
        four_of_a_kind.append(sorted_hand[0])
                              
        return {'score': Hand.FOUR_OF_A_KIND, 'hand': four_of_a_kind}
    
    @staticmethod
    def is_three_of_a_kind(hand):
        numbers = HandSorter.get_hand_numbers(hand)
        numbers.sort(reverse=True)
        
        three_of_a_kind_number = False
        for number in numbers[:5]:
            if numbers.count(number) == 3:
                three_of_a_kind_number = number
                break
                
        if not three_of_a_kind_number:
            return False
        
        hand_without_cards, hand_with_cards = HandSorter.get_split_hands(hand, three_of_a_kind_number)
        
        three_of_a_kind = hand_with_cards
        
        sorted_hand = HandSorter.sort_cards(hand_without_cards)
        
        three_of_a_kind.append(sorted_hand[0])
        three_of_a_kind.append(sorted_hand[1])
            
        return {'score': Hand.THREE_OF_A_KIND, 'hand': three_of_a_kind}
    
    @staticmethod
    def is_pair(hand):
        numbers = HandSorter.get_hand_numbers(hand)
        numbers.sort(reverse=True)
        
        for number in numbers[:6]:
            if numbers.count(number) == 2:
                pair_number = number
                break
                
        if not pair_number:
            return False
        
        hand_without_cards, hand_with_cards = HandSorter.get_split_hands(hand, pair_number)
        
        pair = hand_with_cards
        
        sorted_hand = HandSorter.sort_cards(hand_without_cards)
        
        pair.append(sorted_hand[0])
        pair.append(sorted_hand[1])
        pair.append(sorted_hand[2])
            
        return {'score': Hand.PAIR, 'hand': pair}
    
    @staticmethod
    def is_two_pair(hand):
        high_pair_value = HandSorter.is_pair(hand)
        
        if high_pair_value:
            hand_without_pair = HandSorter.get_stripped_hand(hand, high_pair_value)
            low_pair_value = HandSorter.is_pair(hand_without_pair)
            
            if low_pair_value:
                return (high_pair_value, low_pair_value)
            
        return False
    
    @staticmethod
    def is_full_house(hand):
        three_of_a_kind_value = HandSorter.is_three_of_a_kind(hand)
        
        if three_of_a_kind_value:
            hand_without_three_cards = HandSorter.get_stripped_hand(hand, three_of_a_kind_value)
            
            two_of_a_kind_value = HandSorter.is_pair(hand_without_three_cards)
            if two_of_a_kind_value:
                return (three_of_a_kind_value, two_of_a_kind_value)
            
        return False
    
    @staticmethod
    def get_high_card(hand):
        numbers = HandSorter.get_hand_numbers(hand)
            
        numbers.sort()
        
        return numbers.pop()