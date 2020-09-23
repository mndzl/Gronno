$('.notifications').hover(function(){
    $('.notifications-nav-box').toggleClass('display');
    $('.notifications-count').remove();
        $.ajax({
            type:'GET',
            url:'/see_notifications/',
            data:{},    
        });
});

$('.notifications').click(function(){
    document.location = '/notifications/';
})