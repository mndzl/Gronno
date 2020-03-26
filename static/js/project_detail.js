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
});

$("#new_comment").submit(function(e){
    e.stopImmediatePropagation();
    e.preventDefault();

    var name = $("#name").text();
    var dedication = $("#dedication").text();
    var urlusr = $("#usrlink").attr("href");
    var image = $("#usrimg").attr("src");

    $.post(window.location.href, $(this).serialize())
    .done(function(){
        text = $("#comment_text").val();
        $("#comment_text").val("");
        $(".comments").prepend(`
            <div class="comment" style="border:1px solid #a8a8a8">
            <div class="head">
                <a href="${urlusr}" class="link"></a>
                <div class="comment_user_image">
                    <img class="user_img" src="${image}">
                </div>
                <div class="info_com">
                    <span class="comment_date">Justo ahora</span>
                    <div class="comment_user_name">${name}</div>
                    <div class="comment_user_dedication">${dedication}</div>
                </div>
            </div>
            <div class="comment_content">${text}</div>            
        </div>`
        );
    });

});