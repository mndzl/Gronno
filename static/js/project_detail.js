$(document).ready(function(){
    flag = document.getElementById('report');
    reportSelections = document.getElementById('report-select');
    flag.onclick = function report(){
        reportSelections.classList.toggle('open');
    };

});

$('.medal').click(function(e){
    e.stopImmediatePropagation();
    $.ajax({
        url: $(this).attr('href'),
        
        success: function(json){
            console.log("medal given")
        }
    })

    if (  $( this ).css( "transform" ) == 'none' ){
        $(this).children().children().css({
            "transition":".2s",
            "transform":"scale(1.2)",
        });
        $(this).one("transitionend webkitTransitionEnd oTransitionEnd MSTransitionEnd", function(){
            $(this).children().children().css("transform", "scale(1)");
        });
    } else {
        $(this).css("transform","" );
    }


    if($(this).attr('style')=='opacity:1'){
        $(this).attr('style', 'opacity:.3');
    }else{
        $('.medal').attr('style', 'opacity:.3')
        $(this).attr('style', 'opacity:1');
    }
})

