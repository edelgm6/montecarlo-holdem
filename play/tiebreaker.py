from play.rules import Stage, Suit, Hand

"""
Note: All methods assume that player hands are pre-sorted from highest to lowest number
"""

class TieBreaker:
    
    """
    TODO:
    Break all methods up into DRY components -- e.g.:
        
        top_players = [players[0]]
        for player in players[1:]:
            append_player = True
            top_hand = top_players[0].best_hand['hand']
            player_hand = player.best_hand['hand']
    
    """
    
    @staticmethod
    def break_tie(players):
        score = players[0].best_hand['score']
        
        if (score == Hand.STRAIGHT or score == Hand.STRAIGHT_FLUSH):
            winners = TieBreaker.break_straight(players)
            
        if score == Hand.FLUSH:
            winners = TieBreaker.break_flush(players)
            
        if (score == Hand.FOUR_OF_A_KIND 
            or score == Hand.THREE_OF_A_KIND
            or score == Hand.PAIR):
            
            winners = TieBreaker.break_of_a_kind(players)
            
        if score == Hand.TWO_PAIR:
            winners = TieBreaker.break_two_pair(players)
            
        if score == Hand.FULL_HOUSE:
            winners = TieBreaker.break_full_house(players)
            
        if score == Hand.HIGH_CARD:
            winners = TieBreaker.break_high_card(players)
            
        return winners
    
    @staticmethod
    def break_high_card(players):
        top_players = [players[0]]
        for player in players[1:]:
            append_player = True
            top_hand = top_players[0].best_hand['hand']
            player_hand = player.best_hand['hand']
            
            for i in range(0, len(top_hand)):
                if top_hand[i].number < player_hand[i].number:
                    top_players = [player]
                    append_player = False
                elif top_hand[i].number > player_hand[i].number:
                    append_player = False
                    break
                    
            if append_player:
                top_players.append(player)
                
            return top_players
    
    
    @staticmethod
    def break_full_house(players):
        
        top_players = [players[0]]
        for player in players[1:]:
            append_player = True
            top_hand = top_players[0].best_hand['hand']
            player_hand = player.best_hand['hand']
            
            for i in [0, 3]:
                if top_hand[i].number < player_hand[i].number:
                    top_players = [player]
                    append_player = False
                elif top_hand[i].number > player_hand[i].number:
                    append_player = False
                    break
                    
        if append_player:
            top_players.append(player)
                
        return top_players


    @staticmethod
    def break_two_pair(players):
        
        top_players = [players[0]]
        for player in players[1:]:
            append_player = True
            top_hand = top_players[0].best_hand['hand']
            player_hand = player.best_hand['hand']
            
            for i in [0, 2, 4]:
                if top_hand[i].number < player_hand[i].number:
                    top_players = [player]
                    append_player = False
                elif top_hand[i].number > player_hand[i].number:
                    append_player = False
                    break
                    
        if append_player:
            top_players.append(player)
                
        return top_players
    
    
    @staticmethod
    def break_of_a_kind(players):
        score = players[0].best_hand['score']
        if score == Hand.FOUR_OF_A_KIND:
            index = 4
        elif score == Hand.THREE_OF_A_KIND:
            index = 3
        elif score == Hand.PAIR:
            index = 2

        top_players = [players[0]]
        for player in players[1:]:
            append_player = True
            top_hand = top_players[0].best_hand['hand']
            player_hand = player.best_hand['hand']       

            if top_hand[0].number < player_hand[0].number:
                top_players = [player] 
            elif top_hand[0].number == player_hand[0].number:

                for i in range(index, 5):
                    if top_hand[i].number < player_hand[i].number:
                        top_players = [player]
                        append_player = False
                    elif top_hand[i].number > player_hand[i].number:
                        append_player = False
                        break
                        
            if append_player:
                top_players.append(player)
                        
        return top_players
    
    @staticmethod
    def break_flush(players):
        
        top_players = [players[0]]
        for player in players[1:]:
            top_hand = top_players[0].best_hand['hand']
            player_hand = player.best_hand['hand']
            
            append_player = True
            for i in range(5):
                if top_hand[i].number < player_hand[i].number:
                    top_players = [player]
                    append_player = False
                    break
                elif top_hand[i].number > player_hand[i].number:
                    append_player = False
                    break
                
            if append_player:
                top_players.append(player)
                
        return top_players
    
    @staticmethod
    def break_straight(players):
        
        top_players = [players[0]]
        for player in players[1:]:
            top_hand = top_players[0].best_hand['hand'][0].number
            player_hand = player.best_hand['hand'][0].number
            if player_hand > top_hand:
                top_players = [player]
            if player_hand == top_hand:
                top_players.append(player)
                
        return top_players
            
        