

$(document).ready(function() {
    var qrcode = new QRCode(document.getElementById("qrcode"), {
        text: "test",
        width: 1024,
        height: 1024,
        colorDark : "#000000",
        colorLight : "#ffffff",
        correctLevel : QRCode.CorrectLevel.H
    });

    qrcode.makeCode("test");
});