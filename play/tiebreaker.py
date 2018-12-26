from play.rules import Stage, Suit, Hand

class TieBreaker:
    
    @staticmethod
    def break_tie(players):
        score = players[0].best_hand['score']
        print(score)
        
        if (score == Hand.STRAIGHT or score == Hand.STRAIGHT_FLUSH):
            winners = TieBreaker.break_straight(players)
            
        if score == Hand.FLUSH:
            winners = TieBreaker.break_flush(players)
            
        return winners
        
    def break_flush(players):
        
        top_players = [players[0]]
        for player in players[1:]:
            print(player)
            print(player.best_hand['score'])
            for card in player.best_hand['hand']:
                print(card.suit)
                print(card.number)
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
            
        