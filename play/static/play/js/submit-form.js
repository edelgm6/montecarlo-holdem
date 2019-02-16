jQuery.ajaxSettings.traditional = true

$("#pokerForm").submit(function(event) {
    event.preventDefault();
    $('.overlay').show();
    
    
    //Build user hand
    var user_hand = [];
    var user_input = $("#user_hand")
    if ($(user_input).find("select[name=suit1]").val() != "" && $(user_input).find("select[name=number1]").val() != "") {
        var card1 = $(this).find("select[name=suit1]").val() + $(this).find("select[name=number1]").val();
        user_hand.push(card1);
    }

    if ($(user_input).find("select[name=suit2]").val() != "" && $(user_input).find("select[name=number2]").val() != "") {
        var card2 = $(this).find("select[name=suit2]").val() + $(this).find("select[name=number2]").val();
        user_hand.push(card2);
    }
    
    //Build flop
    var flop_hand = [];
    var flop = $("#flop")
    if ($(flop).find("select[name=suit1]").val() != "" && $(flop).find("select[name=number1]").val() != "") {
        var card1 = $(flop).find("select[name=suit1]").val() + $(flop).find("select[name=number1]").val();
        flop_hand.push(card1);
    }
    
    if ($(flop).find("select[name=suit2]").val() != "" && $(flop).find("select[name=number2]").val() != "") {
        var card2 = $(flop).find("select[name=suit2]").val() + $(flop).find("select[name=number2]").val();
        flop_hand.push(card2);
    }
    
    if ($(flop).find("select[name=suit3]").val() != "" && $(flop).find("select[name=number3]").val() != "") {
        var card3 = $(flop).find("select[name=suit3]").val() + $(flop).find("select[name=number3]").val();
        flop_hand.push(card3);
    }
    
    //Build turn
    var turn_card = '';
    var comm_card = $("#turn")
    if ($(comm_card).find("select[name=suit1]").val() != "" && $(comm_card).find("select[name=number1]").val() != "") {
        var card1 = $(comm_card).find("select[name=suit1]").val() + $(comm_card).find("select[name=number1]").val();
        turn_card=card1;
    }
    
    //Build river
    var river_card = '';
    var comm_card = $("#river")
    if ($(comm_card).find("select[name=suit1]").val() != "" && $(comm_card).find("select[name=number1]").val() != "") {
        var card1 = $(comm_card).find("select[name=suit1]").val() + $(comm_card).find("select[name=number1]").val();
        river_card=card1;
    }
    
    //Build other players' hands
    var other_hands = [
        $("#other_hand_1"),
        $("#other_hand_2"),
        $("#other_hand_3"),
        $("#other_hand_4")
    ];
    

    var submit_hands = [];
    var additional_players = 0;
    for (var i = 0; i < other_hands.length; i++) {
        var hand = other_hands[i];
        if ($(hand).find(".form-check-input").length === 0 || $(hand).find(".form-check-input").is(":checked")) {
            
            var cards = [];
            
            if ($(hand).find("select[name=suit1]").val() != "" && $(hand).find("select[name=number1]").val() != "") {
                var card1 = $(hand).find("select[name=suit1]").val() + $(hand).find("select[name=number1]").val();
                cards.push(card1);
            }

            if ($(hand).find("select[name=suit2]").val() != "" && $(hand).find("select[name=number2]").val() != "") {
                var card2 = $(hand).find("select[name=suit2]").val() + $(hand).find("select[name=number2]").val();
                cards.push(card2);
            }

            submit_hands.push(cards);
            
            additional_players++;
        }
    }
    
    var post_data = {
        runs: $("#id_runs").val(),
        user_hand: user_hand,
        additional_players: additional_players,
        additional_hands: submit_hands,
        flop_cards: flop_hand,
        turn_card: turn_card,
        river_card: river_card
        };
    
    console.log(post_data);
    
    /* Send the data using post with element id name and name2*/
    if (getDuplicateCards().length === 0) {
        /* get the action attribute from the <form action=""> element */
        var $form = $( this ),
          url = $form.attr( "action" );
        
        //var posting = jQuery.post( url, post_data );
        var posting = jQuery.ajax({
            url: url,
            type: "POST",
            data: JSON.stringify(post_data),
            dataType: "json",
            contentType: "application/json; charset=utf-8",
            success: function(){
            }
        });

        /* Alerts the results */
        posting.done(function( data ) {
            $('.overlay').removeAttr('style');
            console.log(data);
            
            writeResults(data);
            
            var results = data.results;
            var wins = [
                results.straight_flush.wins,
                results.four_of_a_kind.wins,
                results.full_house.wins,
                results.flush.wins,
                results.straight.wins,
                results.three_of_a_kind.wins,
                results.two_pair.wins,
                results.pair.wins,
                results.high_card.wins
            ];

            var ties = [
                results.straight_flush.ties,
                results.four_of_a_kind.ties,
                results.full_house.ties,
                results.flush.ties,
                results.straight.ties,
                results.three_of_a_kind.ties,
                results.two_pair.ties,
                results.pair.ties,
                results.high_card.ties
            ];

            var losses = [
                results.straight_flush.losses,
                results.four_of_a_kind.losses,
                results.full_house.losses,
                results.flush.losses,
                results.straight.losses,
                results.three_of_a_kind.losses,
                results.two_pair.losses,
                results.pair.losses,
                results.high_card.losses
            ];

            createHandsChart(wins, losses, ties);
            createWinChart(data.wins, data.losses, data.ties);
        });
        
    }

    
});

