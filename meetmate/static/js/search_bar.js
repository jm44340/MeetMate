
function searchForUser(){
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById('searchBar');
    filter = input.value.toUpperCase();
    ul = document.getElementById("user-list");
    li = ul.getElementsByTagName('li');

    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByTagName("a")[0];
        txtValue = a.textContent || a.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }

    if ($("#user-list").get(0).scrollHeight > $("#user-list").height()) {
        $("#user-list > li").css("padding-right", "1rem");
    } else{
        $("#user-list > li").css("padding-right", "0rem");
    }


}

