$('.notifications').hover(function(){
    if(! /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
        $('.notifications-nav-box').toggleClass('display');
        $('.notifications-count').remove();
            $.ajax({
                type:'GET',
                url:'/see_notifications/',
                data:{},    
            });
    }
});

$('.notifications').click(function(){
    document.location = '/notifications/';
})