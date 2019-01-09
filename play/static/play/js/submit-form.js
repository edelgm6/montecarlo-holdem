jQuery.ajaxSettings.traditional = true

$("#pokerForm").submit(function(event) {
    event.preventDefault();
    
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
                console.log(typeof card2)
            }

            submit_hands.push(cards);
            
            additional_players++;
        }
    }
    
    var post_data = {
        runs: $("#id_runs").val(),
        user_hand: user_hand,
        additional_players: additional_players,
        additional_hands: submit_hands
        };
    
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
            console.log(data);
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
        console.log('come on now')
        handsChart['data']['datasets'][0]['data'] = wins;
        handsChart['data']['datasets'][1]['data'] = losses;
        handsChart['data']['datasets'][2]['data'] = ties;
        handsChart.update()
    };
}