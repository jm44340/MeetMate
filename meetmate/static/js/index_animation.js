



$("#sign-in > input").keyup(function(){
    if(this.value != ""){
        $("path").eq($(this).index()-1).css("fill", "#388037");
    }
    else{
        $("path").eq($(this).index()-1).css("fill", "#77DD76");
    }
});

$("#sign-in > button").hover(
    function() {
        $("circle").css("fill", "#388037");
    
    }, function() {
        $("circle").css("fill", "#77DD76");
    });



$(document).ready(function() {
    



    if(!('hasBeenVisited' in localStorage)) {
        localStorage.setItem("hasBeenVisited", true);

        $("#sign-in > input, #sign-in > button").css("transition", "0s");

        var dotAnimation = anime({
            targets: '#title-dot',
            translateX: [
                { value: -100, duration: 0, delay: 0 , easing: 'easeInOutElastic(1, .8)'},
                { value: 100, duration: 1000, delay: 300,  easing: 'easeInOutElastic(1, .8)'},
               
            ],
            scaleX: [
                { value: 4, duration: 400, delay: 700, easing: 'easeOutExpo' },
                { value: 1, duration: 1000 },
                { value: 4, duration: 400, delay: 0, easing: 'easeOutExpo' },
                { value: 1, duration: 1000 }
            ],
            opacity:[
                { value: 0, duration: 0, delay: 0},
                { value: 1, duration: 500, delay: 300},
                { value: 0, duration: 600, delay: 0 }
            ],   
            easing: 'easeOutElastic(1, .8)'
        });

        
        var titleAnimation = anime({
            targets: '#title',
            translateY:{
                value:['400%', 0],
                duration: 1000,
                delay: 1150
            },
            opacity:{
                value:[0, 1],
                duration: 1000
            },
            
            easing: 'easeInOutSine',
        });
        
        var logoAnimation = anime({
            targets: '#logo',
            translateY:{
                value:['400%', 0],
                duration: 1000,
                delay: 1150
            },
            opacity:{
                value:[0, 1],
                duration: 1000,
                delay: 2000
            },
            
            easing: 'easeInOutSine',
        });
        

        var loginAreaAnimation = anime({
            targets: '#sign-in',
            opacity: [0, 1], 
            translateY: {
                value: [-50, 0],
                easing: 'easeInOutSine',
                duration: 1000,
                delay: 2000
            },
            borderTopLeftRadius:{
                value: [0, '2.5rem'],
                delay: 2700,
            },
            borderBottomRightRadius:{
                value: [0, '2.5rem'],
                delay: 2700,
            },
            scaleY: {
                value: [0, 1],
                easing: 'easeInOutSine',
                duration: 1000,
                delay: 2000
            },
            easing: 'easeInOutSine',
            duration: 1000,
            delay: 2000
        })

        var waveAnimation = anime({
            targets: '#wave',
            opacity: [0, 1],
            translateY: [100, 0],
            easing: 'easeInOutSine',
            duration: 1000,
            delay: 2000
        });
        
        
        var formElementsAnimation = anime({
            targets: '#sign-in *',
            translateX: [-100, 0],
            opacity: [0, 1],
            delay: function(el, i, l) {
                return 3500 + (i * 150);
            }
        })
        
        setTimeout(function(){ 
            $("#sign-in > input, #sign-in > button").css("transition", "0.5s");
        }, 4500);
        

    }
        




});