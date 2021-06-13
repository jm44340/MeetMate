
r = 0
setTimeout(function(){
    navigator.geolocation.getCurrentPosition(function(position){
        var form_data = new FormData()
        form_data.append("latitude", position.coords.latitude);
        form_data.append("longitude", position.coords.longitude);

        var request = new XMLHttpRequest();
        request.open("POST", document.location.href);
        request.onreadystatechange = function(){
            r = request
            if(request.readyState !== XMLHttpRequest.DONE){
                return;
            }

            if(request.status != 200){
               ;
            }

            response = JSON.parse(request.responseText);
            switch(response.status){
                case "ERROR":
                    $('#icon').attr("src","../../static/resources/svg/close.svg");
                    $('#message').text("Błąd.");
                    $('#icon').removeClass("icon-spinner");
                    break;
                case "TOO FAR":
                    $('#icon').attr("src","../../static/resources/svg/close.svg");
                    $('#message').text("Jesteś za daleko.");
                    $('#icon').removeClass("icon-spinner");
                    break;
                case "OK":
                    $('#icon').attr("src","../../static/resources/svg/tick.svg");
                    $('#message').text("Obecność potwierdzona!");
                    $('#icon').removeClass("icon-spinner");
                    break;
            }
        };

        request.send(form_data);
    })
}, 1000);
