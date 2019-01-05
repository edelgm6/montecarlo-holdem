$(".form-control").change(function() {
    
    var hand = $(this).parent()
    var card1 = $(hand).children("select[name=suit1]").val() + $(hand).children("select[name=number1]").val();
    var card2 = $(hand).children("select[name=suit2]").val() + $(hand).children("select[name=number2]").val();

    var cards = [];
    $(".hand").each(function() {
        var card1 = $(this).find("select[name=suit1]").val() + $(this).find("select[name=number1]").val();
        
        var card2 = $(this).find("select[name=suit2]").val() + $(this).find("select[name=number2]").val();
        //alert(card1);
        cards.push(card1);
        cards.push(card2);
    });
    
    console.log(cards);
    
    var card1_count = 0;
    if (card1){
        for (var i=0; i < cards.length; i++) {
            if(cards[i] == card1) {
                card1_count++;
            }
        }
    }
    
    var card2_count = 0;
    if (card2){
        for (var i=0; i < cards.length; i++) {
            if(cards[i] == card2) {
                card2_count++;
            }
        }
    }
    
    if (card1_count > 1) {
        console.log(card1_count);
        $(hand).children("select[name=suit1]").after("<div class='invalid-feedback'>More example invalid feedback text</div>");
    }
    
    if (card2_count > 1) {
        console.log(card2_count);
        $(hand).children("select[name=suit2]").after("<div>More example invalid feedback text</div>").addClass("invalid-feedback");
    }
    
});