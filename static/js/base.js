$('.notifications').click(function(){
    $('.notifications-box').toggleClass('display');
    $('.notifications-count').remove();
        $.ajax({
            type:'GET',
            url:'/see_notifications/',
            data:{},
        });


});