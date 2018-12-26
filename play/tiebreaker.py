from play.rules import Stage, Suit, Hand

class TieBreaker:
    
    @staticmethod
    def break_tie(players):
        score = players[0].best_hand['score']
        
        if score == Hand.STRAIGHT:
            winners = TieBreaker.break_straight(players)
            
        return winners
        
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
            
        