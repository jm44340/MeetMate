
$( "#sign-in > input" )
    .on( "mouseenter", function() {
        var inputHoverOn = anime({
            targets: this,
            backgroundColor: '#aeebad',
            duration: 500,
            easing: 'linear'
        });
    })
    .on( "mouseleave", function() {
        var inputHoverOut = anime({
            targets: this,
            backgroundColor: '#77DD76',
            duration: 500,
            easing: 'linear'
        });
});

$(document).ready(function() {
    
    if(!('hasBeenVisited' in localStorage)) {
        localStorage.setItem("hasBeenVisited", true);


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
        
        var loginAreaAnimation = anime({
            targets: '#sign-in',
            opacity: [0, 1], 
            translateY: {
                value: [-100, 0],
                easing: 'easeInOutSine',
                duration: 1000,
                delay: 3000
            },
            borderTopLeftRadius:{
                value: [0, '2.5rem'],
                delay: 3700,
            },
            borderBottomRightRadius:{
                value: [0, '2.5rem'],
                delay: 3700,
            },
            easing: 'easeInOutSine',
            duration: 1000,
            delay: 3000
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
                return 4500 + (i * 150);
            }
        })



    }
        




});