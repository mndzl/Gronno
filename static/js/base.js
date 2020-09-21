$('.notifications').click(function(){

    $.ajax({
        url: `/get_notifications/${$('#user-id').html()}`,
        type:'GET',
        datatype:'json',
        success: function(data){
            $('.notifications-box').html('');
            for (var i=0; i<data.length; i++){
                $('.notifications-box').append(
                    `   <div class='notification'>
                            -----------
                            <span class='icon-${data[i].fields.icon}'></span>
                            <p>${data[i].fields.message}<p>
                        </div>
                    ` 
                );
            }
        },
        error: function(err){
            console.log(err)
        },
    });
});