$('#ticker-form').on('submit', function(event){
    event.preventDefault();
    close_ticker();
});

function close_ticker() {
  //console.log($('#id_ticker').val())
    $.ajax({
        url : "", // the endpoint
        type : "POST", // http method
        data:{
            ticker:$('#id_ticker').val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            action: 'post'
        },
        success : function(json) {
            $('#id_ticker').val(''); // remove the value from the input
        },
        error : function(xhr,errmsg,err) {
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
 });
};
