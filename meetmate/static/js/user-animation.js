


$(".scan-code-wrapper").hover(
    function() {
        $('.scan-code-wrapper > .image-container').css({
            transform: "rotate(10deg) translateX(10px)"
        });
        $(".scan-code-wrapper > .menu-title > .title-underline").css({
            width: "100%" 
        });
}, function(){
    $('.scan-code-wrapper > .image-container').css({
        transform: "rotate(0) translateX(0)"
    });
    $(".scan-code-wrapper > .menu-title > .title-underline").css({
        width: "0" 
    });
});


$(".meetings-history-wrapper").hover(
    function() {
        $('.meetings-history-wrapper > .image-container').css({
            transform: "rotate(10deg) translateX(10px)"
        });
        $(".meetings-history-wrapper > .menu-title > .title-underline").css({
            width: "100%" 
        });
}, function(){
    $('.meetings-history-wrapper > .image-container').css({
        transform: "rotate(0) translateX(0)"
    });
    $(".meetings-history-wrapper > .menu-title > .title-underline").css({
        width: "0" 
    });
});