function writeResults (data) {
    var user_hand = data.user_hand;
    var other_count = data.additional_players;
    var other_hands = data.additional_hands;
    var flop = data.flop_cards;
    var turn = data.turn_card;
    var river = data.river_card;
    var runs = data.runs;
    var hand_block = $('.hands');
    
    hand_block.find("li").remove();
    
    $(".run-count").text(runs.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","));
    $(".player-count").text(other_count + 1);
    
    var suit_map = {
        D: 'Diamonds',
        S: 'Spades',
        C: 'Clubs',
        H: 'Hearts'
    }
    
    var number_map = {
        2: 'Two',
        3: 'Three',
        4: 'Four',
        5: 'Five',
        6: 'Six',
        7: 'Seven',
        8: 'Eight',
        9: 'Nine',
        10: 'Ten',
        11: 'Jack',
        12: 'Queen',
        13: 'King',
        14: 'Ace'
    }
    
    //Hands section
    var cards = ['Random card', 'Random card'];
    for (i=0; i < user_hand.length; i++) {
        var text = '';
        var card = user_hand[i];
        var suit = card[0];
        var number = card.slice((card.length - 1) * -1);
        
        text = number_map[parseInt(number, 10)] + ' of ' + suit_map[suit];
        cards[i] = text;
    }
    
    hand_block.append("<li>Main player: " + cards[0] + " / " + cards[1] + "</li>");
    
    cards = []
    for (i=0; i < other_count; i++) {
        cards.push(['Random card', 'Random card'])
    }
    
    for (i=0; i < other_hands.length; i++) {
        var hand = other_hands[i];
        for (j=0; j < hand.length; j++) {
            var text = '';
            var card = hand[j];
            var suit = card[0];
            var number = card.slice((card.length - 1) * -1);
            
            text = number_map[parseInt(number, 10)] + ' of ' + suit_map[suit];
            cards[i][j] = text;
        }
    } 
    
    for (i=0; i < other_count; i++) {
        hand_block.append(function() {
            return "<li>Other player: " + cards[i][0] + " / " + cards[i][1] + "</li>";
        });
    }
    
    //Community cards section
    var cards = ['Random card', 'Random card', 'Random card', 'Random card', 'Random card'];
    for (i=0; i < flop.length; i++) {
        var text = '';
        var card = flop[i];
        var suit = card[0];
        var number = card.slice((card.length - 1) * -1);
        
        text = number_map[parseInt(number, 10)] + ' of ' + suit_map[suit];
        cards[i] = text;
    }
    
    if (turn) {
        var text = '';
        var card = flop[i];
        var suit = turn[0];
        var number = turn.slice((turn.length - 1) * -1);
        
        text = number_map[parseInt(number, 10)] + ' of ' + suit_map[suit];
        cards[3] = text;        
    }
    
    if (river) {
        var text = '';
        var suit = river[0];
        var number = river.slice((river.length - 1) * -1);
        
        text = number_map[parseInt(number, 10)] + ' of ' + suit_map[suit];
        cards[4] = text;        
    }
    
    hand_block.append("<li>Community: " + cards[0] + " / " + cards[1] + " / " + cards[2] + " / " + cards[3] +" / " + cards[4] + "</li>");
    
    $('.results').css('visibility', 'visible');
    
}

function createWinChart (wins, losses, ties) {
    if (Object.keys(winChart).length==0) {
        buildWinChart(wins, losses, ties);
    } else {
        winChart['data']['datasets'][0]['data'] = [wins];
        winChart['data']['datasets'][1]['data'] = [losses];
        winChart['data']['datasets'][2]['data'] = [ties];
        winChart.update()
    };
}

function createHandsChart (wins, losses, ties) {
    if (Object.keys(handsChart).length==0) {
        buildHandsChart(wins, losses, ties);
    } else {
        handsChart['data']['datasets'][0]['data'] = wins;
        handsChart['data']['datasets'][1]['data'] = losses;
        handsChart['data']['datasets'][2]['data'] = ties;
        handsChart.update()
    };
}