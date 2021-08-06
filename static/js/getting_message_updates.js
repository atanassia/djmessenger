var timerId = setInterval(function(){
    let lastMessageId = $('.last-message').attr('data-messageid')
    let data = {
        lastMessageId:lastMessageId
    }

    $.ajax({
        method:"GET",
        dataType:"json",
        data:data,
        url:'{% url "more_messages" chat.code %}',
        success:function(data){
            console.log(data)
            let result = data['data']
            if(result){
                $.each(result, function(key, obj){
                    if(obj['last_message']){
                        $('.messages').removeClass("last-message")
                        $('.messages').removeAttr("data-messageid")
                        $('.allmessages').append(
                            '<div class="card mb-3 messages last-message" data-messageid = "' + obj['id'] + '">' +
                                '<div class="row g-0">'+
                                    '<div class="col-md-12">'+
                                        '<div class="card-body">'+
                                        '<div class="row">'+
                                            '<h5 class="card-title"><a class="" style = "text-decoration: none; color: #000 !important;" href="" target="_blank">' + obj['sender'] + '</a></h5>'+
                                            '<spam class="card-text">' + obj['message'] + '</p>' +
                                        '</div>'+
                                            '<spam class="card-text"><small class="text-muted">' + obj['created'] + '</small></spam>' +
                                        '</div>' +
                                    '</div>' +
                                '</div>' +
                            '</div>'
                        )
                    }
                    
                    else{
                        $('.allmessages').append(
                            '<div class="card mb-3 messages">' +
                                '<div class="row g-0">'+
                                    '<div class="col-md-12">'+
                                        '<div class="card-body">'+
                                        '<div class="row">'+
                                            '<h5 class="card-title"><a class="" style = "text-decoration: none; color: #000 !important;" href="" target="_blank">' + obj['sender'] + '</a></h5>'+
                                            '<spam class="card-text">' + obj['message'] + '</p>' +
                                        '</div>'+
                                            '<spam class="card-text"><small class="text-muted">' + obj['created'] + '</small></spam>' +
                                        '</div>' +
                                    '</div>' +
                                '</div>' +
                            '</div>'
                        )
                    }      
                })
            }
        }
    })
}, 1000);