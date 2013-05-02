$(document).ready(function(){
    $("#startmachinebtn").on('click', function () {
        var name = $("#startmachine").data('name');
        alert(name);
    });

});
