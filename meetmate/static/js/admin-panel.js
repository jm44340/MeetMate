$(document).ready(function() {
    

    $("#add-user-button").click(function() {
        $("#add-user-wrapper").slideToggle();
    });
   
    $("#close-add-user").click(function() {
        $("#add-user-wrapper").slideToggle();
    });

    $("#searchbox-form").click(function() {
        $("#add-user-wrapper").slideUp();
    });

    $("#close-add-user").hover(
        function() {
            $("#close-add-user > svg > *").css("fill", "#3f4045");
            $(this).css("background-color", "#77DD76");
        }, function() {
            $("#close-add-user > svg > *").css("fill", "#77DD76");
            $(this).css("background-color", "#3f4045");
    });

    $("#close-edit-user").hover(
        function() {
            $("#close-edit-user > svg > *").css("fill", "#3f4045");
            $(this).css("background-color", "#77DD76");
        }, function() {
            $("#close-edit-user > svg > *").css("fill", "#77DD76");
            $(this).css("background-color", "#3f4045");
    });


    $("#user-list > li").click(function() {
        $("#user-edit-wrapper").css("display", "flex").hide().fadeIn();
        $("#add-user-wrapper").slideUp();
    });

    $("#close-edit-user").click(function() {
        $("#user-edit-wrapper").fadeOut();
        
        
    });

});