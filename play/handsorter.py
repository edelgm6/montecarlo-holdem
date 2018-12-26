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
            return is_hand
        
        is_hand = HandSorter.is_four_of_a_kind(hand)
        if is_hand:
            return is_hand
        
        is_hand = HandSorter.is_full_house(hand)
        if is_hand:
            return is_hand
        
        is_hand = HandSorter.is_flush(hand)
        if is_hand:
            return is_hand
        
        is_hand = HandSorter.is_straight(hand)
        if is_hand:
            return is_hand
        
        is_hand = HandSorter.is_three_of_a_kind(hand)
        if is_hand:
            return is_hand
        
        is_hand = HandSorter.is_two_pair(hand)
        if is_hand:
            return is_hand
        
        is_hand = HandSorter.is_pair(hand)
        if is_hand:
            return is_hand
        
        high_card = HandSorter.get_high_card(hand)
        return high_card
    
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
        print(numbers)
        ordered_hand = HandSorter.sort_cards(hand)
        
        high_straight_card = False
        for card in ordered_hand[:3]:
            if (card.number - 1 in numbers
                and card.number - 2 in numbers
                and card.number - 3 in numbers
                and card.number - 4 in numbers):
                    high_straight_card = card
                    print(high_straight_card)
                    break
        
        if not high_straight_card:
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
        
        pair_number = False
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
        
        try:
            pair.append(sorted_hand[1])
            pair.append(sorted_hand[2])
        except IndexError:
            pass
            
        return {'score': Hand.PAIR, 'hand': pair}
    
    
    """
    TODO
    Refactor to call some method that grabs the high pair from a deck
    and returns that high pair?
    """
    @staticmethod
    def is_two_pair(hand):
        high_pair_hand = HandSorter.is_pair(hand)
        
        if high_pair_hand:
            hand_without_pair, high_pair = HandSorter.get_split_hands(hand, high_pair_hand['hand'][0].number)
            low_pair_hand = HandSorter.is_pair(hand_without_pair)
            
            low_pair = False
            if not low_pair_hand:
                return False
            else:
                remaining_hand, low_pair = HandSorter.get_split_hands(low_pair_hand['hand'], low_pair_hand['hand'][0].number)
                
            sorted_hand = HandSorter.sort_cards(remaining_hand)
            
            two_pair = [high_pair, low_pair, sorted_hand[0]]
            
            return {'score': Hand.TWO_PAIR, 'hand': two_pair}
                 
        return False
    
    @staticmethod
    def is_full_house(hand):
        three_of_a_kind_hand = HandSorter.is_three_of_a_kind(hand)
        
        if three_of_a_kind_hand:
            hand_without_three_cards, three_of_a_kind = HandSorter.get_split_hands(hand, three_of_a_kind_hand['hand'][0].number)
            
            two_of_a_kind_hand = HandSorter.is_pair(hand_without_three_cards)
            if two_of_a_kind_hand:
                hand_without_pair_cards, pair = HandSorter.get_split_hands(two_of_a_kind_hand['hand'], two_of_a_kind_hand['hand'][0].number)
                return {'score': Hand.FULL_HOUSE, 'hand': [three_of_a_kind, pair]}
            
        return False
    
    @staticmethod
    def get_high_card(hand):
        sorted_hand = HandSorter.sort_cards(hand)
        
        return {'score': Hand.HIGH_CARD, 'hand': sorted_hand[:5]}