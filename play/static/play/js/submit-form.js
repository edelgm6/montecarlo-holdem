jQuery.ajaxSettings.traditional = true

$("#pokerForm").validate({
  submitHandler: function(form) {
    // do other things for a valid form
    //form.submit();
  }
});


/* attach a submit handler to the form */
$("#pokerForm").submit(function(event) {
    console.log($('#id_user_suit_1').val())
    console.log([$('#id_user_suit_1').val() + $('#id_user_number_1').val(), $('#id_user_suit_2').val() + $('#id_user_number_2').val()])
    /* stop form from submitting normally */
    event.preventDefault();

    /* get the action attribute from the <form action=""> element */
    var $form = $( this ),
      url = $form.attr( 'action' );

    var post_data = {
        'runs': $('#id_runs').val(),
        'user_hand': [$('#id_user_suit_1').val() + $('#id_user_number_1').val(), $('#id_user_suit_2').val() + $('#id_user_number_2').val()],
        'additional_players': 1
    };

    console.log(post_data);
    
    /* Send the data using post with element id name and name2*/
    var posting = jQuery.post( url, post_data );

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
    });
    
});

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