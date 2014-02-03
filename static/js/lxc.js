$(document).ready(function(){
    $("#machineaction").on("show", function () {
        var action = $(this).data('modal').options.action;
        var message = $(".modal-body", this).html().replace("%action%", action);
        $(".modal-body", this).html(message);
        $(".btn-primary", this).html(action);
    });
    $("#machineaction .btn-primary").click(function () {
        var name = $("#machineaction").data('modal').options.name;
        var action = $("#machineaction").data('modal').options.action;
        $.ajax({
            url: "/" + name + "/" + action,
            success: function () {
                window.location.reload();
            },

        });
        $("#machineaction").modal("hide");
    });
    $("#machineclone .btn-primary").click(function () {
        var name = $("#machineclone").data('modal').options.name;
        var newname = $("#clonename").val();
        if (newname) {
            $.ajax({
                url: "/" + name + "/clone/" + newname,
                success: function () {
                    window.location.reload();
                },
            });
        }
        $("#machineclone").modal("hide");
    });


});
