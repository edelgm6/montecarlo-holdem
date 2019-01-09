function getDuplicateCards() {
    
    //Add all cards currently selected to list
    //TODO: Fix issue where we're checking for an 'active' player both in
    //the duplicateDards method and the Validation method
    var cards = [];
    $(".hand").each(function() {
        if ($(this).find(".form-check-input").length === 0 || $(this).find(".form-check-input").is(":checked")) {

            if ($(this).find("select[name=suit1]").val() != "" && $(this).find("select[name=number1]").val() != "") {
                var card1 = $(this).find("select[name=suit1]").val() + $(this).find("select[name=number1]").val();
                cards.push(card1);
            }

            if ($(this).find("select[name=suit2]").val() != "" && $(this).find("select[name=number2]").val() != "") {
                var card2 = $(this).find("select[name=suit2]").val() + $(this).find("select[name=number2]").val();
                cards.push(card2);
            }
        }
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
    console.log(duplicate_cards);
    return duplicate_cards;
}

//TODO: change to only validate forms that are active
function validateForm() {

    $(".form-control").removeClass("is-invalid");
    $(".invalid-feedback").remove();
    
    var duplicate_cards = getDuplicateCards();
    $(".hand").each(function() {
        
        if ($(this).find(".form-check-input").length === 0 || $(this).find(".form-check-input").is(":checked")) {
        
            var card = $(this).find("select[name=suit1]").val() + $(this).find("select[name=number1]").val();

            if (duplicate_cards.includes(card)) {
                var suit = $(this).find("select[name=suit1]")
                var number = $(this).find("select[name=number1]")
                suit.addClass("is-invalid");
                number.addClass("is-invalid");
                number.after("<div class='invalid-feedback'>Can't have more than one of the same card</div>");
            }

            card = $(this).find("select[name=suit2]").val() + $(this).find("select[name=number2]").val();

            if (duplicate_cards.includes(card)) {
                var suit = $(this).find("select[name=suit2]")
                var number = $(this).find("select[name=number2]")
                suit.addClass("is-invalid");
                number.addClass("is-invalid");
                number.after("<div class='invalid-feedback'>Can't have more than one of the same card</div>");
            }
        }
        
    });
    
}

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
    
    validateForm();
});

$(".form-control").change(function() {  
    
    validateForm();

});