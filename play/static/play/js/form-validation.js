$(".form-check-input").change(function() {  
    
    var checked = this.checked;
    var hand = $(this).parents(".hand");
    
    if (checked) {
        console.log('wtf');
        hand.find(".form-control").removeAttr("disabled");
    } else {
        console.log('nwtf');
        hand.find(".form-control").prop("disabled", true);
    }
    /*
    hand.find(".form-control").each(function() {
        console.log('wtf');
        if (checked) {
            console.log('check');
            $(this).removeAttr("disabled");
        } else {
            console.log('notcheck');
            $(this).attr("disabled");
        }
    })*/
});

function getDuplicateCards() {
    
    //Add all cards currently selected to list
    var cards = [];
    $(".hand").each(function() {
        var card1 = $(this).find("select[name=suit1]").val() + $(this).find("select[name=number1]").val();
        
        var card2 = $(this).find("select[name=suit2]").val() + $(this).find("select[name=number2]").val();
        
        cards.push(card1);
        cards.push(card2);
    });
    
    //Create list of duplicate cards
    var duplicate_cards = [];
    for (var i=0; i < cards.length; i++) {
        var icard = cards[i];
        var count = 0;
        
        if (duplicate_cards.includes(icard)) { continue; }
        if (icard === "") { continue; }
        
        for (var j=0; j < cards.length; j++) {
            var jcard = cards[j];
            if (jcard === icard) {
                count++;
            }
        }
        if (count > 1) {
            duplicate_cards.push(icard);
        }
    }

    return duplicate_cards;
}

$(".form-control").change(function() {  
    
    $(".form-control").removeClass("is-invalid");
    $(".invalid-feedback").remove();
    
    var duplicate_cards = getDuplicateCards();
    $(".hand").each(function() {
        
        var card = $(this).find("select[name=suit1]").val() + $(this).find("select[name=number1]").val();
        
        if (duplicate_cards.includes(card)) {
            var suit = $(this).find("select[name=suit1]")
            var number = $(this).find("select[name=number1]")
            suit.addClass("is-invalid");
            number.addClass("is-invalid");
            number.after("<div class='invalid-feedback'>Can't have more than one of the same card</div>");
            //allow_submit = false;
        }
        
        card = $(this).find("select[name=suit2]").val() + $(this).find("select[name=number2]").val();
        
        if (duplicate_cards.includes(card)) {
            var suit = $(this).find("select[name=suit2]")
            var number = $(this).find("select[name=number2]")
            suit.addClass("is-invalid");
            number.addClass("is-invalid");
            number.after("<div class='invalid-feedback'>Can't have more than one of the same card</div>");
            //allow_submit = false;
        }
        
    });

    //return allow_submit;

});